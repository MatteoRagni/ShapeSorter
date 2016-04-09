import bgl
import bge

vertex_shader = """
varying double DEPTH;

uniform double FARPLANE = 0.6;  // send this in as a uniform to the shader

void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    DEPTH = gl_Position.z / FARPLANE ; // do not divide by w
}
"""
fragment_shader = """
varying double DEPTH;

void main() {
    float m = 0.8;
    float q = -0.85;

    // far things appear white, near things black
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
    return True

def disable_depth():
    scene = bge.logic.getCurrentScene()
    for object in scene.objects:
        if object.meshes:
            for mat in object.meshes[0].materials:
                shader = mat.getShader()
                if shader != None:
                    shader.delSource()
    return False

def toggle_depth(cont):
    scene = bge.logic.getCurrentScene()
    if scene.active_camera.name == 'Isometric':
        if (cont.owner)['depth'] == True:
            (cont.owner)['depth'] = disable_depth()
        else:
            (cont.owner)['depth'] = enable_depth()

def toggle_depth_keyboard(cont):
    for k, f in cont.sensors['depth_sensor'].events:
        if f == bge.logic.KX_INPUT_JUST_ACTIVATED:
            toggle_depth(cont)
