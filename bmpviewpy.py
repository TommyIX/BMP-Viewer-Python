from struct import unpack
import numpy as np
import cv2
#import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("BMPViewer Lite(Python Version) 王锦宏 19351125")
    filePath = "C:\\Users\\jhong\\Desktop\\testbmp\\default\\head.bmp"
    file = open(filePath, "rb")
    
    #BMP文件信息表
    bfType = unpack("<h", file.read(2))[0]       # BM
    bfSize = unpack("<i", file.read(4))[0]       # 位图文件大小
    bfReserved1 = unpack("<h", file.read(2))[0]  # 保留字段 必须设为 0 
    bfReserved2 = unpack("<h", file.read(2))[0]  # 保留字段 必须设为 0 
    bfOffBits = unpack("<i", file.read(4))[0]    # 偏移量
    biSize = unpack("<i", file.read(4))[0]       # 所需要的字节数
    biWidth = unpack("<i", file.read(4))[0]
    biHeight = unpack("<i", file.read(4))[0]
    biPlanes = unpack("<h", file.read(2))[0]     # 颜色平面数
    biBitCount = unpack("<h", file.read(2))[0]   # 比特数 
    biCompression = unpack("<i", file.read(4))[0]  # 图像压缩率
    biSizeImage = unpack("<i", file.read(4))[0]    # 图像大小
    biXPelsPerMeter = unpack("<i", file.read(4))[0]# 水平分辨率
    biYPelsPerMeter = unpack("<i", file.read(4))[0]# 垂直分辨率
    biClrUsed = unpack("<i", file.read(4))[0]      # 实际使用的彩色表中的颜色索引数
    biClrImportant = unpack("<i", file.read(4))[0] # 对图像显示有重要影响的颜色索引的数目
    bmp_data = []

    
    
    if (biBitCount ==24):
        for height in range(biHeight) :
            bmp_data_row = []
            count = 0
            for width in range(biWidth) :
                bmp_data_row.append([unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0]])
                count = count + 3
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
        
        #graydiation = np.zeros((256,dtype = np.int))
        #for x in np.nditer(b):
        cv2.imshow("BMPDisplay-Python", cv2.merge([b,g,r]))
        cv2.waitKey()
        
    #elif (biBitCount==16):
