from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog
from scipy import ndimage
import numpy as np

@RegisterAlgorithm("Canny","Tema4")
@InputDialog(tMin=float,tMax=float)
#@OutputDialog(title="Binarization Output")

def canny(image,tMin,tMax):
    fx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    fy=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    #image=ndimage.gaussian_filter(image,1)
    image = filtruGauss(image, 1)

    maskafx=ndimage.filters.convolve(image,fx,mode='constant',cval=0)
    maskafy=ndimage.filters.convolve(image, fy, mode='constant', cval=0)

    gradient=np.hypot(maskafx,maskafy)
    grade=np.arctan2(maskafy,maskafx)
    directia=detDirection(grade)
    imagineSubtiata=subtiere(gradient,directia).astype('uint8')
    imagineSubtiata=np.where(gradient>tMax,255,imagineSubtiata)
    imagineSubtiata=np.where(gradient<tMin,0,imagineSubtiata)
    return {
        'processedImage': imagineSubtiata
    }


def subtiere(gradient,directia):
    conturImage=np.zeros((gradient.shape[0],gradient.shape[1]))
    vecinSpate=255
    vecinFata=255
    for i in range(gradient.shape[0]):
        for j in range (gradient.shape[1]):
            if (directia[i,j]==1):
                vecinFata=gradient[i+1,j]
                vecinSpate=gradient[i-1,j]
            elif(directia[i,j]==2):
                vecinFata=gradient[i-1,j+1]
                vecinSpate=gradient[i+1,j-1]
            elif(directia[i,j]==3):
                vecinFata=gradient[i+1,j+1]
                vecinSpate=gradient[i-1,j-1]
            elif(directia[i,j]==4):
                vecinFata=gradient[i,j+1]
                vecinSpate=gradient[i,j-1]
            if(gradient[i,j]>vecinSpate and gradient[i,j]>vecinFata):
                conturImage[i,j]=255
            else:
                conturImage[i,j]=0
    return conturImage

def detDirection(degree):
    degree=(degree*180)/np.pi
    horizontal=np.where(np.logical_or(-22.5<degree,degree<22.5),1,0)
    diagonalRight=np.where(np.logical_or(-65.5<degree,degree<-22.5),2,0)
    diagonalLeft=np.where(np.logical_or(22.5<degree,degree<65.5),3,0)
    vertical=np.where(np.logical_or(degree>-65.5,degree<65.5),4,0)
    result=horizontal+diagonalLeft+diagonalRight+vertical
    return result


def filtruGauss(image,sigma):
    matSize=np.round(4*sigma).astype('uint')
    if (matSize%2==0): matSize+=1
    index = np.arange(-(matSize/2).astype('int'),(matSize/2).astype('int')+1,).astype('int')
    #print((matSize/2).astype('uint'))
    halfMat=(matSize/2).astype('uint')
    j=np.ones((matSize,matSize))
    j*=index
    i=np.rot90(j,3)
    #print(i)
    maska=np.where(True,(1/(2*np.pi*np.power(sigma,2)))*np.power(np.e,-(np.power(i,2)+np.power(j,2)/(2*np.power(sigma,2)))),0)
    maska*=(1/maska.sum())
    #print(len(image.shape))
    #print(maska)
    newIm=np.zeros((image.shape[0]*3,image.shape[1]*3))
    newIm=imageMiror(newIm,image)
    #print(newIm[image.shape[0]-halfMat:image.shape[0]+halfMat,image.shape[1]-halfMat:image.shape[1]+halfMat])
    for i in range(image.shape[0],image.shape[0]*2):
        for j in range(image.shape[1],image.shape[1]*2):
            image[i-image.shape[0],j-image.shape[1]]=np.sum(newIm[i-halfMat:i+halfMat+1,j-halfMat:j+halfMat+1]*maska)


    return  image.astype('uint8')

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