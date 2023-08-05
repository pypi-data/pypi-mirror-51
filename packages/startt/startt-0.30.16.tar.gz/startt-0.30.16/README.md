# Simple scaffolding for using startt

Scaffolding tools allow you to create a template for a project's files.
However, most scaffolding tools are meant for software development and are
occasionally a little over the top for latex or simple html projects. This gap
is closed by `startt`, which will in most cases just copy a single text file to
the current folder (although startt also supports small collections of a few
template files).

## Installation

Install `startt` from pypi by

  pip install startt

or from source by running

  pyb install

If you don't normally use [pybuilder](https://pybuilder.github.io/), it is
recommended that you simply use the pypi version.

## Getting started

You will need a folder with your templates (by default, `startt` will look in `$HOME/templates/`) and then you can go ahead by typing:

  startt filename_to_create.tex

See `src/cmdlinetests/useage.t` for more advanced usage.
