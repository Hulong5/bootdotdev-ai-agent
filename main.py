import os
import sys
from dotenv import load_dotenv
from google import genai
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
from functions.prompt import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content,
    ]
)


def main():
    verbose, messages = process_inputs(*sys.argv)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )

    for content in response.content:
        messages.append(content)

    user_prompt = " ".join(messages)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    for function_call in response.function_calls:
        function_response = call_function(function_call, verbose)

    try:
        if verbose:
            print(
                function_response.parts[0].function_response.response["result"])
    except Exception as e:
        raise Exception(e)


def process_inputs(*args):

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    return verbose, args


if __name__ == "__main__":
    main()
