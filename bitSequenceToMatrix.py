def convert_to_matrix(bit_sequence, n):
    """Converts a bit sequence to an n by n matrix."""

    numBitsPerPixel = len(bit_sequence) // (n**2)

    # Convert each bit from string to int and group them into tuples of size n

    matrix = []

    ptr = 0 

    for i in range (n) :
        
        matrix.append([])

        for j in range (n) :
            matrix[i].append ( tuple (int(bit) for bit in bit_sequence[ptr : ptr + numBitsPerPixel])
                )
            ptr += numBitsPerPixel


    return matrix

