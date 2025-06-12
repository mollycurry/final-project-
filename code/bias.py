import numpy as np
from astropy.stats import sigma_clip
from datetime import datetime
from astropy.io import fits

def create_median_bias(bias_list, median_bias_filename):
    
    #create list for 2D arrays
    bias_list_arrays = [] 

    #for each bias file, trim image and add 2D array to list
    for path in bias_list:
        array = fits.getdata(path)
        bias_list_arrays.append(array) 

    #stack 2D arrays into 3D array
    combine_bias = np.stack(bias_list_arrays) 

    #use sigma clipping to ignore outliers of more than 3-sigma from median for each pixel
    sig_clip = sigma_clip(combine_bias, sigma = 3.0, cenfunc = 'median', axis = 0) 

    #calculate median value and return a 2D array, replace masked values with np.nan
    median_bias = np.ma.median(sig_clip, axis = 0).filled(np.nan)

    #create header
    header = fits.Header()
    header['DATE'] = datetime.now().isoformat() #adds date of when file was created
    header['COMMENT'] = "Combined bias frame from a set of bias images using sigma-clipping to mask outliers" 
    header['NSIGMA'] = 3.0 #sigma-clipping value
    header['NBIAS'] = len(bias_list) #will show how many bias frames were used

    #saves median bias frame as FITS file
    primary = fits.PrimaryHDU(data = median_bias, header = header)
    hdul = fits.HDUList([primary])
    hdul.writeto(median_bias_filename, overwrite = True)
    
    return median_bias
    