import requests
import os
import json
import getpass

LIPIKAR_API_BASE_URL = "http://lipikar.apps.iitd.ac.in/api/ocr"
dashes = '\n-------------------------------------------\n'
session = {}

# TODO: add class methods

def set_session(value):
    global session
    session = value

def set_upload_id(value):
    global upload_id
    upload_id = value

def display_list(list_name, list_items):

    print(dashes+list_name+":"+dashes)
    for count,item in enumerate(list_items,1):
        print(count,"->",item)
    print(dashes)

def is_authenticated(func):
    def wrapper():
        if 'access' in session :
            return func()
        else:
            print(dashes+"User is not authenticated. Please login first!"+dashes)
    return wrapper

def login():
    url = LIPIKAR_API_BASE_URL + '/auth/login/'

    username = input("Enter username: ")
    # TODO: avoid echoing passwords
    password = getpass.getpass("Enter password: ")

    payload = {
        'username': username,
        'password': password
    }

    response = requests.post(url, json=payload)
    status = response.status_code
    if status == 200:
        print(dashes+"Login successful!"+dashes)
        set_session(response.json())

    elif status == 401:
        print(dashes+ "Login failed. Please recheck credentials!" +dashes)
    elif status == 400:
        print(dashes+ "Credentials missing. Please re try!" +dashes)


@is_authenticated
def refresh_access_token():
    refresh = session['refresh']

    payload = {
    'refresh': refresh
    }
    url = LIPIKAR_API_BASE_URL + '/auth/token/refresh/'

    response = requests.post(url, json=payload)
    response = response.json()
    access = response['access']
    set_session({'access': access, 'refresh': refresh})

    print(dashes+"Access Token Refreshed"+dashes)


@is_authenticated
def get_modules_config():
    url = LIPIKAR_API_BASE_URL + '/config/'
    headers = {
        'Authorization': 'Bearer ' + session['access']
    }
    response = requests.get(url, headers=headers)
    response = response.json()

    document_parsers = response['result']['config']['document_parsers']
    text_recognizers = response['result']['config']['text_recognizers']

    document_parsers = [parser['displayName'] for parser in document_parsers]
    text_recognizers = [recognizer['displayName'] for recognizer in text_recognizers]

    display_list("Document Parses",document_parsers)
    display_list("Text Recognizers",text_recognizers)


@is_authenticated
def upload_new():
    url = LIPIKAR_API_BASE_URL + '/uploads/'

    # TODO: take input for document parser and text recognizer from user, handle case for urdu
    query_params = {
        'document_parser':'',
        'parsing_postprocessor':'no_postprocessor',
        'text_recognizer':''

    }
    # with open(image_path, 'rb') as file:
    #     files = {'file': file}
    headers = {
        'Authorization': 'Bearer ' + session['access']
    }
    
    response = requests.post(url, headers=headers,params=query_params)
    response = response.json()

    upload_id = response['result']['upload']['id']
    set_upload_id(upload_id)

    print("New file uploaded! ID: " + upload_id)


@is_authenticated
def get_upload_processing_status():
    print("Get upload processing status")
    


@is_authenticated
def get_upload_detail():

    url = LIPIKAR_API_BASE_URL + '/uploads/'

    params = {'id' : upload_id }

    headers = {
        'Authorization': 'Bearer ' + session['access']
    }

    response = requests.get(url,params=params,headers=headers)
    response = response.json()
    upload_details = response['result']
    print(upload_details)

    file_path = 'uploadDetails.json'

    with open(file_path, 'w') as json_file:
        json.dump(upload_details, json_file)




@is_authenticated
def get_all_detections_for_upload():
    url = LIPIKAR_API_BASE_URL + '/detections/'

    params = {'uploadId' : upload_id }

    headers = {
        'Authorization': 'Bearer ' + session['access']
    }

    response = requests.get(url,params=params,headers=headers)
    response = response.json()
    detections = response['result']
    print(detections)

    file_path = 'detections.json'

    with open(file_path, 'w') as json_file:
        json.dump(detections, json_file)




def lipikar_ocr(image_path):
    print("\nChoose an option:\n")
    print("1. Login")
    print("2. Refresh Access Token")
    print("3. Get Modules Config")
    print("4. Upload New")
    print("5. Get Upload Processing Status")
    print("6. Get Upload Detail")
    print("7. Get All Detections For Upload")
    print("8. Exit\n")

    choice = input("Enter your choice: ")
    print(image_path)

    if choice == "1":
        login()
    elif choice == "2":
        refresh_access_token()
    elif choice == "3":
        get_modules_config()
    elif choice == "4":
        upload_new()
    elif choice == "5":
        get_upload_processing_status()
    elif choice == "6":
        get_upload_detail()
    elif choice == "7":
        get_all_detections_for_upload()
    elif choice == "8":
        print("Exiting...")
        return None
    else:
        print("Invalid choice. Please enter a number between 1 and 8.")
    return lipikar_ocr(image_path)
