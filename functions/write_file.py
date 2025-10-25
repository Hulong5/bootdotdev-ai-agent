import os
from google import genai

schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Writes the contents that are passed in to the file that is also passed in",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The file that is to be changed within the working directory. if the file/path does not exist it will be created.",
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The contents that are to be written the the file.",
            )
        },
    ),
)


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
