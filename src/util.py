import re

class UserInputError(Exception):
    pass

def validate_reference(reference):
    if len(reference.author) == 0:
        raise UserInputError("Must have author.")

    if len(reference.title) < 2:
        raise UserInputError("Title must be at least 2 characters long")

    if len(reference.title) > 100:
        raise UserInputError("Title must be under 100 characters long")

    if not reference.year.isdigit() or not 1000 <= int(reference.year) <= 9999:
        raise UserInputError("Year must be a valid 4-digit number between 1000 and 9999")

def generate_key(author, year, title):
    surname = author.split(", ")[0]
    first_word = re.sub(r'[^a-zA-Z]', '', title.split()[0])
    return f"{surname}{year}{first_word}"
