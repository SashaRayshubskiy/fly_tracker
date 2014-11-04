import numpy as np
import math
import time
import Queue
import threading
import scipy.io
from datetime import datetime
from threading import Timer, Event
from PyQt5.QtWidgets import  QWidget
from PyQt5.QtCore import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from fly_tracker_utils import get_all_from_queue

import evdev

class FlyBallPlotterContinuous:
    def __init__(self, 
                 data_q, 
                 geometry_cummulative, 
                 geometry_polar_plot, 
                 central_widget, 
                 experiment_dir ):
        
        self.data_q = data_q
        self.experiment_dir = experiment_dir
        
        ##################################
        # Setup plot area for cummulative
        ##################################
        self.plot_area = QWidget( central_widget )    
        self.plot_area.setGeometry( geometry_cummulative )
        w = geometry_cummulative.width()
        h = geometry_cummulative.height()
        self.dpi = 80
        
        w_inch = math.ceil(float(w) / float(self.dpi)) 
        h_inch = math.ceil(float(h) / float(self.dpi))

        # print "ball_tracker: w_inch, h_inch: ( %f %f )" % ( w_inch, h_inch )
        # print "ball_tracker: w, h: ( %f %f )" % ( w, h )

        self.fig = Figure( figsize=(4, 4), dpi=self.dpi, facecolor="w" )        
        self.canvas = FigureCanvas( self.fig )
        self.canvas.setParent( self.plot_area )

        self.axes = self.fig.add_subplot( 111 )
        ##################################



                
        ##################################
        # Setup plot area for polar plot 1
        ##################################
        matplotlib.rc('grid', color='#316931', linewidth=1, linestyle='-')
        matplotlib.rc('xtick', labelsize=10)
        matplotlib.rc('ytick', labelsize=10)

        self.plot_area_polar = QWidget( central_widget )    
        self.plot_area_polar.setGeometry( geometry_polar_plot )
        w = geometry_polar_plot.width()
        h = geometry_polar_plot.height()
        self.dpi = 80
        
        w_inch = math.ceil(float(w) / float(self.dpi)) 
        h_inch = math.ceil(float(h) / float(self.dpi))

        # print "ball_tracker: w_inch, h_inch: ( %f %f )" % ( w_inch, h_inch )
        # print "ball_tracker: w, h: ( %f %f )" % ( w, h )

        self.fig_polar = Figure( figsize=(3, 4), dpi=self.dpi, facecolor="w" )        
        self.canvas_polar = FigureCanvas( self.fig_polar )
        self.canvas_polar.setParent( self.plot_area_polar )

        self.fig_polar.subplots_adjust(hspace=0.3)
        self.polar_axes_1 = self.fig_polar.add_subplot( 211, polar=True, axisbg='#d5de9c')               
        self.polar_axes_2 = self.fig_polar.add_subplot( 212, polar=True, axisbg='#d5de9c')
        ##################################

        # Setup update timer
        self.update_freq = 0.5
        self.timer = QTimer()
        self.timer.timeout.connect( self.updatePlot )
        self.timer.start( 1000.0 / self.update_freq )

        # 
        self.cur_traj_x = 0
        self.cur_traj_y = 0        

        self.t_all = np.zeros(0)
        self.dx_all = np.zeros(0)
        self.dy_all = np.zeros(0)
        self.FORMAT = '%Y_%m%d_%H%M%S'
        self.RAWDATA_FLUSH_THRESHOLD = 100000
        self.rmax = 2000

        self.dir_cumm_x = 0.0
        self.dir_cumm_y = 0.0        
        self.vel_cumm_sum_x = 0.0
        self.vel_cumm_sum_y = 0.0
        self.vel_cumm_count = 0

        self.NUM_UPDATES_TO_TRACK = 50
        self.start_time = 0.0
        self.dir_win_x = 0.0
        self.dir_win_y = 0.0        
        self.vel_win_sum_x = 0.0
        self.vel_win_sum_y = 0.0
        self.vel_win_count = 0
        self.update_count = 0

        self.f_on = Event()
        self.f_on.set()

    def save_figs(self):
        if self.experiment_dir is not None:        
            datapathbase =  self.experiment_dir + '/' + datetime.now().strftime( self.FORMAT )
            self.fig.savefig( datapathbase + '_cumm_run.eps', format='eps', dpi=1000, bbox_inches='tight' )
            self.fig.savefig( datapathbase + '_cumm_run.png', format='png', dpi=1000, bbox_inches='tight' )
            self.fig_polar.savefig( datapathbase + '_vel_dir.eps', format='eps', dpi=1000, bbox_inches='tight' )
            self.fig_polar.savefig( datapathbase + '_vel_dir.png', format='png', dpi=1000, bbox_inches='tight' )            

    def save_raw(self):
        if self.experiment_dir is not None:        
            datapathbase =  self.experiment_dir + '/' + datetime.now().strftime( self.FORMAT )
            save_d = {}
            save_d['t_all'] = self.t_all
            save_d['dx_all'] = self.dx_all
            save_d['dy_all'] = self.dy_all
            # print "size of self.t_all: ", self.t_all.shape[0]
            # print "size of self.dx_all: ", self.dx_all.shape[0]
            # print "size of self.dy_all: ", self.dy_all.shape[0]
            scipy.io.savemat( datapathbase + '_raw_cummulative_xy.mat', save_d )

    def close(self):
        self.save_raw()
        # self.save_figs()

    def set_max_velocity(self,val):
        self.rmax = val
        
    def flush_on(self):
        self.f_on.set()

    def flush_off(self):
        self.f_on.clear()

    def flush(self):
        self.save_raw()
        # self.save_figs()
        self.t_all = np.zeros(0)
        self.dx_all = np.zeros(0)
        self.dy_all = np.zeros(0)
        self.axes.clear()
        self.cur_traj_x = 0
        self.cur_traj_y = 0        

    def updatePlot(self):
        
        # Read data from queue
        qdata = list(get_all_from_queue(self.data_q))

        if len( qdata ) > 0:
            t, dx, dy = zip(*qdata)

            # Save the data for later output
            self.t_all = np.append(self.t_all, t)
            self.dx_all = np.append(self.dx_all, dx)
            self.dy_all = np.append(self.dy_all, dy)            

            if self.f_on.isSet() and len(self.t_all) > self.RAWDATA_FLUSH_THRESHOLD:
                self.flush()

            # Calculate trajectory
            i=0
            traj_x = np.zeros( len(dx) )
            traj_y = np.zeros( len(dy) )
            while i < len(dx):
                if i == 0:
                    traj_x[i] = self.cur_traj_x + dx[i]
                    traj_y[i] = self.cur_traj_y + dy[i]
                else:
                    traj_x[i] = traj_x[i-1] + dx[i]
                    traj_y[i] = traj_y[i-1] + dy[i]
                i=i+1

            self.cur_traj_x = traj_x[ -1 ]
            self.cur_traj_y = traj_y[ -1 ]

            # plot data        
            self.axes.hold( True )
            # self.axes.plot( dx, dy, color='b' )
            self.axes.plot(traj_x,traj_y, color='b')
            self.fig.canvas.draw()            
            
            # Track update
            if self.update_count == 0:
                self.start_time = t[ 0 ]
            
            self.dir_cumm_x = self.dir_cumm_x + np.sum(dx)
            self.dir_cumm_y = self.dir_cumm_y + np.sum(dy)

            t_from_zero = np.array(t) - t[ 0 ]
            t_from_zero_diff = np.diff( t_from_zero )

            sum_vx = np.sum( dx[1:] / t_from_zero_diff )
            sum_vy = np.sum( dy[1:] / t_from_zero_diff )
            self.vel_cumm_sum_x = self.vel_cumm_sum_x + sum_vx
            self.vel_cumm_sum_y = self.vel_cumm_sum_y + sum_vy
            self.vel_cumm_count = self.vel_cumm_count + (len(t)-1)

            self.dir_win_x = self.dir_win_x + np.sum( dx )
            self.dir_win_y = self.dir_win_y + np.sum( dy )

            self.vel_win_sum_x = self.vel_win_sum_x + sum_vx
            self.vel_win_sum_y = self.vel_win_sum_y + sum_vy
            self.vel_win_count = self.vel_win_count + (len(t)-1)

            self.update_count = self.update_count + 1
            if self.update_count == self.NUM_UPDATES_TO_TRACK:

                # Calculate total avg velocity and direction 
                # Show result in polar plot
                angle_rad = math.atan2( self.dir_cumm_y, self.dir_cumm_x )
                                
                avg_vel_x = self.vel_cumm_sum_x / self.vel_cumm_count;
                avg_vel_y = self.vel_cumm_sum_y / self.vel_cumm_count;
                dir_vel = np.sqrt( math.pow(avg_vel_x,2) + math.pow(avg_vel_y,2) )

                # Calculate avg velocity and direction in window
                angle_rad_win = math.atan2( self.dir_win_y, self.dir_win_x )

                avg_vel_win_x = self.vel_win_sum_x / self.vel_win_count;
                avg_vel_win_y = self.vel_win_sum_y / self.vel_win_count;
                dir_win_vel = np.sqrt( math.pow(avg_vel_win_x,2) + math.pow(avg_vel_win_y,2) )

                self.polar_axes_1.clear()
                self.polar_axes_1.set_title('Total Avg vel,dir', {'fontsize':12})
                self.polar_axes_1.arrow(angle_rad, 0, 0, dir_vel, alpha = 0.5, 
                                        edgecolor = 'black', facecolor = 'green', lw = 2)
                self.polar_axes_1.set_rmax( self.rmax )

                self.polar_axes_2.clear()
                self.polar_axes_2.set_title('Vel/dir in last %f sec' % (t[-1]-self.start_time), {'fontsize':12})
                self.polar_axes_2.arrow(angle_rad_win, 0, 0, dir_win_vel, alpha = 0.5, 
                                        edgecolor = 'black', facecolor = 'green', lw = 2)
                self.polar_axes_2.set_rmax( self.rmax )
                
                self.fig_polar.canvas.draw()            

                self.update_count = 0
                self.dir_win_x = 0.0
                self.dir_win_y = 0.0
                self.vel_win_sum_x = 0.0
                self.vel_win_sum_y = 0.0
                self.vel_win_count = 0
                self.start_time = 0.0


