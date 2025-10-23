import os


def write_file(working_directory, file_path, content):
    wd_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(os.path.join(
        wd_abs, file_path))

    try:
        if not (target_abs == wd_abs or target_abs.startswith(wd_abs + os.sep)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(os.path.dirname(target_abs)):
            os.makedirs(os.path.dirname(target_abs))

        with open(target_abs, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written'
    except Exception as e:
        return f"Error {e}"
