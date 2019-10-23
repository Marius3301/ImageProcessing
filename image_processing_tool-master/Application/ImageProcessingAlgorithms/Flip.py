from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog
import numpy as np

@RegisterAlgorithm("Flip", "Utils", fromMainModel=["rightClickLastPositions"])
@OutputDialog(title="Flip Output")

def Flip(image,rightClickLastPositions):
    if(len(rightClickLastPositions)==4):
        x =np.zeros(4,dtype=int)
        y= np.zeros(4,dtype=int)
        for i in range(4):
            y[i] = int(rightClickLastPositions[i].y)
            x[i] = int(rightClickLastPositions[i].x)
        print (x,y)
        print (y.max(),x.max())
        imageCopy =image[y.min():y.max(),x.min():x.max()]
        imageCopy =imageCopy.transpose(1,0)
    else :
        return {
            'outputMessage' : "There is something wrong with the ClickPositons "
        }
    print(imageCopy.max(),imageCopy.min())
    return {
        'processedImage' : imageCopy
    }