import csv
import os

SCRIPT_PATH = os.path.dirname (__file__)
FILE_NAME = SCRIPT_PATH + '/results/EmbeddingResult.csv'

# Data to append
header = ['ImageFile', 'BitSequenceFile', 'Payload', 'BitSequenceLength', 'OriginalBitChange', 'OptimizedBitChange', 'OptimizedNum', 'TimeTaken']

# Function to check if file is empty
def is_file_empty(file_name):
    """Check if file is empty by reading its size."""
    # Check if file exists and its size is 0
    return os.path.exists(file_name) and os.path.getsize(file_name) == 0


def writeEmbeddingResultToCSV (imageFile, bitSequenceFile, payload, bitSequenceLength, originalBitChange, optimizedBitChange, timeTaken) :
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header if file is new or empty
        if is_file_empty(FILE_NAME):
            writer.writerow(header)

        # Write data rows
        writer.writerow ([imageFile, bitSequenceFile, payload, bitSequenceLength, originalBitChange, optimizedBitChange, originalBitChange - optimizedBitChange, timeTaken])

