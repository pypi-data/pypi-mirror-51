import autofit as af
from autolens.model.galaxy import galaxy as g
from autolens.model.galaxy import galaxy_model as gm
from autolens.model.profiles import light_profiles as lp, mass_profiles as mp
from autolens.pipeline.phase import phase_imaging
from autolens.pipeline import pipeline as pl
from test.integration.tests import runner

test_type = "lens__source"
test_name = "lens_light_mass__source__hyper_bg"
data_type = "lens_light__source_smooth"
data_resolution = "LSST"


def make_pipeline(name, phase_folders, optimizer_class=af.MultiNest):

    phase1 = phase_imaging.PhaseImaging(
        phase_name="phase_1",
        phase_folders=phase_folders,
        galaxies=dict(
            lens=gm.GalaxyModel(
                redshift=0.5,
                light=lp.SphericalDevVaucouleurs,
                mass=mp.EllipticalIsothermal,
            ),
            source=gm.GalaxyModel(redshift=1.0, light=lp.EllipticalSersic),
        ),
        optimizer_class=optimizer_class,
    )

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 60
    phase1.optimizer.sampling_efficiency = 0.8

    phase1 = phase1.extend_with_multiple_hyper_phases(
        hyper_galaxy=True, include_background_sky=True, include_background_noise=True
    )

    class HyperLensSourcePlanePhase(phase_imaging.PhaseImaging):
        def pass_priors(self, results):

            self.galaxies.lens.light = results.from_phase(
                "phase_1"
            ).variable.galaxies.lens.light

            self.galaxies.lens.mass = results.from_phase(
                "phase_1"
            ).variable.galaxies.lens.mass

            self.galaxies.source.light = results.from_phase(
                "phase_1"
            ).variable.galaxies.source.light

            self.galaxies.lens.hyper_galaxy = (
                results.last.hyper_combined.constant.galaxies.lens.hyper_galaxy
            )

            self.galaxies.source.hyper_galaxy = (
                results.last.hyper_combined.constant.galaxies.source.hyper_galaxy
            )

            self.hyper_image_sky = results.last.hyper_combined.constant.hyper_image_sky

            self.hyper_background_noise = (
                results.last.hyper_combined.constant.hyper_background_noise
            )

    phase2 = HyperLensSourcePlanePhase(
        phase_name="phase_2",
        phase_folders=phase_folders,
        galaxies=dict(
            lens=gm.GalaxyModel(
                redshift=0.5,
                light=lp.SphericalDevVaucouleurs,
                mass=mp.EllipticalIsothermal,
                hyper_galaxy=g.HyperGalaxy,
            ),
            source=gm.GalaxyModel(
                redshift=1.0, light=lp.EllipticalSersic, hyper_galaxy=g.HyperGalaxy
            ),
        ),
        optimizer_class=optimizer_class,
    )

    phase2.optimizer.const_efficiency_mode = True
    phase2.optimizer.n_live_points = 40
    phase2.optimizer.sampling_efficiency = 0.8

    phase2 = phase2.extend_with_multiple_hyper_phases(
        hyper_galaxy=True, include_background_sky=True, include_background_noise=True
    )

    return pl.PipelineImaging(name, phase1, phase2)


if __name__ == "__main__":
    import sys

    runner.run(sys.modules[__name__])
