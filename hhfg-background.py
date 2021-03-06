#!/usr/bin/env python

from gimpfu import *
import time

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def hhfg_background(image_width, image_height, radius, margin_width, margin_height, filename_base):

    gimp.context_push()

    image = gimp.Image(image_width, image_height, RGB)
    layer = gimp.Layer(image, "HHFG1", image_width, image_height, RGBA_IMAGE, 100.0, NORMAL_MODE)
    pdb.gimp_image_add_layer(image, layer, -1)
    pdb.gimp_selection_all(image)
    pdb.gimp_edit_bucket_fill(layer, BG_BUCKET_FILL, NORMAL_MODE, 100.0, 0.0, False, 0, 0);
    pdb.gimp_round_rect_select(image, margin_width, margin_height, image_width-margin_width*2, image_height-margin_height*2, radius, radius, CHANNEL_OP_REPLACE, False, False, 0.0, 0.0)
    pdb.gimp_edit_bucket_fill(layer, FG_BUCKET_FILL, NORMAL_MODE, 100, 0, False, 0, 0);
    pdb.gimp_selection_none(image)
    BLUR_RLE = 1
    blur_radius = 100
    pdb.plug_in_gauss(image, layer, blur_radius, blur_radius, BLUR_RLE)
    pdb.gimp_context_set_gradient("Twin Triangles reversed")
    pdb.plug_in_gradmap(image, layer)

    def copy_image():
        temp_image = gimp.Image(image_width, image_height, RGB)
        layer_copy = pdb.gimp_layer_new_from_drawable(layer, temp_image)
        pdb.gimp_image_add_layer(temp_image, layer_copy, -1)
        return temp_image

    def save_crop(x,y,w,h,ext):
        cropped_image = copy_image()
        cropped_image.crop(w, h, x, y)
        fn = ("%s-%s.png" % (filename_base,ext))
        pdb.file_png_save(cropped_image, cropped_image.active_drawable, fn, fn, False, 9, False, False, False, False, False)

    def my_save_crop(name, y, h):
        return save_crop(0, y, image_width, h, name)

    tot_h = margin_height + radius*2
    my_save_crop ("top", 0, tot_h)
    my_save_crop ("bottom", (image_height-tot_h), tot_h)
    my_save_crop ("middle", image_height/2, 1)

    gimp.Display(image)
    gimp.context_pop()

register(
    "python-fu-hhfg-background",
    N_("Create the Human Hacking Field Guide XHTML Background Image"),
    "HHFG Background",
    "Shlomi Fish",
    "Shlomi Fish",
    "2011",
    N_("HHFG Background..."),
    "",
    [
        (PF_INT, "image_width", "Input Image Width", 1024),
        (PF_INT, "image_height", "Input Image Height", 768),
        (PF_INT, "radius", "Input radius of the blur", 50),
        (PF_INT, "margin_width", "Input margin Width", 100),
        (PF_INT, "margin_height", "Input margin height", 100),
        (PF_STRING, "filename_base", "Output filename base", "hhfg-back-"),
    ],
    [],
    hhfg_background,
    menu="<Image>/File/Create/Patterns",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
