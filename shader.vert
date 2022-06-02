#version 330 core

// Variable d'entrée, ici la position
layout (location = 0) in vec3 position;

// Passage de paramètres uniforms
uniform vec4 translation;
uniform mat4 rotation;
uniform mat4 projection;

// Ordre : rotation, translation, projection

//Un Vertex Shader minimaliste
void main (void)
{
  //Coordonnees du sommet
  vec4 p=vec4(position, 1.0);
  p+=translation;
  //if rotation is not identity do not use the rotation matrix
  if(rotation[0][0]!=0.0 || rotation[1][1]!=0.0 || rotation[2][2]!=0.0 || rotation[3][3]!=0.0)
    gl_Position=p*rotation;
  else
    gl_Position=p;
}