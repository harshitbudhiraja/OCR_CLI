import requests
import os
import json
import getpass

LIPIKAR_API_BASE_URL = "http://lipikar.apps.iitd.ac.in/api/ocr"
dashes = '\n-------------------------------------------\n'
session = {}

def get_document_parser():

    print(dashes+"Select a Document Parser:"+dashes)
    print("1. Line-Level (Tess)")
    print("2. Word-Level (Tess)")
    print("3. Line-Level (Kraken)")
    print("4. Word-Level (Kraken + Tess)")

    choice = input("\nEnter your choice (1/2/3/4): ")

    if choice == 1:
        print("You selected Line-Level (Tess)")
    elif choice == 2:
        print("You selected Word-Level (Tess)")
    elif choice == 3:
        print("You selected Line-Level (Kraken)")
    elif choice == 4:
        print("You selected Word-Level (Kraken + Tess)")

    if choice in ('1', '2', '3', '4'):
        choices = ['Line-Level (Tess)','Word-Level (Tess)','Line-Level (Kraken)','Word-Level (Kraken + Tess)']
        selected_choice = choices[int(choice)-1]
        print("You selected "+ selected_choice)
        return selected_choice
    else:
        print("Invalid choice. Please enter a valid option (1/2/3/4).")
        return get_document_parser()

def get_text_recognizer():
        print(dashes+ "Select a Text recognizer:"+dashes)
        print("1. Telugu (IITD)")
        print("2. Hindi (IITD)")
        print("3. Urdu (IITD)")
        print("4. Oriya (IITD)")
        print("5. English (IITD)")
        print("6. Manipuri (Meitei) (IITD)")
        print("7. Punjabi (IITD)")
        print("8. Gujarati (IITD)")
        print("9. Bengali (IITD)")
        print("10. Tamil (IITD)")

        choice = input("\nEnter your choice (1-10): ")

        if choice in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'):
            choices = ['Telugu', 'Hindi','Urdu','Oriya','English','Manipuri','Punjabi','Gujarati','Bengali','Tamil']
            selected_choice = choices[int(choice)-1]
            print("You selected "+ selected_choice)
            return selected_choice
        else:
            print("Invalid choice. Please enter a valid option (1-10).")
            return get_text_recognizer()

def get_json_content(filepath):

    with open(filepath, 'r') as file:
        response = json.load(file)

    return response

def save_to_file(json_content,file_path):
    with open(file_path, 'w') as json_file:
        json.dump(json_content, json_file)


def set_session(value):
    global session
    session = value

def set_upload_id(value):
    global upload_id
    upload_id = value

def set_username(value):
    global username
    username = value

def display_list(list_name, list_items):

    print(dashes+list_name+":"+dashes)
    for count,item in enumerate(list_items,1):
        print(count,"->",item)

def is_authenticated(func):
    def wrapper(args):
        if 'access' in session :
            return func(args)
        else:
            print(dashes+"User is not authenticated. Please login first!"+dashes)
    return wrapper

def login(image_path):
    url = LIPIKAR_API_BASE_URL + '/auth/login/'

    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    payload = {
        'username': username,
        'password': password
    }

    # response = requests.post(url, json=payload)
    # response = response.json()

    json_file_path = '/Users/harshitbudhraja/Documents/ocr_cli/dummy_responses/login.json'
    response = get_json_content(json_file_path)

    
    status = response['status_code']
    if status == 200:
        print(dashes+"Login successful!"+dashes)
        set_session(response)
        set_username(username)

    elif status == 401:
        print(dashes+ "Login failed. Please recheck credentials!" +dashes)
    elif status == 400:
        print(dashes+ "Credentials missing. Please re try!" +dashes)

    return True


@is_authenticated
def refresh_access_token(image_path):
    refresh = session['refresh']

    payload = {
        'refresh': refresh
    }
    url = LIPIKAR_API_BASE_URL + '/auth/token/refresh/'

    # response = requests.post(url, json=payload)
    # response = response.json()

    json_file_path = '/Users/harshitbudhraja/Documents/ocr_cli/dummy_responses/refresh.json'
    response = get_json_content(json_file_path)


    access = response['access']
    set_session({'access': access, 'refresh': refresh})

    print(dashes+"Access Token Refreshed"+dashes)

    return True


@is_authenticated
def get_modules_config(image_path):
    url = LIPIKAR_API_BASE_URL + '/config/'
    headers = {
        'Authorization': 'Bearer ' + session['access']
    }
    # response = requests.get(url, headers=headers)
    # response = response.json()

    json_file_path = '/Users/harshitbudhraja/Documents/ocr_cli/dummy_responses/modules_config.json'
    response = get_json_content(json_file_path)


    document_parsers = response['result']['config']['document_parsers']
    text_recognizers = response['result']['config']['text_recognizers']

    document_parsers = [parser['displayName'] for parser in document_parsers]
    text_recognizers = [recognizer['displayName'] for recognizer in text_recognizers]

    display_list("Document Parses",document_parsers)
    display_list("Text Recognizers",text_recognizers)
    print(dashes)


