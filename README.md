# Rexize - Bulk Resize and Convert Images tool

Welcome to the Rexize CLI Tool, an open-source command-line interface tool designed for bulk resizing and converting image files. This tool efficiently processes images in a directory recursively, outputting them to a specified directory with your chosen dimensions and formats. It is built with flexibility and efficiency in mind, to cater to a wide range of use cases and users.


## Features

- **Bulk Resizing**: Resize multiple images in a batch to your desired dimensions.
- **Format Conversion**: Convert images into different formats (e.g., JPEG, PNG) in one go.
- **Recursive Directory Processing**: Process images in a directory and its subdirectories.
- **Custom Output Directory**: Specify a different directory to output the processed images.


## About
This CLI tool for bulk resizing and converting image files has wide-ranging applications, benefiting users in web development, digital marketing, photography, and data science. It streamlines workflows, ensures consistency in image quality and size, and facilitates efficient storage and transfer.


## Potential Use Cases

This tool is versatile and can be beneficial across various fields. Its potential use cases and benefits span several domains, including but not limited to:

1. **Web Development and Design**: Optimize images for web usage, ensuring fast loading times and responsiveness without compromising quality. Bulk prepare thumbnails, hero images, and other assets for websites.
2. **Digital Marketing**: Prepare images for different social media platforms, email campaigns, and online ads with ease.
3. **Photography**: Resize and convert images for client delivery, portfolio display, or contest submissions efficiently.
4. **Data Science and Machine Learning**: Automate the preprocessing of images for computer vision projects.
5. **Archiving and Digital Libraries**: Standardize image sizes and formats for digital archiving purposes.
6. **Personal Use**: Manage personal image collections, optimizing for storage or preparing for social media and personal websites.


## Benefits

- **Efficiency and Time-Saving**: Automates a task that would be incredibly time-consuming if done manually, especially for large image collections.
- **Quality and Consistency**: Ensures that all images meet set criteria for size and format, maintaining a high standard across a project or campaign.
- **Open-Source Collaboration**: Being open-sourced, it encourages collaboration and contributions from other developers, leading to new features, bug fixes, and improvements.
- **Customization and Flexibility**: Users can adapt the tool to fit their specific needs, whether that's integrating it into larger workflows or customizing it for unique project requirements.
- **Resource Optimization**: Helps in optimizing web pages by reducing load times and improving user experience, which can contribute to better SEO rankings and user retention.


## Getting Started
To get started with Rexize, please ensure you have the Prerequisites and follow the installation instructions below:

### Prerequisites
- Python 3.9 or higher
- Poetry or Pipx package manager
- Git
- Linux, macOS, or Windows with WSL
- Basic knowledge of the command line interface for now. A GUI wrapper is in the works.

### Installation
You can install Rexize using either PipX or Poetry. Choose the method that suits your workflow:

#### Using PipX
Install [pipx](https://github.com/pypa/pipx) if you haven't already, and then run the following command:
```bash
pipx install git+https://github.com/joelee/rexize.git
```

#### Using Poetry
Install [Poetry](https://python-poetry.org/docs/#installation) if you haven't already, and then run the following commands:
```bash
git clone https://github.com/joelee/rexize.git ~/.local/rexize
cd ~/.local/rexize
poetry install
echo "alias rexize='~/.local/rexize/bin/rexize'" >> ~/.bashrc
source ~/.bashrc
```

## Usage
```
rexize [options] input_folder output_folder


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


## How to Contribute

We welcome contributions from the community, whether it's adding new features, fixing bugs, or improving documentation. If you have a feature request or have identified an issue, please open an issue on GitHub. We also encourage you to fork the repository and submit pull requests with your improvements.


## Features TO DO
- User documentation
- Bulk renaming image files
- Rotation and Cropping support
- Custom filters
- A new GUI Wrapper
- Increase Test Coverage to above 90%
