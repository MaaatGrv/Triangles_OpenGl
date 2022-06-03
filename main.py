#!/usr/bin/env python3

import os
from tkinter.messagebox import NO
import OpenGL.GL as GL
import glfw
import numpy as np
import random as rd
import pyrr

x,y,z=0,0,-5
r,g,b=0.0,0.0,0.0
theta=0
far=10

def init_window():
    # initialisation de la librairie glfw
    glfw.init()
    # paramétrage du context opengl
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    # création et parametrage de la fenêtre
    glfw.window_hint(glfw.RESIZABLE, False)
    window = glfw.create_window(800, 800, 'Test', None, None)
    # parametrage de la fonction de gestion des évènements
    glfw.set_key_callback(window, key_callback)
    return window

def init_context(window):
    # activation du context OpenGL pour la fenêtre
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    # activation de la gestion de la profondeur
    GL.glEnable(GL.GL_DEPTH_TEST)
    # choix de la couleur de fond

    GL.glClearColor(0.3, 0.1, 0.7, 1.0)

    print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

def init_program():
    GL.glUseProgram(create_program_from_file('shader.vert', 'shader.frag'))
        
def init_data():
    sommets = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0),(0, 0, 0), (1, 0, 0), (0, 0, 1)), np.float32)
    # sommets = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0),(0, 0, 0), (1, 0, 0), (0, 0, 1)), np.float32)
    # attribution d'une liste d'e ́tat (1 indique la cre ́ation d'une seule liste)
    vao = GL.glGenVertexArrays(1)
    # affectation de la liste d'e ́tat courante
    GL.glBindVertexArray(vao)
    # attribution d’un buffer de donnees (1 indique la cre ́ation d’un seul buffer) 
    vbo = GL.glGenBuffers(1)
    # affectation du buffer courant
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    # copie des donnees des sommets sur la carte graphique
    GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets, GL.GL_STATIC_DRAW)
    # Les deux commandes suivantes sont stocke ́es dans l'e ́tat du vao courant 
    # Active l'utilisation des donne ́es de positions
    # (le 0 correspond a` la location dans le vertex shader) 
    GL.glEnableVertexAttribArray(0)
    # Indique comment le buffer courant (dernier vbo "binde ́")
    # est utilise ́ pour les positions des sommets 
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)


def run(window):
    global x,y,z
    global r,g,b
    # boucle d'affichage
    while not glfw.window_should_close(window):
        # nettoyage de la fenêtre : fond et profondeur^
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # display_callback(glfw.get_time()%-1,0.0,0.0)
        display_callback(x,y,z)
        display_color_callback(r,g,b)
        display_projection_callback(far)
        display_rotation_callback(theta)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)

        #  l'affichage se fera ici

        # time = glfw.get_time()
        # i=1
        # if time > 2*i :
        #     r=rd.uniform(0, 1)
        #     v=rd.uniform(0, 1)
        #     b=rd.uniform(0, 1)
        #     GL.glClearColor(r, v, b, 1.0)
        #     i+=1

        # changement de buffer d'affichage pour éviter un effet de scintillement
        glfw.swap_buffers(window)
        # gestion des évènements
        glfw.poll_events()


def compile_shader(shader_content, shader_type): 
    # compilation d'un shader donné selon son type 
    shader_id = GL.glCreateShader(shader_type) 
    GL.glShaderSource(shader_id, shader_content) 
    GL.glCompileShader(shader_id)
    success = GL.glGetShaderiv(shader_id, GL.GL_COMPILE_STATUS) 
    if not success:
        log = GL.glGetShaderInfoLog(shader_id).decode('ascii') 
        print(f'{25*"-"}\nError compiling shader: \n\{shader_content}\n{5*"-"}\n{log}\n{25*"-"}') 
    return shader_id

def create_program( vertex_source, fragment_source):
    # creation d'un programme gpu
    vs_id = compile_shader(vertex_source, GL.GL_VERTEX_SHADER) 
    fs_id = compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER) 
    if vs_id and fs_id:
        program_id = GL.glCreateProgram()
        GL.glAttachShader(program_id, vs_id)
        GL.glAttachShader(program_id, fs_id)
        GL.glLinkProgram(program_id)
        success = GL.glGetProgramiv(program_id, GL.GL_LINK_STATUS) 
        if not success:
            log = GL.glGetProgramInfoLog(program_id).decode('ascii')
            print(f'{25*"-"}\nError linking program:\n{log}\n{25*"-"}') 
        GL.glDeleteShader(vs_id)
        GL.glDeleteShader(fs_id)
    return program_id

