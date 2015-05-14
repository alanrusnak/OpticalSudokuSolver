# Alan Rusnak, University of Cambridge, 2015

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
import time
import sys
import numpy
from skimage import feature
import socket
from Image import *   #have to import both Image packages in this order
from PIL import Image


def cross(A, B):
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

def parse_grid(grid):
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    return values

def grid_values(grid):
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

def assign(values, s, d):

    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):

    if d not in values[s]:
        return values
    values[s] = values[s].replace(d,'')

    if len(values[s]) == 0:
	return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False

    for u in units[s]:
	dplaces = [s for s in u if d in values[s]]
	if len(dplaces) == 0:
	    return False
	elif len(dplaces) == 1:

            if not assign(values, dplaces[0], d):
                return False
    return values

def display2(values):
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in reversed(rows):
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols)
        if r in 'DG': print line
    print

def toDisplay(values):
    solution = ''
    for r in (rows):
        for c in (cols):
            solution = solution + values[r+c]


    return solution


def solve(grid): return search(parse_grid(grid))

def search(values):
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in squares):
        return values
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d))
		for d in values[s])

def some(seq):
    for e in seq:
        if e: return e
    return False


window = 0
texture = 0

def sudokuGrid():
    glLineWidth(3)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(9, 0, 0)
    glVertex3f(0, 3, 0)
    glVertex3f(9, 3, 0)
    glVertex3f(0, 6, 0)
    glVertex3f(9, 6, 0)
    glVertex3f(0, 9, 0)
    glVertex3f(9, 9, 0)
    glEnd()

    glLineWidth(1)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0, 1, 0)
    glVertex3f(9, 1, 0)
    glVertex3f(0, 2, 0)
    glVertex3f(9, 2, 0)
    glVertex3f(0, 4, 0)
    glVertex3f(9, 4, 0)
    glVertex3f(0, 5, 0)
    glVertex3f(9, 5, 0)
    glVertex3f(0, 7, 0)
    glVertex3f(9, 7, 0)
    glVertex3f(0, 8, 0)
    glVertex3f(9, 8, 0)
    glEnd()

    glLineWidth(3)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 9, 0)
    glVertex3f(3, 0, 0)
    glVertex3f(3, 9, 0)
    glVertex3f(6, 0, 0)
    glVertex3f(6, 9, 0)
    glVertex3f(9, 0, 0)
    glVertex3f(9, 9, 0)
    glEnd()

    glLineWidth(1)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 9, 0)
    glVertex3f(2, 0, 0)
    glVertex3f(2, 9, 0)
    glVertex3f(4, 0, 0)
    glVertex3f(4, 9, 0)
    glVertex3f(5, 0, 0)
    glVertex3f(5, 9, 0)
    glVertex3f(7, 0, 0)
    glVertex3f(7, 9, 0)
    glVertex3f(8, 0, 0)
    glVertex3f(8, 9, 0)
    glEnd()

def drawCharacter(num,blur,x,y):
    LoadTexture(str(num),str(blur))
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)

    glTexCoord2f(0.0, 0.0); glVertex3f(x, y,  -0.001)
    glTexCoord2f(1.0, 0.0); glVertex3f( x+1, y,  -0.001)
    glTexCoord2f(1.0, 1.0); glVertex3f( x+1,  y+1, -0.001)
    glTexCoord2f(0.0, 1.0); glVertex3f(x,  y+1,  -0.001)
    glEnd();


def LoadTexture(num,blur):
    #global texture
    image = open("characters/" + num + "b" + blur + ".bmp")

    ix = image.size[0]
    iy = image.size[1]
    image = image.tostring("raw", "RGBX", 0, -1)


    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def InitGL(width, height):
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutCreateWindow("Sudoku Render")
    glutHideWindow()
    glViewport( 0, 0, width, height )

    glShadeModel( GL_SMOOTH )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    viewport = glGetIntegerv( GL_VIEWPORT )

    glMatrixMode( GL_PROJECTION )
    glLoadIdentity( )
    gluPerspective( 60.0, float( viewport[ 2 ] ) / float( viewport[ 3 ] ), 0.1, 1000.0 )
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity( )
    glClearColor(1,1,1,1)


def ReSizeGLScene(Width, Height):
    if Height == 0:
        Height = 1

    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(Width)/float(Height), 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)

counter = 0
def DrawGLScene(CMDS):
    global texture
    global counter
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glClearColor(1,1,1,1.0)

    if(CMDS[0]=='s'):
        CMDS = CMDS[1:]
        ex,ey,ez,cx,cy,r,characters = CMDS.split("_")
        ex = float(ex)
        ey = float(ey)
        ez = float(ez)
        cx = float(cx)
        cy = float(cy)
        r = float(r)

        glRotatef(r, 0.0, 0.0, 1.0)
        gluLookAt(ex,ey,ez,cx,cy,0, 0, 1, 0)

        characters = toDisplay(solve(characters))
        i = 0
        while i < len(characters):
            if(characters[i]=='0'):
                i = i + 1
            else:
               drawCharacter(characters[i],0,(i)%9,(i)/9)
               i = i+1
    else:
     if (CMDS.count("_")==5):
        ex,ey,ez,cx,cy,r = CMDS.split("_")
        ex = float(ex)
        ey = float(ey)
        ez = float(ez)
        cx = float(cx)
        cy = float(cy)
        r = float(r)
        glRotatef(r, 0.0, 0.0, 1.0)
        gluLookAt(ex,ey,ez,cx,cy,0, 0, 1, 0)
     else:
        ex,ey,ez,cx,cy,r,characters = CMDS.split("_")
        ex = float(ex)
        ey = float(ey)
        ez = float(ez)
        cx = float(cx)
        cy = float(cy)
        r = float(r)

        glRotatef(r, 0.0, 0.0, 1.0)
        gluLookAt(ex,ey,ez,cx,cy,0, 0, 1, 0)


        i = 0
        while i < len(characters):
            if(characters[i]=='0'):
                i = i + 1
            else:
               drawCharacter(characters[i],0,(i)%9,(i)/9)
               i = i+1





    glDisable(GL_TEXTURE_2D)
    sudokuGrid()


    width,height = 720,1280
    #imagepath = "C:/Users/Alan/Documents/SudokuProject/renders/" + str(counter) + ".png"
    counter = counter + 1
    imagepath = "C:/Users/Alan/Documents/SudokuProject/renders2/" + CMDS + ".png"
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.fromstring("RGBA",(width,height),data)
    image = image.transpose( Image.FLIP_TOP_BOTTOM)
    glutSwapBuffers()
    image=image.convert('L')
    image.save(imagepath)

    return imagepath



def runServer(TCP_IP,TCP_PORT):
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    while 1:
        conn, addr = s.accept()
        print 'Connection address:', addr

        while 1:
            CMDS = conn.recv(BUFFER_SIZE)
            CMDS = CMDS.rstrip('\n')
            if not CMDS: break
            print "received data:", CMDS

            imagepath = DrawGLScene(CMDS)
            conn.send(imagepath + "\n")
        conn.close()

InitGL(720,1280)
runServer('127.0.0.1',5005)


