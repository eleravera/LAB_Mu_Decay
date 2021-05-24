import sys
sys.path.insert(1, '/home/ele/lab/LAB_Mu_Decay')

import numpy
import matplotlib.pyplot as plt
import argparse
from scipy.optimize import minimize

import plot_functions
import functions
import utilities

def likelihood_fit(time_diff, model=functions.two_expo, x0=None, bounds=None, title='', legend=''):
    plt.subplot(2,1,1)
    bins_center, n, dn = plot_functions.plot_histogram(time_diff, "time [$\mu$s]", "", n_bins = n_bins, range = range_hist, title = title, legend = legend, fmt = '.b', as_scatter = True)  
    minus_two_ll = functions.poisson_log_likelihood(bins_center, n, model)
    res = minimize(minus_two_ll, x0 = x0, bounds = bounds )
    opt = res.x 
    print('OPT_likelihood 2expo:', opt)
    bins_grid = numpy.linspace(0., 20., 500)
    plot_functions.scatter_plot(bins_grid, model(bins_grid, *opt), "time [$\mu$s]", "", fmt='-')       
    plt.subplot(2,1,2)
    residuals = n - model(bins_center, *opt)
    plot_functions.scatter_plot(bins_center, residuals, "time [$\mu$s]", "res", fmt='.')    
    return 


description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', nargs='*' , default=None, type=str, help='input_file')
options_parser.add_argument('-save_fig', '-s', default=False, action='store_true', help='save fig')
options_parser.add_argument('-ch_start', '-start', default=None, type=int, help='ch_start')
options_parser.add_argument('-ch_stop_up', '-up', default=None, type=int, help='ch_stop_up')
options_parser.add_argument('-ch_stop_down', '-down', default=None, type=int, help='ch_stop_down')

if __name__ == '__main__' :
    options = vars(options_parser.parse_args())
    data_file = options['input_file']
    save_fig = options['save_fig']
    ch_start = options['ch_start']
    ch_stop_up = options['ch_stop_up']
    ch_stop_down = options['ch_stop_down']

    data = numpy.hstack([numpy.loadtxt(_file, unpack=True) for _file in data_file])
    ch = data[0, :]
    time = data[1, :]

    param_names_2exp = ['norm', 'fraction', 'm_short', 'm_long', 'costant']
    param_units_2exp = ['$\mu ^-1$s', '', '$\mu$s', '$\mu$s', '$\mu ^-1$s']
    x0 = numpy.array([800., 0.5, 0.1, 2.2, 5.])
    bounds =  ((0.0, numpy.inf), (0.01, 0.999), (0.02, 1.3), (1.5, 5.), (0., numpy.inf)  )
    n_bins = 100
       
    index, channel_diff_up, time_diff_up = utilities.mask_array(ch, time, ch_start, ch_stop_up)   
    range_hist = (time_diff_up[time_diff_up > 0.].min(), 20.)
    
    title = 'start:%d, stop:%d' %(ch_start, ch_stop_up)
    legend = '%d' % len(time_diff_up)
    plt.figure()
    likelihood_fit(time_diff_up, model=functions.two_expo, x0=x0, bounds=bounds, title=title, legend=legend)
    
    index, channel_diff_down, time_diff_down = utilities.mask_array(ch, time, ch_start, ch_stop_down)   
    range_hist = (time_diff_down[time_diff_down > 0.].min(), 20.)
    title = 'start:%d, stop:%d' %(ch_start, ch_stop_down)
    legend = '%d' % len(time_diff_down)
    plt.figure()
    likelihood_fit(time_diff_down, model=functions.two_expo, x0=x0, bounds=bounds, title=title, legend=legend)


    #AGGREGANDO I DATI: SOPRA E SOTTO    
    ch_stop = numpy.concatenate((channel_diff_up, channel_diff_down)) 
    time_stop = numpy.concatenate((time_diff_up, time_diff_down)) 
    plt.figure()
    title = ''#'start:%d, stop:%d' %(channel_start, channel_stop)
    legend = '%d' % len(ch_stop)
    likelihood_fit(time_stop, model=functions.two_expo, x0=x0, bounds=bounds, title=title, legend=legend)     

    plt.ion()
    plt.show()

