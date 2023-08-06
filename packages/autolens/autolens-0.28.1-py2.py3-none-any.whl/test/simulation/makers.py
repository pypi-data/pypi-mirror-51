import autofit as af
from autolens.data.instrument import abstract_data
from autolens.data.instrument import ccd
from autolens.array import grids
from autolens.lens import ray_tracing
from autolens.model.galaxy import galaxy as g
from autolens.model.profiles import light_profiles as lp
from autolens.model.profiles import mass_profiles as mp
from autolens.data.plotters import ccd_plotters
from autolens.lens.plotters import ray_tracing_plotters

from test.simulation import simulation_util

import os


def simulate_image_from_galaxies_and_output_to_fits(
    data_resolution,
    data_type,
    sub_grid_size,
    galaxies,
    psf_shape=(51, 51),
    exposure_time=300.0,
    background_sky_level=1.0,
):

    pixel_scale = simulation_util.pixel_scale_from_data_resolution(
        data_resolution=data_resolution
    )
    shape = simulation_util.shape_from_data_resolution(data_resolution=data_resolution)

    # Simulate a simple Gaussian PSF for the image.
    psf = abstract_data.PSF.from_gaussian(
        shape=psf_shape, sigma=pixel_scale, pixel_scale=pixel_scale
    )

    # Setup the image-plane grid stack of the CCD array which will be used for generating the image of the
    # simulated strong lens. A high-res sub-grid is necessary to ensure we fully resolve the central regions of the
    # lens and source galaxy light.
    image_plane_grid = grids.Grid.from_shape_pixel_scale_and_sub_grid_size(
        shape=shape, pixel_scale=pixel_scale, sub_grid_size=sub_grid_size
    )

    # Use the input galaxies to setup a tracer, which will generate the image for the simulated CCD instrument.
    tracer = ray_tracing.Tracer.from_galaxies(galaxies=galaxies)

    # Simulate the CCD instrument, remembering that we use a special image which ensures edge-effects don't
    # degrade our modeling of the telescope optics (e.g. the PSF convolution).
    ccd_data = ccd.SimulatedCCDData.from_tracer_grid_and_exposure_arrays(
        tracer=tracer,
        pixel_scale=pixel_scale,
        psf=psf,
        exposure_time=exposure_time,
        background_sky_level=background_sky_level,
        add_noise=True,
    )

    # Now, lets output this simulated ccd-data to the test/data folder.
    test_path = "{}/../".format(os.path.dirname(os.path.realpath(__file__)))

    data_path = af.path_util.make_and_return_path_from_path_and_folder_names(
        path=test_path, folder_names=["data", data_type, data_resolution]
    )

    ccd.output_ccd_data_to_fits(
        ccd_data=ccd_data,
        image_path=data_path + "image.fits",
        psf_path=data_path + "psf.fits",
        noise_map_path=data_path + "noise_map.fits",
        overwrite=True,
    )

    ccd_plotters.plot_ccd_subplot(
        ccd_data=ccd_data,
        output_filename="ccd_data",
        output_path=data_path,
        output_format="png",
    )

    ccd_plotters.plot_ccd_individual(
        ccd_data=ccd_data,
        should_plot_image=True,
        should_plot_noise_map=True,
        should_plot_psf=True,
        should_plot_signal_to_noise_map=True,
        output_path=data_path,
        output_format="png",
    )

    ray_tracing_plotters.plot_ray_tracing_subplot(
        tracer=tracer,
        output_filename="tracer",
        output_path=data_path,
        output_format="png",
    )

    ray_tracing_plotters.plot_ray_tracing_individual(
        tracer=tracer,
        should_plot_profile_image=True,
        should_plot_source_plane=True,
        should_plot_convergence=True,
        should_plot_potential=True,
        should_plot_deflections=True,
        output_path=data_path,
        output_format="png",
    )


def make_lens_light_dev_vaucouleurs(data_resolutions, sub_grid_size):

    data_type = "lens_light_dev_vaucouleurs"

    # This lens-only system has a Dev Vaucouleurs spheroid / bulge.

    lens_galaxy = g.Galaxy(
        redshift=0.5,
        bulge=lp.EllipticalDevVaucouleurs(
            centre=(0.0, 0.0),
            axis_ratio=0.9,
            phi=45.0,
            intensity=0.1,
            effective_radius=1.0,
        ),
    )

    for data_resolution in data_resolutions:

        simulate_image_from_galaxies_and_output_to_fits(
            data_type=data_type,
            data_resolution=data_resolution,
            sub_grid_size=sub_grid_size,
            galaxies=[lens_galaxy, g.Galaxy(redshift=1.0)],
        )


