"""
The ``lowEBMs.Packages.RK4`` provides the numerical scheme to iteratively solve differential equations, hence the :doc:`model equation <modelequation>` which is parsed by ``lowEBMs.Packages.ModelEquation``, initialized with the :doc:`configuration <configuration>` provided by ``lowEBMs.Packages.Configuration``. 

For an example see :doc:`How to use <../howtouse>`.

.. sidebar:: Operating principle RK4

    .. image:: ../_static/RK4.png

    The scheme operates from the initial step :math:`y_0(t_0)` to the subsequent step :math:`y_1(t_1)` with :math:`t_1=t_0+h` and :math:`y_1=y_0+\phi(t_0,y_0) \cdot h` by using a weighted increment :math:`\phi` calculated from increments :math:`k_1,..,k_4`. This operation is continued with :math:`y_1(t_1)` to estimate :math:`y_2(t_2)` an so on.

The increments :math:`k_1,..,k_4` are obtained by solving the model equation, as defined in the :doc:`physical background <models>` for the dynamical term :math:`\\frac{dT}{dt}`. The increments differ in their choice of inital conditions (point of evaluation of the model equation). One iterative step always goes through a cycle of evaluating the model equation four times. It starts with the calculation of :math:`k_1` at point :math:`y_0(t_0)` with:

.. math::

    k_1= f(t_0,y_0),

where :math:`f(t,y(t))` is given by the deviation of :math:`y(t)`, hence :math:`\\frac{dT}{dt} = \\frac{1}{C}\cdot(R_{in}+R_{out}+...)` at :math:`T_0 (t_0)`.

Now the scheme continues the following procedure:

.. math::

    k_2 &= f(t_0+\\frac{h}{2},y_0+ \\frac{h}{2}\cdot k1) \\\\
    k_3 &= f(t_0+\\frac{h}{2},y_0+ \\frac{h}{2}\cdot k2) \\\\
    k_4 &= f(t_0+h,y_0+ h\cdot k3).

As final step of one iterative step the weighted increment :math:`\phi` is calculated by through:

.. math::

    \phi = \\frac{1}{6}\cdot k_1+\\frac{1}{3}\cdot k_2+\\frac{1}{3}\cdot k_3+\\frac{1}{6}\cdot k_4

to estimate :math:`y_1` as final step of one iteration step:

.. math::
    
    y_1=y_0+\phi(t_0,y_0)\cdot h . 



"""

from lowEBMs.Packages.ModelEquation import model_equation
from lowEBMs.Packages.Functions import *
from lowEBMs.Packages.Variables import Vars
import numpy as np
import builtins
import time


