from PyQt5.QtWidgets import  QWidget
from PyQt5.QtCore import *

import time
import math
import sys
import numpy as np

from syringe_pumper import *
from daq_rider import *

from threading import Timer, Event
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from fly_tracker_utils import get_all_from_queue

class FlyTrialer(QThread):
    def __init__(self, sp, dr, geometry, central_widget, trial_data_q, trial_ball_data_acq_start_event):
        super(FlyTrialer, self).__init__(None)
        
        self.sp = sp
        self.dr = dr
        
        self.trial_start_event = Event()
        self.trial_ball_data_acq_start_event = trial_ball_data_acq_start_event
        self.trial_data_q = trial_data_q

        self.experimentDir   = None
        self.prate           = -1.0
        self.num_trials      = -1
        self.pre_stim_t      = -1
        self.stim_t          = -1
        self.flush_t         = -1
        self.trial_period_t  = -1
        self.stim_type       = None

        self.stim_type_d = {}
        self.stim_type_d['Both Air'] = 'BA'
        self.stim_type_d['Both Air'] = 'BO'
        self.stim_type_d['Left Odor'] = 'LO'
        self.stim_type_d['Right Odor'] = 'RO'
        

        # Setup plot area
        self.plot_area = QWidget( central_widget )
        self.plot_area.setGeometry( geometry )

        w = geometry.width()
        h = geometry.height()
        self.dpi = 80
        
        w_inch = math.ceil(float(w) / float(self.dpi))
        h_inch = math.ceil(float(h) / float(self.dpi))

        # print "trialer: w_inch, h_inch: ( %f %f )" % ( w_inch, h_inch )
        # print "trialer: w, h: ( %f %f )" % ( w, h )

        self.fig = Figure( dpi=self.dpi, facecolor="w" )        
        self.fig.set_size_inches(6.0, 6.0, forward=True)

        self.canvas = FigureCanvas( self.fig )
        self.canvas.setParent( self.plot_area )
        self.axes = self.fig.add_subplot(111)
        
        self.start()                    

    def calc_trial_trajectory(self, dx, dy):
        traj_x = np.zeros( len(dx) )
        traj_y = np.zeros( len(dy) )

        traj_x[0] = dx[0]
        traj_y[0] = dy[0]
        
        i=1
        while i<len(dx):
            traj_x[i] = traj_x[i-1] + dx[i]
            traj_y[i] = traj_y[i-1] + dy[i]
            i=i+1

        return (traj_x, traj_y)

    def run(self):
        
        while True:        
            if( not self.trial_start_event.isSet() ):
                QThread.yieldCurrentThread()
            else:
                trial_results = []
                for i in range(self.num_trials):
                                        
                    trial_data = self.run_trial( i )
                    trial_results.append( trial_data )
                    
                    if len(trial_data) > 0:
                        t, dx, dy = zip(*trial_data)
                    
                        traj_x, traj_y = self.calc_trial_trajectory( dx, dy )

                        # plot data
                        label_str = 'Trial: %d %s' % (i,self.stim_type_d[self.stim_type]) 
                        self.axes.hold(True)
                        self.axes.plot( traj_x, traj_y, label=label_str)
                        self.axes.legend()
                        self.fig.canvas.draw()
                    
                    if self.num_trials > 1:
                        # Pause
                        print "Finished trial: ", i
                        self.sleep_with_status_update(self.trial_period_t, "Inter trial wait" )
                    self.trial_start_event.clear()
    
    def sleep_with_status_update(self, sleep_t, name):
        
        if not sleep_t.is_integer():
            raise Exception( "ERROR: sleep time is not an integer: %f" % ( sleep_t ))

        print "(%s): About to sleep for %f sec" % (name, float(sleep_t))
        for st in range(int(sleep_t)):
            time.sleep(1)
            sys.stdout.write('.')
            sys.stdout.flush()
        sys.stdout.write('\n')        

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
        self.sleep_with_status_update(17.0, "Syringe pump withdraw before stim")
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
        self.sleep_with_status_update(5.0, "Wait before start of data acq")

        # Start trial, acquire ball data and camera data to save
        self.trial_ball_data_acq_start_event.set()

        # baseline
        self.sleep_with_status_update(self.pre_stim_t, "Data Acq::Baseline")
        
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
        self.sleep_with_status_update(self.flush_t, "Flush")
        self.sp.stop()

        # Ready to read trial data
        self.trial_ball_data_acq_start_event.clear()
        self.dr.reset_all()

        # Trial data ready to plot
        # Read data from queue
        qdata = list(get_all_from_queue(self.trial_data_q))

        return qdata
