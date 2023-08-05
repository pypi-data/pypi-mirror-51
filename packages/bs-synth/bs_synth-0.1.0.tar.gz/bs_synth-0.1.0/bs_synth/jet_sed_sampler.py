import scipy.stats as stats
import scipy.integrate as integrate
import numpy as np
import astropy.units as units
import astropy.constants as constants

from astropy.cosmology import Planck15 as cosmo


from popsynth.auxiliary_sampler import DerivedLumAuxSampler


_keV2erg = 1.60218e-9


class JetSEDSampler(DerivedLumAuxSampler):
    def __init__(self, bandpass_lo, bandpass_hi, nu_pivot=5, nu_break=1e10):
        """
        Computes the jet SED, and the flux given a bandpass.
        This will eventually store the synchrotron/SSC spectrum.

        :param bandpass_lo:
        :param bandpass_hi:
        :param epivot:
        :param nu_break:
        :param sigma:

        """
        truth = dict(
            bandpass_lo=bandpass_lo,
            bandpass_hi=bandpass_hi,
            nu_pivot=nu_pivot,
            nu_break=nu_break,
        )

        self._bandpass_lo = bandpass_lo
        self._bandpass_hi = bandpass_hi
        self._nu_pivot = nu_pivot
        self._nu_break = nu_break

        self._seds = []

        super(JetSEDSampler, self).__init__(
            "jet_sed", truth=truth, observed=False, sigma=1
        )

        # conversion factor for radio LF
        self._conversion = (
            ((1 * units.Unit("W/Hz")).to("erg/s/Hz")).value
            / (constants.h * 1 * units.Hz).to("erg").value
            / (constants.h * nu_pivot * units.GHz).to("keV").value
        )

    def true_sampler(self, size):
        """
        Essentially, nothing is sampled here, but constructed
        """

        self._true_values = np.zeros(size)

        specific_lum = (
            self._secondary_samplers["radio_lf"].true_values * self._conversion
        )

        nu_peaks = np.power(10, self._secondary_samplers["log_synch_peak"].true_values)

        for i in range(size):

            sed = self._construct_jet_sed(
                specific_lum[i],
                nu_peaks[i],
                self._nu_break,
                self._nu_pivot,
                index=2.0 / 3.0,
            )

            self._seds.append(sed)

            self._true_values[i] = (
                integrate.quad(
                    lambda x: x * self._seds[i](x),
                    self._bandpass_lo * (1 + self._distance[i]),
                    self._bandpass_hi * (1 + self._distance[i]),
                )[0]
                * _keV2erg
            )

    def compute_luminosity(self):

        # integrate the SED over the given bandpass

        return self._true_values

    def _construct_jet_sed(
        self, specific_flux, nu_peak, nu_break, nu_pivot, index, b=0.25
    ):
        """
        Construct an SED function

        :param specific_flux:
        :param nu_peak:
        :param nu_break:
        :param nu_pivot: in GHz
        :param index:
        :param b:
        :returns:
        :rtype:

        """

        epeak = (constants.h * nu_peak * units.Hz).to("keV").value
        ebreak = (constants.h * nu_break * units.Hz).to("keV").value
        epivot = (constants.h * nu_pivot * units.GHz).to("keV").value

        def tmp_fun(energy):

            return log_para_pl(
                energy,
                specific_flux,
                index=index,
                epeak=epeak,
                ebreak=ebreak,
                epivot=epivot,
                b=b,
            )

        return tmp_fun


def log_para_pl(ene, specific_flux, index, epeak, ebreak, epivot, b=0.25):
    """

    Log parabola + power law normalized to epivot

    :param ene:
    :param specific_flux:
    :param index:
    :param epeak:
    :param ebreak:
    :param epivot:
    :param b:
    :returns:
    :rtype:

    """
    ene = np.atleast_1d(ene)

    out = np.zeros_like(ene)
    idx = ene < ebreak

    out[idx] = (ene[idx] / epivot) ** (-index)

    arg = -b * np.log10(ene[~idx] / epeak) ** 2

    log_K = (
        (b * np.log10(ebreak / epeak) ** 2)
        + 2 * np.log10(ebreak)
        - index * np.log10(ebreak / epivot)
    )

    out[~idx] = np.power(10, log_K) * np.power(10, arg) / (ene[~idx]) ** 2

    return specific_flux * out
