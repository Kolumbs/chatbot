#!/bin/sh
#
rm -r dist
set -e
TWINE_USERNAME=__token__
TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmcCJDU5MDdmYjU1LWQwMGYtNGNjZS1iZTI5LWE0YjJhYzQzZjZiZAACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgCDoMU84z_yYrxzq8hOGLOwwlnE5cNk3eeR9htBOTM90
env/bin/python -m build
env/bin/python -m twine upload dist/*
