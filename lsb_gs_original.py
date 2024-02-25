import os
import imageio.v2 as imageio
import math
import random

IMAGE_NAME      = "yagate_gs.png"
SCRIPT_PATH     = os.path.dirname (__file__)
TECHNIQUE       = 0         # 0 for LSB Replacement, 1 for LSB Matching
START_PAYLOAD   = 0         # inclusive
END_PAYLOAD     = 31        # exclusive

# greyscale image
cover = imageio.imread(f"{SCRIPT_PATH}/results/image_cover/{IMAGE_NAME}")
if (len(cover.shape) > 2) :
    print("Not greyscale provided!")
    exit()

height = cover.shape[0]
width = cover.shape[1]
numPixels = height * width

# payLoad from 0 to 0.3, in increment of 0.01
for payload in range (START_PAYLOAD, END_PAYLOAD) :

    with open(SCRIPT_PATH + f'\\random bit sequences\\bit_sequence_payload-{payload}.txt' , 'r') as file:
        bit_sequence = file.read().strip()
    
    dim = int(math.sqrt (len (bit_sequence)))

    stego = cover.copy()

    ptr = 0
    for i in range (1, dim + 1) :
        for j in range (1, dim + 1) :

            if (stego[i][j] % 2) != int(bit_sequence[ptr]) : 
                match (TECHNIQUE) :
                    case 0 : # LSBR
                        stego[i][j] = (stego[i][j] & ~1) | int (bit_sequence[ptr]) # clear lsb of stego[i][j] then set to bit


                    case 1 : #LSBM
                        if (stego[i][j] == 255) :
                            s = -1
                        elif (stego[i][j] == 0) :
                            s = 1 
                        else :
                            s = random.choice ([-1 , +1])
                        stego[i][j] += s # randomly add or subtract 1 so that lsb of stego[i][j] == bit
 
            ptr += 1
                        
    imageio.imwrite (f"{SCRIPT_PATH}/results/image_{'lsbr' if TECHNIQUE == 0 else 'lsbm'}_gs_original/{IMAGE_NAME[:-4]}_{payload}.png" , stego)

print("Output success!")






    
    

