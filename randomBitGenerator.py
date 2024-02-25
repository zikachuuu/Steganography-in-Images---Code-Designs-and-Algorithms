import random
import os

CURRENTPATH = os.path.dirname(os.path.abspath(__file__))

NUM_PIXEL = 64 * 64

# payLoad from 0 to 0.3, in increment of 0.01
for payload in range (31) :

    numBits = int(NUM_PIXEL * payload * 0.01)

    # Generate a sequence of 100 random bits
    bit_sequence = ''.join(str(random.randint(0, 1)) for _ in range(numBits))

    # Specify the filename where you want to save the bit sequence
    filename = f'bit_sequence_payload-{payload}.txt'

    # Open the file in write mode and write the bit sequence
    with open(CURRENTPATH + "/random bit sequences/" + filename, 'w') as file:
        file.write(bit_sequence)

    print(f"sequence has been saved to {filename}.")