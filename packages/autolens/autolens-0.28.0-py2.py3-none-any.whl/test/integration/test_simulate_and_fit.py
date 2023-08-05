import os
import shutil

import numpy as np
import pytest

from autolens.data.instrument import abstract_data
from autolens.data.instrument import ccd
from autolens.array.util import array_util
from autolens.array import grids, mask as msk
from autolens.model.galaxy import galaxy as g
from autolens.lens import lens_data as ld
from autolens.lens import lens_fit
from autolens.lens import ray_tracing
from autolens.model.profiles import light_profiles as lp, mass_profiles as mp


def test__simulate_lensed_source_and_fit__no_psf_blurring__chi_squared_is_0__noise_normalization_correct():

    psf = abstract_data.PSF(
        array=np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]),
        pixel_scale=0.2,
    )

    grid = grids.Grid.from_shape_pixel_scale_and_sub_grid_size(
        shape=(11, 11), pixel_scale=0.2, sub_grid_size=2
    )

    lens_galaxy = g.Galaxy(
        redshift=0.5,
        light=lp.EllipticalSersic(centre=(0.1, 0.1), intensity=0.1),
        mass=mp.EllipticalIsothermal(centre=(0.1, 0.1), einstein_radius=1.8),
    )

    source_galaxy = g.Galaxy(
        redshift=1.0, light=lp.EllipticalExponential(centre=(0.1, 0.1), intensity=0.5)
    )

    tracer = ray_tracing.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])

    ccd_simulated = ccd.SimulatedCCDData.from_tracer_grid_and_exposure_arrays(
        tracer=tracer,
        grid=grid,
        pixel_scale=0.2,
        exposure_time=300.0,
        psf=psf,
        background_sky_level=0.0,
        add_noise=False,
    )

    ccd_simulated.noise_map = np.ones(ccd_simulated.image.shape)

    path = "{}/data_temp/simulate_and_fit".format(
        os.path.dirname(os.path.realpath(__file__))
    )  # Setup path so we can output the simulated image.

    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

    if os.path.exists(path) == False:
        os.makedirs(path)

    array_util.numpy_array_2d_to_fits(
        array_2d=ccd_simulated.image, file_path=path + "/image.fits"
    )
    array_util.numpy_array_2d_to_fits(
        array_2d=ccd_simulated.noise_map, file_path=path + "/noise_map.fits"
    )
    array_util.numpy_array_2d_to_fits(array_2d=psf, file_path=path + "/psf.fits")

    ccd_data = ccd.load_ccd_data_from_fits(
        image_path=path + "/image.fits",
        noise_map_path=path + "/noise_map.fits",
        psf_path=path + "/psf.fits",
        pixel_scale=0.2,
    )

    mask = msk.Mask.circular(
        shape=ccd_data.image.shape, pixel_scale=0.2, radius_arcsec=0.8
    )

    lens_data = ld.LensData(ccd_data=ccd_data, mask=mask, sub_grid_size=2)

    tracer = ray_tracing.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])

    fit = lens_fit.LensProfileFit(lens_data=lens_data, tracer=tracer)

    assert fit.chi_squared == 0.0

    path = "{}/data_temp".format(
        os.path.dirname(os.path.realpath(__file__))
    )  # Setup path so we can output the simulated image.

    if os.path.exists(path) == True:
        shutil.rmtree(path)


def test__simulate_lensed_source_and_fit__include_psf_blurring__chi_squared_is_0__noise_normalization_correct():

    psf = abstract_data.PSF.from_gaussian(shape=(3, 3), pixel_scale=0.2, sigma=0.75)

    grid = grids.Grid.from_shape_pixel_scale_and_sub_grid_size(
        shape=(11, 11), pixel_scale=0.2, sub_grid_size=1
    )

    lens_galaxy = g.Galaxy(
        redshift=0.5,
        light=lp.EllipticalSersic(centre=(0.1, 0.1), intensity=0.1),
        mass=mp.EllipticalIsothermal(centre=(0.1, 0.1), einstein_radius=1.8),
    )
    source_galaxy = g.Galaxy(
        redshift=1.0, light=lp.EllipticalExponential(centre=(0.1, 0.1), intensity=0.5)
    )
    tracer = ray_tracing.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])

    ccd_simulated = ccd.SimulatedCCDData.from_image_and_exposure_arrays(
        image=tracer.padded_profile_image_2d_from_grid_and_psf_shape(
            grid=grid, psf_shape=psf.shape
        ),
        pixel_scale=0.2,
        exposure_time=300.0,
        psf=psf,
        background_sky_level=0.0,
        add_noise=False,
    )
    ccd_simulated.noise_map = np.ones(ccd_simulated.image.shape)

    path = "{}/data_temp/simulate_and_fit".format(
        os.path.dirname(os.path.realpath(__file__))
    )  # Setup path so we can output the simulated image.

    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

    if os.path.exists(path) == False:
        os.makedirs(path)

    array_util.numpy_array_2d_to_fits(
        array_2d=ccd_simulated.image, file_path=path + "/image.fits"
    )
    array_util.numpy_array_2d_to_fits(
        array_2d=ccd_simulated.noise_map, file_path=path + "/noise_map.fits"
    )
    array_util.numpy_array_2d_to_fits(array_2d=psf, file_path=path + "/psf.fits")

    ccd_data = ccd.load_ccd_data_from_fits(
        image_path=path + "/image.fits",
        noise_map_path=path + "/noise_map.fits",
        psf_path=path + "/psf.fits",
        pixel_scale=0.2,
    )

    mask = msk.Mask.circular(
        shape=ccd_data.image.shape, pixel_scale=0.2, radius_arcsec=0.8
    )

    lens_data = ld.LensData(ccd_data=ccd_data, mask=mask, sub_grid_size=1)

    tracer = ray_tracing.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])

    fitter = lens_fit.LensProfileFit(lens_data=lens_data, tracer=tracer)

    assert fitter.chi_squared == pytest.approx(0.0, 1e-4)

    path = "{}/data_temp".format(
        os.path.dirname(os.path.realpath(__file__))
    )  # Setup path so we can output the simulated image.

    if os.path.exists(path) == True:
        shutil.rmtree(path)
