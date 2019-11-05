from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog
import numpy as np

@RegisterAlgorithm("Binarizare HSV", "Tema2",fromMainModel=["rightClickLastPositions"])
@InputDialog(threshold=float,lightThreshold=int)
@OutputDialog(title="BinarizationHSV Output")

def BinarizareHSV(image,rightClickLastPositions,threshold,lightThreshold):
    if(len(rightClickLastPositions)!=1):
        return {
            'outputMessage':'Pls select just a single referece color'
        }
    image=image/255.0
    print(image.shape)
    min=image.min(axis=2)
    max=image.max(axis=2)
    red=np.array(image[:,:,0],dtype='float')
    green=np.array(image[:,:,1],dtype='float')
    blue=np.array(image[:,:,2],dtype='float')
    c=np.array(max-min,dtype='float')
    v=np.array(max,dtype='float')
    h=np.array(max,dtype='float')
    s=np.array(max,dtype='float')
    for line in range(0,max.shape[0]):
        for col in range(0,max.shape[1]):
            if c[line,col]<0.03:
                h[line,col]=np.nan
                s[line, col] =0
            else :
                s[line,col]=c[line,col]/max[line,col]
                if max[line,col]==red[line,col]:
                    h[line,col]=60*(((green[line,col]-blue[line,col])/c[line,col])% 6)
                elif max[line,col]==green[line,col]:
                    h[line,col]=60*(((blue[line,col]-red[line,col])/c[line,col])+2)
                elif max[line,col]==blue[line,col]:
                    h[line,col]=60*(((red[line,col]-green[line,col])/c[line,col])+4)
    h=np.round(h)

    lightThreshold/=100.0
    refColor = h[rightClickLastPositions[0].y,rightClickLastPositions[0].x]
    refLight = v[rightClickLastPositions[0].y,rightClickLastPositions[0].x]
    if np.isnan(refColor):
        image=np.where(np.logical_and(np.isnan(h),abs(refLight-v)<=lightThreshold),255,0)
    else:
        image=np.where((abs(h-refColor)%(360-threshold))<=threshold,255,0)
    image=np.array(image,dtype='uint8')

    return {
        'processedImage': image
    }




