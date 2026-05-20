Lab: dcac-quality-psnr-mse

Topic:
Evaluate stego video quality after hiding data by modifying DC and AC coefficients in DCT domain.

Tasks:

1. Create sample video:
python make_sample_video.py

2. Embed secret message:
python dcac_embed.py

3. Evaluate quality:
python evaluate_quality.py

4. Create answers.txt:
nano answers.txt

Write your conclusion, for example:
PSNR > 30 dB, so the stego video quality is acceptable.
