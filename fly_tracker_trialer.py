from PyQt5.QtWidgets import  QWidget
from PyQt5.QtCore import *

import time
import math
import sys
import numpy as np
from datetime import datetime

import scipy.io

from syringe_pumper import *
from daq_rider import *

from threading import Timer, Event
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from fly_tracker_utils import get_all_from_queue

class FlyTrialer(QThread):
    def __init__(self, start_t, sp, dr, geometry1, geometry2, central_widget, trial_data_q, trial_ball_data_acq_start_event):
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

        self.runId           = 0
        self.trial_withdraw_t = 20.0

        self.FORMAT = '%Y_%m%d_%H%M%S'
        self.start_t = start_t
        self.stim_type_d = {}
        self.stim_type_d['Both Air'] = 'BA'
        self.stim_type_d['Both Odor'] = 'BO'
        self.stim_type_d['Left Odor'] = 'LO'
        self.stim_type_d['Right Odor'] = 'RO'
        

        # Setup plot area
        self.plot_area1 = QWidget( central_widget )
        self.plot_area1.setGeometry( geometry1 )

        self.dpi = 80
        
        self.fig1 = Figure( dpi=self.dpi, facecolor="w" )        
        self.fig1.set_size_inches(5.0, 6.0, forward=True)

        self.canvas1 = FigureCanvas( self.fig1 )
        self.canvas1.setParent( self.plot_area1 )
        self.axes1 = self.fig1.add_subplot(111)

        self.plot_area2 = QWidget( central_widget )
        self.plot_area2.setGeometry( geometry2 )
        self.fig2 = Figure( dpi=self.dpi, facecolor="w" )        
        self.fig2.set_size_inches(5.5, 6.0, forward=True)

        self.canvas2 = FigureCanvas( self.fig2 )
        self.canvas2.setParent( self.plot_area2 )
        self.axes_xt = self.fig2.add_subplot(211)
        self.axes_yt = self.fig2.add_subplot(212)
        
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
                self.axes1.cla()
                self.axes_xt.cla()
                self.axes_yt.cla()
                self.fig1.canvas.draw()
                self.fig2.canvas.draw()

                run_data = []
                
                for i in range(self.num_trials):
                                        
                    trial_data = self.run_trial( i )
                    trial_results.append( trial_data )
                    
                    if len(trial_data) > 0:
                        t, dx, dy = zip(*trial_data)
                        
                        trial_data = {}
                        trial_data['t'] = t
                        trial_data['dx'] = dx
                        trial_data['dy'] = dy
                        run_data.append( trial_data )                    

                        traj_x, traj_y = self.calc_trial_trajectory( dx, dy )

                        # plot data
                        label_str = 'Trial: %d %s' % (i,self.stim_type_d[self.stim_type]) 
                        self.axes1.hold(True)
                        self.axes1.plot( traj_x, traj_y, label=label_str)
                        self.axes1.set_xlabel('x distance (au)')
                        self.axes1.set_ylabel('y distance (au)')
                        lh = self.axes1.legend()
                        lh.draggable(True)

                        self.fig1.canvas.draw()
                        
                        # Plot x and y vs time
                        t_plot = np.asarray(t)-t[0]
                        self.axes_xt.hold(True)
                        self.axes_xt.plot(t_plot, traj_x, label=label_str)
                        self.axes_xt.set_xlabel('Time (s)')
                        self.axes_xt.set_ylabel('x distance (au)')
                        lh = self.axes_xt.legend()
                        lh.draggable(True)

                        self.axes_yt.hold(True)
                        self.axes_yt.plot(t_plot, traj_y, label=label_str)
                        self.axes_yt.set_xlabel('Time (s)')
                        self.axes_yt.set_ylabel('y distance (au)')
                        lh = self.axes_yt.legend()                        
                        lh.draggable(True)

                        self.fig2.canvas.draw()

                        # save data
                        if i == (self.num_trials-1):
                            
                            print "(%f) Saving figures as .eps and .png and raw data as .mat" % (time.time()-self.start_t)
                            datapathbase =  self.experimentDir + '/' + datetime.now().strftime(self.FORMAT) + '_' + self.stim_type
                            self.fig1.savefig( datapathbase + '_xy_traj.eps', format='eps', dpi=1000, bbox_inches='tight')
                            self.fig1.savefig( datapathbase + '_xy_traj.png', format='png', dpi=1000, bbox_inches='tight')

                            self.fig2.savefig( datapathbase + '_xy_t.eps', format='eps', dpi=1000, bbox_inches='tight')
                            self.fig2.savefig( datapathbase + '_xy_t.png', format='png', dpi=1000, bbox_inches='tight')

                            # Save each trial as a separate .mat file
                            for i, td in enumerate( run_data ):
                                trial_datapath = datapathbase + "_raw_trial_" + str(i)
                                scipy.io.savemat( trial_datapath + '.mat', td)                            
                        
                    if self.num_trials > 1 and i != self.num_trials-1:
                        # Pause
                        print "(%f) Finished trial: %d" % (time.time()-self.start_t, i)
                        self.sleep_with_status_update(self.trial_period_t, "Inter trial wait" )

                    print "(%f) Trial runs complete" % (time.time()-self.start_t)
                    self.trial_start_event.clear()
                    self.runId = self.runId + 1

    def sleep_with_status_update(self, sleep_t, name):
        
        if not sleep_t.is_integer():
            raise Exception( "ERROR: sleep time is not an integer: %f" % ( sleep_t ))

        print "(%f::%s): About to sleep for %f sec" % (time.time()-self.start_t, name, float(sleep_t))
        for st in range(int(sleep_t)):
            time.sleep(1)
            sys.stdout.write('.')
            sys.stdout.flush()
        sys.stdout.write('\n')        

    def start_trials(self, num_trials, pre_stim_t, stim_t, flush_t, trial_period_t, stim_type, prate, experiment_dir):
        
        if experiment_dir == None:
            print "ERROR: Please set the experiment directory path"
            return

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
        self.sleep_with_status_update(self.trial_withdraw_t, "Syringe pump withdraw before stim")
        self.sp.stop()

        # Prepare syringe pumps for stim
        self.sp.infuse()
        print "Infuse prate: ", self.prate
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
        print "(%f): About to start stim for %f seconds" % (time.time()-self.start_t, self.stim_t)
        self.sp.start()
        time.sleep(self.stim_t)
        self.sp.stop()

        # Prepare syringe pumps for flush 
        self.sp.set_rate( 10.0 )

        # Set pinch valves for 'Both Air'
        self.dr.activate_pinch_valves('Both Air')

        # Start flush
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

    def close(self):
        pass
