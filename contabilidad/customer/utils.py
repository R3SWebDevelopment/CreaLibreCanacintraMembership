import re


def validate_rfc(rfc):
    pattern = "^([a-zA-Z]{3,4})([0-9]{6})([a-zA-Z0-9]{3})$"
    compile = re.compile(pattern=pattern, flags=re.I)
    result = compile.fullmatch(rfc)
    return result.string == rfc if result is not None else False
