from google.cloud import vision
from google.cloud.vision_v1 import types
dashes = '\n----------------------------------------\n'


# Authenticate using service account credentials
try:
    client = vision.ImageAnnotatorClient.from_service_account_json('service_account.json')
except:
    print("Problem encountered with the service account credentials, Please check the file")


def detected_text(image_path,language='English'):
    """
    Simulates text detection using Google Cloud Vision OCR.

    Args:
        image_path (str): Path to the image file.
        language (str): Language code for text detection (default is 'English').

    Returns:
        list: A list of detected text strings.
    """


    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # response = client.label_detection(image=image)
    
    dummy_responses = {
    'label_annotations':
    {
        'English':
    [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    ],
    'Hindi':
    [
        "लोरेम इप्सम डोलोर सिट अमेट, कॉन्सेक्टेटुर एडिपिस्सिंग एलिट.",
        "सेद दो एमोदस्मोद तेम्पोर इंदिदुंट उत लबोरे एट दोलोरे मग्ना अलिक्वा.",
        "उत एनिम एड मिनिम वेनियाम, क्विस नोस्त्रुद एक्जेर्सीटातिओन उल्लाम्को लाबोरिस निसि उत अलिक्विप एक्स एअ कोम्मोदो कोंसेकुअत.",
        "दुइस आउते इरुरे डोलोर इन रेप्रेहेंदेरित इन वोलुप्टाते वेलित एस्से चिल्लुम डोलोरे एउ फुगिअत नुल्ला पारिआतुर.",
        "एक्स्चेप्तेर सिंट ओक्काएकात् कुपिदातात् नोन प्रोइदेन्त्, सुंत इन कुल्पा कुइ ओफ्फिकिया डेसेरुन्त् मोल्लित् आनिम इद एस्त् लाबोरुम."
    ],
    'Punjabi':
    [
        "ਲੋਰੇਮ ਇਪਸਮ ਦਲੋਰ ਬੈਠੋ, ਕਨਸੈਕਟੇਟੁਰ ਐਡਪਸਿੰਗ ਐਲਿਟ।"
        "ਸੇਡ ਡੂ ਏਮੋਡ੍ਸਮੋਡ ਤੇਮਪੋਰ ਇੰਦਿਦੁੰਤ ਉਤ ਲਬੋਰੇ ਐਟ ਡੋਲੋਰੇ ਮਗਨਾ ਅਲਿਕਵਾ।"
        "ਉਤ ਏਨਿਮ ਐਡ ਮਿਨਿਮ ਵੇਨਿਅਮ, ਕੁਵਿਸ ਨੋਸਟਰੁਦ ਐਕਜੇਰਸੀਟੇਤਿਓਨ ਉਲਲਾਮਕੋ ਲਾਬੋਰਿਸ ਨਿਸਿ ਉਤ ਅਲਿਕਵਿਪ ਏਕਸ ਏਅ ਕੋਮੋਡੋ ਕੋੰਸੇਕੁਅਤ।"
        "ਦੁਇਸ ਆਉਤੇ ਇਰੁਰੇ ਡੋਲੋਰ ਇਨ ਰੇਪਰੇਹੇਂਦੇਰਿਤ ਇਨ ਵੋਲੁਪਟਾਤੇ ਵੇਲਿਤ ਐਸੇ ਚਿਲਮ ਡੋਲੋਰੇ ਐਉ ਫੁਗਿਅਤ ਨੁਲਾ ਪਾਰਿਆਤੁਰ।"
        "ਏਕਸਚੇਪਤੇਰ ਸਿੰਟ ਓਕਕਾਏਕਾਤ ਕੁਪਿਦਾਤਾਤ ਨੋਨ ਪ੍ਰੋਇਦੇਂਤ, ਸੁਂਤ ਇਨ ਕੁਲਪਾ ਕੁਇ ਓਫ਼ਿਕਿਅ ਡੇਸੇਰੁਨਤ ਮੋਲਿਤ ਆਨਿਮ ਇਦ ਏਸਤ ਲਾਬੋਰੁਮ।"

    ],
    "Bengali" :
    [
        "লোরেম ইপসুম দোলর বসিত অমেত, কনসেক্টেতুর এদিপিসেত এলিত।"
        "সেদ ডু এমোডসমোদ তেম্পর ইন্দিদুন্ত উত লবরে এত দোলরে মগনা অলিক্যাঃ।"
        "উত এনিম এদ মিনিম ভেনিয়াম, কুইস নস্ত্রুদ এক্সেরসিটাতিওন উল্লাম্কো লাবরিস নিসি উত অলিক্যাপ এক্স এঅ কোম্মোদো কোন্সেকুআত।"
        "ডুইস আউতে ইরুরে দোলর ইন রেপ্রেহেন্দেরিত ইন ভলুপটাতে ভেলিত এসে চিলম দোলরে এউ ফুগিয়াত নুলা পারিয়াতুর।"
        "এক্সেপ্টেউর সিন্ট অক্কাএকাত কুপিদাতাত নন প্রওইদেন্ত, সুন্ত ইন কুল্পা কুই অফফিকিয়া ডেসেরুন্ত মল্লিত আনিম ইদ এস্ত লাবরুম।"

    ],
    }
    }

    labels = dummy_responses['label_annotations'][language]

    return labels

def get_language():

    print("\nChoose an language to perform OCR:")
    print("1. English")
    print("2. Hindi")
    print("3. Punjabi")
    print("4. Bengali")
    print("5. Back\n")
    
    choice = input("Choose an option (1/2/3/4/5):")
    
    if choice == '1':
        return 'English'
    elif choice == '2':
        return 'Hindi'
    elif choice == '3':
        return 'Punjabi'
    elif choice == '4':
        return 'Bengali'
    elif choice == '5':
        return 'Back'
    else:
        print(dashes+"Invalid choice. Please enter (1/2/3/4)."+dashes)

    return get_language()

def perform_ocr(image_path):

    language = get_language()

    if language == 'Back':
        return
    ocr_inference = detected_text(image_path,language)

    print("\n")
    for label in ocr_inference:
        print("-",label,"\n")


def list_languages():
    """
    Get a list of supported languages with their language codes.

    Returns:
        list: A list of tuples containing language names and their corresponding language codes.
    """
    language_list = [
        ("1","English", "en"),
        ("2","Hindi", "hi"),
        ("3","Punjabi", "pa"),
        ("4","Bengali", "bn"),
        # Add more languages
    ]

    print(dashes+"Supported Languages:")
    for itr,language, code in language_list:
        print(f"{itr}. {language} ({code}) ")
    return language_list
    

def gcloud_ocr(image_path):

    print(dashes+"Choose an operation to perform:\n")
    print("1. List of available languages")
    print("2. Send for OCR")
    print("3. Restart Upload")
    print("4. Exit\n")

    
    choice = input("Enter your choice (1/2/3/4):")

    if choice == '1':
        list_languages()
    elif choice == '2':
        perform_ocr(image_path)
    elif choice == '3':
        return 'restart'
    elif choice == '4':
        return 
    else :
        print(dashes+"Invalid choice. Please enter (1/2/3/4)."+dashes)

    return gcloud_ocr(image_path)




