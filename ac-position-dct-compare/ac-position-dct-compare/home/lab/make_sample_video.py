import json

width = 64
height = 64
frames = 10

video = []

for i in range(frames):
    frame = []
    for y in range(height):
        row = []
        for x in range(width):
            value = (x * 2 + y * 3 + i * 10) % 256
            row.append(float(value))
        frame.append(row)
    video.append(frame)

with open('original_video.json', 'w') as f:
    json.dump(video, f)

print('Created original_video.json')
print('Frames:', frames)
print('Frame size:', width, 'x', height)
