import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clip
from datetime import datetime

def create_median_dark(dark_list, bias_filename, median_dark_filename):

    #read bias file
    bias_data = fits.getdata(bias_filename) 

    #create list for dark arrays
    dark_list_arrays = [] 
    
    for path in dark_list:
        with fits.open(path) as hdul: #open each dark image
            dark_data = hdul[0].data.astype(np.float32) #give 2D numpy array of data from each file, convert to float32 so code below works
            dark_header = hdul[0].header #open dark header
        dark_data -= bias_data #subtract bias from each dark image
        exposure_time = dark_header['EXPTIME'] #get exposure time from header
        dark_data /= exposure_time #get dark current by dividing each dark image by its exposure time 
        dark_list_arrays.append(dark_data) #add 2D arrays to list created above

    #stack 2D arrays into 3D array
    combine_darks = np.stack(dark_list_arrays) #stack 2D arrays into 3D array

    #use sigma clipping to ignore outliers of more than 3-sigma from median for each pixel
    sig_clip = sigma_clip(combine_darks, sigma = 3.0, cenfunc = 'median', axis = 0)

    #calculate median value and returns a 2D array with the outliers set to NaN (Not a Number)
    median_dark = np.ma.median(sig_clip, axis = 0).filled(np.nan)

    #create header
    header = fits.Header()
    header['DATE'] = datetime.now().isoformat() #add date of when file was created
    header['COMMENT'] = "Combined dark frames using sigma-clipping to mask outliers" 
    header['NSIGMA'] = 3.0 #sigma-clipping value
    header['NDARK'] = len(dark_list) #show how many dark frames were used in header

    #save dark frame as FITS file
    primary = fits.PrimaryHDU(data = median_dark, header = header)
    hdul = fits.HDUList([primary])
    hdul.writeto(median_dark_filename, overwrite = True)

    return median_dark