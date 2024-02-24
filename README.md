# resize_imgs

A CLI script to bulk resize and convert image files in a directory recursively into a specified output directory.

### Usage

```
resize_imgs [-h] [-W WIDTH] [-H HEIGHT] [-f FORMAT] input_folder output_folder

Bulk resize and convert images from a directory recursively.

positional arguments:
  input_folder          Input folder containing images
  output_folder         Output folder for resized images

options:
  -h, --help            show this help message and exit
  -W WIDTH, --width WIDTH
                        Width to resize the image. Suffix with for percentage
  -H HEIGHT, --height HEIGHT
                        Height to resize the image. Suffix with for percentage
  -f FORMAT, --format FORMAT
                        Format of the output image: JPEG, PNG, WEBP, GIF, TIFF, BMP
  --rgb                 Downscale RGBA images to RGB
  --grayscale           Downscale images to Grayscale

```
