import h5py
import numpy as np
import os
import astropy.units as u

from bs_synth.utils.package_data import get_path_of_data_file, get_path_of_data_dir


def build_optical_data_file():

    # get elliptical galaxy spectrum

    elliptical_file = get_path_of_data_file("host.txt")

    elliptical_data = np.genfromtxt(elliptical_file)

    normalized_flux_host = elliptical_data[:, 1]

    # the data are in micron. convert it to Hz
    nu_host = (elliptical_data[:, 0] * u.micron).to("Hz", equivalencies=u.spectral()).value

    # some data hacking
    for i in range(len(nu_host)-1):
        if nu_host[i] == nu_host[i+1]:
            drop_idx = i
    
    normalized_flux_host =  np.delete(normalized_flux_host, drop_idx)
    nu_host = np.delete(nu_host, drop_idx)
    

    # we need to re-sort the data

    host_sort_idx = np.argsort(nu_host)

    # Now for the QSO

    qso_file = get_path_of_data_file("qso.txt")

    qso_data = np.genfromtxt(qso_file)

    flux_uncertainty = qso_data[:, 2]

    normalized_flux_qso = qso_data[:, 1]

    # the data are in micron. convert it to Hz
    nu_qso = (qso_data[:, 0] * u.Angstrom).to("Hz", equivalencies=u.spectral()).value

    qso_sort_idx = np.argsort(nu_qso)

    # save the beautiful mess to an HDF5 file

    storage_file = os.path.join(get_path_of_data_dir(), "optical_data.h5")

    with h5py.File(storage_file, "w") as f:

        host_grp = f.create_group("host_galaxy")

        host_grp.create_dataset(
            "flux", data=normalized_flux_host[host_sort_idx], compression="gzip"
        )
        host_grp.create_dataset("nu", data=nu_host[host_sort_idx], compression="gzip")

        qso_grp = f.create_group("qso")

        qso_grp.create_dataset(
            "flux", data=normalized_flux_qso[qso_sort_idx], compression="gzip"
        )
        qso_grp.create_dataset(
            "flux_uncertainty", data=flux_uncertainty[qso_sort_idx], compression="gzip"
        )
        qso_grp.create_dataset("nu", data=nu_qso[qso_sort_idx], compression="gzip")
