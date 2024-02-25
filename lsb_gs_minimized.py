from gbSolver2 import GB_Solver2
import os
import imageio.v2 as imageio
import math
from writeEmbeddingResultToCSV import writeEmbeddingResultToCSV
import time
import random

IMAGE_NAME      = "yagate_gs.png"
SCRIPT_PATH     = os.path.dirname (__file__)
TECHNIQUE       = 0         # 0 for LSB Replacement, 1 for LSB Matching
WRITE_TO_CSV    = True      # True to write emedding result to csv, False otherwise
START_PAYLOAD   = 0         # inclusive
END_PAYLOAD     = 6         # exclusive

'''
0 XOR 0 = 0
0 XOR 1 = 1
1 XOR 0 = 1
1 XOR 1 = 0
XOR = 1 if 2 arguments different, 0 if same
'''

# greyscale image
cover = imageio.imread(f"{SCRIPT_PATH}/results/image_cover/{IMAGE_NAME}")
if (len(cover.shape) > 2) :
    print("Not greyscale provided!")
    exit()

height = cover.shape[0]
width = cover.shape[1]
numPixels = height * width

# payLoad from 0 to 0.3, in increment of 0.01
for payload in range (START_PAYLOAD , END_PAYLOAD) :

    startTime = time.time()

    with open(SCRIPT_PATH + f'\\random bit sequences\\bit_sequence_payload-{payload}.txt' , 'r') as file:
        bit_sequence = file.read().strip()

    dim = int(math.sqrt (len (bit_sequence)))
    
    bit_sequence_list = [int(char) for char in bit_sequence]
    bit_sequence_matrix = [bit_sequence_list[i*dim : (i + 1)*dim] for i in range(dim)]

    originalBitChanges = 0 

    for i in range (1, dim + 1) :
        for j in range (1 , dim + 1) :
            originalBitChanges += 1 if bit_sequence_matrix[i-1][j-1] != (cover[i][j] % 2) else 0    # count the bit changes required if using original image
            bit_sequence_matrix[i-1][j-1] = bit_sequence_matrix[i-1][j-1] ^ (cover[i][j] % 2)       # XOR the bit in bit_sequence matrix and lsb of image

    columnSwitch = [(cover[0][j] % 2) for j in range (1, dim + 1)]
    rowSwitch = [(cover[i][0] % 2) for i in range (1 , dim + 1)]
    
    optimizedMatrix, optimizedBitOneCount = GB_Solver2 (bit_sequence_matrix , columnSwitch, rowSwitch, dim)

    endTime = time.time()


    stego = cover.copy()
    optimizedBitChange = 0

    for i in range (dim + 1) :
        for j in range (dim + 1) :

            if optimizedMatrix[i][j] == 1 : # check if LSB of stego[i][j] == bit 
                optimizedBitChange += 1
                match (TECHNIQUE) :
                    case 0 :
                        stego[i][j] = stego[i][j] ^ 1 # reverse the parity of LSB

                    case 1 :
                        if (stego[i][j] == 255) :
                            s = -1
                        elif (stego[i][j] == 0) :

                            s = 1 
                        else :
                            s = random.choice ([-1 , +1])
                        stego[i][j] += s # randomly add or subtract 1 so that lsb of stego[i][j] == bit

        
    imageio.imwrite (f"{SCRIPT_PATH}/results/image_{'lsbr' if TECHNIQUE == 0 else 'lsbm'}_gs_minimized/{IMAGE_NAME[:-4]}_{payload}.png" , stego)

    if WRITE_TO_CSV :
        writeEmbeddingResultToCSV (IMAGE_NAME, f"bit_sequence_payload-{payload}.txt", payload, len(bit_sequence), originalBitChanges, optimizedBitChange, endTime - startTime)

    print(f"Optimized {originalBitChanges} - {optimizedBitChange} = {originalBitChanges - optimizedBitChange} bits")
