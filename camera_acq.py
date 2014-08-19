import Image
import numpy as np
import time

from OpenGL.GL import *
from PyQt5.QtWidgets import  QWidget
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import *

# Camera communication
from pydc1394 import DC1394Library, Camera

class AcquisitionThread(QThread):
    def __init__(self, cam, parent = None):
        super(AcquisitionThread, self).__init__(parent)

        self._new_image_signal = pyqtSignal()
        self._stopped = False
        self._mutex = QMutex()

        self._cam = cam

        self.start()

    def stop(self):
        try:
            self._mutex.lock()
            self._stopped = True
        finally:
            self._mutex.unlock()

    def isStopped(self):
        s = False
        try:
            self._mutex.lock()
            s = self._stopped
        finally:
            self._mutex.unlock()
        return s

    def run(self):
        if not self._cam.running:
            self._cam.start(interactive=True)

        while not self.isStopped():
            self._cam.new_image.acquire()
            if not self._cam.running:
                self.stop()
            else:
                self.emit(self._new_image_signal, self._cam.current_image)
            self._cam.new_image.release()

class LiveCameraPortal(QGLWidget):

    def __init__(self, cam, geometry, parent):
        f = QGLFormat()
        # The next line decides if the image flickers or not.
        # Unfortunately, if the image doesn't flicker, we do not get
        # a high enough frame rate to display our camera images if we try
        # to display them all. We now use a QTimer to redraw our window
        # every 1/60 of a second, and this seems to work well.
        f.setSwapInterval( 1 )
        super(LiveCameraPortal, self).__init__(f, parent)

        self.setGeometry( geometry )

        self.dtype = cam.mode.dtype
        shape = ( geometry.size().height(), geometry.size().width() )
        self._arr = np.empty(shape, dtype=self.dtype)
        self._gldrawmode = GL_LUMINANCE  if len(shape) == 2 else GL_RGB

        if self.dtype[-1] in ['1','8']:
            self._glinternal = GL_UNSIGNED_BYTE
        elif self.dtype[-2:] == '16' or dtype[-1] == '2':
            self._glinternal = GL_UNSIGNED_SHORT
        else:
            raise RuntimeError, "Unknown datatype!"

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)

        self.setFocusPolicy(Qt.WheelFocus)

        # We redraw our image 60 times per second; no matter what kind of camera
        # is attached
        self.aTimer = QTimer()
        self.aTimer.timeout.connect(self.updateGL)
        self.aTimer.start(1000/60)

        # Initialisations for FPS calculation
        self._ltime = time.time()
        self._drawn_frames = 0
        self._totframes = 0

    """
    def minimumSizeHint(self):
        return QSize(self._arr.shape[1]*self._zoom,
                     self._arr.shape[0]*self._zoom)
    """

    def heightForWidth(self, w):
        return w/self._arr.shape[1] * self._arr.shape[0]

    def newImage(self, img):

        # Resize the incoming camera image to fit the display window
        pil_img = Image.fromarray( img, 'L' )
        pil_img_resized = pil_img.resize( (self._arr[2], self._arr[1]), Image.NEAREST )

        self._arr = numpy.asarray( pil_img_resized )
        # self.updateGL()

    def initializeGL( self ):
        """
        This function initalizes OpenGL according to what we need
        in this context
        """
        glEnable(GL_TEXTURE_2D);					# Enable Texture Mapping
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST); #  Set Texture Max Filter
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST); # Set Texture Min Filter

        # Determine the texture size (which must be 2**x)
        texdim_w, texdim_h = 32,32
        while texdim_w < self._arr.shape[1]:
            texdim_w *= 2
        while texdim_h < self._arr.shape[0]:
            texdim_h *= 2
        self._texture_coords = (float(self._arr.shape[1])/texdim_w,float(self._arr.shape[0])/texdim_h)

        # Generate our Texture
        # The next line makes sure that bytes are read in the correct
        # order while unpacking from python
        glPixelStoref(GL_UNPACK_SWAP_BYTES, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, self._gldrawmode, texdim_w, texdim_h, 0, self._gldrawmode, self._glinternal, None)

        # Set our viewport
        w,h = self.width(), self.height()

        glViewport(0, 0, w, h)
        glClear( GL_COLOR_BUFFER_BIT );

        # Set our Projection to Orthographic and the coordinate system
        # like the picture
        glMatrixMode( GL_PROJECTION );
        glLoadIdentity();
        glOrtho(0.0, self._arr.shape[1], self._arr.shape[0], 0.0, -1.0, 1.0);

        glMatrixMode( GL_MODELVIEW );
        glLoadIdentity();

        # self._quadric = gluNewQuadric()

    def resizeGL(self, width, height):
        # Reset our Viewpoint.
        glViewport(0, 0, width, height)

    def paintGL(self):
        # Remake the Texture from the new image data
        glTexSubImage2D (GL_TEXTURE_2D, 0, 0, 0,
            self._arr.shape[1], self._arr.shape[0],
            self._gldrawmode, self._glinternal, self._arr);

        glColor3f( 1.,1.,1. )

        # Draw the imageplane
        x,y = self._texture_coords
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.); glVertex3f(0., 0., - .5)
        glTexCoord2f(x, 0.); glVertex3f(self._arr.shape[1], 0., - .5)
        glTexCoord2f(x, y); glVertex3f(self._arr.shape[1],
                            self._arr.shape[0], - .5)
        glTexCoord2f(0., y); glVertex3f(0., self._arr.shape[0], - .5)
        glEnd()

        # Calculate the FPS
        ctime = time.time()
        dtime = ctime-self._ltime
        if dtime > 1:
            fps= self._drawn_frames/dtime
            self._ltime = ctime
            self._drawn_frames = 0
            self._fps = fps
        self._drawn_frames += 1
        self._totframes += 1

    def close():
        pass

class CameraRider:
    def __init__(self, cam_geometries, parent):
        cam_lib = DC1394Library()
        
        active_cameras = cam_lib.enumerate_cameras()
        
        self.cams = []
        self.acqThreads = []
        self.liveCamPortals = []
        for i, cam in active_cameras:
            guid = cam['guid']
            cur_cam = Camera( cam_lib, guid=guid )
            self.cams.append( cur_cam )
            
            live_portal = LiveCameraPortal( cur_cam, cam_geometries[i], parent )
            self.liveCamPortals.append( live_portal )

            cur_thread = AcquisitionThread( cur_cam )
            cur_thread._new_image_signal.connect( live_portal.newImage )
            self.acqThreads.append( cur_thread )

    def close(self):
        for i, cam in self.cams:
            cam.close()
            self.liveCamPortals[i].close()        

