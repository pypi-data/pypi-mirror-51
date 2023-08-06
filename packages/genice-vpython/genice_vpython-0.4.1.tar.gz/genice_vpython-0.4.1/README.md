# [genice-vpython](https://github.com/vitroid/genice-vpython/)

A [GenIce](https://github.com/vitroid/GenIce) plugin to visualize the structure with [VPython](http://vpython.org).

version 0.4.1

## Requirements

* vpython
* genice>=0.25

## Installation from PyPI

    % pip install genice_vpython

## Manual Installation

### System-wide installation

    % make install

### Private installation

Copy the files in genice_svg/formats/ into your local formats/ folder.

## Usage

    
    Usage:
        genice III -f vpython
    
        opens a window in the web browser to show the image.
    
    Options:
    
        No options available.

## Test in place

    % make test
