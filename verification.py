import easyocr
import urllib.request


def easy_code_en(path):
    """ Function to output the verification code from url using easyOCR
        By Alan Liu [alan_squirrel@outlook.com]

    Args:
        path (string): URL of verification code

    Returns:
        string: verification code
    """
    reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
    urllib.request.urlretrieve(path, "test.png")

    result = reader.readtext("test.png")
    return result[0][-2]
