import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chisquare
from matplotlib.colors import LogNorm
import scipy.stats

import functions
import utilities

def set_plot(xlabel, ylabel, title = ''):
  plt.title(title, fontsize=12)
  plt.xlabel(xlabel, fontsize=14)
  plt.ylabel(ylabel, fontsize=14)
  plt.yticks(fontsize=14, rotation=0)
  plt.xticks(fontsize=14, rotation=0) 
  plt.subplots_adjust(bottom = 0.13, left = 0.15)
  plt.grid(True)  
  plt.legend() 
  return  

def fit_legend(param_values, param_errors, param_names, param_units, chi2=None, ndof=None):   
  legend = ''
  for (name, value, error, unit) in zip(param_names, param_values, param_errors, param_units):
      legend += ("%s: %s %s\n" % (name, utilities.format_value_error(value, error), unit))
  if chi2 is not None: 
      legend += ("$\chi^2$/d.o.f.=%.2f/%d "% (chi2, ndof))
  return legend


def plot_histogram(x, xlabel, ylabel, n_bins = None, range = None, title = '', legend = '', fmt = '.b', as_scatter = False):
  if(n_bins is None ): 
    n_bins = int(numpy.sqrt(len(x)))
  if (range is None):
   range = (x.min(), x.max()) 
  n, bins = numpy.histogram(x,  bins = n_bins, range = range)
  
  if (as_scatter is True):
    errors = numpy.sqrt(n)
    #errors = errors/n.sum()
    #n = n/n.sum()  
    bin_centers = 0.5 * (bins[1:] + bins[:-1])    
    mask = (n > 0.)
    new_bins = bin_centers[mask]
    n = n[mask]
    dn = errors[mask]
    plt.errorbar(new_bins, n, yerr = dn, fmt = fmt, label = legend)
    set_plot(xlabel, ylabel, title = title)
    return new_bins, n, dn
  else:
    n, bins, patches = plt.hist(bins[1:],  weights = n, bins = bins, label = legend, alpha = 0.4)
    dn = numpy.sqrt(n)
    set_plot(xlabel, ylabel, title = title)
    return bins, n, dn


def do_fit(x, y, dy, param_names, param_units, fit_function, p0 = None, bounds = (-numpy.inf, numpy.inf), x_min = -numpy.inf, x_max = numpy.inf, ex_int = (numpy.inf, -numpy.inf), show=True, draw_on_points = False, output_file = ''): 
  mask = (x > x_min ) * (x < x_max) * (( x < ex_int[0]) | (x > ex_int[1]))
  x = x[mask]
  y = y[mask]
  dy = dy[mask]
  
  opt, pcov = curve_fit(fit_function, x, y, sigma = dy, p0 = p0, bounds = bounds)   
  chi2 = (y - fit_function(x, *opt))**2 / dy**2
  chi2 = chi2.sum()
  ndof = len(y)-len(opt)  
  
  if show:
      legend = fit_legend(opt, numpy.sqrt(pcov.diagonal()), param_names, param_units, chi2, ndof)
      if draw_on_points is True: 
          bin_grid = x
      else:    
          bin_grid = numpy.linspace(x.min(), x.max(), 1000)  
      plt.plot(bin_grid, fit_function(bin_grid, *opt), label = legend)        
      plt.legend() 
      print("LEGEND:", legend)

  if output_file is not '': 
        legend = legend + '\n'
        with open(output_file, 'a') as of:
          of.write(legend)
  return opt, pcov
  
def scatter_plot(x, y, xlabel, ylabel, dx = None, dy = None,  title = '', legend = '', fmt='.'):
  plt.errorbar(x, y, xerr = dx, yerr = dy , fmt = fmt, label = legend)
  #plt.xlim(x.min(), x.max())
  #plt.ylim(y.min(), y.max())  
  set_plot(xlabel, ylabel, title = title)
  return   


def hist2d(x, y, xlabel, ylabel, bins=None, range_x = None, range_y = None, norm = None, title = '', legend = ''):
  plt.figure()
  if (range_x is None):
    range_x = (x.min(), x.max()) 
  if (range_y is None):
    range_y = (y.min(), y.max())   
  if(bins is None ): 
    bins = int(numpy.sqrt(len(x)))
  plt.hist2d(x, y,  bins=bins , range = (range_x, range_y), norm=norm, label = legend)  
  set_plot(xlabel, ylabel, title=title)
  plt.colorbar()
  return   


def line_fit(x, y, xlabel, ylabel, param_units, param_names = ['m', 'q'], dy = None, dx = None, err_fit = None, title = ''):
    p0 = [1., 1. ]
    opt, pcov = curve_fit(functions.line, x, y, sigma = err_fit)    
    param_errors = numpy.sqrt(numpy.diagonal(pcov)[0])  
    res = y - functions.line(x, *opt)
    chi2 = (res**2)/(err_fit**2)
    chi2 = chi2.sum()
    ndof = len(x) - len(opt)
  
    plt.figure()
    plt.subplot(2, 1, 1)   
    plt.errorbar(x, y, yerr = dy, xerr = dx, fmt = '.')
    legend = fit_legend(opt, param_errors, param_names, param_units, chi2, ndof)
    x_new = numpy.linspace(0., 300., 1000)
    plt.plot(x_new, functions.line(x_new, *opt), 'r', label = legend)
    set_plot(xlabel, ylabel, title = title)  
    plt.subplot(2, 1, 2)
    plt.errorbar(x, res, yerr = err_fit, fmt = '.')  
    set_plot(xlabel, "residui", title = '')
    return opt, pcov
  
  
#fa plot in log, forse :P
def hist_log(x, xlabel, ylabel, bins = None, range = None):
  if (range is None):
   range = (x.min(), x.max())   
  
  if (bins is None): 
    bins = numpy.logspace( numpy.log(x.min()), numpy.log(x.max()), 101)
  plt.hist(x, bins = bins)
  plt.gca().set_xscale('log') 
  set_plot(xlabel, ylabel, title=None) 
  return     
