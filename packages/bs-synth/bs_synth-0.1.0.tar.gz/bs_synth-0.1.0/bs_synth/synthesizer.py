import numpy as np

from bs_synth.electron_sampler import ElectronSampler
from bs_synth.synch_peak_sampler import SynchPeakSampler
from bs_synth.blazar_sampler import BlazarPopulation
from bs_synth.radio_lf import RadioLFSampler
from bs_synth.jet_sed_sampler import JetSEDSampler

import astropy.units as u


class BSSynthesizer(object):
    def __init__(
        self, r0, Lmin=1.9e24, Lmax=4.2e27, p=-3, beta=-1.5, k=7.0, r_max=5.0, B=0.015
    ):

        # this is the population synth
        
        base_sampler = BlazarPopulation(r0=r0, beta=beta, k=k, r_max=r_max)

        # sample the radio LF
        radio_lf_sampler = RadioLFSampler(Lmin=Lmin, Lmax=Lmax, p=p)

        # sample the electron distribution
        electron_sampler = ElectronSampler()

        # sample the peak 
        peak_sampler = SynchPeakSampler(B=B)

        # luminosity sampler

        lo = (0.3 *u.keV).to('erg').value # keV
        hi = (3.5 * u.keV).to('erg').value # keV 

        lo = 0.3 # keV
        hi = 3.5 # keV 

        
        jet_sed_sampler = JetSEDSampler(bandpass_lo=lo,
                                        bandpass_hi=hi,
                                        nu_pivot = 5, # GHz
                                        nu_break = 1E10 # Hz
                                        
        )
        
        
        peak_sampler.set_secondary_sampler(electron_sampler)

        jet_sed_sampler.set_secondary_sampler(radio_lf_sampler)
        jet_sed_sampler.set_secondary_sampler(peak_sampler)
        
        #base_sampler.add_observed_quantity(peak_sampler)
        base_sampler.add_observed_quantity(jet_sed_sampler)


        self._jet = jet_sed_sampler
        self._base_sampler = base_sampler

    @property
    def population_gen(self):

        return self._base_sampler
