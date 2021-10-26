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

    code_res = "INITIAL"
    try_time = 0
    while len(code_res) != 4:
        reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
        urllib.request.urlretrieve(path, (str(try_time) + "test.png"))

        result = reader.readtext(str(try_time) + "test.png")
        code_res = result[0][-2]
        try_time += 1
    return code_res


