from popsynth.auxiliary_sampler import AuxiliarySampler
import scipy.stats as stats
import numpy as np



class AlphaBlueBumpSampler(AuxiliarySampler):
    def __init__(self):
        """
        Samples blue bump relation from Giommi et al (2012)
        """

        super(AlphaBlueBumpSampler, self).__init__('alphabb', sigma=1., observed=False)


        
    def true_sampler(self, size):

        # get the radio luminosity as 5 GHz
        log10_lum_radio = np.log10(self._secondary_samplers['radio_lf'].true_values)

        # construct the relation
        abb_mean = 0.04 * log10_lum_radio - 0.67

        # sample
        self._true_values = np.random.normal(abb_mean,0.1, size=size)
