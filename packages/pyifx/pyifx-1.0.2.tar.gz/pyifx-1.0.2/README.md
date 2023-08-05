# pyifx
An image processing, editing &amp; handling library in Python.

## Version History 
0.0.1 - InDev <br />
0.0.2 - Brightness module added, main classes, internal + misc functions <br />
0.0.3 - Color overlay module added <br />
0.1.0 - HSL Module Added <br />
0.1.1 - Convolutional Framework + Blur functions added <br />
0.1.2 - Create kernel based on blur type <br />
0.1.3 - Added pixelation <br />
0.1.4 - Added edge detection <br />
0.2.0 - Graphics module added <br />
0.2.1 - Resize feature added <br />
0.2.2 - File naming & formatting features added <br />
0.3.0 - Composition module added <br />
<b>1.0.0 - Initial Release (CURRENT)</b><br />

## Features
pyifx contains 4 main modules, giving users access to functions such as:
<ul>
	<li>HSL Modification</li>
	<li>Convolution-based functions</li>
	<li>Image format conversion & resizing</li>
	<li>And much more.</li>
</ul>

pyifx also allows for images to be read in from directories instead of individually importing them, allowing for image modification processes to be automated.

A full list of features is available in the [user guide & documentation](https://pyifx.readthedocs.io).

## Code Example
The code block below perfectly details the use of the library.

``` python
#demo_file.py
import pyifx

# Creating the image
image = pyifx.misc.PyifxImage(input_path="path/to/img.png", output_path="path/to/new_img.png")

# Creating the volume
volume = pyifx.misc.ImageVolume(input_path="lots/of/images/", output_path="lots/of/images/modified/", prefix="_")

#Creating the list
image_2 = pyifx.misc.PyifxImage(input_path="different/path/to/img.png", output_path="different/path/to/new_img.png")
image_list = [image, image_2]

brightened_image = pyifx.hsl.brighten(image, 50)
brightened_list = pyifx.hsl.brighten(image_list, 50)
```

For more information about using the library, read the [image classes](https://pyifx.readthedocs.io/en/latest/image_classes.html) and [usage](https://pyifx.readthedocs.io/en/latest/usage.html) pages of the user guide, which go into more detail about using the library.

## Installation

To install the library, use the command below:
```bash
	pip install pyifx
```

This will install the library and its dependencies (if needed).

## Documentation
The documentation of this project can be found [here](https://pyifx.readthedocs.io).


## Tests
TBA - The testing portion of the contribution section is currently being written.

## Usage
To learn more about using the library, read the [image classes](https://pyifx.readthedocs.io/en/latest/image_classes.html) and [usage](https://pyifx.readthedocs.io/en/latest/usage.html) pages of the user guide, which go into more detail about using it.

## Contribute
To learn how to contribute to the project, read the [contribution guide](https://pyifx.readthedocs.io/en/latest/contribution.html).

**Note**: The contribution guide for testers is still being added.

## License
[MIT © 2019 Jad Khalili](https://pyifx.readthedocs.io/en/latest/license.html).
