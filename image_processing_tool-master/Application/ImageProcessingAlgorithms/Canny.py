from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog
from scipy import ndimage
import numpy as np
import queue
from skimage import data, filters
import cv2

@RegisterAlgorithm("Canny","Tema4")
@InputDialog(tMin=float,tMax=float)
#@OutputDialog(title="Binarization Output")

def canny(image,tMin,tMax):
    fx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    fy=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    image=ndimage.gaussian_filter(image,1)
    #image = filtruGauss(image, 1)
    #print(fx)
    #print(fy)
    image=np.array(image,dtype='float')
    maskafx=ndimage.filters.convolve(image,fx,mode='constant',cval=0.0)
    maskafy=ndimage.filters.convolve(image,fy, mode='constant', cval=0.0)

    gradient=np.hypot(maskafx,maskafy)
    print(maskafx[39,560],maskafy[39,560])
    grade=np.arctan2(maskafy,maskafx)
    print(gradient[39,560])
    directia=detDirection(grade)
    imagineSubtiata=subtiere(gradient,directia)
    imagineSubtiata = np.where(imagineSubtiata >= tMax, 255, imagineSubtiata)
    imagineSubtiata = np.where(imagineSubtiata < tMin, 0, imagineSubtiata)
    sus_jos=np.array(imagineSubtiata).astype('uint8')
    stanga_dreapta=np.array(imagineSubtiata).astype('uint8')
    dreapta_stanga=np.array(imagineSubtiata).astype('uint8')
    jos_sus=np.array(imagineSubtiata).astype('uint8')
    sus_jos=parcurgereSJ(sus_jos,tMin,tMax)
    stanga_dreapta=parcurgereSD(stanga_dreapta,tMin,tMax)
    dreapta_stanga=parcurgereDS(dreapta_stanga,tMin,tMax)
    jos_sus=parcurgereJS(jos_sus,tMin,tMax)
    imagine=sus_jos+stanga_dreapta+dreapta_stanga+jos_sus
    #print(imagine.max())
    return {
        'processedImage': imagine.astype('uint8')
    }

def parcurgereSJ(imagine,tMin,tMax):
    for i in range(imagine.shape[0] - 1):
        for j in range(imagine.shape[1] - 1):
            if (tMin < imagine[i, j] < tMax):
                if (imagine[i - 1, j + 1] == 255)  or\
                        (imagine[i - 1, j - 1] == 255) or\
                        (imagine[i - 1, j] == 255) or\
                        (imagine[i, j - 1] == 255) or\
                        (imagine[i, j + 1] == 255) or\
                        (imagine[i + 1, j - 1] == 255) or\
                        (imagine[i + 1, j] == 255) or\
                        (imagine[i + 1, j + 1] == 255):
                    imagine[i, j] = 255
                else:
                    imagine[i, j] = 0
    return imagine

def parcurgereSD(imagine,tMin,tMax):
    for i in range(imagine.shape[0] - 1,0,-1):
        for j in range(imagine.shape[1] - 1):
            if (tMin < imagine[i, j] < tMax):
                if (imagine[i - 1, j + 1] == 255)  or\
                        (imagine[i - 1, j - 1] == 255) or\
                        (imagine[i - 1, j] == 255) or\
                        (imagine[i, j - 1] == 255) or\
                        (imagine[i, j + 1] == 255) or\
                        (imagine[i + 1, j - 1] == 255) or\
                        (imagine[i + 1, j] == 255) or\
                        (imagine[i + 1, j + 1] == 255):
                    imagine[i, j] = 255
                else:
                    imagine[i, j] = 0
    return imagine

def parcurgereDS(imagine,tMin,tMax):
    for i in range(imagine.shape[0] - 1):
        for j in range(imagine.shape[1] - 1,0,-1):
            if (tMin < imagine[i, j] < tMax):
                if (imagine[i - 1, j + 1] == 255)  or\
                        (imagine[i - 1, j - 1] == 255) or\
                        (imagine[i - 1, j] == 255) or\
                        (imagine[i, j - 1] == 255) or\
                        (imagine[i, j + 1] == 255) or\
                        (imagine[i + 1, j - 1] == 255) or\
                        (imagine[i + 1, j] == 255) or\
                        (imagine[i + 1, j + 1] == 255):
                    imagine[i, j] = 255
                else:
                    imagine[i, j] = 0
    return imagine

