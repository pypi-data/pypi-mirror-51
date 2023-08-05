from popsynth.auxiliary_sampler import AuxiliarySampler
import scipy.stats as stats
import numpy as np

from bs_synth.optical_spectrum QSOSpectrum

class QSOSampler(AuxiliarySampler):
    def __init__(self):
        """
        Samples the blue bump 
        """

        super(QSOSampler, self).__init__('blue_bump', sigma=1., observed=False)


        
    def true_sampler(self, size):

        pass

