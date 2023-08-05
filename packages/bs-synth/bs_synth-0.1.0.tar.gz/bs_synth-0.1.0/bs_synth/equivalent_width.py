from popsynth.auxiliary_sampler import AuxiliarySampler
import scipy.stats as stats
import numpy as np
import astropy.units as u

from bs_synth.qso_lines import *




class EquivalentWidthSampler(AuxiliarySampler):
    def __init__(self, qso_line):
        """
        base EW sampler for a QSO line
        :param qso_line: A QSOLine object

        """
         assert isinstance(qso_line, QSOLine), "Must be a QSOLine object"

        super(EquivalentWidthSampler, self).__init__(
            name=qso_line.name, sigma=1.0, observed=True
        )

        self._qso_line = qso_line

    def true_sampler(self, size):

        self._true_values = self._distribution.rvs(size=size)

    @property
    def qso_line(self):
        return self._qso_line


class HalphaSampler(EquivalentWidthSampler):
    def __init__(self):

        super(HalphaSampler, self).__init__(Halpha())


class HbetaSampler(EquivalentWidthSampler):
    def __init__(self):

        super(HbetaSampler, self).__init__(Hbeta())


class MgIISampler(EquivalentWidthSampler):
    def __init__(self):

        super(MgIISampler, self).__init__(MgII())


class CIIISampler(EquivalentWidthSampler):
    def __init__(self):

        super(CIIISampler, self).__init__(CIII())


class CIVSampler(EquivalentWidthSampler):
    def __init__(self):

        super(CIVSampler, self).__init__(CIV())


class CaBreakSampler(EquivalentWidthSampler):
    def __init__(self):

        super(CaBreakSampler, self).__init__(CaBreak())


class LyaSampler(EquivalentWidthSampler):
    def __init__(self):

        super(LyaSampler, self).__init__(Lya())
