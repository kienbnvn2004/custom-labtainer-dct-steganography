Lab: dcac-compression-robustness

Topic:
Evaluate the ability to recover hidden data from DC/AC coefficients after compression simulation.

Tasks:

1. Create sample video data:
python make_sample_video.py

2. Embed hidden message into DC/AC coefficients:
python embed_dcac.py

3. Simulate compression:
python compress_stego.py

4. Recover hidden message after compression:
python recover_after_compression.py

5. View result files:
ls ~/.local/result
cat ~/.local/result/embed_result.txt
cat ~/.local/result/compression_result.txt
cat ~/.local/result/recovery_result.txt

6. Check your work:
checkwork

7. Stop the lab:
stoplab
