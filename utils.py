import os
dashes = '\n----------------------------------------\n'


def get_ocr_engine():
    '''
        Record the select OCR engine selected by user
        1: Google Cloud Vision
        2: Lipikar API [IITD]
        3. Restart Upload
        4: Exit
    Returns:
        String corresponding the selected choice.
    '''

    print("\nChoose OCR engine:")
    print("1. Google Cloud Vision")
    print("2. Lipikar")
    print("3. Restart Upload")
    print("4. Exit\n")
    engine_choice = input("Enter your choice (1/2/3/4): ")

    if engine_choice == "1":
        print("\nGoogle Cloud Vision selected!")
        return "google"
    elif engine_choice == "2":
        return "lipikar"
    elif engine_choice == "3":
        return "restart"
    elif engine_choice == "4":
        return ""
    else:
        print(dashes+"Invalid choice. Please enter (1/2/3/4)."+dashes)
        return get_ocr_engine()


def check_supported_extension(image_path):
    """
    Check if the file extension is supported (jpg/pdf).

    Args:
        image_path (str): The path to the image file.

    Returns:
        bool: True if the file extension is supported, False otherwise.
    """

    file_name_parts = image_path.split(".")
    extension = file_name_parts[-1]
    supported_extensions = ["jpg", "pdf"]

    if extension.lower() in supported_extensions:
        return True
    else:
        print(dashes+"Invalid format detected. Currently, only image files (jpg/pdf) are supported."+dashes)
        return False
        

def is_valid_file(file_path):

    """
    Check if the file exists at the given file path.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """

    if os.path.exists(file_path) and os.path.isfile(file_path):
        return True
    else:
        print(dashes+"Could not locate the given file, please try again."+dashes)
        return False
    

def remove_extra_spaces(image_path):
    """
    Trims all spaces from the given image path, including trailing and leading spaces.

    Args:
        image_path (str): The image path with extra spaces.

    Returns:
        str: The image path with extra spaces removed.
    """
    # Remove extra spaces using strip() method
    cleaned_image_path = image_path.strip()
    
    return cleaned_image_path



def get_image_path():
    """
    Returns the input image path provided by the user.

    Returns:
        str: The input image path.
    """
    image_path = input("Enter the path to the image file for OCR: ")
    image_path = remove_extra_spaces(image_path)

    if not check_supported_extension(image_path) or not is_valid_file(image_path):
        return get_image_path()

    return image_path
