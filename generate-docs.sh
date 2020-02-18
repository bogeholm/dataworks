#! /bin/bash

# pip3 install pdoc3
# https://github.com/pdoc3/pdoc
# https://github.com/pdoc3/pdoc/issues/6
pdoc --html -c show_type_annotations=True dataworks --output-dir public/