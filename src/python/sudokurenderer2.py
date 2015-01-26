__author__ = 'Alan'

import socket
import time
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

width, height = 720,1280

def sudokuGrid():
    glLineWidth(2)
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

    glLineWidth(2)
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

def initialiseGL():
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

def render(CMDS):

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    ex,ey,ez,cx,cy,cz = CMDS.split("_")
    ex = float(ex)
    ey = float(ey)
    ez = float(ez)
    cx = float(cx)
    cy = float(cy)
    cz = float(cz)

    gluLookAt(ex,ey,ez,cx,cy,cz, 0, 1, 0)

    sudokuGrid()
    imagepath = "C:/Users/Alan/Documents/SudokuProject/renders/" + CMDS + ".png"
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.fromstring("RGBA", (width, height), data)
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

            imagepath = render(CMDS)
            conn.send(imagepath + "\n")  # echo
        conn.close()

initialiseGL()
runServer('127.0.0.1',5005)
