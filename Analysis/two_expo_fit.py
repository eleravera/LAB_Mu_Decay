import sys
sys.path.insert(1, '/home/elo/ele/LAB_Mu_Decay')

import numpy
import matplotlib.pyplot as plt
import argparse

import plot_functions
import functions
import utilities

def plot_channel_histogram(time_diff, channel_start, channel_stop, n_bins, fit_function = None, param_names = None , param_units = None, p0 = None,  bounds = (-numpy.inf, numpy.inf), save_fig = False, range_hist = None, x_min = 0., label = '', ex_int = (numpy.inf, -numpy.inf), title = ''):
    print('\n')
    legend = '%s%d eventi' % (label, len(time_diff))
    bin_width = int(1000 * (range_hist[1]- range_hist[0])/n_bins)
    ylabel = 'ev./%d ns ' % (bin_width)
    if fit_function is not None:
        plt.subplot(2, 1, 1)
        bins, n, dn = plot_functions.plot_histogram(time_diff, "$\Delta t$ [$\mu$s]", ylabel, n_bins = n_bins, range = range_hist, title = title, legend = legend, fmt = '.b', as_scatter = True)  
        opt, pcov = plot_functions.do_fit(bins, n, dn, param_names, param_units, fit_function = fit_function, p0 = p0, bounds = bounds, x_min = x_min, ex_int = ex_int)
        l_likelihood = functions.gauss_log_likelihood(bins, n, dn, fit_function, *opt)
        plt.subplot(2, 1, 2)
        residuals = n - fit_function(bins, *opt)
        plot_functions.scatter_plot(bins, residuals, "$\Delta t$ [$\mu$s]", 'Res.', dx = None, dy = dn,  title = '')       
    #if save_fig == True:
    #    figlabel = 'dt_%d_%d_%s.pdf' % (channel_start, channel_stop, label)
    #    plt.savefig('%s' % figlabel , format = 'pdf')
        return  l_likelihood       
    else:
        bins, n, dn = plot_functions.plot_histogram(time_diff, "$\Delta t$ [$\mu$s]", ylabel, n_bins = n_bins, range = range_hist, title = title, legend = legend, fmt = '.b', as_scatter = True)  
        return bins, n, dn

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
    param_names_2expo_gauss = ['norm', 'fraction', 'm_short', 'm_long', 'costant', 'norm', 'mean', 'sigma']
    param_units_2expo_gauss = ['$\mu ^-1$s', '', '$\mu$s', '$\mu$s', '$\mu ^-1$s', '', 'mus', 'mus']
    param_names = ['a_long', 'm_long', 'costant']
    param_units = ['1/$\mu$s', '$\mu$s', '']

    #PARAMETRI INIZIALI DEL FIT E BOUNDARIES DEI PARAMETRI PER I FIT CON DOPPIA ESPONENZIALE
    p0 = [1000., 0.45, 0.880, 2.2, 0.008]
    bounds =  (0.0, 0.42, 0.02, 1.5, 0.), (numpy.inf, 0.48, 1.3, 5., 1000)
    ex_int = (+numpy.inf, -numpy.inf)
    x_min = 0.02 #0.045# 0.64 
    fit_min = 0.3
    x_max = 12.
    n_bins_up = 300
    n_bins_down = 300
    n_bins = 300
       
    index, channel_diff_up, time_diff_up = utilities.mask_array(ch, time, ch_start, ch_stop_up)
    xmin_mask = time_diff_up > x_min
    index = index[0][xmin_mask]
    channel_diff_up = channel_diff_up[xmin_mask]
    time_diff_up = time_diff_up[xmin_mask]
    range_hist = (x_min, x_max)

    #FIT DEI DATI VERSO L'ALTO
    plt.figure()            
    l_likelihood_2exp = plot_channel_histogram(time_diff_up, ch_start, ch_stop_up, n_bins = n_bins_up, fit_function = functions.two_expo, param_names = param_names_2exp, param_units = param_units_2exp, p0 = p0 , bounds = bounds, x_min = fit_min, range_hist = range_hist, save_fig=save_fig, ex_int = ex_int)       
    #l_likelihood_exp = plot_channel_histogram(time_diff_up, ch_start, ch_stop_up, n_bins = n_bins_up, fit_function = functions.exponential, param_names = param_names, param_units = param_units, p0 = None ,  x_min = x_min, range_hist = range_hist, save_fig=save_fig)       
    #test = utilities.ll_ratio_test_stat(l_likelihood_2exp, l_likelihood_exp)
    #print("test: ", test)
    plt.subplot(2,1,1)
    xgrid = numpy.linspace(0., 20., 500)
    plt.plot(xgrid, functions.two_expo(xgrid, 60, 0.45, 0.880, 2.2, 1.), 'r-')
    

    #FIT DEI DATI VERSO IL BASSO   
    index, channel_diff_down, time_diff_down = utilities.mask_array(ch, time, ch_start, ch_stop_down)   
    xmin_mask = time_diff_down > x_min
    index = index[0][xmin_mask]
    channel_diff_down = channel_diff_down[xmin_mask]
    channel_diff_down = channel_diff_down[xmin_mask]
    range_hist = (x_min, x_max)

    plt.figure()        
    l_likelihood_2exp = plot_channel_histogram(time_diff_down, ch_start, ch_stop_down, n_bins = n_bins_down, fit_function = functions.two_expo, param_names = param_names_2exp, param_units = param_units_2exp, p0 = p0, bounds = bounds, x_min = fit_min, range_hist = range_hist, save_fig=save_fig, ex_int = ex_int)      
    #l_likelihood_exp = plot_channel_histogram(time_diff_down, ch_start, ch_stop_down, n_bins = n_bins_down, fit_function = functions.exponential, param_names = param_names, param_units = param_units, p0 = None, x_min = x_min, range_hist = range_hist, save_fig=save_fig) 
    #test = utilities.ll_ratio_test_stat(l_likelihood_2exp, l_likelihood_exp)
    #print("test: ", test)
    #print("-------\n")

    #AGGREGANDO I DATI: SOPRA E SOTTO    
    ch_stop = numpy.concatenate((channel_diff_up, channel_diff_down)) 
    time_stop = numpy.concatenate((time_diff_up, time_diff_down)) 
    plt.figure()
    plt.subplot(2, 1, 1)
    title = 'piombo'#'start:%d, stop:%d' %(channel_start, channel_stop)
    legend = '%d' % len(ch_stop)
    bins, n, dn = plot_functions.plot_histogram(time_stop, "time [$\mu$s]", "", n_bins = n_bins, range = range_hist, title = title, legend = legend, fmt = '.b', as_scatter = True) 
    opt_two_expo, pcov_two_expo = plot_functions.do_fit(bins, n, dn, param_names_2exp, param_units_2exp, fit_function = functions.two_expo, p0 = p0, bounds = bounds, x_min = fit_min, x_max = x_max, ex_int = ex_int) 
    #opt_expo, pcov_expo = plot_functions.do_fit(bins, n, dn, param_names = param_names, param_units = param_units, fit_function = functions.exponential, p0 = None, bounds = (-numpy.inf, numpy.inf), x_min = x_min, x_max = x_max)
    plt.subplot(2, 1, 2)
    residuals_two_expo = n - functions.two_expo(bins, *opt_two_expo)
    plot_functions.scatter_plot(bins, residuals_two_expo, 'time [$\mu$s]', 'residuals', dx = None, dy = dn,  title = '')       
    #residuals_expo = n - functions.exponential(bins, *opt_expo)
    #plot_functions.scatter_plot(bins, residuals_expo, 'time [$\mu$s]', 'residuals', dx = None, dy = dn/residuals_expo,  title = '')  

    
    
    """
    #ALCUNI PLOT DI MONITORAGGIO
    plt.figure()
    n_bins = 20
    plt.subplot(2, 3, 1)
    index, channel_diff, time_diff = utilities.mask_array(ch, time, ch_stop_down, ch_stop_up)   
    plot_channel_histogram(time_diff, ch_stop_down, ch_stop_up, n_bins = n_bins, range_hist = (-0.1, 0.1), save_fig=save_fig)
    plt.subplot(2, 3, 2)
    index, channel_diff, time_diff = utilities.mask_array(ch, time, ch_stop_down, ch_stop_down)   
    plot_channel_histogram(time_diff, ch_stop_down, ch_stop_down, n_bins = n_bins, save_fig=save_fig)
    plt.subplot(2, 3, 3)
    index, channel_diff, time_diff = utilities.mask_array(ch, time, ch_stop_up, ch_stop_up)   
    plot_channel_histogram(time_diff, ch_stop_up, ch_stop_up, n_bins = n_bins, save_fig=save_fig)
    plt.subplot(2, 3, 4)
    index, channel_diff, time_diff = utilities.mask_array(ch, time, ch_stop_up, ch_stop_down)   
    plot_channel_histogram(time_diff, ch_stop_up, ch_stop_down, n_bins = n_bins, save_fig=save_fig)
    plt.subplot(2, 3, 5)
    index, channel_diff, time_diff = utilities.mask_array(ch, time, ch_stop_up, ch_start)   
    plot_channel_histogram(time_diff, ch_stop_up, ch_start, n_bins = n_bins, range_hist = (0., 0.2), save_fig=save_fig)
    plt.subplot(2, 3, 6)
    index, channel_diff, time_diff = utilities.mask_array(ch, time, ch_stop_down, ch_start)   
    plot_channel_histogram(time_diff, ch_stop_down, ch_start, n_bins = n_bins, save_fig=save_fig)    
    """

    """
    #DELTA T RELATIVO AI SEGNALI DI START (PER SAPERE PIU O MENO IL RATE DEI MUONI CHE SI FERMANO)
    p0 = [1000., 1.e5, 0.008]
    index, channel_diff, time_diff = utilities.mask_array(ch, time, ch_start, ch_start)   
    plt.figure()    
    plot_channel_histogram(time_diff, ch_start, ch_start, n_bins = n_bins, range_hist = (0., 1.))#, fit_function = functions.exponential, param_names = param_names, param_units = param_units, p0 = p0)    

    #PLOT DI DUE ESPONENZIALI PIU UNA GAUSSIANA PICCOLINA (PER MODELLIZZARE EVENTUALMENTE IL BUMP  CHE SI VEDE IN ALCUNI FILE A 2.2 MICROSECONDI)
    p0 = [0.05, 0.5, 0.08, 2.2, 0.008, 0.05, 2.8, 0.2]
    bounds =  (0.0, 0.0, 0.05, 1.5, 0., 0.0, 0., 0.), (numpy.inf, 1., 1.2, 5., 1., numpy.inf, numpy.inf, numpy.inf)
    plt.figure()
    title = ''#'start:%d, stop:%d' %(channel_start, channel_stop)
    legend = '%d' % len(ch_stop)
    bins, n, dn = plot_functions.plot_histogram(time_stop, "time [$\mu$s]", "", n_bins = 100, range = (0., 20.), title = title, legend = legend, fmt = '.b', as_scatter = True) 
    plot_functions.fit_histogram(bins, n, dn, param_names_2expo_gauss, param_units_2expo_gauss, fit_function = functions.two_expo_gauss, p0 = p0, bounds = bounds, x_min = x_min, x_max = x_max) 
    """  

    plt.ion()
    plt.show()