def make_lens_bulge_disk(data_resolutions, sub_grid_size):

    data_type = "lens_bulge_disk"

    # This source-only system has a Dev Vaucouleurs spheroid / bulge and surrounding Exponential envelope

    lens_galaxy = g.Galaxy(
        redshift=0.5,
        bulge=lp.EllipticalDevVaucouleurs(
            centre=(0.0, 0.0),
            axis_ratio=0.9,
            phi=45.0,
            intensity=0.1,
            effective_radius=1.0,
        ),
        envelope=lp.EllipticalExponential(
            centre=(0.0, 0.0),
            axis_ratio=0.7,
            phi=60.0,
            intensity=1.0,
            effective_radius=2.0,
        ),
    )

    for data_resolution in data_resolutions:

        simulate_image_from_galaxies_and_output_to_fits(
            data_type=data_type,
            data_resolution=data_resolution,
            sub_grid_size=sub_grid_size,
            galaxies=[lens_galaxy, g.Galaxy(redshift=1.0)],
        )


def make_lens_x2_light(data_resolutions, sub_grid_size):

    data_type = "lens_x2_light"

    # This source-only system has two Sersic bulges separated by 2.0"

    lens_galaxy_0 = g.Galaxy(
        redshift=0.5,
        bulge=lp.EllipticalSersic(
            centre=(-1.0, -1.0),
            axis_ratio=0.8,
            phi=0.0,
            intensity=1.0,
            effective_radius=1.0,
            sersic_index=3.0,
        ),
    )

    lens_galaxy_1 = g.Galaxy(
        redshift=0.5,
        bulge=lp.EllipticalSersic(
            centre=(1.0, 1.0),
            axis_ratio=0.8,
            phi=0.0,
            intensity=1.0,
            effective_radius=1.0,
            sersic_index=3.0,
        ),
    )

    for data_resolution in data_resolutions:

        simulate_image_from_galaxies_and_output_to_fits(
            data_type=data_type,
            data_resolution=data_resolution,
            sub_grid_size=sub_grid_size,
            galaxies=[lens_galaxy_0, lens_galaxy_1, g.Galaxy(redshift=1.0)],
        )


def make_lens_mass__source_smooth(data_resolutions, sub_grid_size):

    data_type = "lens_mass__source_smooth"

    # This source-only system has a smooth source (low Sersic Index) and simple SIE mass profile.

    lens_galaxy = g.Galaxy(
        redshift=0.5,
        mass=mp.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.6, axis_ratio=0.7, phi=45.0
        ),
    )

    source_galaxy = g.Galaxy(
        redshift=1.0,
        light=lp.EllipticalSersic(
            centre=(0.0, 0.0),
            axis_ratio=0.8,
            phi=60.0,
            intensity=0.4,
            effective_radius=0.5,
            sersic_index=1.0,
        ),
    )

    for data_resolution in data_resolutions:

        simulate_image_from_galaxies_and_output_to_fits(
            data_type=data_type,
            data_resolution=data_resolution,
            sub_grid_size=sub_grid_size,
            galaxies=[lens_galaxy, source_galaxy],
        )


def make_lens_mass__source_cuspy(data_resolutions, sub_grid_size):

    data_type = "lens_mass__source_cuspy"

    # This source-only system has a smooth source (low Sersic Index) and simple SIE mass profile.

    lens_galaxy = g.Galaxy(
        redshift=0.5,
        mass=mp.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.6, axis_ratio=0.7, phi=45.0
        ),
    )

    source_galaxy = g.Galaxy(
        redshift=1.0,
        light=lp.EllipticalSersic(
            centre=(0.0, 0.0),
            axis_ratio=0.8,
            phi=60.0,
            intensity=0.1,
            effective_radius=0.5,
            sersic_index=3.0,
        ),
    )

    for data_resolution in data_resolutions:

        simulate_image_from_galaxies_and_output_to_fits(
            data_type=data_type,
            data_resolution=data_resolution,
            sub_grid_size=sub_grid_size,
            galaxies=[lens_galaxy, source_galaxy],
        )


