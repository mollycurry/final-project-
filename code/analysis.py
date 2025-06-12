import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.visualization import make_lupton_rgb, ZScaleInterval, ImageNormalize

#code for several color image figures using different filters

def irg_image(i_image, r_image, g_image):
    
    #read images
    i = fits.getdata(i_image)
    r = fits.getdata(r_image)
    g = fits.getdata(g_image)

    #use astropy visualization package to create Red/Green/Blue color image using i, r, and g filters
    irg = make_lupton_rgb(i, r, g, stretch = 5, Q = 10)

    #crop to zoom in on nebula
    irg_scaled = irg[200:800, 200:900]

    #show and save plot
    plt.imshow(irg_scaled)
    plt.title("Cat's Eye Nebula - IRG Color Image")
    plt.axis('off')
    plt.savefig("irg_color_image.png")
    plt.close()


def zir_image(z_image, i_image, r_image):
    
    #read images
    z = fits.getdata(z_image)
    i = fits.getdata(i_image)
    r = fits.getdata(r_image)

    #use astropy visualization package to create Red/Green/Blue color image using science images in z, i, and r filters
    zir = make_lupton_rgb(z, i, r, stretch = 5, Q = 10)

    #crop to zoom in on nebula
    zir_scaled = zir[200:800, 200:900]

    #show and save plot
    plt.imshow(zir_scaled)
    plt.title("Cat's Eye Nebula - ZIR Color Image")
    plt.axis('off')
    plt.savefig("zir_color_image.png")
    plt.close()


def harg_image(halpha_image, r_image, g_image):
    
    #read science images
    ha = fits.getdata(halpha_image)
    r = fits.getdata(r_image)
    g = fits.getdata(g_image)

    #use astropy visualization to create Red/Green/Blue color image from H-Alpha, r, and g science images 
    harg = make_lupton_rgb(ha, r, g, stretch = 3, Q = 10)
    harg_scaled = harg[200:800, 200:900,]

    #show and save plot
    plt.imshow(harg_scaled)
    plt.title("Cat's Eye Nebula - HARG Color Image")
    plt.axis('off')
    plt.savefig("harg_color_image.png")
    plt.close()

    
def ionized_h(science_halpha):

    #get data from H-Alpha science image 
    data = fits.getdata(science_halpha)

    #normalize pixel values
    norm = ImageNormalize(data, interval = ZScaleInterval())

    #show and save figure of H-Alpha emissions
    plt.figure(figsize = (8,8))
    plt.imshow(data, cmap = 'GnBu', origin = 'lower', norm = norm)
    plt.colorbar(label = 'Flux')
    plt.title('Cat\'s Eye Nebula - H-alpha Emission')
    plt.axis('off')
    plt.savefig('H-Alpha_emission_figure.png')
    plt.close()
    