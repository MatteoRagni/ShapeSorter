# Prepares the environment. Requires meshes
# [hl0, hl3, hl4, hl5, hl6, hlr]
# to be loaded in the different layers with respect to the first one

import bpy
import random
import re

options = {
  "seed": 73,
  "basement": "hl0",
  "holes": ["hl3", "hl4", "hl5", "hl6", "hlr"],
  "width": 12,
  "height": 12,
  "generated": [],
  "scale": 0.02,
  "center": [0.6, 0.6, 0.1],
  "sense_ext": "_sensor"
}

# Forcing random generation
random.seed(options["seed"])

def chunk(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

def create_list(options):
    size = (options["width"] - 2) *  (options["height"] - 2)
    basement_size = size - len(options["holes"])
    options["generated"] = ([options["basement"]] * basement_size) + options["holes"]

    random.shuffle(options["generated"])
    options["generated"] = chunk(options["generated"], options["width"] - 2)

    for i in range(0,len(options["generated"])):
        options["generated"][i].insert(0, options["basement"])
        options["generated"][i].append(options["basement"])

    options["generated"].insert(0, [options["basement"]] * options["width"])
    options["generated"].append([options["basement"]] * options["width"])

    print("============================================================")
    for i in range(0, len(options["generated"])):
        print(options["generated"][i])
    print("============================================================")

    #return options["generated"]

def position_objects(options):
    scene = bpy.context.scene
    rgx = re.compile("hl[3456r]")
    for x in range(0, len(options["generated"])):
        for y in range(0, len(options["generated"][0])):
            # Creating location copy
            name = options["generated"][x][y]
            obj = bpy.data.meshes[name]
            obj_copy = obj.copy()
            obj_scene = bpy.data.objects.new("%s_%d_%d" % (name, x+1, y+1), obj_copy)
            # Localize in workspace object
            obj_scene.location = (options["center"][0] * (2 * x + 1 - options["width"]), options["center"][1] * (2 * y + 1 - options["height"]), -options["center"][2])
            # Scale final mesh
            obj_scene.scale = (options["scale"],options["scale"],options["scale"])
            obj_scene.layers[0] = True
            for i in range(1,19): obj_scene.layers[i] = False
            obj_scene.game.use_collision_bounds = True
            # obj_scene.game.collision_bounds_type = 'BOX'
            if rgx.match(name):
                bpy.data.objects[name + options["sense_ext"]].location = obj_scene.location
            scene.objects.link(obj_scene)
            scene.update()

def select_all_board():
    for obj in bpy.data.objects:
        obj.select = False
    rgx = re.compile("hl[03456r]_(\d*)_(\d*)") # alternative for mesh = hl[03456r].(\d\d\d)
    for obj in bpy.data.objects:
        if rgx.match(obj.name):
            obj.select = True

# delete all elements that responds to the regular expression: "hl[03456r]_(\d*)_(\d*)"
def delete_board():
    select_all_board()
    bpy.ops.object.delete()


def create_new_board():
    print("Creating a new board...")
    delete_board()
    create_list(options)
    position_objects(options)
    print("Board crated!")

####### WORKSPACE UTILITY ######


def create_board():
    create_new_board()

def delete_all_board():
    delete_board()
