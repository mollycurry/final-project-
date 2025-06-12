from astropy.io import fits
import numpy as np


def calculate_gain(files):

    #get data from flats
    flat1 = fits.getdata(files[0]).astype('f4')
    flat2 = fits.getdata(files[1]).astype('f4')

    #calculate mean 
    mean1 = np.mean(flat1)
    mean2 = np.mean(flat2)
    mean_combined = (mean1 + mean2) / 2
    
    #calculate the variance of the difference between the flats
    flat_diff = flat1 - flat2
    flat_diff_var = np.var(flat_diff) / 2

    #calculate gain
    gain = mean_combined / flat_diff_var
    
    return gain



def calculate_readout_noise(files, gain):

    #get data from both biases
    bias1 = fits.getdata(files[0]).astype(np.float32)
    bias2 = fits.getdata(files[1]).astype(np.float32)
    
    #calculate the variance of the difference between the two biases
    bias_diff = bias1 - bias2
    bias_diff_var = np.var(bias_diff) 

    #calculate the readout noise
    readout_noise_adu = np.sqrt(bias_diff_var / 2)
    readout_noise_e = readout_noise_adu * gain

    return readout_noise_e
    