from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from Image import *

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0
texture = 0

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

def drawCharacter(num,x,y):
    LoadTexture(str(num))
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)                # Start Drawing The Cube
    # Front Face (note that the texture's corners have to match the quad's corners)
    glTexCoord2f(0.0, 0.0); glVertex3f(x, y,  -0.01)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f( x+1, y,  -0.01)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( x+1,  y+1, -0.01)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(x,  y+1,  -0.01)    # Top Left Of The Texture and Quad
    glEnd();                # Done Drawing The Cube


def LoadTexture(num):
    #global texture
    image = open(num + ".bmp")
    
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
def InitGL(Width, Height):                # We call this right after our OpenGL window is created.
    #LoadTextures()
    #glEnable(GL_TEXTURE_2D)
    glClearColor(1.0, 1.0, 1.0, 1.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:                        # Prevent A Divide By Zero If The Window Is Too Small 
        Height = 1

    glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# The main drawing function. 
def DrawGLScene():
    global texture

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    # Clear The Screen And The Depth Buffer
    glLoadIdentity()                    # Reset The View
    glClearColor(1,1,1,1.0)
    
    #glTranslatef(-4.0,-4.0,-10.0)            # Move Into The Screen
    #glRotate(45,0,0,1)
    gluLookAt(3.0,3.0,20,4.5,4.5,0, 0, 1, 0)



    drawCharacter(1,0,0);
    drawCharacter(2,1,1);
    drawCharacter(3,2,2);
    drawCharacter(4,3,3);
    drawCharacter(5,4,4);
    drawCharacter(6,5,5);
    drawCharacter(7,6,6);
    drawCharacter(8,7,7);
    drawCharacter(9,8,8);

    glDisable(GL_TEXTURE_2D)
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 1, 0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 1)
    glEnd()
    sudokuGrid()



    


    #  since this is double buffered, swap the buffers to display what just got drawn. 
    glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == ESCAPE:
        sys.exit()

def main():
    global window
    glutInit(sys.argv)

    # Select type of Display mode:   
    #  Double buffer 
    #  RGBA color
    # Alpha components supported 
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    
    # get a 640 x 480 window 
    glutInitWindowSize(720, 1280)
    
    # the window starts at the upper left corner of the screen 
    glutInitWindowPosition(0, 0)
    
    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("SudokuRenderer")

       # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.    
    glutDisplayFunc(DrawGLScene)
    
    # Uncomment this line to get full screen.
    # glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)
    
    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)
    
    # Register the function called when the keyboard is pressed.  
    glutKeyboardFunc(keyPressed)

    # Initialize our window. 
    InitGL(640, 480)

    # Start Event Processing Engine    
    glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
if __name__ == "__main__":
    print "Hit ESC key to quit."
    main()
        
