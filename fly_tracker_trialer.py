from PyQt5.QtWidgets import  QWidget
from PyQt5.QtCore import *

from syringe_pumper import *
from daq_rider import *

import threading import Timer
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from fly_tracker_utils import get_all_from_queue

class FlyTrialer(QThread):
    def __init__(self, sp, dr, geometry, central_widget, trial_data_q, trial_ball_data_acq_start_event):
        super(FLyTrialer, self).__init__(None)
        
        self.sp = sp
        self.dr = dr
        
        self.trial_start_event = theading.Event()
        self.trial_ball_data_acq_start_event = trial_ball_data_acq_start_event
        self.trial_data_q = self.trial_data_q

        self.experimentDir   = None
        self.prate           = -1.0
        self.num_trials      = -1
        self.pre_stim_t      = -1
        self.stim_t          = -1
        self.flush_t         = -1
        self.trial_period_t  = -1
        self.stim_type       = None

        # Setup plot area
        self.plot_area = QWidget( central_widget )
        self.plot_area.setGeometry( geometry )
        self.dpi = 100
        self.fig = Figure( dpi=self.dpi )
        self.canvas = FigureCanvas( self.fig )
        self.canvas.setParent( self.plot_area )
        self.axes = self.fig.add_subplot(111)
        
        self.start()                    

    def run(self):
        
        while True:        
            if( not self.trial_start_event.isSet() ):
                QThread.yieldCurrentThread()
            else:
                trial_results = []
                for i in range(self.num_trials):
                    trial_data = self.run_trial( i )
                    trial_results.append( trial_data )
                    
                    t, x, y = zip(*trial_data)
                    
                    # plot data
                    label_str = 'Trial: %d' % (i) 
                    self.axes.plot( x, y, hold=True, label=label_str)
                    self.axes.legend()
                    
                    # Pause
                    print "Finished trial: ", i
                    for st in range(self.trial_period_t):
                        time.sleep(1)
                        print('.',end="",flush=True)
                
                self.trial_start_event.clear()
    
    def start_trials(self, num_trials, pre_stim_t, stim_t, flush_t, trial_period_t, stim_type, prate, experiment_dir):
        
        self.experimentDir   = experiment_dir
        self.prate           = prate
        self.num_trials      = num_trials
        self.pre_stim_t      = pre_stim_t
        self.stim_t          = stim_t
        self.flush_t         = flush_t
        self.trial_period_t  = trial_period_t
        self.stim_type       = stim_type
    
        self.trial_start_event.set() 
        
            
    def run_trial(self, trial_ord):
        
        # Reset all daq board channels
        self.dr.reset_all()

        # Set syringe pump to max rate and withdraw
        self.sp.set_rate(10.0)
        self.sp.withdraw()

        self.sp.start()
        time.sleep( 17.0 )
        self.sp.stop()

        # Prepare syringe pumps for stim
        self.sp.infuse()
        self.sp.set_rate( self.prate )

        # Prepare valves for stim
        self.dr.activate_pinch_valves( self.stim_type )
        self.dr.activate_3way_valves()
        
        # Pause for 10 seconds before starting stim, as per Gaudry et al.
        # Wait for 5 seconds after valve switch
        # Take 5 seconds of baseline
        time.sleep(5)

        # Start trial, acquire ball data and camera data to save
        self.trial_ball_data_acq_start_event.set()

        # baseline
        time.sleep(5)
        
        # Start stim
        self.sp.start()
        time.sleep(self.stim_t)
        self.sp.stop()

        ## WARNING: This is a temp workaround some race condition in 
        # communicating with the daq board
        time.sleep(1.0)
        
        # Prepare syringe pumps for flush 
        self.sp.set_rate( 10.0 )

        # Set pinch valves for 'Both Air'
        self.dr.activate_pinch_valves('Both Air')

        # Start stim
        self.sp.start()
        time.sleep( self.flush_t )
        self.sp.stop()

        # Ready to read trial data
        self.trial_ball_data_acq_start_event.clear()
        self.dr.reset_all()

        # Trial data ready to plot
        # Read data from queue
        qdata = list(get_all_from_queue(self.trial_data_q))

        return qdata
