#version 330 core

// Variable de sortie (sera utilisé comme couleur)
out vec4 color;

uniform vec4 couleur;

//Un Fragment Shader minimaliste
void main (void)
{
  //Couleur du fragment
  color = vec4(couleur);
}
