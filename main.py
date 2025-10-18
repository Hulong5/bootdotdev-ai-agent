import os, sys
from dotenv import load_dotenv 
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    args = sys.argv
    messages = [args[1]]
    if len(args) < 2:
        print("You need to provide a prompt")
        sys.exit(1)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def process_inputs(*args):
    return 




if __name__ == "__main__":
    main()
