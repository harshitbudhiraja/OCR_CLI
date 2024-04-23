<h2 align="center">OCR CLI Utility</h2>

## 📝 Table of Contents

- [About](#context)
- [Requirements](#requirements)
- [Quick Start](#quick_start)
- [Description](#description)
- [Error Handling](#error_handling)
- [Authors](#authors)


## About: <a name = "context"></a>
<p align="center">
This is a cli utility, which provides functionality for Optical Character Recognition (OCR) tasks on .jpg and .pdf files. Users can choose between Google Cloud Vision's OCR API (GCP) or Lipikar (IITD Internal) for OCR processing.
<br>
</p>

## Requirements: <a name = "requirements"></a>
1. You’ll need to have [Python >= 3.7](https://www.python.org/downloads/) on your machine.
2. Your user credentials to be set up by the lab mantaining [Lipikar,IITD](https://mail.google.com/mail/u/0/#inbox?compose=new)

## Quick Start: <a name = "quick_start"></a>

1: Clone the repository:
``` bash
git clone https://github.com/your-username/ocr_cli.git
```

2: Navigate to the repository directory:
``` bash
cd ocr_cli
```

3: Add virtual environment 
``` bash
python3 -m venv venv
```

4: Activate the virtual environment
``` bash
source venv/bin/activate
```

5: Install dependencies:
``` bash
pip install -r requirements.txt
```

6: Run the CLI utility:
``` bash
python main.py
```

7: Run the CLI utility with particular OCR Engine: (Lipikar/Google Cloud Vision): 
``` bash
python main.py --engine lipikar 
python main.py --engine gcv 
```



After running the script, the CLI utility prompts users to choose between Google Cloud Vision and Lipikar for OCR processing. Users then provide the file path for the image or PDF to be processed. Progress status is displayed during processing, and upon completion. 


## Brief Description <a name = "description"></a>

Once the user selects among the available options for OCR provided required to choose between an API Engine, Lipikar.

A set of APIs is running at http://lipikar.apps.iitd.ac.in/api

| LIPIKAR APIS                      |                                                                            |
| --------------------------------- | -------------------------------------------------------------------------- |
| Login                             | Log in with your credentials to obtain Access and Refresh Tokens.          |
| Refresh                           | Obtain a new access token using the Refresh Token upon expiration          |
| Get Modules Config                | Get the available document_parsers and text_recognizers.                   |
| Upload New                        | Upload a new file for OCR                                                  |
| Get Upload Processing Status      | See how much of the Upload has been processed.                             |
| Get Upload Detail                 | Get a single upload – only call this once the upload has been processed    |
| Get All Detections For Upload     | Get all the detection objects corresponding to an upload.                  |


Note: For URDU, there are only `Line Level Parsers`.
Upon completion, the upload details and OCR detections are stored in uploadDetails.json and detections.json respectively.



## Error Handling <a name = "error_handling"></a>

WIP


## Further Improvements (WIP) <a name = "improvements"></a>

1. `Logger class` with log handlers at abover certain levels (as per future requirements)
2. Installation with `flake8` for linting and `black` for python code formatting 
3. Pre-commit configuration
4. UI Enhancements with `CLI formatting` library 
5. Better and Robust `error handling`. 



## ✍️ Authors <a name = "authors"></a>
[Harshit Budhiraja](https://github.com/harshitbudhiraja)

