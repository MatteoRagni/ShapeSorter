from bge import logic
from math import sqrt

GRASP_ON  = [0, 1, 0, 1] # green
GRASP_OFF = [1, 1, 1, 1] # white

vertex_shader = """
void main(void) {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
"""

grasp_on_fragment = """
void main (void) {
    gl_FragColor.rgb = vec3(0.0, 1.0, 0.0);
}
"""
grasp_off_fragment = """
void main(void) {
    gl_FragColor.rgb = vec3(1.0, 1.0, 1.0);
}
"""

def grasp_color():
    own = (logic.getCurrentController()).owner
    fragment_shader = grasp_off_fragment
    if own['Grasp']:
        fragment_shader = grasp_on_fragment

    for mesh in own.meshes:
        for material in mesh.materials:
            shader = material.getShader()
            if shader is not None:
                shader.delSource()
                shader.setSource(vertex_shader, fragment_shader, True)

OBJECTS = ["l3", "l4", "l5", "l6", "lr"]
THR     = 0.45
def update_target():
    own = (logic.getCurrentController()).owner
    if own['Grasp']:
        scene = logic.getCurrentScene()
        min_dist = 9999
        for obj in OBJECTS:
            loc_t = scene.objects[obj].worldPosition
            loc_o = own.worldPosition
            dist = sqrt((loc_t[0] - loc_o[0])**2 + (loc_t[1] - loc_o[1])**2)
            scene.objects[obj]['robot'] = dist
            if dist < min_dist:
                min_dist = dist
            if (dist <= THR):
                own['Target'] = obj
        own['Dist'] = min_dist
    else:
        own['Target'] = ''

## Sensors function
def sensor(a):
    hole   = (logic.getCurrentScene()).objects["hl{}_sensor".format(a)]
    object = (logic.getCurrentScene()).objects["l{}".format(a)]
    h_pos  = hole.worldPosition
    o_pos  = object.worldPosition
    dist = sqrt((h_pos[0] - o_pos[0])**2 + (h_pos[1] - o_pos[1])**2)
    object['dist'] = dist
    if dist < 0.2:
        object['solved'] = 1
        object.worldPosition = h_pos
        r = (logic.getCurrentScene()).objects["Robot"]
        r['Grab'] = False
        r['Target'] = ''
        object.suspendDynamics()

def sensor_3():
    sensor("3")

def sensor_4():
    sensor("4")

def sensor_5():
    sensor("5")

def sensor_6():
    sensor("6")

def sensor_r():
    sensor("r")
