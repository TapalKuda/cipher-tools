def vigenere_cipher(text, key, mode='encrypt'):
    key = key.upper()
    text = text.upper()
    key_len = len(key)
    result = []
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_len]) - ord('A')
            if mode == 'decrypt':
                shift = -shift
            new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result.append(new_char)
        else:
            result.append(char)
    return ''.join(result)

def prepare_playfair_text(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        
        if a == b:
            pairs.append(a + 'X')
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    
    return pairs

def playfair_pair(pair, matrix, mode='encrypt'):
    pos_a = find_position(matrix, pair[0])
    pos_b = find_position(matrix, pair[1])
    
    if pos_a is None or pos_b is None:
        raise ValueError("Character not found in matrix.")
    
    row_a, col_a = pos_a
    row_b, col_b = pos_b
    
    if row_a == row_b:  
        return (matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]) if mode == 'encrypt' else (matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5])
    elif col_a == col_b:  
        return (matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]) if mode == 'encrypt' else (matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b])
    else:  # Rectangle
        return matrix[row_a][col_b] + matrix[row_b][col_a]

def find_position(matrix, char):
    for row in range(5):
        if char in matrix[row]:
            return row, matrix[row].index(char)
    return None

def playfair_cipher(text, key, mode='encrypt'):
    key_matrix = create_playfair_matrix(key)
    pairs = prepare_playfair_text(text)
    result = []
    for pair in pairs:
        result.append(playfair_pair(pair, key_matrix, mode))
    return ''.join(result)

def create_playfair_matrix(key):
    key = ''.join(sorted(set(key.upper()), key=key.index))
    matrix = []
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in key:
        if char in alphabet:
            matrix.append(char)
            alphabet = alphabet.replace(char, "")
    matrix.extend(list(alphabet))
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def hill_cipher(text, key_matrix, mode='encrypt'):
    text = text.upper().replace(" ", "")
    n = len(key_matrix)
    padded_text = text + 'X' * ((n - len(text) % n) % n)
    result = []
    
    if mode == 'decrypt':
        key_matrix = invert_matrix(key_matrix)
    
    for i in range(0, len(padded_text), n):
        block = [ord(char) - ord('A') for char in padded_text[i:i+n]]
        new_block = matrix_mult(key_matrix, block)
        result.extend([chr(val % 26 + ord('A')) for val in new_block])
    return ''.join(result)

def matrix_mult(matrix, vector):
    return [(sum(matrix[i][j] * vector[j] for j in range(len(vector))) % 26) for i in range(len(matrix))]

def invert_matrix(matrix):
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det_inv = pow(det, -1, 26)
    
    inv_matrix = [[(matrix[1][1] * det_inv) % 26, (-matrix[0][1] * det_inv) % 26],
                  [(-matrix[1][0] * det_inv) % 26, (matrix[0][0] * det_inv) % 26]]
    
    return inv_matrix