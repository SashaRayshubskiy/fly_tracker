from PyQt5.QtWidgets import  QMainWindow, QFileDialog
from PyQt5.QtCore import *

# Import the GUI created in Qt Designer
from fly_tracker_gui_auto import Ui_FlyTracker

from camera_acq import *
from syringe_pumper_chemyx import *
#from syringe_pumper_new_era import *

from daq_rider_v2 import *
from fly_tracker_trialer import *
from fly_tracker_ball_tracker import *

import Queue
import threading 
import time

from subprocess import call

class FlyTrackerWindow(QMainWindow):
    def __init__(self):
        super(FlyTrackerWindow, self).__init__()

        self.start_t = time.time()

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
        self.ui.choose_task_file_button.clicked.connect(self.choose_task_file_clicked_callback)


        # Create UI text edit connections 
        self.ui.rate_box.valueChanged.connect(self.rate_changed_callback)
        self.ui.stim_prate_box.valueChanged.connect(self.stim_rate_changed_callback)
        self.ui.flush_prate_box.valueChanged.connect(self.flush_rate_changed_callback)
        self.ui.syringe_size_box.valueChanged.connect(self.syringe_size_changed_callback)
        self.ui.pre_stim_box.valueChanged.connect(self.pre_stim_changed_callback)
        self.ui.stim_box.valueChanged.connect(self.stim_changed_callback)
        self.ui.flush_box.valueChanged.connect(self.flush_changed_callback)
        self.ui.trial_period_box.valueChanged.connect(self.trial_period_changed_callback)
        self.ui.num_trials_box.valueChanged.connect(self.num_trials_changed_callback)
        self.ui.max_velocity.valueChanged.connect(self.max_velocity_changed_callback)
        self.ui.using2p_toggle.toggled.connect(self.using2p_toggle_changed_callback)
        self.ui.using_optostim_toggle_2.toggled.connect(self.using_optostim_changed_callback)
        self.ui.session_id_box.valueChanged.connect(self.session_id_changed_callback)

        self.ui.stim_type.currentIndexChanged['QString'].connect(self.stim_type_changed_callback)

        # Init GUI variables
        self.task_file       = '/home/sasha/fly_tracker/task_file.txt'
        self.experimentDir   = None
        self.syringe_size    = self.ui.syringe_size_box.value()
        self.prate           = self.ui.rate_box.value()
        self.stim_prate      = self.ui.stim_prate_box.value()
        self.flush_prate     = self.ui.flush_prate_box.value()
        self.num_trials      = self.ui.num_trials_box.value()
        self.pre_stim_t      = self.ui.pre_stim_box.value()
        self.stim_t          = self.ui.stim_box.value()
        self.flush_t         = self.ui.flush_box.value()
        self.trial_period_t  = self.ui.trial_period_box.value()
        self.stim_type       = self.ui.stim_type.currentText()
        self.using2p         = self.ui.using2p_toggle.isChecked() 
        self.using_optostim  = self.ui.using_optostim_toggle_2.isChecked() 
        self.session_id      = self.ui.session_id_box.value()

        # Set the experiment directory
        self.choose_dir_clicked_callback(0)
        
        # Init device communication variables
        self.init()

    def closeEvent(self, event):
        self.finalize()        
        event.accept() # let the window close

    def session_id_changed_callback(self,val):
        self.session_id = val

    def using2p_toggle_changed_callback(self, val):
        self.using2p = val

    def using_optostim_changed_callback(self, val):
        self.using_optostim = val

    def stim_type_changed_callback(self, val):        
        self.stim_type = val # recorded as text

    # Text edit callbacks
    def rate_changed_callback(self, val):
        self.prate           = val
        self.sp.set_rate(val)

    def stim_rate_changed_callback(self, val):
        self.stim_prate           = val

    def flush_rate_changed_callback(self, val):
        self.flush_prate           = val

    def syringe_size_changed_callback(self, val):
        self.syringe_size = val
        self.sp.set_syringe_size(val)

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

    def choose_task_file_clicked_callback(self, val):
        rc = QFileDialog.getOpenFileName(self,
                                         "Choose a task file", 
                                         "/home/sasha/fly_tracker/")
        self.task_file = rc[0]

        print self.task_file

        self.ui.task_file_dir.setPlainText( self.task_file )        

    def choose_dir_clicked_callback(self, val):
                
        self.experimentDir = QFileDialog.getExistingDirectory(self,
                                                              "Choose an experiment directory", "/home/sasha/fly_trackball_data/")

        self.ui.experimental_dir_text.setPlainText( self.experimentDir )    
        
        # chown the directory by user
        call(['chown', 'sasha', self.experimentDir])

    def finalize(self):
        self.sp.close()
        self.cr.close()
        self.dr.close()
        self.th.close()
        self.ballPlotterCont.close()

    # Button callbacks
    def init(self):

        # Init syringe pump
        self.sp = SyringePumper(self.start_t, self.syringe_size, self.prate)

        # Connect to cameras
        camera_geometries = [ self.ui.camera1.geometry(), self.ui.camera2.geometry() ]
        self.cr = CameraRider( camera_geometries, self.ui.centralwidget, self.experimentDir )

        # Init daq board connection for valve control
        self.dr = DAQRider(self.start_t)

        # Init the fly ball reader, for contineous and trial acq
        self.data_q_cont = Queue.Queue()
        self.data_q_trial = Queue.Queue()
        self.trial_ball_data_acq_start_event = threading.Event() # Needed to trigger start of trial
        self.ballReader  = FlyBallReaderThread( self.data_q_cont, 
                                                self.data_q_trial, 
                                                self.trial_ball_data_acq_start_event ) 
        
        # Init fly ball tracker
        self.ballPlotterCont = FlyBallPlotterContinuous( self.data_q_cont, 
                                                         self.ui.cummulative_run.geometry(), 
                                                         self.ui.polar_plot_1.geometry(), 
                                                         self.ui.centralwidget, 
                                                         self.experimentDir )

        # Init trial handler
        self.th = FlyTrialer( self.start_t,
            self.sp, 
            self.dr,
            self.ui.trial_run1.geometry(), 
            self.ui.trial_run2.geometry(), 
            self.ui.centralwidget, 
            self.data_q_trial, 
            self.trial_ball_data_acq_start_event,
            self.ballPlotterCont )

    def infuse_clicked_callback(self, val):
        self.sp.infuse()

    def withdraw_clicked_callback(self, val):
        self.sp.withdraw()

    def start_clicked_callback(self, val):
        self.sp.start()
        
    def stop_clicked_callback(self, val):
        self.sp.stop()

    def run_clicked_callback(self, val):
        self.th.start_trials( self.num_trials, self.pre_stim_t, 
                              self.stim_t, self.flush_t, 
                              self.trial_period_t, self.stim_type, 
                              self.stim_prate, self.flush_prate, 
                              self.using2p, self.using_optostim,
                              self.experimentDir,
                              self.task_file,
                              self.session_id )

        
        self.ui.session_id_box.setValue(self.session_id+1)
        self.session_id = self.session_id + 1
        
    def max_velocity_changed_callback(self,val):
        self.ballPlotterCont.set_max_velocity(val)

