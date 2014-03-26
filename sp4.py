# Simple simulation and display of results for pendulum

import PyDSTool as dst
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import matplotlib.mlab as mlab

# plot settings
plt.close('all')
plt.rc('text', usetex=True)  # enable LaTex in plots
plt.rc('font', family='times new roman')  # set font
ls = 12  # label font size
plt.ion()  # turn on interactive mode


# Set values of parameters
q = 0.2  # Forcing amplitude
OMEGA = 2.0  # Forcing frequency
omega0 = 1.0  # Stiffness coefficient (=squared natural freq. if omega02>0)
beta = 0.1  # Damping coefficient

# Set values of initial conditions
theta0 = np.pi/10.0  # Angle at t = 0
v0 = 0.0  # Angular velocity at t = 0

# Set simulation parameters
tstart = 0  # Start time for for the simulation
tstop = 20.0*2.0*np.pi  # Ending time for the simulation
nSimTimeSteps = 100  # Number of timesteps per period of the excitation for
timestep = 2*np.pi/OMEGA / nSimTimeSteps

# name (no spaces allowed)
DSargs = dst.args(name='Duffing_Oscillator')

# parameters
DSargs.pars = {'q': q,
               'OMEGA': OMEGA,
               'omega0': omega0,
               'beta': beta}

# rhs of the differential equation
# pendulum eq (3.11)
DSargs.varspecs = {'theta': 'v',
                   'v': '-2*beta*omega0*v\
                   -(omega0*omega0-q*OMEGA*OMEGA*cos(OMEGA*t))*sin(theta)'}


# initial conditions
DSargs.ics = {'theta': theta0, 'v': v0}

# time range
DSargs.tdomain = [tstart, tstop]  # set the range of integration.

# lang = "python"
lang = "c"

# Create ode-object
if (lang == 'python'):
    ode = dst.Generator.Vode_ODEsystem(DSargs)
if (lang == 'c'):
    DSargs['nobuild'] = True
    ode = dst.Generator.Dopri_ODEsystem(DSargs)
    ode.makeLib()  # compile (remove gen files and dirs before recompiling)

traj = ode.compute('polarization')  # integrate ODE
pts = traj.sample(dt=timestep, precise=True)  # sampling data for plotting

# Use theta from ouput for frequency analysis
signal = pts['theta']  # choose signal to analyze by fft
nfft = len(signal)     # lenght of signal
dt = timestep          # sampling interval (= sampling period)
fs = 1.0/dt            # sampling frequency (= sampling rate)
fNyq = 1.0/2.0*fs      # Nyquist frequency

# PLOTS
fig1 = plt.figure(num=1)


# TIME SERIES
ax11 = fig1.add_subplot(221)
ax11.plot(pts['t'], pts['theta'])
ax11.set_xlabel(r'Time')
ax11.set_ylabel(r'$\theta$')  # ...
ax11.set_title('Time serie')
ax11.grid(True)


# PHASE PLANE ORBITS
ax21 = fig1.add_subplot(222, aspect='equal')
ax21.plot(pts['theta'], pts['v'], 'b-', linewidth=2)
ax21.set_xlabel(r'$\theta$')
ax21.set_ylabel(r'$v$')
ax21.set_title('Phase plot')
ax21.grid(True)


# POWER SPECTRUM DENSITY (used: omegas = fs*2*pi)
ax12 = fig1.add_subplot(223)
ax12.psd(signal, nfft, fs*2.0*np.pi,
         scale_by_freq=False, window=mlab.window_none)
ax12.set_xlabel(r'$\omega$')
ax12.set_xlim([0, 6])  # fNyq*2*np.pi])
ax12.set_title('Power spectrum density')
ax12.grid(True)


# ANIMATION
# fig2 = plt.figure()
# ax22 = fig2.add_subplot(111, aspect='equal', autoscale_on=False,
#                         xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))
ax22 = fig1.add_subplot(224, aspect='equal', autoscale_on=False,
                        xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))

ax22.grid(True)
ax22.set_xlabel(r'$x$')
ax22.set_ylabel(r'$y$')
ax22.set_title('Animation')

theta = pts['theta']
t = pts['t']
# Position of support and pendulum
xSupport = q*np.cos(OMEGA*t)
ySupport = 0

xPendul = np.cos(theta) - xSupport
yPendul = np.sin(theta)

pendul,     = ax22.plot([], [], 'o-', lw=2)
lineFading, = ax22.plot([], [], 'b--', lw=3)
lineFollow2, = ax22.plot([], [], 'r-', lw=1)
lineFixed1, = ax22.plot([], [], 'k-', lw=4)
lineFixed2, = ax22.plot([], [], 'k-', lw=4)

time_template = 'time = %.1fs'
time_text = ax22.text(0.05, 0.9, '', transform=ax22.transAxes)


def init():
    """initialize animation"""
    pendul.set_data([], [])
    lineFading.set_data([], [])
    lineFollow2.set_data([], [])
    lineFixed1.set_data([-0.04, -0.04], [np.min(xSupport), np.max(xSupport)])
    lineFixed2.set_data([0.04, 0.04], [np.min(xSupport), np.max(xSupport)])
    time_text.set_text('')
    return pendul, lineFading, lineFollow2, time_text, lineFixed1, lineFixed2


def animate(i):
    """perform animation step"""
    i += 20
    thisx = [ySupport, yPendul[i]]
    thisy = [xSupport[i], -xPendul[i]]
    thisx1 = yPendul[i-20:i+1]
    thisy1 = -xPendul[i-20:i+1]
    thisx2 = yPendul[0:i+1]
    thisy2 = -xPendul[0:i+1]
    pendul.set_data(thisx, thisy)
    lineFading.set_data(thisx1, thisy1)
    lineFollow2.set_data(thisx2, thisy2)
    time_text.set_text(time_template % (i*timestep))
    return pendul, lineFading, lineFollow2, time_text


anim = animation.FuncAnimation(fig1, animate, init_func=init,
                               frames=len(t)-20, interval=20, blit=True)

# anim.save('pendulumSupport.mp4', fps=15)

plt.tight_layout()  # avoid overlapping title and labels
fig1.show()         # show figure
