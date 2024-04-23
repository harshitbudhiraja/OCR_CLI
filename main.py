import argparse
from utils import *
from lipikar_ocr import *
from gcv_ocr import *


def main():

    '''Entry point for OCR task.
    
    ARGS:
    --engine : To choose an engine name between Lipikar and Google Cloud Vision API
    Options: lipikar , gcv

    RETURNS:
    uploadDetails.json: A JSON file containing details of the upload process.
    
    Detections.json: A JSON file containing the results of the OCR detection process, such as recognized text, bounding boxes..


    '''

    parser = argparse.ArgumentParser(description="Perform OCR using Google Cloud Vision or Lipikar")
    parser.add_argument("--engine", choices=["google", "lipikar"],  help="OCR engine to use (default: google)")
    args = parser.parse_args()

    print(dashes+"Welcome to the OCR CLI tool!"+dashes)

    image_path = get_image_path()


    if args.engine == "gcv" or args.engine == "lipikar":
        engine = args.engine
    else:
        engine = get_ocr_engine()


    if engine == "lipikar":
        lipikar_ocr(image_path)
        
    elif engine == "gcv":
        gcloud_ocr(image_path)
    else :
        return


if __name__ == "__main__":
    main()
