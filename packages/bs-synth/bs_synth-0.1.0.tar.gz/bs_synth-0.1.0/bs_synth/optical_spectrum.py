import h5py
import numpy as np
import scipy.interpolate as interpolate

from bs_synth.utils.package_data import get_path_of_data_file


__all__ = ["HostGalaxySpectrum", "QSOSpectrum"]

_known_types = ["host_galaxy", "qso"]


class OpticalSpectrum(object):
    def __init__(self, object_type, scaling_factor=1.0):
        """
        A generic optical spectrum.

        :param object_type: 
        :param scaling_factor: 
        :returns: 
        :rtype: 

        """

        assert object_type in _known_types, "this optical data is not known"

        with h5py.File(get_path_of_data_file("optical_data.h5")) as f:

            grp = f[object_type]

            self._normed_flux = grp["flux"][()]
            self._nu = grp["nu"][()]

        self._scaling_factor = scaling_factor

        self._interpolate_flux()

    def _interpolate_flux(self):
        """
        interpolate the flux using a cubic spline.
        values outside of the bounds are zero

        :returns: 
        :rtype: 

        """

        self._interpolated_flux = interpolate.interp1d(
            self._nu,
            self._normed_flux,
            kind="cubic",
            bounds_error=False,
            fill_value=0.0,
        )

    def _redshift_spectrum(self, z):
        """
        redshift scaling of wavelength

        :param z: 
        :returns: 
        :rtype: 

        """

        return 1 + z

    def get_flux(self, nu, z=1):
        """
        return the flux of the spectrum at a given redshift.
        The units (should be) ergs/s/Hz

        :param nu: 
        :param z: 
        :returns: 
        :rtype: 

        """

        return self._scaling_factor * self._interpolated_flux(
            nu * self._redshift_spectrum(z)
        )

    @property
    def flux_data(self):
        """FIXME! briefly describe function

        :returns: 
        :rtype: 

        """

        return self._normed_flux

    @property
    def nu_data(self):
        """FIXME! briefly describe function

        :returns: 
        :rtype: 

        """
        return self._nu


class HostGalaxySpectrum(OpticalSpectrum):
    def __init__(self, scaling_factor):
        """
        The spectrum of the ellipitcal host galaxy
        of an AGN

        :param scaling_factor: 
        :returns: 
        :rtype: 

        """

        super(HostGalaxySpectrum, self).__init__(
            object_type="host_galaxy", scaling_factor=scaling_factor
        )


class QSOSpectrum(OpticalSpectrum):
    def __init__(self, scaling_factor):
        """
        The spectrum of the QSO + BLR 
        of an AGN

        :param scaling_factor: 
        :returns: 
        :rtype: 

        """

        super(QSOSpectrum, self).__init__(
            object_type="qso", scaling_factor=scaling_factor
        )
