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
    fx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]],dtype='float')
    fy=np.array([[-1,-2,-1],[0,0,0],[1,2,1]],dtype='float')
    image=ndimage.gaussian_filter(image,1)
    #image = filtruGauss(image, 1)
    #print(fx)
    #print(fy)
    image=np.array(image,dtype='float')
    maskafx=ndimage.filters.convolve(image,fx,mode='constant',cval=0.0)
    maskafy=ndimage.filters.convolve(image,fy, mode='constant', cval=0.0)
    #maskafx=calculMaska(image,fx)
    #maskafy=calculMaska(image,fy)
    gradient=np.hypot(maskafx,maskafy)
    maskafx[maskafx==0]=1
    #maskafy[maskafy==0]=1
    grade=np.arctan2(maskafy,maskafx)
    directia=detDirection2(grade)
    #gradient[gradient < 80] += 20
    #directia*=50
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
def calculMaska(imagine,maska):
    resultat=np.zeros((imagine.shape[0],imagine.shape[1]))
    for y in range(1,imagine.shape[0]-1):
        for x in range(1,imagine.shape[1]-1):
            resultat[y,x]=np.sum(imagine[y-1:y+2,x-1:x+2]*maska)
    return resultat

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


def subtiere(gradient,directia):
    conturImage=np.zeros((gradient.shape[0],gradient.shape[1]))
    maskaOrizontala=np.ones(5).reshape((5,1))
    maskaOrizontala=np.ones(5).reshape((1,5))
    maskaDiagonalaDreapta=np.array([[],[],[],[],[]])
    for y in range(1,gradient.shape[0]-1):
        for x in range (1,gradient.shape[1]-1):
            vecinSpate = 255
            vecinFata = 255
            #orizontal
            if (directia[y,x]==1):
                vecinFata=gradient[y,x-1]
                vecinSpate=gradient[y,x+1]
            #135
            elif(directia[y,x]==2):
                vecinFata=gradient[y+1,x+1]
                vecinSpate=gradient[y-1,x-1]
            #verticala
            elif(directia[y,x]==4):
                vecinFata=gradient[y+1,x]
                vecinSpate=gradient[y-1,x]
            #45
            elif(directia[y,x]==3):
                vecinFata=gradient[y-1,x+1]
                vecinSpate=gradient[y+1,x-1]
            if(gradient[y,x]>=vecinSpate) and (gradient[y,x]>=vecinFata):
                conturImage[y,x]=gradient[y,x]
            else:
                conturImage[y,x]=0
    return conturImage

def subtiereMaska5(gradient,directia):
    conturImage=np.zeros((gradient.shape[0],gradient.shape[1]))
    for y in range(2,gradient.shape[0]-2):
        for x in range (2,gradient.shape[1]-2):
            vecinSpate = 255
            vecinFata = 255
            vecinSpate2 = 255
            vecinFata2 = 255
            #orizontal
            if (directia[y,x]==1):
                vecinFata=gradient[y,x-1]
                vecinFata2=gradient[y,x-2]
                vecinSpate=gradient[y,x+1]
                vecinSpate2=gradient[y,x+2]
            #45
            elif(directia[y,x]==2):
                vecinFata=gradient[y+1,x+1]
                vecinSpate=gradient[y-1,x-1]
                vecinFata2=gradient[y+2,x+2]
                vecinSpate2=gradient[y-2,x-2]
            #verticala
            elif(directia[y,x]==4):
                vecinFata=gradient[y+1,x]
                vecinSpate=gradient[y-1,x]
                vecinFata2=gradient[y+2,x]
                vecinSpate2=gradient[y-2,x]
            #135
            elif(directia[y,x]==3):
                vecinFata=gradient[y-1,x+1]
                vecinSpate=gradient[y+1,x-1]
                vecinFata2=gradient[y-2,x+2]
                vecinSpate2=gradient[y+2,x-2]
            if(gradient[y,x]>vecinSpate and gradient[y,x]>vecinFata and gradient[y,x]>vecinFata2 and gradient[y,x]>vecinSpate2):
                conturImage[y,x]=gradient[y,x]
            else:
                conturImage[y,x]=0
    return conturImage

def detDirection(degree):
    degree=degree*180/np.pi
    degree[degree<0]+=180
    degree=np.round(degree,1)
    #numele matricilor este dat de directia pe care se verifica maximul
    #conturul avand defapt directi opusa
    horizontal=np.where(np.logical_or(np.logical_and(0<=degree,degree<22.5),np.logical_and(157.5<=degree,degree<=180.0)),1,0)
    diagonalRight=np.where(np.logical_and(22.5<=degree,degree<67.5),2,0)
    vertical=np.where(np.logical_and(67.5<=degree,degree<112.5),4,0)
    diagonalLeft=np.where(np.logical_and(degree>=112.5,degree<157.5),3,0)
    result=np.add(np.add(np.add(horizontal,diagonalLeft),diagonalRight),vertical)
    print(result.max(),result.min())
    return result

def detDirection2(degree):
    degree=degree*180/np.pi
    print(np.round(degree,1))
    degree=np.round(degree,1)
    print(degree.max(),degree.min())
    #numele matricilor este dat de directia pe care se verifica maximul
    #conturul avand defapt directi opusa
    horizontal=np.where(np.logical_or(np.logical_and(degree<22.5,degree>=-22.5),np.logical_or(degree<-157.5,degree>=157.5)),1,0)
    diagonal135=np.where(np.logical_or(np.logical_and(degree<-22.5 ,degree>=-67.5),np.logical_and(degree>=112.5,degree<157.5)),3,0)
    vertical=np.where(np.logical_or(np.logical_and(degree<-67.5 , degree>=-112.5),np.logical_and(degree>=67.5 ,degree<112.5)),4,0)
    diagonal45=np.where(np.logical_or(np.logical_and(degree<-112.5 , degree>=-157.5),np.logical_and(degree>=22.5 , degree<67.5)),2,0)
    result=np.add(np.add(np.add(horizontal,diagonal45),diagonal135),vertical)
    print(result.max(),result.min())
    return result

def detDirectieArcTan(degree):
    degree = degree * 180 / np.pi
    horizontal=np.where(np.logical_and(-22.5<=degree,degree<22.5),1,0)
    diagonalRight=np.where(np.logical_and(22.5<=degree,degree<=67.5),2,0)
    vertical=np.where(np.logical_or(np.logical_and(-90.0<=degree,degree<-67.5),np.logical_and(67.5<degree,degree<=90.0)),4,0)
    diagonalLeft=np.where(np.logical_and(-67.5<=degree,degree<=-22.5),3,0)
    result=horizontal+vertical+diagonalLeft+diagonalRight
    print(result.max(), result.min())
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