def validate_todo(todo,is_done):
    errors = []
    if is_done is None:
        errors.append('is done required')
    else:
        if is_done not in ['0','1']:
            errors.append('is_done must be 0 or 1')
    
    if todo is None:
        errors.append('todo is required')

    if len(errors) > 0:
        return {'errors': errors}
    
class ValidateError(Exception):
    def __init__(self, message):
        super().__init__(message)


import json


def validate_todo_error(todo, is_done):
    """
    Fungsi ini digunakan untuk validasi todo dan is_done
    menggunakan ValidateError dan akan mengembalikan error
    jika ada error cukup tangkap menggunakan try except ValidateError
    lalu di return saja contohnya ada pada route create

    """
    errors = []

    # Jika is done tidak ada isinya
    if is_done is None:
        errors.append("is_done is required")
    # Else: Jika is done ada isinya
    else:
        # Cek lagi isinya 0 atau 1
        if is_done not in ["0", "1"]:
            errors.append("is_done must be 0 or 1")

    if todo is None:
        errors.append("todo is required")

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))