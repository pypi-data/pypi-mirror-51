# styletransfer
A Python library to transfer the style of one picture to another using PyTorch.

## Installation
You can install styletransfer from PyPi using:

`pip install styletransfer`

This package requires Python 3.x

## Basic usage
The easiest way to get started is taking an online image for style transfer and just running with the default parameters:

```python
from styletransfer import StyleTransfer
styleTransfer = StyleTransfer()

#Set the content image from URL
styleTransfer.setContentFromUrl('https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Felis_silvestris_catus_lying_on_rice_straw.jpg/640px-Felis_silvestris_catus_lying_on_rice_straw.jpg')

#Set the style image from URL
styleTransfer.setStyleFromUrl('https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Tsunami_by_hokusai_19th_century.jpg/640px-Tsunami_by_hokusai_19th_century.jpg')

#Use default settings and train the model
#If you do not have a GPU that can take 30-60 minutes
styleTransfer.apply()

#Write the result image to a file
styleTransfer.writeFinalImage('stylized_image.jpg')
```

## Advanced usage
*TBD: Detailed instructions to follow*