def parcurgereJS(imagine,tMin,tMax):
    for i in range(imagine.shape[0] - 1,0,-1):
        for j in range(imagine.shape[1] - 1,0,-1):
            if (tMin < imagine[i, j] < tMax):
                if (imagine[i - 1, j + 1] == 255)  or\
                        (imagine[i - 1, j - 1] == 255) or\
                        (imagine[i - 1, j] == 255) or\
                        (imagine[i, j - 1] == 255) or\
                        (imagine[i, j + 1] == 255) or\
                        (imagine[i + 1, j - 1] == 255) or\
                        (imagine[i + 1, j] == 255) or\
                        (imagine[i + 1, j + 1] == 255):
                    imagine[i, j] = 255
                else:
                    imagine[i, j] = 0
    return imagine

def hister(imagineSubtiata,tMax):
    Q=queue.Queue()
    Q.put([0,0])
    Visited=[]
    while not Q.empty():
        flag=False
        i,j=Q.get()
        if (imagineSubtiata[i - 1, j + 1] > tMax and not (i,j) in Visited):
            imagineSubtiata[i, j] = 255
            flag=True
        elif (imagineSubtiata[i - 1, j - 1] > tMax and not (i,j) in Visited):
            imagineSubtiata[i, j] = 255
            flag = True
        elif (imagineSubtiata[i - 1, j] > tMax and not (i,j) in Visited):
            imagineSubtiata[i, j] = 255
            flag = True
        elif (imagineSubtiata[i, j - 1] > tMax and not (i,j) in Visited):
            imagineSubtiata[i, j] = 255
            flag = True
        elif(imagineSubtiata[i, j + 1] > tMax and not (i,j) in Visited) :
            imagineSubtiata[i, j] = 255
            flag = True
        elif(imagineSubtiata[i + 1, j - 1] > tMax and not (i,j) in Visited) :
            imagineSubtiata[i, j] = 255
            flag = True
        elif(imagineSubtiata[i + 1, j] > tMax and not (i,j) in Visited) :
            imagineSubtiata[i, j] = 255
            flag = True
        elif(imagineSubtiata[i + 1, j + 1] > tMax and not (i,j) in Visited):
            imagineSubtiata[i, j] = 255
            flag = True
        else:
            imagineSubtiata[i, j] = 0
        if(flag==True):
            if(i+1<imagineSubtiata.shape[0] and j+1<imagineSubtiata.shape[1]):
                Q.put([i + 1, j + 1])
                Q.put([i + 1, j])
                Q.put([i, j + 1])
            if (i + 1 < imagineSubtiata.shape[0] and j - 1 >=0 ):
                Q.put([i + 1, j - 1])
                Q.put([i, j - 1])
            if (i - 1 >=0 and j - 1 >= 0):
                Q.put([i - 1, j])
                Q.put([i - 1, j - 1])
                Q.put([i - 1, j + 1])
            Visited.append((i,j))
    return  imagineSubtiata

def subtiere(gradient,directia):
    conturImage=np.zeros((gradient.shape[0],gradient.shape[1]))
    maskaOrizontala=np.ones(5).reshape((5,1))
    maskaOrizontala=np.ones(5).reshape((1,5))
    maskaDiagonalaDreapta=np.array([[],[],[],[],[]])
    for y in range(gradient.shape[0]-1):
        for x in range (gradient.shape[1]-1):
            #vecinSpate = 255
            #vecinFata = 255
            #orizontal
            if (directia[y,x]==1):
                vecinFata=gradient[y,x-1]
                vecinSpate=gradient[y,x+1]
            #digonala dreapta
            elif(directia[y,x]==2):
                vecinFata=gradient[y+1,x+1]
                vecinSpate=gradient[y-1,x-1]
            #verticala
            elif(directia[y,x]==4):
                vecinFata=gradient[y+1,x]
                vecinSpate=gradient[y-1,x]
            #digonala stanga
            elif(directia[y,x]==3):
                vecinFata=gradient[y-1,x+1]
                vecinSpate=gradient[y+1,x-1]
            if(gradient[y,x]>vecinSpate and gradient[y,x]>vecinFata):
                conturImage[y,x]=gradient[y,x]
            else:
                conturImage[y,x]=0
    return conturImage

def detDirection(degree):
    degree=degree*180/np.pi
    degree[degree<0]+=180
    #numele matricilor este dat de directia pe care se verifica maximul
    #conturul avand defapt directi opusa
    horizontal=np.where(np.logical_or(np.logical_and(0<=degree,degree<22.5),np.logical_and(157.5<=degree,degree<=180.5)),1,0)
    diagonalRight=np.where(np.logical_and(22.5<=degree,degree<67.5),2,0)
    vertical=np.where(np.logical_and(67.5<=degree,degree<112.5),4,0)
    diagonalLeft=np.where(np.logical_and(degree>=112.5,degree<157.5),3,0)
    result=np.add(np.add(np.add(horizontal,diagonalLeft),diagonalRight),vertical)
    print(result.max(),result.min())
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