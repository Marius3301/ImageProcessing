from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog
import numpy as np
import math

@RegisterAlgorithm("Filtru Gauss","Tema3")
@InputDialog(sigma=float)
#@OutputDialog(title="Binarization Output")

def filtruGauss(image,sigma):
    matSize=np.round(4*sigma).astype('uint')
    if (matSize%2==0): matSize+=1
    index = np.arange(-(matSize/2).astype('int'),(matSize/2).astype('int')+1,).astype('int')
    print((matSize/2).astype('uint'))
    halfMat=(matSize/2).astype('uint')
    j=np.ones((matSize,matSize))
    j*=index
    i=np.rot90(j,3)
    maska=np.where(True,(1/(2*np.pi*np.power(sigma,2)))*np.power(math.e,-(np.power(i,2)+np.power(j,2)/(2*np.power(sigma,2)))),0)
    maska*=(1/maska.sum())
    print(len(image.shape))
    print(maska)
    if (len(image.shape)==3):
        newIm = np.zeros((image.shape[0] * 3, image.shape[1] * 3, image.shape[2]))
        newIm =imageMiror(newIm,image)
        print("Color")
        for i in range(image.shape[0],image.shape[0]*2):
            for j in range(image.shape[1],image.shape[1]*2):
                image[i-image.shape[0],j-image.shape[1],0]=np.sum(newIm[i-halfMat:i+halfMat+1,j-halfMat:j+halfMat+1,0]*maska)
                image[i - image.shape[0], j - image.shape[1],1] = np.sum(
                    newIm[i - halfMat:i + halfMat + 1, j - halfMat:j + halfMat + 1,1] * maska)
                image[i - image.shape[0], j - image.shape[1],2] = np.sum(
                    newIm[i - halfMat:i + halfMat + 1, j - halfMat:j + halfMat + 1,2] * maska)
    elif (len(image.shape)==2):
        newIm=np.zeros((image.shape[0]*3,image.shape[1]*3))
        newIm=imageMiror(newIm,image)
        print("Gray")
        print(newIm[image.shape[0]-halfMat:image.shape[0]+halfMat,image.shape[1]-halfMat:image.shape[1]+halfMat])
        for i in range(image.shape[0],image.shape[0]*2):
            for j in range(image.shape[1],image.shape[1]*2):
                image[i-image.shape[0],j-image.shape[1]]=np.sum(newIm[i-halfMat:i+halfMat+1,j-halfMat:j+halfMat+1]*maska)


    return {
        'processedImage' : image.astype('uint8')
    }

def imageMiror(newIm,image):
    newIm[:image.shape[0], :image.shape[1]] = np.flip(np.flip(image, 0), 1)
    newIm[:image.shape[0], image.shape[1]:image.shape[1] * 2] = np.flip(image, 0)
    newIm[:image.shape[0], image.shape[1] * 2:image.shape[1] * 3] = np.flip(np.flip(image, 0), 1)
    newIm[image.shape[0]:image.shape[0] * 2, :image.shape[1]] = np.flip(image, 1)
    newIm[image.shape[0]:image.shape[0] * 2, image.shape[1]:image.shape[1] * 2] = image
    newIm[image.shape[0]:image.shape[0] * 2, image.shape[1] * 2:image.shape[1] * 3] = np.flip(image, 1)
    newIm[image.shape[0] * 2:image.shape[0] * 3, :image.shape[1]] = np.flip(np.flip(image, 0), 1)
    newIm[image.shape[0] * 2:image.shape[0] * 3, image.shape[1]:image.shape[1] * 2] = np.flip(image, 0)
    newIm[image.shape[0] * 2:image.shape[0] * 3, image.shape[1] * 2:image.shape[1] * 3] = np.flip(np.flip(image, 0), 1)
    return newIm