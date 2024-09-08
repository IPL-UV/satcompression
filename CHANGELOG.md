# **Changelog**

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## **[Unreleased]**

### **Added**
- Improved efficiency of Quad-Tree compression for larger satellite images.
- Support for advanced pseudo-MTF calculations based on image compression levels.
- Enhanced classification map generation for compressed images.

### **Changed**
- Optimized image reconstruction speed after decompression.
- Updated documentation with more detailed examples and improved clarity.

### **Fixed**
- Fixed issue where memory usage spiked during large image decompression.
- Resolved bug causing incorrect detail error thresholds in the compression algorithm.

## **[0.0.3] - 2024-07-13**

### **Added**
- Added new API for creating classification maps based on Quad-Tree compression.
- Fine-tuning options for adjusting the detail error threshold in image compression.

### **Changed**
- Improved performance of pseudo-MTF calculations for compressed images.

## **[0.0.2] - 2024-07-12**

### **Added**
- Introduced support for multi-channel satellite images in compression and reconstruction processes.
- Enhanced image compression using a customizable Quad-Tree structure.

### **Fixed**
- Fixed memory leak issue when processing large satellite images during compression.

## **[0.0.1] - 2024-07-12**

### **Added**
- Initial release of **satcompression** with basic Quad-Tree compression and decompression functionality for satellite images.
- Support for encoding and decoding image data using the Quad-Tree structure.
