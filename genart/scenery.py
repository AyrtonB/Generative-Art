# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/03-scenery-dither.ipynb (unless otherwise specified).

__all__ = ['load_img_data', 'rgb_to_bw', 'change_resolution', 'scale_pixel_intensity', 'get_img_negative',
           'process_img', 'draw_scenery_dither']

# Cell
import pandas as pd
import numpy as np

from scipy import ndimage
from PIL import Image

import matplotlib.pyplot as plt
import seaborn as sns

import FEAutils as hlp

from genart import svg

# Cell
def load_img_data(img_fp):
    raw_img = Image.open(img_fp)
    img_matrix = np.asarray(raw_img.getdata())

    expected_num_dims = 2
    assert len(img_matrix.shape) == expected_num_dims, f'The image matrix should have {expected_num_dims} dimensions but yours has {len(img_matrix.shape)}'

    num_colour_dims = img_matrix.shape[-1]
    assert num_colour_dims == 3, f'There should be 3 colour dimensions but instead there are {num_colour_dims}'
    img_cube = img_matrix.reshape(raw_img.size[1], raw_img.size[0], num_colour_dims)

    return img_cube

# Cell
rgb_to_bw = lambda img_rgb: np.dot(img_rgb[...,:3], [0.2989, 0.5870, 0.1140])

# Cell
def change_resolution(data, num_rows=64, num_cols=64):
    x_zoom = num_rows/data.shape[0]
    y_zoom = num_cols/data.shape[1]

    resized_data = ndimage.zoom(data, [x_zoom, y_zoom])

    return resized_data

# Cell
def scale_pixel_intensity(img_bw, min_threshold_frac=0.25, max_threshold_frac=0.95):
    img_pass1_intensity_range = img_bw.max() - img_bw.min()
    img_scaled_pass1 = (img_bw - img_bw.min())/img_pass1_intensity_range

    img_clipped = img_scaled_pass1.clip(min_threshold_frac, max_threshold_frac) - min_threshold_frac

    img_pass2_intensity_range = img_clipped.max() - img_clipped.min()
    img_scaled_pass2 = (img_clipped - img_clipped.min())/img_pass2_intensity_range

    return img_scaled_pass2

# Cell
get_img_negative = lambda img: 1-scale_pixel_intensity(img, 0, 1)

# Cell
def process_img(img_fp, num_rows=64, num_cols=64, min_threshold_frac=0.25, max_threshold_frac=0.95):
    img_cube = load_img_data(img_fp)
    img_bw = rgb_to_bw(img_cube)
    img_resized = change_resolution(img_bw, num_rows, num_cols)
    img_scaled = scale_pixel_intensity(img_resized, min_threshold_frac, max_threshold_frac)
    img_neg = get_img_negative(img_scaled)

    return img_neg

# Cell
def draw_scenery_dither(width=500, height=500,
                        bkg_r=0.3, bkg_g=0.3, bkg_b=0.3):

    draw_ops = [
        (svg.draw_background, {
            'width': width,
            'height': height,
            'bkg_r': bkg_r,
            'bkg_g': bkg_g,
            'bkg_b': bkg_b
        })
    ]

    img = svg.draw_img(draw_ops)

    return img