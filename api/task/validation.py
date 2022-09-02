from api.core.validation import is_str, is_bool

def validate_title(val):
    return is_str(val) and len(val)

def validate_description(val):
    return is_str(val)

    
def validate_done(val):
    return is_bool(val)