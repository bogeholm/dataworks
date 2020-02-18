#! /bin/bash

# pip3 install pdoc3
# https://github.com/pdoc3/pdoc
# https://github.com/pdoc3/pdoc/issues/6
pdoc --html --force -c show_type_annotations=True dataworks --output-dir docs
rm -rf public/
mkdir -p public/
mv docs/dataworks/* public/
touch public/.nojekyll