import os

import numpy as np
import pytest

from autolens.data.instrument import abstract_data
from autolens.data.instrument import ccd
from autolens.array import scaled_array
from autolens.array import grids, mask as msk
from autolens.model.galaxy import galaxy as g
from autolens.model.inversion import pixelizations as pix
from autolens.model.inversion.plotters import mapper_plotters
from autolens.model.profiles import light_profiles as lp, mass_profiles as mp


@pytest.fixture(name="mapper_plotter_path")
def make_mapper_plotter_setup():
    return "{}/../../../test_files/plotting/mapper/".format(
        os.path.dirname(os.path.realpath(__file__))
    )


@pytest.fixture(name="image")
def make_image():
    image = scaled_array.ScaledSquarePixelArray(array=np.ones((3, 3)), pixel_scale=1.0)
    noise_map = ccd.NoiseMap(array=2.0 * np.ones((3, 3)), pixel_scale=1.0)
    psf = abstract_data.PSF(array=3.0 * np.ones((3, 3)), pixel_scale=1.0)

    return ccd.CCDData(image=image, pixel_scale=1.0, noise_map=noise_map, psf=psf)


@pytest.fixture(name="mask")
def make_mask():
    return msk.Mask.circular(shape=((3, 3)), pixel_scale=0.1, radius_arcsec=0.1)


@pytest.fixture(name="galaxy_light")
def make_galaxy_light():
    return g.Galaxy(redshift=0.5, light=lp.EllipticalSersic(intensity=1.0))


@pytest.fixture(name="galaxy_mass")
def make_galaxy_mass():
    return g.Galaxy(redshift=0.5, mass=mp.SphericalIsothermal(einstein_radius=1.0))


@pytest.fixture(name="grid")
def make_grid():
    return grids.Grid.from_shape_pixel_scale_and_sub_grid_size(
        shape=(100, 100), pixel_scale=0.05, sub_grid_size=2
    )


@pytest.fixture(name="rectangular_pixelization")
def make_rectangular_pixelization():
    return pix.Rectangular(shape=(25, 25))


@pytest.fixture(name="rectangular_mapper")
def make_rectangular_mapper(rectangular_pixelization, grid):
    return rectangular_pixelization.mapper_from_grid_and_pixelization_grid(
        grid=grid, pixelization_grid=None, inversion_uses_border=False
    )


def test__image_and_rectangular_mapper_is_output(
    image, rectangular_mapper, mapper_plotter_path, plot_patch
):
    mapper_plotters.plot_image_and_mapper(
        ccd_data=image,
        mapper=rectangular_mapper,
        should_plot_centres=True,
        should_plot_grid=True,
        image_pixels=[[0, 1, 2], [3]],
        source_pixels=[[1, 2], [0]],
        output_path=mapper_plotter_path,
        output_format="png",
    )
    assert mapper_plotter_path + "image_and_mapper.png" in plot_patch.paths


def test__rectangular_mapper_is_output(
    rectangular_mapper, mapper_plotter_path, plot_patch
):
    mapper_plotters.plot_mapper(
        mapper=rectangular_mapper,
        should_plot_centres=True,
        should_plot_grid=True,
        image_pixels=[[0, 1, 2], [3]],
        source_pixels=[[1, 2], [0]],
        output_path=mapper_plotter_path,
        output_filename="rectangular_mapper",
        output_format="png",
    )
    assert mapper_plotter_path + "rectangular_mapper.png" in plot_patch.paths
