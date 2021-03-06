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


# Number of the glut window.
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
    glBegin(GL_QUADS)                # Start Drawing The Cube
    # Front Face (note that the texture's corners have to match the quad's corners)
    glTexCoord2f(0.0, 0.0); glVertex3f(x, y,  -0.001)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f( x+1, y,  -0.001)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( x+1,  y+1, -0.001)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(x,  y+1,  -0.001)    # Top Left Of The Texture and Quad
    glEnd();                # Done Drawing The Cube


def LoadTexture(num,blur):
    #global texture
    image = open("characters/" + num + "b" + blur + ".bmp")
    
    ix = image.size[0]
    iy = image.size[1]
    image = image.tostring("raw", "RGBX", 0, -1)
    
    # Create Texture    
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))   # 2d texture (x and y size)
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(width, height):                # We call this right after our OpenGL window is created.
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

# The function called when our window is resized
def ReSizeGLScene(Width, Height):
    if Height == 0:                        # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(Width)/float(Height), 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)

counter = 0
# The main drawing function. 
def DrawGLScene(CMDS):
    global texture
    global counter
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    # Clear The Screen And The Depth Buffer
    glLoadIdentity()                    # Reset The View
    glClearColor(1,1,1,1.0)

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

        #draws the first character
        #if(characters[0]!='0'):
        #   drawCharacter(characters[0],characters[1],0%9,0/9)



        i = 0
        while i < len(characters):
            if(characters[i]=='0'):
                i = i + 1
            else:
               drawCharacter(characters[i],5,(i)%9,(i)/9)
               i = i+1

        '''
        i = 0
        for c in characters:
            if(c==0):
                i = i + 1
            else:
                drawCharacter(c,i%9,i/9)
                i = i+1
        '''



    glDisable(GL_TEXTURE_2D)
    sudokuGrid()


    #a = time.time()
    width,height = 720,1280
    #imagepath = "C:/Users/Alan/Documents/SudokuProject/renders/" + str(counter) + ".png"
    counter = counter + 1
    imagepath = "C:/Users/Alan/Documents/SudokuProject/renders/" + CMDS + ".png"
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.fromstring("RGBA",(width,height),data)
    image = image.transpose( Image.FLIP_TOP_BOTTOM)
    glutSwapBuffers()
    image=image.convert('L')
    image.save(imagepath)

    '''
    img = numpy.asarray(image)
    img = cv2.GaussianBlur(img,(3,3),0)
    img= cv2.Canny(img,300,400)
    cv2.imwrite(imagepath,img)
    #print((time.time()-a)*1000)
    '''

    return imagepath


# Print message to console, and kick off the main to get it rolling.
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
            conn.send(imagepath + "\n")  # echo
        conn.close()

InitGL(720,1280)
runServer('127.0.0.1',5005)
#DrawGLScene("4.5_4.5_16_4.5_5.5_0_1")
#DrawGLScene("4.3_5_16_4.5_5_-0.4_0102030405")
        
