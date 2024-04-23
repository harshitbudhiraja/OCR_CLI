import argparse
from utils import *
from lipikar_ocr import *



def main():
    '''Entry point for OCR task.
    
    ARGS:
    --engine : To choose an engine name between Lipikar and Google Cloud Vision API

    RETURNS:
    uploadDetails.json and Detections.json saved 


    '''
    parser = argparse.ArgumentParser(description="Perform OCR using Google Cloud Vision or Lipikar")
    parser.add_argument("--engine", choices=["google", "lipikar"],  help="OCR engine to use (default: google)")
    args = parser.parse_args()

    print(dashes+"Welcome to the OCR CLI tool!"+dashes)

    image_path = get_image_path()
    # image_path = '1.pdf'


    if args.engine == "gcv" or args.engine == "lipikar":
        engine = args.engine
    else:
        # engine = "lipikar"
        engine = get_ocr_engine()


    if engine == "lipikar":
        lipikar_ocr(image_path)
        
    elif engine == "gcv":
        print("google cloud vision selected")
    else :
        return

    print("engine: ", engine)


if __name__ == "__main__":
    main()
