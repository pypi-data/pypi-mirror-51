import autofit as af
from autolens.model.galaxy import galaxy_model as gm
from autolens.pipeline.phase import phase_imaging
from autolens.pipeline import pipeline as pl
from autolens.model.profiles import light_profiles as lp
from test.integration.tests import runner

test_type = "model_mapper"
test_name = "link_importance_sampling_off"
data_type = "lens_light_dev_vaucouleurs"
data_resolution = "LSST"


def make_pipeline(name, phase_folders, optimizer_class=af.MultiNest):
    class MMPhase(phase_imaging.PhaseImaging):
        pass

    phase1 = MMPhase(
        phase_name="phase_1",
        phase_folders=phase_folders,
        galaxies=dict(lens=gm.GalaxyModel(redshift=0.5, light=lp.EllipticalSersic)),
        optimizer_class=optimizer_class,
    )

    phase1.optimizer.n_live_points = 20
    phase1.optimizer.sampling_efficiency = 0.8
    phase1.optimizer.importance_nested_sampling = False

    class MMPhase2(phase_imaging.PhaseImaging):
        def pass_priors(self, results):
            self.galaxies = results.from_phase("phase_1").variable.galaxies

    phase2 = MMPhase2(
        phase_name="phase_2",
        phase_folders=phase_folders,
        galaxies=dict(lens=gm.GalaxyModel(redshift=0.5, light=lp.EllipticalSersic)),
        optimizer_class=optimizer_class,
    )

    phase2.optimizer.n_live_points = 20
    phase2.optimizer.sampling_efficiency = 0.8
    phase2.optimizer.importance_nested_sampling = False

    return pl.PipelineImaging(name, phase1, phase2)


if __name__ == "__main__":
    import sys

    runner.run(sys.modules[__name__])
