import numpy as np
import astropy.units as u

from bs_synth.utils.conversions import wavelength2Hz



__all__ = ['Halpha', 'Hbeta', 'MgII', 'CIII', 'CIV', 'CaBreak', 'Lya']

# in angstrom

_allowed_line_names = ['Halpha', 'Hbeta', 'MgII', 'CIII', 'CIV', 'CaBreak', 'Lya']


_restwaves = dict(
    Halpha=6565.0,
    Hbeta=4863.0,
    MgII=2799.0,
    CIII=1908.0,
    CIV=1550.0,
    CaBreak=4000.0,
    Lya=1216.0,
)

_restwidths = dict(
    Halpha=6565.0,
    Hbeta=4863.0,
    MgII=2799.0,
    CIII=1908.0,
    CIV=1550.0,
    CaBreak=4000.0,
    Lya=1216.0,
)

_ews = dict(Halpha=200, Hbeta=23, MgII=18.0, CIII=16.0, CIV=20.0, CaBreak=-99, Lya=47.0)

_ews_spread = dict(Halpha=200, Hbeta=23, MgII=18.0, CIII=16.0, CIV=20.0, CaBreak=-99, Lya=47.0)


class QSOLine(object):
    def __init__(
        self,
        name,
        rest_wave,
        rest_width,
        equivalent_width_mean,
        equivalent_width_spread):
        """
        A class for holding QSO line properties
        like location and equivalent width

        :param name: the name of the line
        :param rest_wave: the rest frame location of the line in Angstrom
        :param rest_width:  the rest frame width of the line in Angstrom
        :param equivalent_width_mean: the mean EW of the line
        :param equivalent_width_spread: the variance in the EW
        :returns: 
        :rtype: 

        """
        
        assert name in _allowed_line_names, '%s is not a valid line name' %name
        
        self._name = name
        self._rest_wave = rest_wave
        self._rest_width = rest_width
        self._equivalent_width_mean = equivalent_width_mean
        self._equivalent_width_spread = equivalent_width_spread

    @property
    def rest_wave(self):
        """
        The rest wave in Angstrom

        :returns: 
        :rtype: 

        """
        
        return self._rest_wave

    @property
    def rest_freq(self):
        """
        the rest wave in Hz

        :returns: 
        :rtype: 

        """
        
        return wavelength2Hz(self._rest_wave * u.Angstrom).value

    @property
    def rest_width(self):
        return self._rest_width

    @property
    def equivalent_width_mean(self):
        return self._equivalent_width_mean

    @property
    def equivalent_width_spread(self):
        return self._equivalent_width_spread

    @property
    def name(self):
        return self._name
    
    
class Halpha(QSOLine):

    def __init__(self):

        name = 'Halpha'
        
        super(Hbeta, self).__init__(name=name,
                                    rest_wave=_restwaves[name],
                                    rest_width=_restwidths[name],
                                    equivalent_width_mean=_ews[name],
                                    equivalent_width_spread_ews_spread[name]
        )

class Hbeta(QSOLine):

    def __init__(self):

        name = 'Hbeta'
        
        super(Hbeta, self).__init__(name=name,
                                    rest_wave=_restwaves[name],
                                    rest_width=_restwidths[name],
                                    equivalent_width_mean=_ews[name],
                                    equivalent_width_spread_ews_spread[name]
        )

class MgII(QSOLine):

    def __init__(self):

        name = 'MgII'
        
        super(MgII, self).__init__(name=name,
                                    rest_wave=_restwaves[name],
                                    rest_width=_restwidths[name],
                                    equivalent_width_mean=_ews[name],
                                    equivalent_width_spread_ews_spread[name]
        )

class CIII(QSOLine):

    def __init__(self):

        name = 'CIII'
        
        super(CIII, self).__init__(name=name,
                                    rest_wave=_restwaves[name],
                                    rest_width=_restwidths[name],
                                    equivalent_width_mean=_ews[name],
                                    equivalent_width_spread_ews_spread[name]
        )

class CIV(QSOLine):

    def __init__(self):

        name = 'CIV'
        
        super(CIV, self).__init__(name=name,
                                    rest_wave=_restwaves[name],
                                    rest_width=_restwidths[name],
                                    equivalent_width_mean=_ews[name],
                                    equivalent_width_spread_ews_spread[name]
        )

class CaBreak(QSOLine):

    def __init__(self):

        name = 'CaBreak'
        
        super(CaBreak, self).__init__(name=name,
                                    rest_wave=_restwaves[name],
                                    rest_width=_restwidths[name],
                                    equivalent_width_mean=_ews[name],
                                    equivalent_width_spread_ews_spread[name]
        )

class Lya(QSOLine):

    def __init__(self):

        name = 'Lya'
        
        super(Lya, self).__init__(name=name,
                                    rest_wave=_restwaves[name],
                                    rest_width=_restwidths[name],
                                    equivalent_width_mean=_ews[name],
                                    equivalent_width_spread_ews_spread[name]
        )

        
