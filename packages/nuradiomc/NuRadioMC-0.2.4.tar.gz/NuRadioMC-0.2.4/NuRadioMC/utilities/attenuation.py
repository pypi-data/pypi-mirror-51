import numpy as np
from NuRadioMC.utilities import units

model_to_int = {"SP1" : 1, "GL1" : 2}

def fit_GL1(z):
    # Model for Greenland. Taken from DOI: https://doi.org/10.3189/2015JoG15J057
	# Returns the attenuation length at 75 MHz as a function of depth
    fit_values = [1.16052586e+03, 6.87257150e-02, -9.82378264e-05,
                    -3.50628312e-07, -2.21040482e-10, -3.63912864e-14]
    min_length = 100 * units.m
    if(not hasattr(z, '__len__')):
        att_length = 0
    else:
        att_length = np.zeros_like(z)
    for power, coeff in enumerate(fit_values):
        att_length += coeff * z**power

    if (not hasattr(att_length, '__len__')):
        if ( att_length < min_length ):
            att_length = min_length
    else:
        att_length[ att_length < min_length ] = min_length
    return att_length

def get_temperature(z):
    """
    returns the temperature in Celsius as a function of depth
    """
    # from https://icecube.wisc.edu/~araproject/radio/#icetabsorption

    z2 = np.abs(z / units.m)
    return 1.83415e-09 * z2**3 + (-1.59061e-08 * z2**2) + 0.00267687 * z2 + (-51.0696)

def get_attenuation_length(z, frequency, model):
    if(model == "SP1"):
        t = get_temperature(z)
        f0 = 0.0001
        f2 = 3.16
        w0 = np.log(f0)
        w1 = 0.0
        w2 = np.log(f2)
        w = np.log(frequency / units.GHz)
        b0 = -6.74890 + t * (0.026709 - t * 0.000884)
        b1 = -6.22121 - t * (0.070927 + t * 0.001773)
        b2 = -4.09468 - t * (0.002213 + t * 0.000332)
        if(not hasattr(frequency, '__len__')):
            if (frequency < 1. * units.GHz):
                a = (b1 * w0 - b0 * w1) / (w0 - w1)
                bb = (b1 - b0) / (w1 - w0)
            else:
                a = (b2 * w1 - b1 * w2) / (w1 - w2)
                bb = (b2 - b1) / (w2 - w1)
        else:
            a = np.ones_like(frequency) * (b2 * w1 - b1 * w2) / (w1 - w2)
            bb = np.ones_like(frequency) * (b2 - b1) / (w2 - w1)
            a[frequency < 1. * units.GHz] = (b1 * w0 - b0 * w1) / (w0 - w1)
            bb[frequency < 1. * units.GHz] = (b1 - b0) / (w1 - w0)

        return 1. / np.exp(a + bb * w)
    elif(model == "GL1"):

        att_length_75 = fit_GL1(z/units.m)
        att_length_f = att_length_75 - 0.55 * units.m * (frequency/units.MHz - 75)

        min_length = 100 * units.m
        if(not hasattr(frequency, '__len__') and not hasattr(z, '__len__')):
            if (att_length_f < min_length):
                att_length_f = min_length
        else:
            att_length_f[ att_length_f < min_length ] = min_length

        return att_length_f
    else:
        raise NotImplementedError("attenuation model {} is not implemented.".format(model))