def rk4alg(func,eqparam,rk4input,funccomp,progressbar=True,monthly=False):
    from tqdm import tqdm, tnrange
    """This functions main task is performing the numerical integration explained above by using the solution of the model equation from ``lowEBMs.Packages.ModelEquations``. 

    In some cases the scheme only needs to run until an equilibrium state (a sufficient amount of data points without any change) is reached.
    Therefore a stop criterion is formulated within this function which prevents unnecessary long tasks (if the value of the equilibrium state is required only). 
    The stop criterion sets in if the standard deviation of a set of consecutive last data points is lower than a predefined limit.

    Input has to be given as `Dictionaries` supplied by ``lowEBMs.Packages.Configuration.importer`` from a specific **configuration.ini**.


    **Function-call arguments** \n
    
    :param function func:       The name of the model equation which will be solved (for now always model_equation)

    :param dict eqparam:        Configuration dictionary containing information needed for **func**:
                                
                                    * C_ao: The systems heat capacity (time the height of the system)

                                        * type: float
                                        * unit: Joule*Meter/Kelvin
                                        * value: > 0

    :param dict rk4input:       Configuration dictionary containing the parameters to run:

                                    * builtins.number_of_integration: Number of iterations to perfom
                                        
                                        * type: integer
                                        * unit: dimensionless
                                        * value: minimum 1

                                    * builtins.stepsize_of_integration: Time steps between iteration steps

                                        * type: float
                                        * unit: seconds
                                        * value: positive float (for hours 3600, days 86400,..)

                                    * builtins.spatial_resolution: Grid resolution (width of one latitudinal band)

                                        * type: float
                                        * unit: dimensionless
                                        * value: 0 to <90, (0 to run a 0D EBM, >0 to run a 1D EBM)

                                    * both_hemispheres: Indicates if both hemispheres are modeled or exclusively the northern hemisphere 

                                        * type: boolean
                                        * unit:  -
                                        * value: True for both, False for northern

                                    * latitudinal_circle: Indicates that data is evaluated on latitudinal circles

                                        * type: boolean
                                        * unit:  -
                                        * value: True/False

                                    * latitudinal_circle: Indicates that data is evaluated on latitudinal belts (the centre between two latitudinal circles)

                                        * type: boolean
                                        * unit:  -
                                        * value: True/False

                                    * eq_condition: Activation/Deactivation of stop criterion (equilibrium condition)

                                        * type: boolean
                                        * unit:  -
                                        * value: True/False

                                    * eq_condition_length: Indicates the number of last datapoints which are used calculate the standard deviation which is compared with the predefined limit (eq_condition_value)

                                        * type: integer
                                        * unit: dimensionless
                                        * value: minimum 2 but for physical sense much higher (probably higher than 100)

                                    * eq_condition_amplitude: The limiting value which defines the stop criterion

                                        * type: float
                                        * unit: Kelvin
                                        * value: > 0, but for physical sense use low values (lower than 1e-3)

                                    * data_readout: Indicates the number of iteration steps are performed until data in written into the output (to decrease computational cost)

                                        * type: integer
                                        * unit: dimensionless
                                        * value: minimum 1 (1 for every step, 2 for every second...)

                                    * number_of_externals: Indicates the number of external forcings are used (to create lists where the data is stored)

                                        * type: integer
                                        * unit: dimensionless
                                        * value: minimum 0


    :param dict funccomp:       Configuration 2D dictionary containing function names and function parameters parsed to the **func**

                                    * funcnames: a dictionary of function names which will build up the model equation. See :doc:`here <functions>` for a list of functions

                                    * funcparams: a dictionary of functions parameters corresponding to the functions chosen within **funcnames**. For details on the parameters see the specific function :doc:`here <functions>`

    :returns:                   An array of the outputdata of the numercial integrator, containing: 
                                    
                                    * time (seconds)
                                    * zonal mean temperature (ZMT, Kelvin)
                                    * global mean temperature (GMT, Kelvin)

    :rtype:                     array( array(time) , array(ZMT) , array(GMT) )

                                        


    
    """
    
    #Start the runtime tracker
    Vars.start_time = time.time()
    #print('Starting simulation...')
    #locally defining rk4input parameters
    n,h=int(builtins.number_of_integration),builtins.stepsize_of_integration
    #Creating an array of the variables t,T,Lat,T_global which will be the outputarray
    if builtins.spatial_resolution>0:
        if builtins.parallelization:
            data=[np.zeros(n+1),np.reshape(np.zeros((n+1)*number_of_parallels*len(Vars.Lat)),(n+1,number_of_parallels,len(Vars.Lat))),np.reshape(np.zeros((n+1)*number_of_parallels),(n+1,number_of_parallels))]
        else:
            data=[np.zeros(n+1),np.reshape(np.zeros((n+1)*len(Vars.Lat)),(n+1,len(Vars.Lat))),np.zeros(n+1)]
    else:
        if builtins.parallelization:
            data=[np.zeros(n+1),np.reshape(np.zeros((n+1)*number_of_parallels),(n+1,number_of_parallels)),np.reshape(np.zeros((n+1)*number_of_parallels),(n+1,number_of_parallels))]
        else:
            data=[np.zeros(n+1),np.zeros(n+1),np.zeros(n+1)]
    #Filling data with intitial conditions at positions data[.][0]
    #data=nal(data)
    data[0][0]=Vars.t #time t
    data[1][0]=Vars.T #Temperature T
    data[2][0]=Vars.T_global #Global mean temperature T_global
    ###Running runge Kutta 4th order n times###
    j=0
    if progressbar:
        progress=tnrange(1, n + 1)
    else:
        progress=range(1, n + 1)
        
    for i in progress:  
        #Calculating increments at 4 positions from the model equation (func)
        T0=Vars.T
        k1 = h * func(eqparam,funccomp)
        builtins.Runtime_Tracker += 1
        Vars.T=T0+0.5*k1
        k2 = h * func(eqparam,funccomp)
        builtins.Runtime_Tracker += 1
        Vars.T=T0+0.5*k2
        k3 = h * func(eqparam,funccomp)
        builtins.Runtime_Tracker += 1
        Vars.T=T0+k3
        k4 = h * func(eqparam,funccomp)
        builtins.Runtime_Tracker += 1
        
        #filling output array "data" with values from the generated increments
        #For the time simply adding the integration stepsize
        Vars.t = Vars.t + h
        Vars.T = T0 + (k1 + k2 + k2 + k3 + k3 + k4) / 6
        if builtins.spatial_resolution>0:
            Vars.T_global = earthsystem().globalmean_temperature()
        else: #if 0 dimensional
            Vars.T_global = Vars.T
            
        if monthly:
            month=int((i%365)/365*12)
            day=int(i%(365/12))
            if day==15:
                builtins.Readout_Tracker+=1
                
                data[0][builtins.Readout_Tracker] = Vars.t
                data[1][builtins.Readout_Tracker] = Vars.T  
                data[2][builtins.Readout_Tracker] = Vars.T_global
                
        elif (i) % builtins.data_readout == 0: 
            j += 1       
            data[0][j] = Vars.t 
            #The Temperature is an average over the generated increments
            data[1][j] = Vars.T  
            #The globalmeantemp calculated from the new generated temperature distribution
            data[2][j] = Vars.T_global
        #Check if the equilibrium condition is fulfilled. If true, break the loop, cut the output array to
        #the current length and move on to return the output data
        if builtins.eq_condition:
            if (builtins.Runtime_Tracker+4) % (4*builtins.eq_condition_length+4) == 0:
                if builtins.parallelization:
                    if all(SteadyStateConditionGlobal(data[2][(j-builtins.eq_condition_length):j,k]) for k in range(builtins.number_of_parallels)):
                        for l in range(len(data)):
                            data[l]=data[l][:(j+1)]
                        for m in Vars.Read.keys():
                            if type(Vars.Read[m])==np.ndarray:
                                Vars.Read[m]=Vars.Read[m][:(j)]
                        print('Eq. State reached after %s steps, within %s seconds'%(int(builtins.Runtime_Tracker/4),(time.time() - Vars.start_time)))
                        break
                else:
                    if SteadyStateConditionGlobal(data[2][(j-builtins.eq_condition_length):j])==True:
                        for l in range(len(data)):
                            data[l]=data[l][:(j+1)]
                        for m in Vars.Read.keys():
                            if type(Vars.Read[m])==np.ndarray:
                                Vars.Read[m]=Vars.Read[m][:(j)]
                        print('Eq. State reached after %s steps, within %s seconds'%(int(builtins.Runtime_Tracker/4),(time.time() - Vars.start_time)))
                        break
            elif builtins.Runtime_Tracker==(builtins.number_of_integration)*4:
                print('Transit State reached after %s steps within %s seconds' %(int(builtins.Runtime_Tracker/4),time.time() - Vars.start_time))
                break
    j=builtins.Readout_Tracker
    #Return the written data (Cut excessive 0s)
    dataout=[np.array(data[0][:(j+1)]),np.array(data[1][:(j+1)]),np.array(data[2][:(j+1)])]
    
    if builtins.control:
        #runtime=time.time()-Vars.start_time

        #print('Finished controlrun over %s years. Runtime: %s s' %(dataout[0][-1]/60/60/24/365,runtime))
        #reset
        builtins.eq_condition=rk4input['eq_condition']
        builtins.eq_condition_length=rk4input['eq_condition_length']
        builtins.eq_condition_amplitude=rk4input['eq_condition_amplitude']
        builtins.data_readout=rk4input['data_readout']
        builtins.number_of_integration=rk4input['number_of_integration']
        Vars.t=0
        builtins.Runtime_Tracker=0
    #print('Simulation finished within %s seconds' %(time.time() - Vars.start_time))
    return dataout

    
    
    

