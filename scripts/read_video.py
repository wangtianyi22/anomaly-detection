import torch
import cv2
from skimage.transform import resize
import numpy as np

def get_tensor(arr, segment_length):
	blocc = np.array([cv2.resize(frame, (112, 112), interpolation = cv2.INTER_AREA) for frame in arr])
	#blocc = blocc[:, :, 44:44+112, :]
	blocc = blocc.transpose(3, 0, 1, 2)  # ch, fr, h, w
	#blocc = np.expand_dims(blocc, axis=0)  # batch axis
	blocc = np.array(np.split(blocc, segment_length, axis=1))
	#blocc = (blocc-blocc.mean())/(blocc.max()-blocc.mean())
	blocc = np.float32(blocc)
	blocc = torch.from_numpy(blocc)
	return blocc

def generate_block(video, segment_length):
	cap = cv2.VideoCapture(video)
	# Check if camera opened successfully
	i = 0
	arr = []
	frame_counter = 0
	while(cap.isOpened()):
		# Capture frame-by-frame
		ret, frame = cap.read()
		#print(frame)
		if (ret == True):
			if(i<16*segment_length):
				arr.append(frame)
				i+=1
				frame_counter +=1
			else:
				i = 0
				arr = []

			if(len(arr) == (16*segment_length)):
				X = get_tensor(arr, segment_length)
				yield X

	cap.release()
if __name__ == '__main__':
	generate_block('/home/nevin/nevin/datasets/anomaly detection/arson/Arson016_x264.mp4', 3)