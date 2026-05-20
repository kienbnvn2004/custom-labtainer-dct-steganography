import json
import math
import os

ORIGINAL_VIDEO = 'original_video.json'
COMPRESSED_VIDEO = 'compressed_stego.json'
SECRET_FILE = 'secret_message.txt'
OUTPUT_FILE = 'extracted_message.txt'
RESULT_DIR = os.path.expanduser('~/.local/result')
RESULT_FILE = os.path.join(RESULT_DIR, 'recovery_result.txt')

N = 8
DC_POS = (0, 0)
AC_POS = (1, 2)

def dct_2d(block):
    result = [[0.0 for _ in range(N)] for _ in range(N)]
    for u in range(N):
        for v in range(N):
            total = 0.0
            for x in range(N):
                for y in range(N):
                    total += block[x][y] * math.cos(((2*x+1)*u*math.pi)/(2*N)) * math.cos(((2*y+1)*v*math.pi)/(2*N))
            cu = 1 / math.sqrt(2) if u == 0 else 1
            cv = 1 / math.sqrt(2) if v == 0 else 1
            result[u][v] = 0.25 * cu * cv * total
    return result

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = ''.join(bits[i:i+8])
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

if not os.path.exists(COMPRESSED_VIDEO):
    print('Missing compressed_stego.json. Please run python compress_stego.py first.')
    exit(1)

with open(ORIGINAL_VIDEO, 'r') as f:
    original = json.load(f)

with open(COMPRESSED_VIDEO, 'r') as f:
    compressed = json.load(f)

with open(SECRET_FILE, 'r') as f:
    secret = f.read().strip()

expected_bits = len(secret) * 8
bits = []

for frame_index in range(len(original)):
    frame_o = original[frame_index]
    frame_c = compressed[frame_index]
    height = len(frame_o)
    width = len(frame_o[0])

    for row in range(0, height - 8 + 1, 8):
        for col in range(0, width - 8 + 1, 8):
            if len(bits) >= expected_bits:
                break

            block_o = []
            block_c = []

            for i in range(8):
                row_o = []
                row_c = []
                for j in range(8):
                    row_o.append(frame_o[row+i][col+j])
                    row_c.append(frame_c[row+i][col+j])
                block_o.append(row_o)
                block_c.append(row_c)

            dct_o = dct_2d(block_o)
            dct_c = dct_2d(block_c)

            dc_diff = dct_c[DC_POS[0]][DC_POS[1]] - dct_o[DC_POS[0]][DC_POS[1]]
            ac_diff = dct_c[AC_POS[0]][AC_POS[1]] - dct_o[AC_POS[0]][AC_POS[1]]

            score = dc_diff + ac_diff

            if score >= 0:
                bits.append('1')
            else:
                bits.append('0')

        if len(bits) >= expected_bits:
            break

    if len(bits) >= expected_bits:
        break

message = bits_to_text(bits)

with open(OUTPUT_FILE, 'w') as f:
    f.write(message + '\n')

same = 0
for i in range(min(len(secret), len(message))):
    if secret[i] == message[i]:
        same += 1

total = max(len(secret), len(message))
accuracy = same * 100.0 / total

if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)

with open(RESULT_FILE, 'w') as f:
    f.write('RECOVERED_MESSAGE={}\n'.format(message))
    f.write('ORIGINAL_MESSAGE={}\n'.format(secret))
    f.write('RECOVERY_ACCURACY={:.2f}%\n'.format(accuracy))

print('Recovered message:', message)
print('Original message:', secret)
print('Recovery accuracy: {:.2f}%'.format(accuracy))
print('Result saved to', RESULT_FILE)
