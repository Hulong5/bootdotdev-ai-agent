from google import genai
from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .run_python_file import run_python_file
from .write_file import write_file
from .config import WORKING_DIR

functions = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"calling function: {
              function_call_part.name}({function_call_part.args})")
    else:
        print(print(f" - Calling function: {function_call_part.name}"))
    kwargs = dict(function_call_part.args)
    kwargs["working_directory"] = WORKING_DIR
    if function_call_part.name in functions:
        result = functions[function_call_part.name](**kwargs)
        return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )
    else:
        return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknownfunction: {
                        function_call_part.name}"},
                )
            ],
        )
