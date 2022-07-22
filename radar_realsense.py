import time
import socket
import numpy as np
import pandas as pd
import pyrealsense2 as rs

from config import SOCKET_IP, SOCKET_PORT

"""
ラズパイとPC間のSocket通信を行う場合
PC側のファイアーウォール設定を変更する必要がある

ポート指定で外部との通信を許可する設定にする必要がある
ラズパイ側にServerを設ける場合、
Socketの設定でラズパイのIPを指定する必要がある
"""
xyz = []

# -------------------------- Realsenseの設定 --------------------------
print("[*] Realsense Setting...")
pipe = rs.pipeline()

# Build config object and request pose data
cfg = rs.config()
cfg.enable_stream(rs.stream.pose)

# Start streaming with requested config
pipe.start(cfg)
print("[*] Realsense ready")

# -------------------------- Socket通信の設定 --------------------------
print(f"[*] Connecting Socket in {SOCKET_PORT} Port...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SOCKET_IP, SOCKET_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("[*] Connecting done")
filename = s.recv(1024).decode('utf-8')

try:
    for _ in range(100):
        # Wait for the next set of frames from the camera
        frames = pipe.wait_for_frames()

        # Fetch pose frame
        pose = frames.get_pose_frame()
        if pose:
            # Print some of the pose data to the terminal
            data = pose.get_pose_data()
            s.send(bytes("True", 'utf-8'))
            print(data.translation)
            
            xyz.append([data.translation.x,
                        data.translation.y,
                        data.translation.z,])
            time.sleep(0.1)
            # print("Frame #{}".format(pose.frame_number))
            # print("Position: {}".format(data.translation))
            # print("Velocity: {}".format(data.velocity))
            # print("Acceleration: {}\n".format(data.acceleration))

except:
    pass

finally:
    pass

pipe.stop()
xyz = np.array(xyz)
df = pd.DataFrame(xyz)
columns = ["x", "y", "z"]
df.to_csv(f"captured/csv/{filename}.csv", index=False, columns=columns)
s.send(bytes("False", "utf-8"))
s.close()