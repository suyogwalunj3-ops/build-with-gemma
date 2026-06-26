from math import log
import sys
import ollama

MODEL_NAME="gemma4:e4b"

def build_promt(log_content):
    return f"""
    You are an expert at analyzing logs files and analyzing the errors.
    Analyze the following exception stack trace and provide a summary of the error.
    {log_content}
    
    ##Root Cause
    ## Likely Failing File or Function
    ## Immediate Fix
    ## Commands to Try
    ## Prevention
    ## Severity

    Rules:
    - Be concise and focused.
    - Do not invent file names or line numbers.
    - If information is missing, clearly state what is missing.
    """

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python log_error.py <log_file>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    
    with open(log_file, "r") as f:
        log_content = f.read()
    
    prompt = build_promt(log_content)
    print(f"Prompt: {prompt}")
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        stream=False,
    )
    
    print(response["message"]["content"])
