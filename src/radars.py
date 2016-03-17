from bge import logic
import mathutils
import math

object_ref = {
  "l3radar": ["l3", lambda a: abs(a % 360) == 30 or abs(a % 360) == 150 or abs(a % 360) == 270,
                1.51, 1.51],
  "l4radar": ["l4", lambda a: abs(a % 90) == 0,
                2.1, -1.48],
  "l5radar": ["l5", lambda a: abs(a % 72) == 0,
                -1.49, 2.12],
  "l6radar": ["l6", lambda a: abs(a % 60) == 0,
                -0.3, -0.29],
  "lrradar": ["lr", lambda a: True,
                -1.5, -2.08]
}
final_z = -0.03
dist_threshold = 0.280 ** 2

def radar(cont):
    sensor = cont.sensors[0]
    s_list = object_ref[sensor.name]
    if sensor.positive:
        for obj in sensor.hitObjectList:
            if obj.name == s_list[0]:
                angle = obj.worldOrientation.to_euler('XYZ').z
                angle = round(math.degrees(angle))
                if s_list[1](angle):
                    pos1 = obj.worldPosition
                    pos2 = logic.getCurrentScene().objects[sensor.name].worldPosition
                    dist = (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2
                    if dist <= dist_threshold:
                        obj.worldPosition = [s_list[2], s_list[3], final_z]
                        obj.sendMessage(s_list[0] + "_solved")
                        obj.suspendDynamics()
                        logic.getCurrentScene().objects[sensor.name].endObject()
        sensor.reset()
