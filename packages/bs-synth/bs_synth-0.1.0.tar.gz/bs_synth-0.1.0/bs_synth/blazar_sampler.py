import numpy as np

from popsynth.distributions.cosmological_distribution import CosmologicalDistribution
from popsynth.population_synth import PopulationSynth


class PowerLawZDistribution(CosmologicalDistribution):
    def __init__(self, r0, k=7, beta=-1.5, r_max=5, seed=1234, name="_pzcosmo"):

        spatial_form = r"\rho_0(1+z)^{k+\beta z}}"

        truth = dict(r0=r0, k=k, beta=beta)

        super(PowerLawZDistribution, self).__init__(
            r_max=r_max, seed=seed, name=name, form=spatial_form, truth=truth, is_rate=True
        )

        self._construct_distribution_params(r0=r0, k=k, beta=beta)

    def dNdV(self, z):

        return self.r0 * np.power(1 + z, self.k + self.beta * z)

    def __get_r0(self):
        """Calculates the 'r0' property."""
        return self._params["r0"]

    def ___get_r0(self):
        """Indirect accessor for 'r0' property."""
        return self.__get_r0()

    def __set_r0(self, r0):
        """Sets the 'r0' property."""
        self.set_distribution_params(r0=r0, k=self.k, beta=self.beta)

    def ___set_r0(self, r0):
        """Indirect setter for 'r0' property."""
        self.__set_r0(r0)

    r0 = property(___get_r0, ___set_r0, doc="""Gets or sets the r0.""")

    def __get_k(self):
        """Calculates the 'k' property."""
        return self._params["k"]

    def ___get_k(self):
        """Indirect accessor for 'k' property."""
        return self.__get_k()

    def __set_k(self, k):
        """Sets the 'k' property."""
        self.set_distribution_params(r0=self.r0, k=k, beta=self.beta)

    def ___set_k(self, k):
        """Indirect setter for 'k' property."""
        self.__set_k(k)

    k = property(___get_k, ___set_k, doc="""Gets or sets the k.""")

    def __get_beta(self):
        """Calculates the 'beta' property."""
        return self._params["beta"]

    def ___get_beta(self):
        """Indirect accessor for 'beta' property."""
        return self.__get_beta()

    def __set_beta(self, beta):
        """Sets the 'beta' property."""
        self.set_distribution_params(r0=self.r0, k=self.k, beta=beta)

    def ___set_beta(self, beta):
        """Indirect setter for 'beta' property."""
        self.__set_beta(beta)

    beta = property(___get_beta, ___set_beta, doc="""Gets or sets the beta.""")


class BlazarPopulation(PopulationSynth):
    def __init__(self, r0, k=7, beta=-1.5, r_max=5.0, seed=1235):

        spatial_distribution = PowerLawZDistribution(
            r0=r0, k=k, beta=beta, r_max=r_max, seed=seed
        )

        # luminosity_distribution = ParetoDistribution(Lmin=Lmin, alpha=alpha, seed=seed)
        luminosity_distribution = None

        super(BlazarPopulation, self).__init__(
            spatial_distribution=spatial_distribution,
            luminosity_distribution=luminosity_distribution,
            seed=seed,
        )
