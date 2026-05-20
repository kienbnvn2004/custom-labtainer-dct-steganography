# Custom Labtainer Labs - Video Steganography DCT

This repository contains custom Labtainer labs about video steganography in the DCT domain.

## Labs

1. `dcac-quality-psnr-mse`  
   Evaluate stego video quality using MSE and PSNR after hiding data in DC/AC coefficients.

2. `ac-position-dct-compare`  
   Compare the impact of different AC coefficient positions in an 8x8 DCT block.

3. `dcac-compression-robustness`  
   Evaluate the ability to recover hidden data from DC/AC coefficients after compression simulation.

## How to install

Copy the lab folders into your Labtainer labs directory:

```bash
cp -r dcac-quality-psnr-mse ~/labtainer/trunk/labs/
cp -r ac-position-dct-compare ~/labtainer/trunk/labs/
cp -r dcac-compression-robustness ~/labtainer/trunk/labs/
