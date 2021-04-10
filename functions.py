import numpy
from scipy.interpolate import interp1d
import scipy.special

#Distributions for the generation of the events:
def dist_theta(theta):
  return (numpy.cos(theta))**2
  
def power_law(x, index, x0=1.):
    return (x/x0)**index

def positive_erf(x, mean, sigma):
    return 0.5 + 0.5 * scipy.special.erf((x - mean)/sigma)

def spectrum(x, index, x_drop, drop_width = 1.):
    return positive_erf(x, x_drop, drop_width)  * power_law(x, index)


    
#Fit functions:   
def line(x, m , q):
  return m * x +q

def proportional(x, m ):
  return m * x

def costant(x,  q): 
  q = numpy.ones(len(x))*q
  return q

def gauss(x, norm, mean, sigma): 
  return (norm) * numpy.exp(-0.5 * ((x - mean)/sigma )**2)
  
def two_gauss(x, a, norm, mean1, sigma1, mean2, sigma2):
  return a * gauss(x, norm, mean1, sigma1) + (1.-a) * gauss(x, norm, mean2, sigma2)

def exponential(x, a, m): 
  return a * numpy.exp(-x * m)    