@is_authenticated
def upload_new(image_path):

    url = LIPIKAR_API_BASE_URL + '/uploads/'

    selected_document_parser = get_document_parser()
    selected_text_recognizer = get_text_recognizer()

    
    json_file_path = '/Users/harshitbudhraja/Documents/ocr_cli/dummy_responses/upload_file.json'
    response = get_json_content(json_file_path)

    # Save upload details to file
    save_to_file(response,'uploadDetails.json')

    headers = {
        'Authorization': 'Bearer ' + session['access']
    }
    query_params = {
        'document_parser':selected_document_parser,
        'parsing_postprocessor':'no_postprocessor',
        'text_recognizer':selected_text_recognizer
    }

    # response = requests.post(url, headers=headers,params=query_params)
    # response = response.json()

    upload_id = response['result']['upload']['id']
    set_upload_id(upload_id)

    response_ = get_json_content('/Users/harshitbudhraja/Documents/ocr_cli/dummy_responses/get_detections.json')
    detections = response_['result']
    

    save_to_file(detections,'detections.json')
    
    print(dashes,detections,dashes)
    print(dashes+"New file uploaded! ID: " + str(upload_id) + "\nContents saved to [uploadDetails.json] and [detections.json]"+dashes)

    return True

@is_authenticated
def get_upload_processing_status(image_path):


    if 'upload_id' not in locals() and 'upload_id' not in globals():
        print(dashes+"Please upload a file first!"+dashes)
        return lipikar_ocr(image_path)

    json_file_path = '/Users/harshitbudhraja/Documents/ocr_cli/dummy_responses/processing_status.json'
    response = get_json_content(json_file_path)
    
    progress = response['progress']
    print(dashes+f'File is {progress}% uploaded!'+dashes)
    return True


@is_authenticated
def get_upload_detail(image_path):

    url = LIPIKAR_API_BASE_URL + '/uploads/'

    if 'upload_id' not in locals() and 'upload_id' not in globals():
        print(dashes+"Please upload a file first!"+dashes)
        return lipikar_ocr(image_path)
    
    params = {'id' : upload_id }

    headers = {
        'Authorization': 'Bearer ' + session['access']
    }


    json_file_path = '/Users/harshitbudhraja/Documents/ocr_cli/dummy_responses/upload_detail.json'
    response = get_json_content(json_file_path)

    # response = requests.get(url,params=params,headers=headers)
    # response = response.json()

    upload_details = response['result']
    print(dashes,upload_details,dashes)

    file_path = 'uploadDetails.json'

    with open(file_path, 'w') as json_file:
        json.dump(upload_details, json_file)

    return True

@is_authenticated
def get_all_detections_for_upload(image_path):
    url = LIPIKAR_API_BASE_URL + '/detections/'

    if 'upload_id' not in locals() and 'upload_id' not in globals():
        print(dashes+"Please upload a file first!"+dashes)
        return lipikar_ocr(image_path)
    
    params = {'uploadId' : upload_id }

    headers = {
        'Authorization': 'Bearer ' + session['access']
    }

    # response = requests.get(url,params=params,headers=headers)
    # response = response.json()

    json_file_path = '/Users/harshitbudhraja/Documents/ocr_cli/dummy_responses/get_detections.json'
    response = get_json_content(json_file_path)

    detections = response['result']
    
    print(dashes,detections,dashes)

    file_path = 'detections.json'

    with open(file_path, 'w') as json_file:
        json.dump(detections, json_file)

    return True



def lipikar_ocr(image_path):

    if 'username' in locals() or 'username' in globals():
        print(f'\n[{username}] Choose an option: \n')
    else:
        print("\nChoose an option: \n")

    print("1. Login")
    print("2. Refresh Access Token")
    print("3. Get Modules Config")
    print("4. Upload New")
    print("5. Get Upload Processing Status")
    print("6. Get Upload Detail")
    print("7. Get All Detections For Upload")
    print("8. Restart Upload")
    print("9. Exit\n")

    choice = input("Enter your choice: ")

    if choice == "1":
        login(image_path)
    elif choice == "2":
        refresh_access_token(image_path)
    elif choice == "3":
        get_modules_config(image_path)
    elif choice == "4":
        upload_new(image_path)
    elif choice == "5":
        get_upload_processing_status(image_path)
    elif choice == "6":
        get_upload_detail(image_path)
    elif choice == "7":
        get_all_detections_for_upload(image_path)
    elif choice == "8":
        return "restart"
    elif choice == "9":
        print("Exiting...")
        return None
    else:
        print("Invalid choice. Please enter a number between 1 and 8.")
    return lipikar_ocr(image_path)
