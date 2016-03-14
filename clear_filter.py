import bge

cont = bge.logic.getCurrentController()

mesh = cont.owner.meshes[0]
for mat in mesh.materials:
    shader = mat.getShader()
    if shader != None:
       shader.delSource()