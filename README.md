# satcompression
Efficient decomposition of satellite images in a Quad-Tree structure


## Installation

```bash
pip install satcompression
```

## Usage

Compression and decompression of satellite images using the Quad-Tree structure.

```python
import satcompression
import rasterio as rio

# Load an image
with rio.open('path/to/image.tif') as src:
    image_meta = src.meta
    image_data = src.read()

# Compress the image
image_data_compress = satcompression.compress_and_encode_image_data(
    image_data=image_data, detail_error_threshold=20
)

# Decompress the image
image_data_decompress = satcompression.reconstruct_image_data(
    data=image_data_compress, dtype=image_data.dtype, nchannels = image_data.shape[0]
)
```

![image](docs/images/visual_comparison.png)

Obtain the pseudo-mtf from the quadtree structure.

```python
import satcompression
import matplotlib.pyplot as plt

with rio.open('path/to/image.tif') as src:    
    image_data = src.read()

mtf_values1, x_axis1 = satcompression.quadtree_mtf(image_data, 10, detail_error_threshold=20)
mtf_values2, x_axis2 = satcompression.quadtree_mtf(image_data, 10, detail_error_threshold=10)
mtf_values3, x_axis3 = satcompression.quadtree_mtf(image_data, 10, detail_error_threshold=5)

plt.plot(x_axis1, mtf_values1, label="Detail Error Threshold: 0.002")
plt.plot(x_axis2, mtf_values2, label="Detail Error Threshold: 0.001")
plt.plot(x_axis3, mtf_values3, label="Detail Error Threshold: 0.0005")
plt.legend()
plt.ylim(0, 1.2)
plt.title("Pseudo-MTF obtained from the quadtree decomposition")
plt.show()
```

![image](docs/images/mtf_comparison.png)

Obtain the classification of the quadtree nodes.

```python
import satcompression

with rio.open('path/to/image.tif') as src:    
    image_data = src.read()

satcompression.create_classification_map(image_data, detail_error_threshold=20)
```

![image](docs/images/classification_map.png)
