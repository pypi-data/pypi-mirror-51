from popsynth.auxiliary_sampler import AuxiliarySampler
import scipy.stats as stats


class ElectronSampler(AuxiliarySampler):
    def __init__(self):
        """
        This samples the electron lorentz factors from a fixed distribtuion
        """

        super(ElectronSampler, self).__init__("log_gamma_el", sigma=1.0, observed=False)

        # these are the log values of the lorentz factors
        # I've hard coded it to match the distribution
        # paolo provided me

        self._distribution = stats.skewnorm(loc=2.75, scale=0.7, a=5)

    def true_sampler(self, size):

        self._true_values = self._distribution.rvs(size=size)
