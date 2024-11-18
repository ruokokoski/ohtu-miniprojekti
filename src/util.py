class UserInputError(Exception):
    pass

def validate_reference(data):
    if not data:
        raise UserInputError("Must have data")
    