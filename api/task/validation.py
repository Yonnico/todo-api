from api.core.validation import is_str, is_bool

def validate_title(val):
    return val != None and is_str(val) and len(val)


def validate_description(val):
    return val != None and is_str(val) and len(val)

    
def validate_done(val):
    return val != None and is_bool(val)