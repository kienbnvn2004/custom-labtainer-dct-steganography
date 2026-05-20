import json
import math
import os

N = 8
RESULT_DIR = os.path.expanduser('~/.local/result')

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

def copy_video(video):
    copied = []
    for frame in video:
        new_frame = []
        for row in frame:
            new_frame.append(list(row))
        copied.append(new_frame)
    return copied

def embed_with_ac_position(video, bits, ac_u, ac_v):
    stego = copy_video(video)
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
                    dct_block[ac_u][ac_v] += 1.0
                else:
                    dct_block[ac_u][ac_v] -= 1.0

                restored = idct_2d(dct_block)

                for i in range(8):
                    for j in range(8):
                        frame[row+i][col+j] = clip(restored[i][j])

                bit_index += 1

            if bit_index >= len(bits):
                break

        if bit_index >= len(bits):
            break

    return stego, bit_index

def calculate_mse_psnr(original, stego):
    total_error = 0.0
    total_pixels = 0

    for f in range(len(original)):
        frame1 = original[f]
        frame2 = stego[f]
        for y in range(len(frame1)):
            for x in range(len(frame1[0])):
                diff = frame1[y][x] - frame2[y][x]
                total_error += diff * diff
                total_pixels += 1

    mse = total_error / total_pixels

    if mse == 0:
        psnr = 99.0
    else:
        psnr = 10 * math.log10((255 * 255) / mse)

    return mse, psnr

def run_one_position(ac_u, ac_v, result_name):
    if not os.path.exists('original_video.json'):
        print('Missing original_video.json. Please run python make_sample_video.py first.')
        exit(1)

    with open('original_video.json', 'r') as f:
        original_video = json.load(f)

    with open('secret_message.txt', 'r') as f:
        secret = f.read().strip()

    bits = text_to_bits(secret)

    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)

    stego, hidden_bits = embed_with_ac_position(original_video, bits, ac_u, ac_v)
    mse, psnr = calculate_mse_psnr(original_video, stego)

    stego_file = 'stego_ac{}{}.json'.format(ac_u, ac_v)
    with open(stego_file, 'w') as f:
        json.dump(stego, f)

    result_file = os.path.join(RESULT_DIR, result_name)

    with open(result_file, 'w') as f:
        f.write('AC_POSITION=({},{})\n'.format(ac_u, ac_v))
        f.write('HIDDEN_BITS={}\n'.format(hidden_bits))
        f.write('MSE={:.4f}\n'.format(mse))
        f.write('PSNR={:.4f}\n'.format(psnr))

    print('AC({},{}) completed.'.format(ac_u, ac_v))
    print('MSE={:.4f}'.format(mse))
    print('PSNR={:.4f}'.format(psnr))
    print('Result saved to', result_file)