def make_lens_sis__source_smooth(data_resolutions, sub_grid_size):

    data_type = "lens_sis__source_smooth"

    # This source-only system has a smooth source (low Sersic Index) and simple SIE mass profile.

    lens_galaxy = g.Galaxy(
        redshift=0.5,
        mass=mp.SphericalIsothermal(centre=(0.0, 0.0), einstein_radius=1.6),
    )

    source_galaxy = g.Galaxy(
        redshift=1.0,
        light=lp.EllipticalSersic(
            centre=(0.0, 0.0),
            axis_ratio=0.8,
            phi=60.0,
            intensity=0.4,
            effective_radius=0.5,
            sersic_index=1.0,
        ),
    )

    for data_resolution in data_resolutions:

        simulate_image_from_galaxies_and_output_to_fits(
            data_type=data_type,
            data_resolution=data_resolution,
            sub_grid_size=sub_grid_size,
            galaxies=[lens_galaxy, source_galaxy],
        )


def make_lens_sis__source_smooth__offset_centre(data_resolutions, sub_grid_size):

    data_type = "lens_sis__source_smooth__offset_centre"

    # This source-only system has a smooth source (low Sersic Index) and simple SIE mass profile.

    lens_galaxy = g.Galaxy(
        redshift=0.5,
        mass=mp.SphericalIsothermal(centre=(4.0, 4.0), einstein_radius=1.6),
    )

    source_galaxy = g.Galaxy(
        redshift=1.0,
        light=lp.EllipticalSersic(
            centre=(4.0, 4.0),
            axis_ratio=0.8,
            phi=60.0,
            intensity=0.4,
            effective_radius=0.5,
            sersic_index=1.0,
        ),
    )

    for data_resolution in data_resolutions:

        simulate_image_from_galaxies_and_output_to_fits(
            data_type=data_type,
            data_resolution=data_resolution,
            sub_grid_size=sub_grid_size,
            galaxies=[lens_galaxy, source_galaxy],
        )


def make_lens_light__source_smooth(data_resolutions, sub_grid_size):

    data_type = "lens_light__source_smooth"

    # This source-only system has a smooth source (low Sersic Index) and simple SIE mass profile.

    lens_galaxy = g.Galaxy(
        redshift=0.5,
        light=lp.EllipticalSersic(
            centre=(0.0, 0.0),
            axis_ratio=0.9,
            phi=45.0,
            intensity=0.5,
            effective_radius=0.8,
            sersic_index=4.0,
        ),
        mass=mp.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.6, axis_ratio=0.7, phi=45.0
        ),
    )

    source_galaxy = g.Galaxy(
        redshift=1.0,
        light=lp.EllipticalSersic(
            centre=(0.0, 0.0),
            axis_ratio=0.8,
            phi=60.0,
            intensity=0.4,
            effective_radius=0.5,
            sersic_index=1.0,
        ),
    )

    for data_resolution in data_resolutions:

        simulate_image_from_galaxies_and_output_to_fits(
            data_type=data_type,
            data_resolution=data_resolution,
            sub_grid_size=sub_grid_size,
            galaxies=[lens_galaxy, source_galaxy],
        )


def make_lens_light__source_cuspy(data_resolutions, sub_grid_size):

    data_type = "lens_light__source_cuspy"

    # This source-only system has a smooth source (low Sersic Index) and simple SIE mass profile.

    lens_galaxy = g.Galaxy(
        redshift=0.5,
        light=lp.EllipticalSersic(
            centre=(0.0, 0.0),
            axis_ratio=0.9,
            phi=45.0,
            intensity=0.5,
            effective_radius=0.8,
            sersic_index=4.0,
        ),
        mass=mp.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.6, axis_ratio=0.7, phi=45.0
        ),
    )

    source_galaxy = g.Galaxy(
        redshift=1.0,
        light=lp.EllipticalSersic(
            centre=(0.0, 0.0),
            axis_ratio=0.8,
            phi=60.0,
            intensity=0.1,
            effective_radius=0.5,
            sersic_index=3.0,
        ),
    )

    for data_resolution in data_resolutions:

        simulate_image_from_galaxies_and_output_to_fits(
            data_type=data_type,
            data_resolution=data_resolution,
            sub_grid_size=sub_grid_size,
            galaxies=[lens_galaxy, source_galaxy],
        )
