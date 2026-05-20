import json
import os

INPUT_FILE = 'stego_video.json'
OUTPUT_FILE = 'compressed_stego.json'
RESULT_DIR = os.path.expanduser('~/.local/result')
RESULT_FILE = os.path.join(RESULT_DIR, 'compression_result.txt')

QUANT_STEP = 2.0

if not os.path.exists(INPUT_FILE):
    print('Missing stego_video.json. Please run python embed_dcac.py first.')
    exit(1)

with open(INPUT_FILE, 'r') as f:
    video = json.load(f)

for frame in video:
    for y in range(len(frame)):
        for x in range(len(frame[0])):
            value = frame[y][x]
            compressed = round(value / QUANT_STEP) * QUANT_STEP
            frame[y][x] = compressed

with open(OUTPUT_FILE, 'w') as f:
    json.dump(video, f)

if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)

with open(RESULT_FILE, 'w') as f:
    f.write('COMPRESSED=YES\n')
    f.write('QUANT_STEP={}\n'.format(QUANT_STEP))

print('Compression simulation completed.')
print('Output file:', OUTPUT_FILE)