def create_program_from_file(vs_file, fs_file):
    # creation d'un programme gpu a` partir de fichiers
    vs_content = open(vs_file, 'r').read() if os.path.exists(vs_file)\
        else print(f'{25*"-"}\nError reading file:\n{vs_file}\n{25*"-"}') 
    fs_content = open(fs_file, 'r').read() if os.path.exists(fs_file)\
        else print(f'{25*"-"}\nError reading file:\n{fs_file}\n{25*"-"}')
    return create_program(vs_content, fs_content)

def key_callback(win, key, scancode, action, mods):
    global x,y,z
    global r,g,b
    global theta
    global far
    # sortie du programme si appui sur la touche 'echap'
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(win, glfw.TRUE)

    # deplacement directionnels
    if key == glfw.KEY_RIGHT  and action == glfw.PRESS:
        x+=0.1
        display_callback(1.0,x,0.0)
    if key == glfw.KEY_LEFT and action == glfw.PRESS:
        x-=0.1
        display_callback(-1.0,x,0.0)
    if key == glfw.KEY_UP and action == glfw.PRESS:
        y+=0.1
        display_callback(0.0,y,0.0)
    if key == glfw.KEY_DOWN and action == glfw.PRESS:
        y-=0.1
        display_callback(0.0,y,0.0)
    
    # Changement de couleur
    if key == glfw.KEY_R and action == glfw.PRESS:
        r=1.0
        g,b=0.0,0.0
        display_color_callback(r,g,b)
    if key == glfw.KEY_G and action == glfw.PRESS:
        g=1.0
        r,b=0.0,0.0
        display_color_callback(r,g,b)
    if key == glfw.KEY_B and action == glfw.PRESS:
        b=1.0
        r,g=0.0,0.0
        display_color_callback(r,g,b)

    # Rotation
    if key == glfw.KEY_I and action == glfw.PRESS:
        theta+=np.pi/4
        display_rotation_callback(theta)
    
    if key == glfw.KEY_J and action == glfw.PRESS:
        theta-=np.pi/4
        display_rotation_callback(theta)

    # Projection
    if key == glfw.KEY_Y and action == glfw.PRESS:
        z+=0.1
        display_projection_callback(far)
    
    if key == glfw.KEY_H and action == glfw.PRESS:
        z-=0.1
        display_projection_callback(far)

def display_callback(x,y,z):
    # Récupère l'identifiant du programme courant
    prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
    # Récupère l'identifiant de la variable translation dans le programme courant 
    loc = GL.glGetUniformLocation(prog, "translation")
    # Vérifie que la variable existe
    if loc == -1 :
        print("Pas de variable uniforme : translation")
    # Modifie la variable pour le programme courant 
    GL.glUniform4f(loc, x, y, z, 0)

def display_color_callback(r,g,b):
    # Récupère l'identifiant du programme courant
    prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
    # Récupère l'identifiant de la variable translation dans le programme courant 
    loc = GL.glGetUniformLocation(prog, "couleur")
    # Vérifie que la variable existe
    if loc == -1 :
        print("Pas de variable uniforme : couleur")
    # Modifie la variable pour le programme courant 
    GL.glUniform4f(loc, r, g, b, 0)

def display_rotation_callback(theta):
    # Récupère l'identifiant du programme courant
    prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
    # Récupère l'identifiant de la variable translation dans le programme courant 
    loc = GL.glGetUniformLocation(prog, "rotation")
    # Vérifie que la variable existe
    if loc == -1 :
        print("Pas de variable uniforme : rotation")
    # Création matrice 4x4
    rot3 = pyrr.matrix33.create_from_z_rotation(theta)
    rot4= pyrr.matrix44.create_from_matrix33(rot3)
    # Modifie la variable pour le programme courant 
    GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot4)

def display_projection_callback(far):
    # Récupère l'identifiant du programme courant
    prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
    # Récupère l'identifiant de la variable translation dans le programme courant 
    loc = GL.glGetUniformLocation(prog, "projection")
    # Vérifie que la variable existe
    if loc == -1 :
        print("Pas de variable uniforme : projection")
    # Création matrice 4x4
    projection = pyrr.matrix44.create_perspective_projection_matrix(50, 1, 0.5, 10)
    # Modifie la variable pour le programme courant 
    GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, projection)
    
def main():
    window = init_window()
    init_context(window)
    init_program()
    init_data()
    run(window)
    glfw.terminate()

if __name__ == '__main__':
    main()