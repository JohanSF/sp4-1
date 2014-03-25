
SP4 with python
===============

Introduction
------------

This python script solves the equation of motion for a *Pendulum with an
Oscillating Support*, as given by eq. (3.11) in `Vibration and Stability - JJT`.


Requirements
------------

This script requires the python packages: `numpy`, `matplotlib` and `PyDSTool`. The first two are common and usually already installed, whereas `PyDSTool` needs to be installed manually - more on that later.


Using this script
=================

There are several ways to solve a system of ODE's numerically in python. The
easiest(and most MATLAB like) is to include scipy and use the function
`scipy.integrate.odeint`. However - like using MATLAB's `ode45` - this is quite
slow. To demonstrate a way faster approach, we will use the library
[PyDSTool](http://www.ni.gsu.edu/~rclewley/PyDSTool/FrontPage.html) which is generally
considered essential in modelling dynamic systems. This library is also able to
do continuation and thus make bifurcation diagrams very efficiently.


Solve the EOM
-------------

To solve the EOMs, they need to be recasted into a system of first order
equations. Equations, parameters(here: `q, OMEGA, omega0, beta`) and initial
conditions are set in the function `setupODE`.



PyDSTool
--------

`PyDSTool` gains it speedup by compiling the code containing the ODE's into pure c-code(and then machine code). A low level compiled language like `c` is generally way faster than high level interpreted language like python and MATLAB.
For installing PyDSTool` we refer to the projects homepage, where installation guides can be found for Linux, Windows and OS X(mac).




# General notes #
## Uniform time sampling  ##

Calculating the FFT needs a uniform time interval. This is achieved by setting `precise=True` in the `sample` call:

```python
traj = ode.compute('polarization')  # integrate ODE
pts = traj.sample(dt=timestep, precise=True) 
```


## setting PYTHONPATH  ##

When setting the PYTHONPATH variable, you must include
the parent directory of `PyDSTool`, eg:

```sh
$PYTHONPATH=$PYTHONPATH:$HOME/src/python/lib:$HOME/src/python/lib/PyDSTool/:$HOME/src/PyDSTool/tests/
```

## Making it work on 64 bit  ##
See the [manual](http://www2.gsu.edu/~matrhc/GettingStarted.html#head-a0d8e24369bee9e328d05911e9a0ca95495b9c62) and this [discussion](http://sourceforge.net/p/pydstool/discussion/472291/thread/b7e16ec0/)

Remove the `-m32` flags from the files `PyDSTool/Generator/{Dopri_ODEsystem.py/Radau_ODEsystem.py}`.
These are around line 794 of `Dopri` and 935 of `Radau`. Remember to remove them from both `extra_compile_args, extra_link_args`.

It might also be necessary to install the following 32 bit libs:

```sh
sudo apt-get install ia32-libs libc6-i386 libc6-dev-i386 build-essential
```


Is it really worth the trouble?
===============================
Speedup compared to matlab:
![alt text](./timing.pdf)
