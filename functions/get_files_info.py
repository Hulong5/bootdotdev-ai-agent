import os


def get_files_info(working_directory, directory="."):
    try:
        response = ""

        abs_path_working_dir = os.path.abspath(working_directory)
        target_abs = os.path.abspath(
            os.path.join(abs_path_working_dir, directory))  # python
        if not (target_abs == abs_path_working_dir or target_abs.startswith(abs_path_working_dir + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
        if not os.path.isdir(target_abs):
            return f'Error: "{directory}" is not a directory\n'

        for file in os.listdir(target_abs):
            file_path = os.path.join(target_abs, file)
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            response += (f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n")
        return response
    except Exception as e:
        return f"Error: {e}\n"

# - README.md: file_size=1032 bytes, is_dir=False
# - src: file_size=128 bytes, is_dir=True
# - package.json: file_size=1234 bytes, is_dir=False
