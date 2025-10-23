import os
from .config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(
            wd_abs, file_path))

        # python
        if not (target_abs == wd_abs or target_abs.startswith(wd_abs + os.sep)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if (f.read(1) == ""):
                file_content_string += f'[...File "{
                    file_path}" truncated at 10000 characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {e}"
