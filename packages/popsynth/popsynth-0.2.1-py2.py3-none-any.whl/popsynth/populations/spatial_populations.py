from popsynth.distributions.spherical_distribution import (
    ConstantSphericalDistribution,
    ZPowerSphericalDistribution,
)
from popsynth.distributions.cosmological_distribution import (
    SFRDistribtution,
    MergerDistribution,
    ZPowerCosmoDistribution,
)

from popsynth.population_synth import PopulationSynth

## First create a bunch of spatial distributions


class SphericalPopulation(PopulationSynth):
    def __init__(self, Lambda, r_max=5.0, seed=1234, luminosity_distribution=None):
        """FIXME! briefly describe function

        :param Lambda:
        :param r_max:
        :param seed:
        :param luminosity_distribution:
        :returns:
        :rtype:

        """

        spatial_distribution = ConstantSphericalDistribution(
            Lambda=Lambda, r_max=r_max, seed=seed
        )

        super(SphericalPopulation, self).__init__(
            spatial_distribution=spatial_distribution,
            luminosity_distribution=luminosity_distribution,
            seed=seed,
        )


class ZPowerSphericalPopulation(PopulationSynth):
    def __init__(
        self, Lambda, delta, r_max=5.0, seed=1234, luminosity_distribution=None
    ):
        """FIXME! briefly describe function

        :param Lambda:
        :param delta:
        :param r_max:
        :param seed:
        :param luminosity_distribution:
        :returns:
        :rtype:

        """

        spatial_distribution = ZPowerSphericalDistribution(
            Lambda=Lambda, delta=delta, r_max=r_max, seed=seed
        )

        super(ZPowerSphericalPopulation, self).__init__(
            spatial_distribution=spatial_distribution,
            luminosity_distribution=luminosity_distribution,
            seed=seed,
        )


class ZPowerCosmoPopulation(PopulationSynth):
    def __init__(
        self, Lambda, delta, r_max=5.0, seed=1234, luminosity_distribution=None
    ):
        """FIXME! briefly describe function

        :param Lambda:
        :param delta:
        :param r_max:
        :param seed:
        :param luminosity_distribution:
        :returns:
        :rtype:

        """

        spatial_distribution = ZPowerCosmoDistribution(
            Lambda=Lambda, delta=delta, r_max=r_max, seed=seed
        )

        super(ZPowerCosmoPopulation, self).__init__(
            spatial_distribution=spatial_distribution,
            luminosity_distribution=luminosity_distribution,
            seed=seed,
        )


class SFRPopulation(PopulationSynth):
    def __init__(
        self, r0, rise, decay, peak, r_max=5, seed=1234, luminosity_distribution=None
    ):
        """FIXME! briefly describe function

        :param r0:
        :param rise:
        :param decay:
        :param peak:
        :param r_max:
        :param seed:
        :param luminosity_distribution:
        :returns:
        :rtype:

        """

        spatial_distribution = SFRDistribtution(
            r0=r0, rise=rise, decay=decay, peak=peak, r_max=r_max, seed=seed
        )

        super(SFRPopulation, self).__init__(
            spatial_distribution=spatial_distribution,
            luminosity_distribution=luminosity_distribution,
            seed=seed,
        )
