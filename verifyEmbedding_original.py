import os
import imageio.v2 as imageio
import math

IMAGE_PATH = "image_lsbr_gs_original/yagate_gs_30.png"
BIT_SEQUENCE_PATH = "bit_sequence_payload-30.txt"
SCRIPT_PATH = os.path.dirname (__file__)

# greyscale image
stego = imageio.imread(f"{SCRIPT_PATH}/results/{IMAGE_PATH}")
if (len(stego.shape) > 2) :
    print("Not greyscale provided!")
    exit()

height = stego.shape[0]
width = stego.shape[1]
numPixels = height * width

with open(SCRIPT_PATH + f'\\random bit sequences\\{BIT_SEQUENCE_PATH}' , 'r') as file:
    bit_sequence = file.read().strip()

dim = int(math.sqrt (len (bit_sequence)))
ptr = 0 

for i in range (1, dim + 1) :
    for j in range (1, dim + 1) :

        if (stego[i][j] % 2) != int(bit_sequence[ptr]) :
            print ("Embedding Failed!")
            exit() 
        
        ptr += 1

print ("Embedding Success!")



