import base64
import io
import os
from pathlib import Path

import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "image_select", url="http://localhost:3001"
    )
else:
    path = (Path(__file__).parent / "frontend" / "build").resolve()
    _component_func = components.declare_component("image_select", path=path)


@st.cache_data
def _encode_file(img):
    with open(img, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpeg;base64, {encoded}"


@st.cache_data
def _encode_numpy(img):
    pil_img = Image.fromarray(img)
    buffer = io.BytesIO()
    pil_img.save(buffer, format="JPEG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/jpeg;base64, {encoded}"


def img_picker(
    label: str,
    images: list,
    captions: list = None,
    index = None,
    *,
    use_container_width: bool = True,
    return_value: str = "original",
    allow_multiple: bool = True,
    key: str = None,
):
    """Shows several images and returns the image(s) selected by the user.

    Args:
        label (str): The label shown above the images.
        images (list): The images to show. Allowed image formats are paths to local
            files, URLs, PIL images, and numpy arrays.
        captions (list of str): The captions to show below the images. Defaults to
            None, in which case no captions are shown.
        index (int or list, optional): The index(es) of the image(s) that are selected 
            by default. When allow_multiple=False, must be an int. When allow_multiple=True,
            must be a list of ints (can be empty). Defaults to [] for multi-select, 0 for single-select.
        use_container_width (bool, optional): Whether to stretch the images to the
            width of the surrounding container. Defaults to True.
        return_value ("original" or "index", optional): Whether to return the
            original object(s) passed into `images` or the index(es) of the selected image(s).
            Defaults to "original".
        allow_multiple (bool, optional): Whether to allow selecting multiple images.
            When True, returns a list. Defaults to True.
        key (str, optional): The key of the component. Defaults to None.

    Returns:
        (any or list): The image(s) selected by the user. When allow_multiple=False,
            returns single item. When allow_multiple=True, returns list of items.
    """

    # Do some checks to verify the input.
    if len(images) < 1:
        raise ValueError("At least one image must be passed but `images` is empty.")
    if captions is not None and len(images) != len(captions):
        raise ValueError(
            "The number of images and captions must be equal but `captions` has "
            f"{len(captions)} elements and `images` has {len(images)} elements."
        )
    
    # Set default index based on allow_multiple if not provided
    if index is None:
        index = [] if allow_multiple else 0
    
    # Validate index parameter based on allow_multiple
    if allow_multiple:
        if not isinstance(index, list):
            raise ValueError(
                f"When `allow_multiple=True`, `index` must be a list but got {type(index).__name__}. "
                "Use an empty list [] for no default selection, or [0, 2] for multiple selections."
            )
        for i in index:
            if i >= len(images):
                raise ValueError(
                    f"All values in `index` must be smaller than the number of images ({len(images)}) "
                    f"but found {i}."
                )
    else:
        if not isinstance(index, int):
            raise ValueError(
                f"When `allow_multiple=False`, `index` must be an int but got {type(index).__name__}."
            )
        if index >= len(images):
            raise ValueError(
                f"`index` must be smaller than the number of images ({len(images)}) "
                f"but it is {index}."
            )

    # Encode local images/numpy arrays/PIL images to base64.
    encoded_images = []
    for img in images:
        if isinstance(img, (np.ndarray, Image.Image)):  # numpy array or PIL image
            encoded_images.append(_encode_numpy(np.asarray(img)))
        elif os.path.exists(img):  # local file
            encoded_images.append(_encode_file(img))
        else:  # url, use directly
            encoded_images.append(img)

    # Pass everything to the frontend.
    component_value = _component_func(
        label=label,
        images=encoded_images,
        captions=captions,
        index=index,
        use_container_width=use_container_width,
        allow_multiple=allow_multiple,
        key=key,
        default=index,
    )

    # The frontend component returns the index(es) of the selected image(s).
    # Handle both single and multi-selection cases.
    if allow_multiple:
        # component_value should be a list of indices
        if return_value == "original":
            return [images[i] for i in component_value]
        elif return_value == "index":
            return component_value
        else:
            raise ValueError(
                "`return_value` must be either 'original' or 'index' "
                f"but is '{return_value}'."
            )
    else:
        # component_value should be a single index
        if return_value == "original":
            return images[component_value]
        elif return_value == "index":
            return component_value
        else:
            raise ValueError(
                "`return_value` must be either 'original' or 'index' "
                f"but is '{return_value}'."
            )
