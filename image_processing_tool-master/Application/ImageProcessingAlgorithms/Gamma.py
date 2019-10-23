from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog
import numpy as np

@RegisterAlgorithm("Gamma", "Teme")
@InputDialog(threshold=float)
@OutputDialog(title="Binarization Output")

def gamma(image,threshold):
    lut=np.arange(0,256,1)
    lut=lut/255
    lut=np.array(255*np.power(lut,threshold),dtype='uint8')
    image=lut[image]
    return {
        'processedImage': image
    }