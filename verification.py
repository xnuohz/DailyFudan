import easyocr
from numpy.lib.npyio import save


def easy_code_en(code_response, save_name):
    """ Function to output the verification code from url using easyOCR
        By Alan Liu [alan_squirrel@outlook.com]

    Args:
        path (string): URL of verification code

    Returns:
        string: verification code
    """

    img_data = code_response.content
    newFile = open(save_name, "wb")
    newFile.write(img_data)
    newFile.close()
    # OCR reader
    reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
    result = reader.readtext(save_name)
    code_res = result[0][-2].replace(" ", "")

    return code_res
    