import bge
import os
from time import sleep

# This will print the camera matrix parameter
def calib_matrix():
    #cam   = bpy.data.cameras["Camera"]
    #scene = bpy.data.scenes["Scene"]
    #f     = cam.lens
    #rx    = scene.render.resolution_x/2.0
    #ry    = scene.render.resolution_y
    #sh    = cam.sensor_height
    #sw    = cam.sensor_width
    # I know this value, there are no accessor in BGE
    f  = bge.render.getFocalLength()
    rx = bge.render.getWindowWidth() / 2.0
    ry = bge.render.getWindowHeight()
    sh = 32.0
    sw = 18.0
    scale = 1.0 # This is an hipothesys
    su    = rx * scale / sw
    sv    = ry * scale / sh
    au    = f * su
    av    = f * sv
    u0    = rx * scale / 2.0
    v0    = ry * scale / 2.0
    skew  = 0.0
    # printing matrix
    print("| %6.4f %6.4f %6.4f %6.4f |" % (au, skew, u0, 0))
    print("| %6.4f %6.4f %6.4f %6.4f |" % (0, av, v0, 0))
    print("| %6.4f %6.4f %6.4f %6.4f |" % (0, 0, 1, 0))
    # Exporting to a file
    local_dir = os.path.dirname(bge.logic.expandPath("//"))
    fl = open("%s/camera_matrix.yaml" % local_dir, "w")
    fl.write("%" + "YAML:1.0\n")
    fl.write("cameraMatrix:\n")
    fl.write("\trows: 3\n")
    fl.write("\tcols: 4\n")
    fl.write("\tdt: d\n")
    fl.write("\tdata: [")
    fl.write("%5.5f, %5.5f, %5.5f, %5.5f, " % (au, skew, u0, 0))
    fl.write("%5.5f, %5.5f, %5.5f, %5.5f, " % (0, av, v0, 0))
    fl.write("%5.5f, %5.5f, %5.5f, %5.5f]\n" % (0, 0, 1, 0))
    fl.close()

# This will make a screenshot of the actual scene
def make_screenshot():
    render.makeScreenshot("//image.png")

def composite_screenshot():
    cam = bge.logic.getCurrentScene().active_camera
    cam.sendMessage("enable_depth")
    sleep(1.0)
    bge.render.makeScreenshot("//depth.png")
    #cam.sendMessage("disable_depth")
    #sleep(0.2)
    #bge.render.makeScreenshot("//scene.png")
