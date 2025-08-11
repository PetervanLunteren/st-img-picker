# st-img-picker

**Fork of [streamlit-image-select](https://github.com/jrieke/streamlit-image-select) with multiple selection support.**

**A Streamlit custom component for image selection.**

This custom component works just like `st.selectbox` but with images. It's a great option
if you want to let the user select example images, e.g. for a computer vision app.

---

## Installation

```bash
pip install st-img-picker
```

## Simple usage

```python
import streamlit as st
from st_img_picker import img_picker

imgs = img_picker(
    "Select images", 
    ["image1.png", "image2.png", "image3.png"]
)
st.write(f"Selected {len(imgs)} images")
```

### Advanced usage
```python
from st_img_picker import img_picker
import numpy as np
from PIL import Image

# Mix different image types
imgs = img_picker(
    label="Choose your favorites",
    images=[
        "local/path/image.jpg",              # Local file
        "https://example.com/image.png",     # URL
        Image.open("another_image.jpg"),     # PIL Image
        np.array(Image.open("numpy.jpg"))    # NumPy array
    ],
    captions=["Local", "Remote", "PIL", "NumPy"],
    index=[0, 2],                            # Pre-select first and third
    use_container_width=True,
    return_value="index",                    # Return indices instead of images
    key="my_picker"
)

st.write(f"Selected indices: {imgs}")
```

## Parameters

- **label** (str): The label shown above the images.
- **images** (list): The images to show. Supports local files, URLs, PIL images, and numpy arrays.
- **captions** (list of str, optional): Captions to show below images. Defaults to None.
- **index** (int or list, optional): Initially selected image(s). For single selection: int. For multiple selection: list of ints. Defaults to [] for multi-select, 0 for single-select.
- **use_container_width** (bool, optional): Whether to stretch images to container width. Defaults to True.
- **return_value** ("original" or "index", optional): Return original objects or indices. Defaults to "original".
- **allow_multiple** (bool, optional): Enable multiple selection. Defaults to **True**.
- **key** (str, optional): Component key. Defaults to None.

## Returns

- **Multiple selection** (`allow_multiple=True`): Returns list of items (images or indices)
- **Single selection** (`allow_multiple=False`): Returns single item (image or index)

## Development

> **Warning**
> You only need to run these steps if you want to change this component or 
contribute to its development!

### Setup

First, clone the repository:

```bash
git clone <your-fork-repo-url>
cd st-img-picker
```

Install the Python dependencies:

```bash
poetry install --dev
```

And install the frontend dependencies:

```bash
cd st_img_picker/frontend
npm install
```

### Making changes

To make changes, first go to `st_img_picker/__init__.py` and make sure the 
variable `_RELEASE` is set to `False`. This will make the component use the local 
version of the frontend code, and not the built project. 

Then, start one terminal and run:

```bash
cd st_img_picker/frontend
npm start
```

This starts the frontend code on port 3001.

Open another terminal and run:

```bash
cp demo/streamlit_app.py .
poetry shell
streamlit run streamlit_app.py
```

This copies the demo app to the root dir (so you have something to work with and see 
your changes!) and then starts it. Now you can make changes to the Python or Javascript 
code in `st_img_picker` and the demo app should update automatically!

If nothing updates, make sure the variable `_RELEASE` in `st_img_picker/__init__.py` is set to `False`. 

### Publishing on PyPI

Switch the variable `_RELEASE` in `st_img_picker/__init__.py` to `True`. 
Increment the version number in `pyproject.toml`. Make sure the copy of the demo app in 
the root dir is deleted or merged back into the demo app in `demo/streamlit_app.py`.

Build the frontend code with:

```bash
cd st_img_picker/frontend
NODE_OPTIONS="--openssl-legacy-provider" npm run build
```

After this has finished, build and upload the package to PyPI:

```bash
cd ../..
poetry build
poetry publish
```

## License

MIT License - See LICENSE file for details.

## Credits

- Original [streamlit-image-select](https://github.com/jrieke/streamlit-image-select) by Johannes Rieke
- Fork enhancements by Peter van Lunteren