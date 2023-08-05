# SimpleBrainViewer
A simple brain viewer using matplotlib

###### What is this?
Pretty self-explanatory... It's a simple brain viewer written
with matplotlib. Useful if you just want to view a volume quickly
in python.

Will add 4D volume viewing and voxel selection soon...

###### Usage

You can call BrainViewer from python or the command line (via nifti file or any other nibabel compatible format):

```
"""
  Example
"""
import nibabel as nib
from simplebrainviewer import *
import matplotlib.pyplot as plt

# load a volume
data = nib.load('/a/nifti/file').get_fdata()

# plot the data
simplebrainviewer.plot_brain(data)

```

###### Command Line Usage
```
usage: brainviewer.py [-h] volume

View a brain volume (Only does 3D, no 4D yet!)

positional arguments:
  volume      brain volume to view

optional arguments:
  -h, --help  show this help message and exit
```