class FlyBallReaderThread(threading.Thread):
    def __init__(self, 
                 data_q, 
                 trial_data_q, 
                 trial_ball_data_acq_start_event):
        threading.Thread.__init__(self)
        
        self.data_q = data_q
        self.trial_data_q = trial_data_q
        self.trial_ball_data_acq_start_event = trial_ball_data_acq_start_event
        
        # self.mouse = file('/dev/input/mouse0')
        self.mouse_dev = evdev.InputDevice('/dev/input/event2')

        self.setDaemon(True)
        self.start()

    def to_signed(self, n):
        return n - ((0x80 & n) << 1)

    def run(self):
        prev_t = -1.0
        prev_coord = -1
        reset_prev = False
        prev_dx = 0
        prev_dy = 0
        dx = 0
        dy = 0

        is_first_time_point_of_trial = True

        # Merge t,dx and t,dy data streams  
        # into t,dx,dy
        for event in self.mouse_dev.read_loop():
            if event.type == evdev.ecodes.EV_REL:

                t = event.timestamp()                
                coord = event.code

                if coord == evdev.ecodes.REL_X:
                    dx = event.value
                elif coord == evdev.ecodes.REL_Y:
                    #dy = -1 * event.value
                    dy = event.value

                # Wait for both x and y to be there for the same t
                # Assumes no duplicates, and monotonically increasing times
                if abs( prev_t - t ) < 0.00001:
                    # both dx and dy are set
                    reset_prev = True
                    self.data_q.put( ( t, dx, dy ) )

                    if self.trial_ball_data_acq_start_event.isSet():
                        # print "TD: %f TC: %f" % (time.time(), t )
                        self.trial_data_q.put( ( t, dx, dy ) )

                elif prev_t != -1:
                    self.data_q.put( ( prev_t, prev_dx, prev_dy ) )
            
                    if self.trial_ball_data_acq_start_event.isSet():
                        if is_first_time_point_of_trial: 
                            is_first_time_point_of_trial = False
                        else:
                            # print "TD: %f TP: %f TC: %f" % (time.time(), prev_t, t )
                            self.trial_data_q.put( ( prev_t, prev_dx, prev_dy ) )                         
                    else:
                        is_first_time_point_of_trial = True                        
                    
                if reset_prev:
                    reset_prev = False
                    prev_t = -1
                    prev_coord = -1
                    prev_dx = 0
                    prev_dy = 0
                    dx = 0
                    dy = 0
                else:
                    prev_t = t
                    prev_coord = coord
                    if prev_coord == evdev.ecodes.REL_X:
                        prev_dx = dx
                        prev_dy = 0
                    elif prev_coord == evdev.ecodes.REL_Y:
                        prev_dx = 0
                        prev_dy = dy
                        
    """
    def run_xx(self):

        for event in self.mouse_dev.read_loop():
            if event.type == evdev.ecodes.EV_REL:

                t = event.timestamp()

                if( event.code == evdev.ecodes.REL_X ):
                    dx = event.value

                    # print "FlyBallReaderThread: ( %f %d %d )" % ( t, dx, dy )
                    self.data_q_x.put((t,dx))
            
                    if self.trial_ball_data_acq_start_event.isSet():
                        self.trial_data_q_x.put((t,dx)) 
                    # print "%#02x %d %d" % (status, dx, dy)            
                elif( event.code == evdev.ecodes.REL_Y ):
                    dy = -1 * event.value

                    # print "FlyBallReaderThread: ( %f %d %d )" % ( t, dx, dy )
                    self.data_q_y.put((t,dy))
            
                    if self.trial_ball_data_acq_start_event.isSet():
                        self.trial_data_q_y.put((t,dy)) 
    def run(self):        

        while True:
            status, dx, dy = tuple(ord(c) for c in self.mouse.read(3))
                        
            t = time.time()
            
            # x+ => right, x- => left
            dx = self.to_signed(dx)
            
            # y+ => backward, y- => forward
            # reverse the sign to make y+ => forward
            dy = -1 * self.to_signed(dy)
            # print "FlyBallReaderThread: ( %f %d %d )" % ( t, dx, dy )
            self.data_q.put((t,dx,dy))
            
            if self.trial_ball_data_acq_start_event.isSet():
                self.trial_data_q.put((t,dx,dy)) 
            # print "%#02x %d %d" % (status, dx, dy)            
                
    """
