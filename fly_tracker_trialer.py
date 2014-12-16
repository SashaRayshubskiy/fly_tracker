from PyQt5.QtWidgets import  QWidget
from PyQt5.QtCore import *

import random
import time
import math
import sys
import numpy as np
from datetime import datetime

import scipy.io

from syringe_pumper_new_era import *
from scanimage_client import *
from daq_rider_v2 import *

from threading import Timer, Event
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from fly_tracker_utils import get_all_from_queue
from subprocess import call

import os

class FlyTrialer(QThread):
    def __init__(self, start_t, sp, dr, geometry1, geometry2, central_widget, 
                 trial_data_q, 
                 trial_ball_data_acq_start_event,
                 ball_plotter_cont ):
        super(FlyTrialer, self).__init__(None)
                
        self.sp = sp
        self.dr = dr

        self.ball_plotter_cont = ball_plotter_cont
        self.GLOBAL_DATA_FLUSH_PERIOD_IN_TRIALS = 5
        
        self.trial_start_event = Event()
        self.trial_ball_data_acq_start_event = trial_ball_data_acq_start_event
        self.trial_data_q = trial_data_q

        self.experimentDir   = None
        self.num_trials      = -1
        self.pre_stim_t      = -1.0
        self.stim_t          = -1.0
        self.flush_t         = -1.0
        self.trial_period_t  = -1.0
        self.stim_type_selected       = None

        self.using2p = False

        self.runId           = 0
        self.trial_withdraw_t = -1.0
        self.stim_prate       = -1.0
        self.flush_prate      = -1.0
        self.withdrawal_prate = self.sp.get_max_rate()

        self.FORMAT = '%Y_%m%d_%H%M%S'
        self.start_t = start_t
        self.stim_type_d = {}
        self.stim_type_d['Both_Air'] = 'BA'
        self.stim_type_d['Both_Odor'] = 'BO'
        self.stim_type_d['Left_Odor'] = 'LO'
        self.stim_type_d['Right_Odor'] = 'RO'
        self.stim_type_d['Left_Air'] = 'LA'
        self.stim_type_d['Right_Air'] = 'RA'

        self.stim_type_for_random = [ 'Both_Air', 'Both_Odor', 'Left_Odor', 'Right_Odor', 'Left_Air', 'Right_Air' ]
        self.stim_type_color_d = {}
        self.stim_type_color_d['Both_Air'] = 'black'
        self.stim_type_color_d['Both_Odor'] = 'blue'
        self.stim_type_color_d['Left_Odor'] = 'green'
        self.stim_type_color_d['Right_Odor'] = 'cyan'
        self.stim_type_color_d['Left_Air'] = 'red'
        self.stim_type_color_d['Right_Air'] = 'magenta'
        

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


        self.task_file_data = None
        self.SIclient = None
        
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

                stim_type = None
                
                run_stim_types = []

                first_time_labels_d = {}
                for key in self.stim_type_color_d:
                    first_time_labels_d[ key ] = True
                
                # Create a list of stimulation types 
                trial_types_d = []
                num_of_trials_per_stim_type = int(math.ceil(float(self.num_trials)/len(self.stim_type_for_random)))
                for stim_type_idx in range(len(self.stim_type_for_random)):
                    for trial_idx in range( num_of_trials_per_stim_type ):
                        trial_types_d.append( stim_type_idx )

                # Save basedir
                savedatabase =  self.experimentDir + '/' + datetime.now().strftime( self.FORMAT ) 

                self.ball_plotter_cont.flush_off()

                for i in range(self.num_trials):
                                        
                    # Select a random stim type
                    if self.stim_type_selected == 'Task_File':
                        stim_type = self.task_file_data[ i ]

                        self.SIclient.send( stim_type + '_' + str(self.session_id) + '_' )

                    elif self.stim_type_selected == 'Random':
                        
                        # rand_idx  = random.randrange( len(self.stim_type_for_random) )
                        # stim_type = self.stim_type_for_random[ rand_idx ] 

                        rand_idx  = random.randrange( len( trial_types_d ) )                        
                        stim_type_idx = trial_types_d[ rand_idx ]
                        del trial_types_d[ rand_idx ]
                        stim_type = self.stim_type_for_random[ stim_type_idx ] 

                        # stim_type = random.choice( trial_types_d )
                    else:
                        stim_type = self.stim_type_selected

                    run_stim_types.append(stim_type)

                    trial_data = self.run_trial( i, stim_type )
                    trial_results.append( trial_data )
                    
                    # Will always have at least 2: {begin time, end time}
                    if len(trial_data) > 2:
                        t, dx, dy = zip(*trial_data)
                        
                        trial_data = {}
                        trial_data['t'] = t
                        trial_data['dx'] = dx
                        trial_data['dy'] = dy

                        # save trial data
                        cur_datapath = savedatabase + '_' + stim_type
                        trial_datapath = cur_datapath + "_raw_trial_" + str( i )
                        
                        scipy.io.savemat( trial_datapath + '.mat', trial_data )

                        # rsync the data to orchestra
                        # call(['rsync', '-rite', 'ssh', self.experimentDir, 'ar296@orchestra:~/data/'])

                        traj_x, traj_y = self.calc_trial_trajectory( dx, dy )

                        plt_clr = self.stim_type_color_d[stim_type]

                        # plot data
                        # label_str = 'Trial: %d %s' % ( i, self.stim_type_d[stim_type] ) 

                        if first_time_labels_d[stim_type] == True:
                            label_str = '%s' % ( self.stim_type_d[stim_type] ) 
                            first_time_labels_d[stim_type] = False
                        else:
                            label_str = ''

                        self.axes1.hold(True)
                        self.axes1.plot( traj_x, traj_y, label=label_str, color=plt_clr)
                        
                        # Find the x,y value corresponding to the start of stim
                        # label this value with an 'X'
                        t_plot = np.asarray( t ) - t[ 0 ]
                                                
                        t_plot_stim = np.where( t_plot > self.stim_t )
                        t_idx = t_plot_stim[0]
                                                
                        self.axes1.plot( traj_x[t_idx], traj_y[t_idx], 'x', color=plt_clr)
                        self.axes1.set_xlabel('x distance (au)')
                        self.axes1.set_ylabel('y distance (au)')
                        lh = self.axes1.legend(prop={'size':6})
                        lh.draggable(True)

                        self.fig1.canvas.draw()
                        
                        # Plot x and y vs time
                        self.axes_xt.hold(True)
                        self.axes_xt.plot(t_plot, traj_x, label=label_str, color=plt_clr)
                        self.axes_xt.set_xlim([0, max(t_plot)])
                        self.axes_xt.set_xlabel('Time (s)')
                        self.axes_xt.set_ylabel('x distance (au)')
                        lh = self.axes_xt.legend( prop={'size':6} )
                        lh.draggable( True )

                        self.axes_yt.hold(True)
                        self.axes_yt.plot(t_plot, traj_y, label=label_str, color=plt_clr)
                        self.axes_yt.set_xlim([0, max(t_plot)])
                        self.axes_yt.set_xlabel('Time (s)')
                        self.axes_yt.set_ylabel('y distance (au)')
                        lh = self.axes_yt.legend( prop={'size':6} )         
                        lh.draggable( True )

                        self.fig2.canvas.draw()
                        
                        # save data
                        if i == (self.num_trials-1):
                            
                            print "(%f) Saving figures as .eps and .png and raw data as .mat" % (time.time()-self.start_t)
                            datapathbase =  self.experimentDir + '/' + datetime.now().strftime(self.FORMAT) 
                            self.fig1.savefig( datapathbase + '_xy_traj.eps', format='eps', dpi=1000, bbox_inches='tight')
                            self.fig1.savefig( datapathbase + '_xy_traj.png', format='png', dpi=1000, bbox_inches='tight')

                            self.fig2.savefig( datapathbase + '_xy_t.eps', format='eps', dpi=1000, bbox_inches='tight')
                            self.fig2.savefig( datapathbase + '_xy_t.png', format='png', dpi=1000, bbox_inches='tight')
                    else:
                        print 'WARNING: Trial produced no data, the fly wasn\'t moving'
                        # Send warning email
                        flyId = os.path.basename( self.experimentDir )
                        #FNULL = open(os.devnull, 'w')
                        #call(['mail', '-s', 'WARNING:: %s: trial %d produced no data.' % (flyId,i), 'druzhiche@gmail.com'], stdin=FNULL )
                        #FNULL.close()

                    if self.num_trials > 1 and i != self.num_trials-1:
                        # Pause
                        print "(%f) Finished trial: %d" % (time.time()-self.start_t, i)
                        self.sleep_with_status_update(self.trial_period_t, "Inter trial wait" )

                    # Flush out continuously recording data
                    if i % self.GLOBAL_DATA_FLUSH_PERIOD_IN_TRIALS == 0:
                        self.ball_plotter_cont.flush() 

                self.ball_plotter_cont.flush_on()
                print "(%f) Trial runs complete" % (time.time()-self.start_t)
                self.trial_start_event.clear()
                
                if self.stim_type_selected == 'Task_File':                    
                    self.SIclient.send( 'END_OF_SESSION' )
                
                self.runId = self.runId + 1

    def sleep_with_status_update(self, sleep_t, name):

        t0 = time.time()
        sleep_t_int = math.floor(sleep_t)

        print "(%f::%s): About to sleep for %f sec" % (time.time()-self.start_t, name, float(sleep_t))
        for st in range(int(sleep_t_int)):
            time.sleep(1)
            sys.stdout.write('.')
            sys.stdout.flush()
        sys.stdout.write('\n')        

        # Sleep for the rest of the time [0,1)
        time.sleep(sleep_t-sleep_t_int)
        t1 = time.time()
        print 'Sleep_t: %f   sleep call time actual: %f' % ( sleep_t, t1-t0 )

    def start_trials(self, num_trials, pre_stim_t, stim_t, flush_t, trial_period_t, stim_type, stim_prate, flush_prate, using2p, experiment_dir, task_file, session_id ):
        
        if experiment_dir == None:
            print "ERROR: Please set the experiment directory path"
            return

        self.task_file       = task_file
        self.experimentDir   = experiment_dir
        self.stim_prate      = stim_prate
        self.flush_prate     = flush_prate
        self.num_trials      = num_trials
        self.pre_stim_t      = pre_stim_t
        self.stim_t          = stim_t
        self.flush_t         = flush_t
        self.trial_period_t  = trial_period_t
        self.stim_type_selected = stim_type
        self.using2p            = using2p
        self.session_id         = session_id

        if self.stim_type_selected == 'Task_File':
            self.task_file_data = []

            # Read open the file 
            ins = open( self.task_file, "r" )
            for line in ins:
                self.task_file_data.append( line.strip() )
            ins.close()
                
            self.num_trials = len( self.task_file_data )
            print self.num_trials

            # Connection to the scanimage server
            self.SIclient = SI_Client() 

        # Write a log file with run parameters
        log_filename =  self.experimentDir + '/' + datetime.now().strftime( self.FORMAT ) + '_' + 'run.log'
        with open(log_filename, 'a') as log_file:
            log_file.write('stim pump rate: %f\n' % (self.stim_prate))
            log_file.write('flush pump rate: %f\n' % (self.flush_prate))
            log_file.write('number of trials: %d\n' % (self.num_trials))
            log_file.write('pre stim: %f\n' % (self.pre_stim_t))
            log_file.write('stim: %f\n' % (self.stim_t))
            log_file.write('flush: %f\n' % (self.flush_t))
            log_file.write('trial period: %f\n' % (self.trial_period_t))
            log_file.write('stim type: %s\n' % (self.stim_type_selected))

            if self.stim_type_selected == 'Task_File':
                log_file.write( '\n\n' )
                for i, line in enumerate( self.task_file_data ):
                    log_file.write(line + '\n')                
                
        # Set the time needed to withdraw air for each trial
        self.trial_withdraw_t = (self.stim_prate*self.stim_t + self.flush_prate*self.flush_t) / self.withdrawal_prate
        print 'self.trial_withdraw_t: ', self.trial_withdraw_t

        self.trial_start_event.set()         
            
    def run_trial(self, trial_ord, stim_type):
        
        # Reset all daq board channels
        self.dr.reset_all()

        # Set syringe pump to max rate and withdraw
        self.sp.set_rate( self.withdrawal_prate )
        if stim_type.endswith('_Rev'):
            self.sp.infuse()
        else:
            self.sp.withdraw()

        # WARNING: Syringe pumps require some flush time (see, sleep call in write_to_serial_socket)
        # This flush time needs to be accounted syringe movement duration.
        t = self.sp.start()
        MAGIC_FACTOR = 1.0*t # Needed to have pumps return to the same place after a cycle
        #MAGIC_FACTOR = 0 # Needed to have pumps return to the same place after a cycle
        self.sleep_with_status_update(self.trial_withdraw_t+MAGIC_FACTOR, "Syringe pump withdraw before stim")
        self.sp.stop()

        # Prepare syringe pumps for stim
        if stim_type.endswith('_Rev'):
            self.sp.withdraw()
        else:
            self.sp.infuse()

        print "Infuse prate: ", self.stim_prate
        self.sp.set_rate( self.stim_prate )

        # Prepare valves for stim
        self.dr.activate_pinch_valves( stim_type )
        
        if stim_type == 'Left_Air' or stim_type == 'Left_Air_Rev':
            self.dr.activate_3way_valve_left()
        elif stim_type == 'Right_Air' or stim_type == 'Right_Air_Rev':
            self.dr.activate_3way_valve_right()
        else:
            self.dr.activate_3way_valves()
        
        # CAREFUL: BEGIN trial timing
        # Pause for 10 seconds before starting stim, as per Gaudry et al.
        # Wait for 5 seconds after valve switch
        # Take 5 seconds of baseline
        self.sleep_with_status_update(5.0, "Wait before start of data acq")

        ####
        ## Start trial, acquire ball data and camera data to save
        ####
        if self.using2p:
            print '(%f): Activating 2p trigger' % (time.time())
            self.dr.activate_2p_external_trigger()
            self.dr.activate_2p_olfactometer_trigger()
            self.dr.deactivate_2p_olfactometer_trigger()
        
        # First clear the trial queue, and add time point 0
        # This is neccessary because the event based system, might not have 
        # a time point 0 until the first event
        self.trial_data_q.queue.clear()
        self.trial_data_q.put( (time.time(), 0, 0) )

        self.trial_ball_data_acq_start_event.set()
        print "Set the trial ball time: %f" % ( time.time() )

        # baseline
        self.sleep_with_status_update(self.pre_stim_t, "Data Acq::Baseline")
        
        # Start stim
        print "(%f): About to start stim for %f seconds" % (time.time()-self.start_t, self.stim_t)

        t = self.sp.start()
        time.sleep(self.stim_t-t)
        self.sp.stop()

        # Prepare syringe pumps for flush 
        self.sp.set_rate( self.flush_prate )

        # Set pinch valves for 'Both Air'
        self.dr.activate_pinch_valves('Both_Air')

        # Start flush
        t = self.sp.start()
        self.sleep_with_status_update(self.flush_t-t, "Flush")
        self.sp.stop()
        # CAREFUL: END trial timing

        # Ready to read trial data
        print "Clearing the trial ball time: %f" % ( time.time() )
        self.trial_ball_data_acq_start_event.clear()

        # Lastly add a time point, this is neccessary because the 
        # event based system might not have a time point at the end.
        self.trial_data_q.put( (time.time(), 0, 0) )

        if self.using2p:
            print '(%f): Deactivating 2p trigger' % (time.time())
            self.dr.deactivate_2p_external_trigger()

        self.dr.reset_all()

        # Trial data ready to plot
        # Read data from queue
        qdata = list( get_all_from_queue( self.trial_data_q ) )

        return qdata

    def close(self):
        pass
