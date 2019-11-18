from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog
import numpy as np
from scipy import ndimage


@RegisterAlgorithm("Cloasing", "Tema5")
@InputDialog(threshold=int,w=int,h=int)
@OutputDialog(title="Binarization Output")

def closing(image,threshold,w,h):
    """when it comes to images we have shape[0]==line==height==y and the oposite for width"""
    image=thresholding(image,threshold)
    if w%2==0:
        wBoard=int(w/2)
        w+=1
    else:
        wBoard=int((w-1)/2)
    if h%2==0:
        hBoard=int(h/2)
        h+=1
    else:
        hBoard=int((h-1)/2)
    image=boardingImage(image,w,h)
    imagineDilatat=np.zeros((image.shape[0],image.shape[1]))
    mask=np.ones((h,w))
    for y in range(hBoard,image.shape[0]-hBoard):
        for x in range(wBoard,image.shape[1]-wBoard):
            imagineDilatat[y,x]=np.max(image[y-hBoard:y+hBoard+1,x-wBoard:x+wBoard+1]*mask)
    imagineErodata=np.zeros((imagineDilatat.shape[0],imagineDilatat.shape[1]))
    for y in range(hBoard,image.shape[0]-hBoard):
        for x in range(wBoard,image.shape[1]-wBoard):
            imagineErodata[y,x]=np.min(imagineDilatat[y-hBoard:y+hBoard+1,x-wBoard:x+wBoard+1]*mask)
    return{
        'processedImage':imagineErodata.astype('uint8')
    }
def thresholding(image, threshold):
    return np.where(image>threshold,255,0)

def boardingImage(image,wBoard,hBoard):
    newImage=np.zeros((image.shape[0]+(hBoard*2),image.shape[1]+(wBoard*2)))
    newImage[hBoard:image.shape[0]+hBoard,wBoard:image.shape[1]+wBoard]=image
    return newImage


