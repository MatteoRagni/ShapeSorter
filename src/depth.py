import bgl
import bge

vertex_shader = """
varying double DEPTH;

uniform double FARPLANE = 14.0;  // send this in as a uniform to the shader

void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    DEPTH = gl_Position.z / FARPLANE ; // do not divide by w
}
"""
fragment_shader = """
varying double DEPTH;

void main() {
    // float m = 1.75;
    float m = 1.90;
    // float q = 0.0;
    float q = 0;

    // far things appear white, near things black
    //float val = (1-DEPTH) * 1.75;
    float val = m * (1-DEPTH) + q;
    gl_FragColor.rgb = vec3(val, val, val);
}
"""

def enable_depth():
    scene = bge.logic.getCurrentScene()
    for object in scene.objects:
        if object.meshes:
            for mat in object.meshes[0].materials:
                shader = mat.getShader()
                if shader != None:
                    if not shader.isValid():
                        shader.setSource(vertex_shader, fragment_shader, 1)

def disable_depth():
    scene = bge.logic.getCurrentScene()
    for object in scene.objects:
        if object.meshes:
            for mat in object.meshes[0].materials:
                shader = mat.getShader()
                if shader != None:
                    shader.delSource()
