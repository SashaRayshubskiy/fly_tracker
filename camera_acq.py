import time

from PyQt5.QtWidgets import  QLabel 
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap

# Camera communication
from pydc1394 import DC1394Library, Camera

from qimage2ndarray import *

import cv2
from datetime import datetime
import numpy as np

class AcquisitionThread(QThread):
    _new_image_signal = pyqtSignal('QImage')

    def __init__(self, cam, parent = None):
        super(AcquisitionThread, self).__init__(parent)

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
                cur_img = self._cam.current_image
                qimage = gray2qimage(cur_img)
                self._new_image_signal.emit( qimage )
            self._cam.new_image.release()

class LiveCameraPortal:
    def __init__(self, geometry, centralwidget, guid, location, experiment_dir ):

        self.imageLabel = QLabel( parent=centralwidget )
        # self.imageLabel.setBackgroundRole( QPalette.Base )
        # imageLabel.setSizePolicy( QSizePolicy.Ignored, QSizePolicy.Ignored )
        self.imageLabel.setScaledContents( True )
        self.imageLabel.setGeometry( geometry )

        self.shape = ( geometry.size().width(), geometry.size().height() )
        self.cur_img = QImage( self.shape[0], self.shape[1], QImage.Format_Indexed8 )
    
        """
        # We redraw our image 60 times per second; no matter what kind of camera
        # is attached
        self.aTimer = QTimer()
        self.aTimer.timeout.connect(self.updateCamera)
        self.aTimer.start(1000/60)
        """

        # Initialisations for FPS calculation
        self._ltime = time.time()
        self._drawn_frames = 0
        self._totframes = 0

        self.guid = guid
        self.location = location

        self.FORMAT = '%Y_%m%d_%H%M%S'
        
        self.img_cnt = 0
        self.IMG_SAVE_MOD_CONST = 100
        self.video_out = None
        self.experiment_dir = experiment_dir

    def newImage(self, img):

        # Resize the incoming camera image to fit the display window        
        if self.location == 'front':
            self.cur_img = img.scaled( self.shape[0], self.shape[1] ).mirrored(horizontal=True, vertical=True)
        else:
            self.cur_img = img.scaled( self.shape[0], self.shape[1] )
            
            """
            # save movie frame 
            #self.pipe.communicate(input=img.bits())
            if self.video_out == None or ((self.img_cnt % self.IMG_SAVE_MOD_CONST) == 0):

                if self.video_out != None:
                    print 'Writing video to disk'
                    self.video_out.release()

                avi_file = self.experiment_dir + '/' + datetime.now().strftime(self.FORMAT) + '_side_cam.avi'
                fourcc = cv2.cv.CV_FOURCC(*'XVID')
                self.video_out = cv2.VideoWriter(avi_file,fourcc, 20.0, (img.height(),img.width()))
                
            np_img = qimage2numpy( img )
            # print 'np_img.shape', np_img.shape
            self.video_out.write( np_img )
            self.img_cnt = self.img_cnt + 1
            """

        # Show image
        self.imageLabel.setPixmap(QPixmap.fromImage(self.cur_img))            


    def close(self):
        pass

class CameraRider:
    def __init__(self, cam_geometries, centralwidget, experiment_dir):
        cam_lib = DC1394Library()
        
        active_cameras = cam_lib.enumerate_cameras()
        
        self.cams = []
        self.acqThreads = []
        self.liveCamPortals = []
        self.camera_location = None
        for i, cam in enumerate(active_cameras):
            
            guid = cam['guid']
            
            # One of the cameras needs to have their mode set
            if guid==582164335768600639:
                cur_mode=(640, 480, "Y8")
                self.camera_location = 'front'
            else:
                self.camera_location = 'side'
                cur_mode=None

            cur_cam = Camera( cam_lib, mode=cur_mode, guid=guid )
            self.cams.append( cur_cam )
            
            live_portal = LiveCameraPortal( cam_geometries[i], centralwidget, guid, self.camera_location, experiment_dir )
            self.liveCamPortals.append( live_portal )

            cur_thread = AcquisitionThread( cur_cam )
            cur_thread._new_image_signal.connect( live_portal.newImage )
            # self.connect(self.cur_thread, SIGNAL("newImage"), live_portal.newImage )
            self.acqThreads.append( cur_thread )

    def close(self):
        for i, cam in enumerate(self.cams):
            cam.close()
            self.liveCamPortals[i].close()        

