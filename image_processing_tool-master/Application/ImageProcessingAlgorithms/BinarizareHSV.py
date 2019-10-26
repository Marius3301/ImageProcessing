from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog
import numpy as np
import cv2

@RegisterAlgorithm("Binarizare HSV", "Tema2",fromMainModel=["rightClickLastPositions"])
@InputDialog(threshold=float,lightThreshold=int)
#@OutputDialog(title="Binarization Output")

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
            if c[line,col]==0:
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

def hsv_to_rgb(h,s,v):
    c=v*s
    h=h/60.0
    x=c*(1-np.abs(h % 2-1))
    m=v-c
    r=v
    g=v
    b=v
    for line in range(0,m.shape[0]):
        for col in range(0,m.shape[1]):
            if np.isnan(h[line,col]):
                r[line,col]=0
                g[line,col]=0
                b[line,col]=0
            elif h[line,col]>=0 and h[line,col]<1:
                r[line,col]=c[line,col]
                g[line,col]=x[line,col]
                b[line,col]=0
            elif h[line,col]>=1 and h[line,col]<2:
                r[line,col]=x[line,col]
                g[line,col]=c[line,col]
                b[line,col]=0
            elif h[line, col] >= 2 and h[line, col] < 3:
                r[line, col] = 0
                g[line, col] = c[line, col]
                b[line, col] = x[line,col]
            elif h[line,col]>=3 and h[line,col]<4:
                r[line,col]=0
                g[line,col]=x[line,col]
                b[line,col]=c[line,col]
            elif h[line,col]>=4 and h[line,col]<5:
                r[line,col]=x[line,col]
                g[line,col]=0
                b[line,col]=c[line,col]
            elif h[line,col]>=5 and h[line,col]<6:
                r[line,col]=c[line,col]
                g[line,col]=0
                b[line,col]=x[line,col]
    r+=m
    g+=m
    b+=m
    R=r*255
    G=g*255
    B=b*255
    print(np.dstack((r,g,b)))
    return np.dstack((R,G,B))


