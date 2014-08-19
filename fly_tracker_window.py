from PyQt5.QtWidgets import  QMainWindow, QFileDialog
from PyQt5.QtCore import *

# Import the GUI created in Qt Designer
from fly_tracker_gui_auto import Ui_FlyTracker

from camera_acq import *
from syringe_pumper import *
from daq_rider import *
from fly_tracker_trialer import *

import threading 
import time

class FlyTrackerWindow(QMainWindow):
    def __init__(self):
        super(FlyTrackerWindow, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_FlyTracker()
        self.ui.setupUi(self)

        # Create UI botton press connections 

        # self.ui.init_button.clicked.connect(self.init_clicked_callback)
        self.ui.start_button.clicked.connect(self.start_clicked_callback)
        self.ui.stop_button.clicked.connect(self.stop_clicked_callback)
        self.ui.infuse_button.clicked.connect(self.infuse_clicked_callback)
        self.ui.withdraw_button.clicked.connect(self.withdraw_clicked_callback)
        self.ui.run_button.clicked.connect(self.run_clicked_callback)
        self.ui.choose_dir_button.clicked.connect(self.choose_dir_clicked_callback)        

        # Create UI text edit connections 
        self.ui.rate_box.valueChanged.connect(self.rate_changed_callback)
        self.ui.diameter_box.valueChanged.connect(self.diameter_changed_callback)
        self.ui.pre_stim_box.valueChanged.connect(self.pre_stim_changed_callback)
        self.ui.stim_box.valueChanged.connect(self.stim_changed_callback)
        self.ui.flush_box.valueChanged.connect(self.flush_changed_callback)
        self.ui.trial_period_box.valueChanged.connect(self.trial_period_changed_callback)
        self.ui.num_trials_box.valueChanged.connect(self.num_trials_changed_callback)

        self.ui.stim_type.currentIndexChanged['QString'].connect(self.stim_type_changed_callback)

        # Init GUI variables
        self.experimentDir   = None
        self.diameter        = self.ui.diameter_box.value()
        self.prate           = self.ui.rate_box.value()
        self.num_trials      = self.ui.num_trials_box.value()
        self.pre_stim_t      = self.ui.pre_stim_box.value()
        self.stim_t          = self.ui.stim_box.value()
        self.flush_t         = self.ui.flush_box.value()
        self.trial_period_t  = self.ui.trial_period_box.value()
        self.stim_type       = self.ui.stim_type.currentText()

        # Init device communication variables
        self.init()

    def closeEvent(self, event):
        self.finalize()        
        event.accept() # let the window close

    def stim_type_changed_callback(self, val):        
        self.stim_type = val # recorded as text

    # Text edit callbacks
    def rate_changed_callback(self, val):
        self.prate           = val
        self.sp.set_rate(val)

    def diameter_changed_callback(self, val):
        self.diameter = val
        self.sp.set_diameter(val)

    def pre_stim_changed_callback(self, val):
        self.pre_stim_t = val

    def stim_changed_callback(self, val):
        self.stim_t = val

    def flush_changed_callback(self, val):
        self.flush_t = val
        
    def trial_period_changed_callback(self, val):
        self.trial_period_t = val

    def num_trials_changed_callback(self, val):
        self.num_trials = val

    def choose_dir_clicked_callback(self, val):
        self.experimentDir = QFileDialog.getExistingDirectory(self,
                                                              "Choose an experiment directory", "/home/sasha")

        self.ui.experimental_dir_text.setPlainText( self.experimentDir )

    def finalize(self):
        self.sp.close()
        self.cr.close()
        self.dr.close()

    # Button callbacks
    def init(self):

        # Init syringe pump
        self.sp = SyringePumper(self.diameter, self.prate)

        # Connect to cameras
        camera_geometries = [ self.ui.camera1.geometry(), self.ui.camera2.geometry() ]
        self.cr = CameraRider( camera_geometries, self.ui.centralwidget )

        # Init daq board connection for valve control
        self.dr = DAQRider()

        # Init the fly ball reader, for contineous and trial acq
        self.data_q_cont = Queue.Queue()
        self.data_q_trial = Queue.Queue()
        self.trial_ball_data_acq_start_event = threading.Event() # Needed to trigger start of trial
        self.ballReader  = FlyBallReaderThread( self.data_q, self.data_q_trial, self.trial_ball_data_acq_start_event ) 
        
        # Init trial handler
        self.th = FlyTrialer( self.sp, 
                              self.dr,
                              self.ui.trial_run.geometry(), 
                              self.ui.centralwidget, 
                              self.data_q_trial, 
                              self.trial_ball_data_acq_start_event )

        # Init fly ball tracker
        self.ballPlotterCont = FlyBallPlotterContinuous( self.data_q_cont, self.ui.cummulative_run.geometry(), central_widget )


    def infuse_clicked_callback(self, val):
        self.sp.infuse()

    def withdraw_clicked_callback(self, val):
        self.sp.withdraw()

    def start_clicked_callback(self, val):
        self.sp.start()
        
    def stop_clicked_callback(self, val):
        self.sp.stop()

    def run_clicked_callback(self, val):        
        
        self.th.start_trial( self.num_trials, self.pre_stim_t, 
                             self.stim_t, self.flush_t, 
                             self.trial_period_t, self.stim_type, 
                             self.prate, self.experimentDir )
        

