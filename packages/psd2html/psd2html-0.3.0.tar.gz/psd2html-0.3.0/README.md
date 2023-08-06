PSD2HTML
===========

PSD to HTML converter based on [`psd-tools`](https://github.com/psd-tools/psd-tools)

Install
---------

Use ``pip`` to install::

    pip install psd2html

Usage
---------

### As a command-line tool

The package comes with a command-line tool::

    psd2html input.psd output.html

When the output path is a directory, or omitted, the tool infers the output
name from the input::

    psd2html file.psd                 # => file.html
    psd2html file.psd dir/            # => dir/file.html
    psd2html file.psd dir/file1       # => dir/file1.html
    psd2html file.psd dir/file1.html  # => dir/file1.html

### As a python library

Example:

    from psd2html import PSD2HTML
    
    with open('file.psd', 'rb') as f:
        converter = PSD2HTML(f)
        html = converter.html
        html_string = converter.html_str



Notes:
--------
Not all PSD layers are being converted to HTML elements. Current release only converts the [TypeLayer](https://psd-tools.readthedocs.io/en/latest/reference/psd_tools.api.layers.html#typelayer) to HTML, all the others types i.e Artboard, PixelLayer, ShapeLayer and SmartObjectLayer are rendered as png images. 

Future releases will include support for other types of layers.