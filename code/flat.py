import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clip
from datetime import datetime
import matplotlib.pyplot as plt

def create_median_flat(flat_list, bias_filename, median_flat_filename, dark_filename = None):

    #read bias file
    bias_data = fits.getdata(bias_filename) 

    #read dark file if given in argument, does nothing if not
    dark_data = None
    if dark_filename:
        dark_data = fits.getdata(dark_filename)

    #create list to hold 2D arrays
    flat_list_arrays = [] 

    #read filter for first image in flat_list
    with fits.open(flat_list[0]) as hdul:
        reference_filter = hdul[0].header['FILTER'] 
        
    for path in flat_list:
        with fits.open(path) as hdul: #open file
            flat_data = hdul[0].data.astype(np.float32) #gets data from flats
            flat_header = hdul[0].header #gets header for flat image
            flat_filter = flat_header['FILTER'] #reads filter for each flat
            if flat_filter != reference_filter:
                raise ValueError('Filters do not match') #will print error if the filters are not the same
            exposure_time = flat_header.get('EXPTIME') #gets exposure time from each flat header
        
        flat_data -= bias_data #subtracts bias from each flat
        
        if dark_data is not None: 
            flat_data -= dark_data * exposure_time #subtracts scaled dark frame from each flat image if dark is provided
        flat_list_arrays.append(flat_data) #appends flat_data to flat_list_arrays 

    combine_flats = np.stack(flat_list_arrays) #stacks 2D arrays into 3D array
    sig_clip = sigma_clip(combine_flats, sigma = 3.0, cenfunc = 'median', axis = 0) #ignores outliers of more than 3-sigma from median for each pixel

    median_flat = np.ma.median(sig_clip, axis = 0).filled(np.nan) #calculates median value and returns a 2D array with the outliers set to NaN (Not a Number)
    median_flat_normalized = median_flat / np.nanmedian(median_flat) #normalizes median flat by dividing by median pixel value

    #create header
    header = fits.Header() 
    header['CREATOR'] = 'create_median_flat'
    header['DATE'] = datetime.now().isoformat() #adds date of when file was created
    header['COMMENT'] = "Combined flat frames with subtracted bias and optional dark frame subtraction, uses sigma-clipping to mask outliers and divides by median value to normalize" 
    header['NSIGMA'] = 3.0 #sigma-clipping value
    header['NFLAT'] = len(flat_list) #will show how many flat frames were used
    header['FILTER'] = reference_filter #shows filter flats were taken with
    
    primary = fits.PrimaryHDU(data = median_flat_normalized, header = header)
    hdul = fits.HDUList([primary])
    hdul.writeto(median_flat_filename, overwrite = True)
    
    #returns normalized median flat as 2D numpy array
    return median_flat_normalized 