import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import time
import socket
import numpy as np
import pandas as pd

from config import SOCKET_IP, SOCKET_PORT

"""
# !!!!Caution!!!!
ラズパイとPC間のSocket通信を行う場合
PC側のファイアーウォール設定を変更する必要がある

ポート指定で外部との通信を許可する設定にする必要がある
ラズパイ側にServerを設ける場合、
Socketの設定でラズパイのIPを指定する必要がある

# Summary
プログラムの説明
1. 研究室のRaspberry Py4を用意する
2. Raspberry Pyを起動
3. Raspberry PyとPCが同じwifiに接続されていることを確認する
4. config.pyの'SOCKET_IP'と'SOCKET_PORT'が正しいことを確認
5. 

"""

outname = "test"

# -------------------------- WEBカメラの設定 --------------------------
print("[*] Camera Setting...")
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

fps = int(cap.get(cv2.CAP_PROP_FPS))                    
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))             
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))            
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        
video = cv2.VideoWriter(f'./captured/video/{outname}.mp4', fourcc, fps, (w, h)) 


# -------------------------- Socket通信の設定 --------------------------
print(f"[*] Connecting Socket in {SOCKET_PORT} Port...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SOCKET_IP, SOCKET_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("[*] Connecting done")
filename = s.recv(1024).decode('utf-8')

try:
    while True:
        # Wait for the next set of frames from the camera
        _, vid_frame = cap.read()                             
        video.write(vid_frame)   
        s.send(bytes("True", 'utf-8'))
         
except:
    pass

finally:
    pass

s.send(bytes("False", "utf-8"))
s.close()