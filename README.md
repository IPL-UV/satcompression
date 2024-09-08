# 



<p align="center">
  <img src="https://huggingface.co/datasets/JulioContrerasH/DataMLSTAC/resolve/main/banner_satcompression.png" width="40%">
</p>

<p align="center">
    <em>A Python package for efficient decomposition of satellite images in a Quad-Tree structure</em> 🚀
</p>

<p align="center">
<a href='https://pypi.python.org/pypi/satcompression'>
    <img src='https://img.shields.io/pypi/v/satcompression.svg' alt='PyPI' />
</a>
<a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
</a>
<a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
</a>
<a href="https://pycqa.github.io/isort/" target="_blank">
    <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="isort">
</a>
</p>

---

**GitHub**: [https://github.com/IPL-UV/satcompression](https://github.com/IPL-UV/satcompression) 🌐

**PyPI**: [https://pypi.org/project/satcompression/](https://pypi.org/project/satcompression/) 🛠️

---

## **Overview** 📊

**satcompression** is a Python package designed for efficient compression and decompression of satellite images using a Quad-Tree structure. The package provides a structured way to partition satellite images into hierarchical blocks, enabling efficient image storage, analysis, and pseudo-MTF (Modulation Transfer Function) calculations based on the compression.

## **Key features** ✨
- **Quad-Tree compression**: Efficiently compress satellite images by recursively subdividing the image into smaller blocks based on pixel variability. 🖼️
- **Image reconstruction**: Restore compressed images to their original state from the Quad-Tree structure. 📂
- **Pseudo-MTF calculation**: Obtain pseudo-MTF values from the quadtree structure to assess the impact of compression on image sharpness. 📈
- **Classification map**: Generate a classification map of the nodes in the Quad-Tree structure based on compression detail thresholds. 🗺️

## **Installation** ⚙️
Install the latest version from PyPI:

```bash
pip install satcompression
```

## **How to use** 🛠️

### **Compression and decompression of satellite images** 🛰️

#### **Load libraries**

```python
import satcompression
import rasterio as rio
```

#### **Load an image**

```python
with rio.open('path/to/image.tif') as src:
    image_meta = src.meta
    image_data = src.read()
```
#### **Compress the image**
```python
image_data_compress = satcompression.compress_and_encode_image_data(
    image_data=image_data, detail_error_threshold=20
)
```
#### **Decompress the image**
```python
image_data_decompress = satcompression.reconstruct_image_data(
    data=image_data_compress, dtype=image_data.dtype, nchannels=image_data.shape[0]
)
```
<p align="center">
  <img src="https://huggingface.co/datasets/JulioContrerasH/DataMLSTAC/resolve/main/mtf_comparison.png" width="70%">
</p>


### **Calculate pseudo-MTF from Quad-Tree decomposition** 📊

#### **Load libraries**

```python
import satcompression
import matplotlib.pyplot as plt
```

#### **Obtain pseudo-MTF values**

```python
with rio.open('path/to/image.tif') as src:    
    image_data = src.read()

# Calculate pseudo-MTF with different detail error thresholds
mtf_values1, x_axis1 = satcompression.quadtree_mtf(image_data, 10, detail_error_threshold=20)
mtf_values2, x_axis2 = satcompression.quadtree_mtf(image_data, 10, detail_error_threshold=10)
mtf_values3, x_axis3 = satcompression.quadtree_mtf(image_data, 10, detail_error_threshold=5)

# Plot the pseudo-MTF results
plt.plot(x_axis1, mtf_values1, label="Detail Error Threshold: 20")
plt.plot(x_axis2, mtf_values2, label="Detail Error Threshold: 10")
plt.plot(x_axis3, mtf_values3, label="Detail Error Threshold: 5")
plt.legend()
plt.ylim(0, 1.2)
plt.title("Pseudo-MTF obtained from the quadtree decomposition")
plt.show()
```
### **Create a classification map from the Quad-Tree nodes** 🗺️

#### **Load libraries**

```python
import satcompression
```

#### **Generate classification map from Quad-Tree compression**
```python
with rio.open('path/to/image.tif') as src:    
    image_data = src.read()

satcompression.create_classification_map(image_data, detail_error_threshold=20)
```

<p align="center">
  <img src="https://huggingface.co/datasets/JulioContrerasH/DataMLSTAC/resolve/main/classification_map.png" width="100%">
</p>
