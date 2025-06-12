import numpy as np
from astropy.io import fits
from datetime import datetime

def reduce_science_frame(science_filename, median_bias_filename, median_flat_filename, median_dark_filename,
    reduced_science_filename = "reduced_science.fits"):

    #read bias, flat, dark, and science files
    bias_data = fits.getdata(median_bias_filename)
    flat_data = fits.getdata(median_flat_filename)
    dark_data = fits.getdata(median_dark_filename)
    science_data = fits.getdata(science_filename)
    
    #subtract bias 
    science_minusb = science_data - bias_data

    #open science file and get exposure time from header
    with fits.open(science_filename) as hdul:
            exposure_time = hdul[0].header['EXPTIME']

    #subtract dark 
    science_minusd = science_minusb - (dark_data * exposure_time)

    #correct science image with flat frame by dividing by flat
    reduced_science = science_minusd / flat_data

    #create header
    header = fits.Header() 
    header['DATE'] = datetime.now().isoformat() #adds date of when file was created
    header['COMMENT'] = "Science frame with bias and dark frames subtracted, and corrected with flat."

    #save science frame to FITS file
    primary = fits.PrimaryHDU(data = reduced_science, header = header)
    hdul = fits.HDUList([primary])
    hdul.writeto(reduced_science_filename, overwrite = True)

    return reduced_science