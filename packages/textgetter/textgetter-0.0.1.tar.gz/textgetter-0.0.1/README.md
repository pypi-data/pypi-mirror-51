# textgetter 

[textgetter v0.0.1](https://pypi.org/project/textgetter/)

This python package can be used for extracting text from PDF/TIF,jpg and png files.


## How to use

### get output as txt files 

```python

from textgetter.gettxt import img_txt_extract
from textgetter.gettxt import tif_txt_extract
from textgetter.gettxt import pdf_txt_extract

if __name__ == "__main__":
    
    # use img_txt_extract for extracting text from images like jpg,png etc
    img_txt_extract('/home/user/test', '/home/user/output', ['jpeg','png'],ocr_path='C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe',
                    verbose=True)
    # use tif_txt_extract for extracting text from tif files
    tif_txt_extract('/home/user/test', '/home/user/output', verbose=True)
    # use pdf_txt_extract for extracting text from pdf files
    pdf_txt_extract('/home/user/test', '/home/user/output', verbose=True)

```

### get output as docx files 

```python

from textgetter.getdocx import img_txt_extract
from textgetter.getdocx import tif_txt_extract
from textgetter.getdocx import pdf_txt_extract

if __name__ == "__main__":

    # use img_txt_extract for extracting text from images like jpg,png etc
    img_txt_extract('/home/user/test', '/home/user/output', ['jpeg','png'], verbose=True)
    # use tif_txt_extract for extracting text from tif files
    tif_txt_extract('/home/user/test', '/home/user/output', ocr_path='C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe',
                    verbose=True)
    # use pdf_txt_extract for extracting text from pdf files
    pdf_txt_extract('/home/user/test', '/home/user/output', verbose=True)


```
### get output as csv files 

```python

from textgetter.getcsv import img_txt_extract
from textgetter.getcsv import tif_txt_extract
from textgetter.getcsv import pdf_txt_extract

if __name__ == "__main__":

   # use img_txt_extract for extracting text from images like jpg,png etc
    img_txt_extract('/home/user/test', '/home/user/output', ['jpeg','png'], verbose=True)
    # use tif_txt_extract for extracting text from tif files
    tif_txt_extract('/home/user/test', '/home/user/output', verbose=True)
    # use pdf_txt_extract for extracting text from pdf files
    pdf_txt_extract('/home/user/test', '/home/user/output', ocr_path='C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe',
                    verbose=True)


```
### get output as excel files 

```python

from textgetter.getexcel import img_txt_extract
from textgetter.getexcel import tif_txt_extract
from textgetter.getexcel import pdf_txt_extract

if __name__ == "__main__":

    # use img_txt_extract for extracting text from images like jpg,png etc
    img_txt_extract('/home/user/test', '/home/user/output', ['jpeg','png'], verbose=True)
    # use tif_txt_extract for extracting text from tif files
    tif_txt_extract('/home/user/test', '/home/user/output', verbose=True)
    # use pdf_txt_extract for extracting text from pdf files
    pdf_txt_extract('/home/user/test', '/home/user/output', verbose=True)


```

## Arguments 

#### img_txt_extract

* input_files_path - folder path for input files e.g., '/home/user/test'
* output_files_path - folder path for output files e.g., '/home/user/output'
* file_extensions - list of file extensions from input folder e.g., ['jpeg','png']
* ocr_path - path of tesseract ocr (Windows only) defualte.g., 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe' , if linux ignore this argument
* verbose - for printing logs e.g., True/False\

#### tif_txt_extract and pdf_txt_extract

* input_files_path - folder path for input files e.g., '/home/user/test'
* output_files_path - folder path for output files e.g., '/home/user/output'
* ocr_path - path of tesseract ocr (Windows only) e.g., 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe', if linux ignore this argument
* verbose - for printing logs e.g., True/False


## Requirements

This package uses poppler for reading pdf files, for windows platform poppler is included in the package but for linux we have to install it manually.

### How to install poppler

We can download poppler from [poppler](https://poppler.freedesktop.org/) 

OR

We can install poppler using below command 

```
sudo apt-get install python-poppler
```
### How to install tesseract ocr

This package uses tesseract for extracting text from files, we have to install it manually for both windows and linux platforms.

Use this [link](https://digi.bib.uni-mannheim.de/tesseract/) to install tesseract ocr for Windows OS

Use below command for Linux OS

```
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```