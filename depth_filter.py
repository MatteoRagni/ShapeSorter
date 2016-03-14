import bge

cont = bge.logic.getCurrentController()

VertexShader = """
   void main() // all vertex shaders define a main() function
   {
      gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
         // this line transforms the predefined attribute gl_Vertex 
         // of type vec4 with the predefined uniform 
         // gl_ModelViewProjectionMatrix of type mat4 and stores 
         // the result in the predefined output variable gl_Position 
         // of type vec4. (gl_ModelViewProjectionMatrix combines 
         // the viewing transformation, modeling transformation and 
         // projection transformation in one matrix.)
   }
"""

FragmentShader = """
    float near = 1.0; 
    float far  = 100.0; 
      
    float LinearizeDepth(float depth) 
    {
        float z = depth * 2.0 - 1.0; // Back to NDC 
        return (2.0 * near * far) / (far + near - z * (far - near));	
    }
    void main()
    {  
      float depth = LinearizeDepth(gl_FragCoord.z) / far;
      gl_FragColor = vec4(vec3(depth), 1.0);
    }
"""

mesh = cont.owner.meshes[0]
for mat in mesh.materials:
    shader = mat.getShader()
    if shader != None:
        if not shader.isValid():
            shader.setSource(VertexShader, FragmentShader, 1)