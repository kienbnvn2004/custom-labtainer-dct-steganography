import json
import math
import os

ORIGINAL_VIDEO = 'original_video.json'
STEGO_VIDEO = 'stego_video.json'
RESULT_FILE = 'quality_result.txt'
LAB_RESULT_DIR = os.path.expanduser('~/.local/result')
LAB_RESULT_FILE = os.path.join(LAB_RESULT_DIR, 'quality_result.txt')

if not os.path.exists(ORIGINAL_VIDEO):
    print('Missing original_video.json')
    exit(1)

if not os.path.exists(STEGO_VIDEO):
    print('Missing stego_video.json. Please run python dcac_embed.py first.')
    exit(1)

with open(ORIGINAL_VIDEO, 'r') as f:
    original = json.load(f)

with open(STEGO_VIDEO, 'r') as f:
    stego = json.load(f)

total_error = 0.0
total_pixels = 0

for frame_index in range(len(original)):
    frame1 = original[frame_index]
    frame2 = stego[frame_index]

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

result_text = ''
result_text += 'MSE={:.4f}\n'.format(mse)
result_text += 'PSNR={:.4f}\n'.format(psnr)
result_text += 'CONCLUSION=PSNR higher than 30 dB usually indicates acceptable visual quality.\n'

with open(RESULT_FILE, 'w') as f:
    f.write(result_text)

if not os.path.exists(LAB_RESULT_DIR):
    os.makedirs(LAB_RESULT_DIR)

with open(LAB_RESULT_FILE, 'w') as f:
    f.write(result_text)

print('MSE={:.4f}'.format(mse))
print('PSNR={:.4f}'.format(psnr))
print('Result saved to', RESULT_FILE)
print('Labtainer result saved to', LAB_RESULT_FILE)
