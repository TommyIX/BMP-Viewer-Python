from struct import unpack
import numpy as np
import threading
import cv2
import os
import math
from collections import deque
import matplotlib.pyplot as plt

def grayplot(graydi):
    plt.hist(graydi.reshape(1,-1))
    plt.show()

if __name__ == "__main__":
    print("BMPViewer Lite(Python Version)\n图像处理课程2020 第一次作业\n王锦宏 19351125")
    filePath = "C:\\Users\\jhong\\Desktop\\testbmp\\4.bmp"
    file = open(filePath, "rb")
    
    #BMP文件信息表
    bfType = unpack("<h", file.read(2))[0]
    bfSize = unpack("<i", file.read(4))[0]
    bfReserved1 = unpack("<h", file.read(2))[0]  #为0
    bfReserved2 = unpack("<h", file.read(2))[0]  #为0 
    bfOffBits = unpack("<i", file.read(4))[0]
    biSize = unpack("<i", file.read(4))[0]
    biWidth = unpack("<i", file.read(4))[0]
    biHeight = unpack("<i", file.read(4))[0]
    biPlanes = unpack("<h", file.read(2))[0]     # 颜色平面数
    biBitCount = unpack("<h", file.read(2))[0]
    biCompression = unpack("<i", file.read(4))[0]
    biSizeImage = unpack("<i", file.read(4))[0]
    biXPelsPerMeter = unpack("<i", file.read(4))[0]
    biYPelsPerMeter = unpack("<i", file.read(4))[0]
    biClrUsed = unpack("<i", file.read(4))[0]
    biClrImportant = unpack("<i", file.read(4))[0]
    bmp_data = []

    if (biBitCount ==24):
        for height in range(biHeight) :
            bmp_data_row = []
            for width in range(biWidth) :
                bmp_data_row.append([unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0]])
            bmp_data.append(bmp_data_row) 
    elif (biBitCount==16):
        for height in range(biHeight) :
            bmp_data_row = []
            count = 0
            for width in range(biWidth) :
                rawtwodata = unpack("<h", file.read(2))[0]
                if(biCompression==0):
                    bmp_data_row.append([((rawtwodata & 0x001f)+1)*8-1,(((rawtwodata & 0x03e0)>>5)+1)*8-1,(((rawtwodata & 0x7c00)>>10)+1)*8-1])
                else:
                    bmp_data_row.append([((rawtwodata&0x001f)>>5)*8+7, ((rawtwodata&0x07e0)>>5)*4+3,((rawtwodata & 0xf800)>>11)*8+7])
                count = count + 3
            bmp_data.append(bmp_data_row)
    elif (biBitCount==8):
        bmp_color_table=[] #B G R A
        for x in range(pow(2,biBitCount)):
            bmp_color_table.append([unpack("<B", file.read(1))[0],unpack("<B", file.read(1))[0],unpack("<B", file.read(1))[0],unpack("<B", file.read(1))[0]])
        for height in range(biHeight) :
            bmp_data_row = []
            for width in range(biWidth) :
                suoyin=unpack("<B", file.read(1))[0]
                bmp_data_row.append([bmp_color_table[suoyin][0],bmp_color_table[suoyin][1],bmp_color_table[suoyin][2]])
            bmp_data.append(bmp_data_row)
    elif (biBitCount==4):
        bmp_color_table=[]
        for x in range(pow(2,biBitCount)):
            bmp_color_table.append([unpack("<B", file.read(1))[0],unpack("<B", file.read(1))[0],unpack("<B", file.read(1))[0],unpack("<B", file.read(1))[0]])
        suoyinempty=1
        for height in range(biHeight) :
            bmp_data_row = []
            for width in range(biWidth) :
                if(suoyinempty==1):
                    suoyin=unpack("<B", file.read(1))[0]
                    suoyinempty=0
                    bmp_data_row.append([bmp_color_table[(suoyin&0xF0)>>4][0],bmp_color_table[(suoyin&0xF0)>>4][1],bmp_color_table[(suoyin&0xF0)>>4][2]])
                else:
                    suoyinempty=1
                    bmp_data_row.append([bmp_color_table[(suoyin&0x0F)>>4][0],bmp_color_table[(suoyin&0x0F)>>4][1],bmp_color_table[(suoyin&0x0F)>>4][2]])
            if(biWidth%8!=0):
                duoyu = math.ceil(biWidth%8/2)
                for x in range(4-duoyu):unpack("<B", file.read(1))[0]
            bmp_data.append(bmp_data_row)
    elif (biBitCount==1): #bug
        bmp_color_table=[]
        initbuffer = deque([])
        for x in range(2):
            bmp_color_table.append([unpack("<B", file.read(1))[0],unpack("<B", file.read(1))[0],unpack("<B", file.read(1))[0],unpack("<B", file.read(1))[0]])
        for height in range(biHeight) :
            bmp_data_row = []
            for width in range(biWidth) :
                if(not initbuffer):
                    tempduru = unpack("<B", file.read(1))[0]
                    initbuffer.append((tempduru&0x80)>>7)
                    initbuffer.append((tempduru&0x40)>>6)
                    initbuffer.append((tempduru&0x20)>>5)
                    initbuffer.append((tempduru&0x10)>>4)
                    initbuffer.append((tempduru&0x08)>>3)
                    initbuffer.append((tempduru&0x04)>>2)
                    initbuffer.append((tempduru&0x02)>>1)
                    initbuffer.append(tempduru&0x01)
                bmp_data_row.append([bmp_color_table[initbuffer[0]][0],bmp_color_table[initbuffer[0]][1],bmp_color_table[initbuffer[0]][2]])
                initbuffer.popleft()
            if(biWidth%32!=0):
                duoyu = math.ceil(biWidth%32/8)
                for x in range(4-duoyu):unpack("<B", file.read(1))[0]
            bmp_data.append(bmp_data_row)

    file.close()
    R=[]
    G=[]
    B=[]
    for row in range(biHeight):
        R_row = []
        G_row = []
        B_row = []
        for col in range(biWidth) :
            B_row.append(bmp_data[row][col][0])
            G_row.append(bmp_data[row][col][1])
            R_row.append(bmp_data[row][col][2])
        B.append(B_row)
        G.append(G_row)
        R.append(R_row)
    b = np.flipud(np.array(B, dtype = np.uint8))
    g = np.flipud(np.array(G, dtype = np.uint8))
    r = np.flipud(np.array(R, dtype = np.uint8))
    graydiation = r*0.3+b*0.11+g*0.59
    print("关闭两个窗口以执行剩余代码")
    threadplt = threading.Thread(target = grayplot, args=(graydiation,))
    threadplt.start()
    cv2.imshow("BMPDisplay-Python", cv2.merge([b,g,r]))
    cv2.waitKey()
    print("如果需要保存文件，请输入目录(需要包含保存的文件名)，如果不需要，直接回车即可结束程序")
    savecatelog=input("目录：")
    if(savecatelog!=""):
        cv2.imwrite(savecatelog,cv2.merge([b,g,r]))
        print("保存成功！")
    os.system("pause")
    exit()