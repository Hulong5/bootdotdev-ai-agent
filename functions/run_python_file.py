import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    wd_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(os.path.join(
        wd_abs, file_path))

    if not (target_abs == wd_abs or target_abs.startswith(wd_abs + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_abs):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(
            ['python3', file_path] + args, cwd=wd_abs, capture_output=True, timeout=30)
        return_string = f'STDOUT: {completed_process.stdout.decode('utf-8')} STDERR: {
            completed_process.stderr.decode('utf-8')}'

        if completed_process.returncode != 0:
            return_string += f' Process exited with code {
                completed_process.returncode}'

        if completed_process.stdout == "":
            return_string = 'No output produced.'

        return return_string
    except Exception as e:
        return f'Error: {e}'
