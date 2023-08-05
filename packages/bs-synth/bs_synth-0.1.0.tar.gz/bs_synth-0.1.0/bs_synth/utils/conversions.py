import astropy.units as u


def wavelength2Hz(wavelength):
    return wavelength.to('Hz', equivalencies=u.spectral() )
