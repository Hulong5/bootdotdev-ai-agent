import os
import sys
from dotenv import load_dotenv
from google import genai
from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)


def main():
    verbose, args = process_inputs(*sys.argv)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=args, config=genai.types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )

    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text
    # print(response.text)
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")


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
