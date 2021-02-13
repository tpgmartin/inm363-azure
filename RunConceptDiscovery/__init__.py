import logging
import azure.functions as func
import io
import sys
from PIL import Image

def main(blobin: func.InputStream, blobout: func.Out[bytes],  blobout2: func.Out[bytes],context: func.Context):
    logging.info(f"--- Python blob trigger function processed blob \n"
                 f"----- Name: {blobin.name}\n"
                 f"----- Blob Size: {blobin.length} bytes")

    input_image = blobin

    try:
        base_image = Image.open(input_image)
    except OSError as e:
        print(f'EXCEPTION: Unable to read input as image. {e}')
        sys.exit(254)
    except Exception as e:
        print(f'EXCEPTION: {e}')
        sys.exit(255)
    
    img = Image.new('RGBA', (base_image.width, base_image.height), (0, 0, 0, 0))
    img.paste(base_image, (0, 0))

    img.show()

    # Store final composite in a memory stream
    img_byte_arr = io.BytesIO()
    # Convert composite to RGB so we can save as JPEG
    img.convert('RGB').save(img_byte_arr, format='JPEG')

    # Write to output blob
    #
    # Use this to set blob content from a file instead:  
    # with open(output_image, mode='rb') as file:
    #     blobout.set(file.read())
    #
    # Set blob content from byte array in memory
    blobout.set(img_byte_arr.getvalue())
    blobout2.set(img_byte_arr.getvalue())

    logging.info(f"Image saved successfully")
