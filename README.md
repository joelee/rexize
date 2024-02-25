# resize_imgs

A CLI script to bulk resize and convert image files in a directory recursively into a specified output directory.

## Usage

```
resize_imgs [options] input_folder output_folder


  Bulk resize and convert images from a folder recursively.


  positional arguments:
    input_folder          Input folder containing images
    output_folder         Output folder for resized images

  options:
    -h, --help            show this help message and exit
    -W WIDTH, --width WIDTH
                          Width to resize the image. Suffix with for percentage
    -H HEIGHT, --height HEIGHT
                          Height to resize the image. Suffix with for percentage
    -M MAX_SIZE, --max-size MAX_SIZE
                          Maximum size in pixels for the image. Resize if larger than this size
    -f FORMAT, --format FORMAT
                          Format of the output image: JPEG, PNG, WEBP, GIF, TIFF, BMP
    --rgb                 Downscale RGBA images to RGB
    --grayscale           Downscale images to Grayscale
    -q, --quiet           Suppress all output messages, except errors
    --verbose             Verbose output for debugging

```

## Features TO DO
- User documentation
- Bulk renaming image files
- Rotation and Cropping support
- Custom filters
