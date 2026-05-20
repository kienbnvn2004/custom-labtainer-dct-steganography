Lab: ac-position-dct-compare

Topic:
Compare the impact of different AC coefficient positions in an 8x8 DCT block when hiding data into video data.

Tasks:

1. Create sample video data:
python make_sample_video.py

2. Test AC position (1,2):
python run_ac12.py

3. Test AC position (2,1):
python run_ac21.py

4. Test AC position (3,3):
python run_ac33.py

5. Compare all AC positions:
python compare_result.py

6. Check your work:
checkwork

7. Stop the lab:
stoplab
