import os

RESULT_DIR = os.path.expanduser('~/.local/result')

items = [
    ('AC(1,2)', 'ac12_result.txt'),
    ('AC(2,1)', 'ac21_result.txt'),
    ('AC(3,3)', 'ac33_result.txt')
]

summary = []
best_name = None
best_psnr = -1.0

for name, filename in items:
    path = os.path.join(RESULT_DIR, filename)

    if not os.path.exists(path):
        print('Missing', path)
        print('Please run all AC position scripts first.')
        exit(1)

    mse = None
    psnr = None

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('MSE='):
                mse = float(line.split('=')[1])
            if line.startswith('PSNR='):
                psnr = float(line.split('=')[1])

    summary.append((name, mse, psnr))

    if psnr > best_psnr:
        best_psnr = psnr
        best_name = name

compare_path = os.path.join(RESULT_DIR, 'compare_result.txt')

with open(compare_path, 'w') as f:
    f.write('AC_POSITION_COMPARISON\n')
    for name, mse, psnr in summary:
        f.write('{} MSE={:.4f} PSNR={:.4f}\n'.format(name, mse, psnr))
    f.write('BEST_POSITION={}\n'.format(best_name))

print('Comparison completed.')
print('Best position:', best_name)
print('Result saved to', compare_path)
