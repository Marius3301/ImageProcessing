from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog
import numpy as np

@RegisterAlgorithm("Scalare","Tema6")
@InputDialog(factor_scalare=float)
#@OutputDialog(title="Binarization Output")

def Scalare(image,factor_scalare):
    image=image.astype('float64')
    if(len(image.shape)==2):
        rezult = np.zeros(
            (int(np.round(image.shape[0] * factor_scalare)), int(np.round(image.shape[1] * factor_scalare))))
        for y in range(1,rezult.shape[0]):
            for x in range(1,rezult.shape[1]):
                x_c=x/factor_scalare
                y_c=y/factor_scalare
                x_0=int(x_c)
                y_0=int(y_c)
                x_1=x_0+1
                y_1=y_0+1
                if (x_1<image.shape[0]) and (y_1<image.shape[1]):
                    fx1 =(image[y_0,x_1]-image[y_0,x_0])*(x_c-x_0)+image[y_0,x_0]
                    fx2=(image[y_1,x_1]-image[y_1,x_0])*(x_c-x_0)+image[y_1,x_0]
                    rezult[y,x]=(fx2-fx1)*(y_c-y_0)+fx1
                else:
                    rezult[y,x]=image[y_0,x_0]
    else:
        rezult = np.zeros(
            (int(np.round(image.shape[0] * factor_scalare)), int(np.round(image.shape[1] * factor_scalare)),image.shape[2]))
        for y in range(1,rezult.shape[0]):
            for x in range(1,rezult.shape[1]):
                x_c=x/factor_scalare
                y_c=y/factor_scalare
                x_0=int(x_c)
                y_0=int(y_c)
                x_1=x_0+1
                y_1=y_0+1
                if (x_1<image.shape[0]) and (y_1<image.shape[1]):
                    fx1R =(image[y_0,x_1,0]-image[y_0,x_0,0])*(x_c-x_0)+image[y_0,x_0,0]
                    fx2R=(image[y_1,x_1,0]-image[y_1,x_0,0])*(x_c-x_0)+image[y_1,x_0,0]
                    rezult[y,x,0]=(fx2R-fx1R)*(y_c-y_0)+fx1R
                    fx1G = (image[y_0, x_1, 1] - image[y_0, x_0, 1]) * (x_c - x_0) + image[y_0, x_0, 1]
                    fx2G = (image[y_1, x_1, 1] - image[y_1, x_0, 1]) * (x_c - x_0) + image[y_1, x_0, 1]
                    rezult[y, x, 1] = (fx2G - fx1G) * (y_c - y_0) + fx1G
                    fx1B = (image[y_0, x_1, 2] - image[y_0, x_0, 2]) * (x_c - x_0) + image[y_0, x_0, 2]
                    fx2B = (image[y_1, x_1, 2] - image[y_1, x_0, 2]) * (x_c - x_0) + image[y_1, x_0, 2]
                    rezult[y, x, 2] = (fx2B - fx1B) * (y_c - y_0) + fx1B
                else:
                    rezult[y,x]=image[y_0,x_0]
    return{
        'processedImage' : rezult.astype('uint8')
    }

