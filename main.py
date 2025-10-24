import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'


def main():
    verbose, args = process_inputs(*sys.argv)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=args, config=genai.types.GenerateContentConfig(system_instruction=system_prompt),
    )

    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")
    print(response.text)


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
