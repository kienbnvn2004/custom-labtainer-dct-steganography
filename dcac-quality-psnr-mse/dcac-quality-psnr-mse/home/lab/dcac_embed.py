import json
import math
import os

INPUT_VIDEO = 'original_video.json'
OUTPUT_VIDEO = 'stego_video.json'
SECRET_FILE = 'secret_message.txt'

N = 8

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

def text_to_bits(text):
    bits = []
    for char in text:
        binary = format(ord(char), '08b')
        for b in binary:
            bits.append(int(b))
    return bits

def clip(value):
    if value < 0:
        return 0.0
    if value > 255:
        return 255.0
    return value

if not os.path.exists(INPUT_VIDEO):
    print('original_video.json not found. Creating sample video first...')
    import make_sample_video

with open(SECRET_FILE, 'r') as f:
    secret = f.read().strip()

bits = text_to_bits(secret)

with open(INPUT_VIDEO, 'r') as f:
    video = json.load(f)

stego = video
bit_index = 0

for frame_index in range(len(stego)):
    frame = stego[frame_index]
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
                dct_block[0][0] += 1.0
                dct_block[1][2] += 0.5
            else:
                dct_block[0][0] -= 1.0
                dct_block[1][2] -= 0.5

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
    json.dump(stego, f)

print('Embedding completed.')
print('Hidden bits:', bit_index)
print('Output file:', OUTPUT_VIDEO)
