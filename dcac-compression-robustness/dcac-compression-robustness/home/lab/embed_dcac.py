import json
import math
import os

INPUT_VIDEO = 'original_video.json'
OUTPUT_VIDEO = 'stego_video.json'
SECRET_FILE = 'secret_message.txt'
RESULT_DIR = os.path.expanduser('~/.local/result')
RESULT_FILE = os.path.join(RESULT_DIR, 'embed_result.txt')

N = 8
DC_POS = (0, 0)
AC_POS = (1, 2)
STRENGTH = 8.0

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

def idct_2d(block):
    result = [[0.0 for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            total = 0.0
            for u in range(N):
                for v in range(N):
                    cu = 1 / math.sqrt(2) if u == 0 else 1
                    cv = 1 / math.sqrt(2) if v == 0 else 1
                    total += cu * cv * block[u][v] * math.cos(((2*x+1)*u*math.pi)/(2*N)) * math.cos(((2*y+1)*v*math.pi)/(2*N))
            result[x][y] = 0.25 * total
    return result

def clip(value):
    if value < 0:
        return 0.0
    if value > 255:
        return 255.0
    return value

def text_to_bits(text):
    bits = []
    for ch in text:
        binary = format(ord(ch), '08b')
        for b in binary:
            bits.append(int(b))
    return bits

if not os.path.exists(INPUT_VIDEO):
    import make_sample_video

with open(INPUT_VIDEO, 'r') as f:
    video = json.load(f)

with open(SECRET_FILE, 'r') as f:
    secret = f.read().strip()

bits = text_to_bits(secret)
bit_index = 0

for frame in video:
    height = len(frame)
    width = len(frame[0])

    for row in range(0, height - 8 + 1, 8):
        for col in range(0, width - 8 + 1, 8):
            if bit_index >= len(bits):
                break

            block = []
            for i in range(8):
                block_row = []
                for j in range(8):
                    block_row.append(frame[row+i][col+j])
                block.append(block_row)

            dct_block = dct_2d(block)
            bit = bits[bit_index]

            if bit == 1:
                dct_block[DC_POS[0]][DC_POS[1]] += STRENGTH
                dct_block[AC_POS[0]][AC_POS[1]] += STRENGTH
            else:
                dct_block[DC_POS[0]][DC_POS[1]] -= STRENGTH
                dct_block[AC_POS[0]][AC_POS[1]] -= STRENGTH

            restored = idct_2d(dct_block)

            for i in range(8):
                for j in range(8):
                    frame[row+i][col+j] = clip(restored[i][j])

            bit_index += 1

        if bit_index >= len(bits):
            break

    if bit_index >= len(bits):
        break

with open(OUTPUT_VIDEO, 'w') as f:
    json.dump(video, f)

if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)

with open(RESULT_FILE, 'w') as f:
    f.write('EMBEDDED_BITS={}\n'.format(bit_index))
    f.write('DC_POSITION=(0,0)\n')
    f.write('AC_POSITION=(1,2)\n')

print('Embedding completed.')
print('Embedded bits:', bit_index)
print('Output file:', OUTPUT_VIDEO)
