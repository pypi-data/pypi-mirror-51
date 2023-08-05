from popsynth.auxiliary_sampler import AuxiliarySampler
import scipy.stats as stats
import numpy as np


class RadioLFSampler(AuxiliarySampler):
    def __init__(self, Lmin=1.9e24, Lmax=4.2e27, p=-3):
        """
        This samples the radio luminosity function
        """

        truth = dict(Lmin=Lmin, Lmax=Lmax, p=p)

        super(RadioLFSampler, self).__init__(
            "radio_lf", sigma=1.0, truth=truth, observed=False
        )

        self._Lmin = Lmin
        self._Lmax = Lmax
        self._p = p

        
    def true_sampler(self, size):

        u = stats.uniform.rvs(0, 1, size=size)

        self._true_values = np.power(
            u * (np.power(self._Lmax, self._p + 1.0) - np.power(self._Lmin, self._p + 1.0))
            + np.power(self._Lmin, self._p + 1.0),
            1.0 / (1 + self._p)
        )
