
SP4 with python
===============

Introduction
------------

This python script solves the equation of motion for a *Pendulum with an
Oscillating Support*, as given by eq. (3.11) in **Vibration and Stability -
JJT**.


Requirements
------------

This script requires the python packages: `numpy`, `matplotlib` and `PyDSTool`.
The first two are common and usually already installed, whereas `PyDSTool` needs
to be installed manually - more on that later.


Using this script
=================

There are several ways to solve a system of ODE's numerically in python. The
easiest(and most MATLAB like) is to include scipy and use the function
`scipy.integrate.odeint`. However - like using MATLAB's `ode45` - this is quite
slow. To demonstrate a way faster approach, we will use the library
[PyDSTool](http://www.ni.gsu.edu/~rclewley/PyDSTool/FrontPage.html) which is
generally considered essential in modelling dynamic systems. This library is
also able to do continuation and thus make bifurcation diagrams very
efficiently.


Solve the EOM
-------------

To solve the EOMs, they need to be recasted into a system of first order
equations. Equations(here: `theta=..., v=...`), parameters(here: `q, OMEGA,
omega0, beta`) and initial conditions(here: `q0, theta0`) are set in
`DSargs.pars`, `DSargs.varspecs` and `DSargs.ics` respectively.



PyDSTool
--------

`PyDSTool` gains it speedup by compiling the code containing the ODE's into pure
c-code(and then machine code). A low level compiled language like `c` is
generally way faster than high level interpreted language like python and
MATLAB. For installing PyDSTool` we refer to the projects homepage, where
installation guides can be found for Linux, Windows and OS X(mac).




General notes
=============

Uniform time sampling
---------------------

Calculating the FFT needs a uniform time interval. This is achieved by setting
`precise=True` in the `sample` call:

```python
traj = ode.compute('polarization')  # integrate ODE
pts = traj.sample(dt=timestep, precise=True) 
```


setting PYTHONPATH
------------------

When setting the PYTHONPATH variable, you must include
the parent directory of `PyDSTool`, eg:

```sh
$PYTHONPATH=$PYTHONPATH:$HOME/src/python/lib:$HOME/src/python/lib/PyDSTool/:$HOME/src/PyDSTool/tests/
```

## Making it work on 64 bit ## See the
[manual](http://www2.gsu.edu/~matrhc/GettingStarted.html#head-a0d8e24369bee9e328d05911e9a0ca95495b9c62)
and this
[discussion](http://sourceforge.net/p/pydstool/discussion/472291/thread/b7e16ec0/)

Remove the `-m32` flags from the files
`PyDSTool/Generator/{Dopri_ODEsystem.py/Radau_ODEsystem.py}`. These are around
line 794 of `Dopri` and 935 of `Radau`. Remember to remove them from both
`extra_compile_args, extra_link_args`.

It might also be necessary to install the following 32 bit libs:

```sh
sudo apt-get install ia32-libs libc6-i386 libc6-dev-i386 build-essential
```

Animation
=========

The important parameters when calling the `animation.FuncAnimation` class are:

- `interval=20` - 20 ms between frames. To get the "correct" interval(eg. the
  pendulum moves in real time), use: `interval=t[-1]/len(t)*1000` - gives the
  correct time in ms

- `blit=True` - only redraw the pieces of the plot which have changed. Remember
  that func and init_func should return an iterable of drawables to clear.

- `fps=50` - fps should match the `interval`, eg if there's a frame for each 20
  ms then `fps = 1000/20 = 40`

Example


```python
def init():
    line.set_data([], [])
    return line,

\# animation function. This is called sequentially
def animate(i):
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,
anim = animation.FuncAnimation(fig1, animate, init_func=init,
frames=len(t)-25, interval=20, blit=True)

\# save the animation
anim.save('basic_animation.mp4', fps=50, extra_args=['-vcodec', 'libx264'])
plt.show()
```

Note the comma(,) ín the return statement! This means that the function returns
a tupple which is needed by the animate class.

The extra_args ensure that the x264 codec is used, so that the video can be
embedded in html5 (and gives better quality and smaller file). This requires
ffmpeg or mencoder to be installed. In order to install ffmpeg + x264 codec use
this [PPA](https://launchpad.net/~jon-severinsson/+archive/ffmpeg)(simplest) or
compile from source using this
[guide](http://ubuntu-sols.blogspot.dk/2012/06/how-to-install-ffmpeg-and-x264-on.html).
It might be necessary to set the `LDPATH` to the directory of `x264` -
especially if there's multiple version installed:
`LD_LIBRARY_PATH=/path/to/my/compiled/x264/library` before configuring `ffmpeg`.

If `anim.save` throws an error, try to run it with `--verbose-debug` to see what
went wrong(missing encoder library probably). To see if `x264` installed run:

```sh
ffmpeg -codecs | grep 264
EV    libx264         libx264 H.264 / AVC / ...  # output
```

Running on gbar
===============


matplotlib
----------

In order to run a script with matplotlib on a machine without `X11`(headless),
use another backend. To do this, have the following `PyDSTool` and general
`matplotlib` stuff are imported:

```python
import matplotlib
matplotlib.use('Agg')
```

Now `matplotlib` uses the `Agg` backend.

It is also possible to forward `X` by using thinlinc or `ssh -X
student@login.gbar.dtu.dk`. This can be set up in `~/.ssh/config` using the
option `ForwardX11 yes`.


virtualenv
----------

On `linuxsh` it is possible to create virtual environments. add
`--no-site-packages` if you want to isolate your environment from the main site
packages directory (which you probably won't)
```sh
mkdir virtualenv
virtualenv ~/virtualenv/myEnv
source ~/virtualenv/myEnv/bin/activate
```

update the needed packages(remember to this on the platform you want to use the
env in. Eg. HPC or APP nodes):

```sh
pip install --update numpy matplotlib
```

To exit the virtualenv just type `deactivate`.


Another way would be to create a clean virtualenv and link the packages that you
need:
```sh
virtualenv --no-site-packages foo
source foo/bin/activate
ln -s /usr/lib/python2.7/dist-packages/PIL* $VIRTUAL_ENV/lib/python*/site-packages
```

Is it really worth the trouble?
===============================
Speedup compared to matlab:
![alt text](timing.pdf)



Fading lines
============

I've had to do something similar to what you need, and I found the 
following example from the Gallery quite helpful: 
http://matplotlib.org/examples/pylab_examples/multicolored_line.html
I think the second plot in particular is pretty close to what you want; 
however, you'll need to set the alpha values manually. This is what I've 
done for line collections, scatter plots, etc. 


```python
import numpy as np 
import matplotlib.pyplot as plt 

norm_data = np.random.rand(20) 
xs = np.random.rand(20) 

# Pick a colormap and generate the color array for your data 
cmap = plt.cm.spectral 
colors = cmap(norm_data) 
# Reset the alpha data using your desired values 
colors[:,3] = norm_data 

# Adding a colorbar is a bit of a pain here, need to use a mappable 
fig = plt.figure() 
plt.scatter(xs, norm_data, c=colors, s=55) 
mappable = plt.cm.ScalarMappable(cmap=cmap) 
mappable.set_array(norm_data) 
fig.colorbar(mappable) 
plt.show() 
```
