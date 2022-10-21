import glob
import io
import logging
import os
import uuid
from typing import Union, Dict

import numpy as np
from PIL import Image
from fastapi import FastAPI, UploadFile
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse

from src.core import process_inpaint


def schema():
    openapi_schema = get_openapi(
        title="Object Removal API",
        version="1.0",
        description="From given Image and Mask generates Processed Image",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI()
app.openapi = schema
logger = logging.getLogger(__name__)


@app.get('/')
async def app_works(summary="Create an item"):
    """
        **Route to check if Object Removal API works**
    """
    return {"message": "App Works!"}


@app.post("/process_image/")
async def upload_image_and_mask(image_to_process: Union[UploadFile, None] = None,
                                image_mask: Union[UploadFile, None] = None) -> Dict[str, str] or FileResponse:
    """
    From given Image and Mask generates Processed Image

    **image_to_process** Image to be Processed

    **image_mask** Image mask

    **return** Processed Image
    """
    if not image_to_process or not image_mask:
        return {"message": "Please upload files correctly!"}
    elif image_to_process and image_mask and image_to_process.content_type in ["image/jpeg",
                                                                               "image/jpg",
                                                                               "image/png"] \
            and image_mask.content_type in ["image/jpeg",
                                            "image/jpg",
                                            "image/png"]:
        files = glob.glob('./images/*')

        for f in files:
            os.remove(f)

        try:
            img_input_bytes = await image_to_process.read()
            img_input = Image.open(io.BytesIO(img_input_bytes)).convert("RGBA")

            image_mask_bytes = await image_mask.read()
            image_mask = Image.open(io.BytesIO(image_mask_bytes)).convert("RGBA")

            output = process_inpaint(np.array(img_input), np.array(image_mask))
            img_output = Image.fromarray(output).convert("RGB")

            save_here = f"./images/{str(uuid.uuid1())}.jpeg"
            img_output.save(save_here)

            return FileResponse(save_here)
        except Exception as e:
            logger.info(f"Error: {e}")
            return {"message": "Please provide correct file for the mask!"}
