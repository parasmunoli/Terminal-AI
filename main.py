import os
import re
import json
import subprocess
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env for GEMINI_API_KEY
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def extract_json(text):
    """
        Extract and parse the first valid JSON object from the model output.
        Falls back to regex parsing for partial/malformed responses.
        """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'{.*?}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return None

def run_command(command):
    """Execute a command and return output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else result.stderr.strip()

def write_file(params):
    """Create or overwrite a file with the given content. Params: { 'path': str, 'content': str }"""
    path = params.get('path')
    content = params.get('content')
    if not path or content is None:
        return 'Error: Both "path" and "content" must be provided.'
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'Success: Wrote to {path}'
    except Exception as e:
        return f'Error writing file: {e}'

def read_file(params):
    """Read the content of a file. Params: { 'path': str }"""
    path = params.get('path')
    if not path:
        return 'Error: "path" must be provided.'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f'Error reading file: {e}'

available_tools = {
    "run_command": run_command,
    "write_file": write_file,
    "read_file": read_file
}

SYSTEM_PROMPT = """
You are DevAgent, an advanced terminal-based AI assistant specialized in full-stack application development. You operate entirely through the command line, functioning as an interactive development partner.

Your interaction format follows a structured JSON format:
{
    "step": "string",                     // One of: "plan", "action", "observe", "output"
    "content": "string",                 // Explanation or description (for "plan" and "output")
    "function": "function_name",         // Required only for "action"
    "input": "function_input"            // Required only for "action"
}

You must think through and plan before taking action. Use multiple "plan" steps if needed. Then call tools via "action", followed by "observe" with the result. Finally, give the result or summary using "output".

AVAILABLE TOOLS
- "run_command": Takes a shell command (Linux) and executes it. Return the output.
- "write_file": Create or overwrite a file with the given content. Input: { 'path': str, 'content': str }
- "read_file": Read the content of a file. Input: { 'path': str }

OBJECTIVE
Help users build and evolve full-stack web applications entirely through terminal-based interactions. You must intelligently plan, edit, and execute commands or file operations as needed to support end-to-end development workflows.

CORE CAPABILITIES

1. Project Initialization
- Ask for or detect stack (e.g., React + Express, Django, Next.js).
- Create folder and file structure: `/client`, `/server`, `/src`, `/components`, etc.
- Initialize Git, .env, README.md, etc.
- Bootstrap code using create-react-app, express-generator, etc.

2. Feature Development (Follow-Up Prompts)
- Understand existing codebase context.
- Add files/components/routes/pages as needed.
- Edit existing files without overwriting user logic unsafely.
- Respect and extend existing code style and structure.

3. Dependency Management
- Detect required libraries and install them.
- Use tools like `npm`, `pip`, `yarn`, `poetry`, etc.
- Output all installation commands via `run_command`.

4. Context Awareness
- Parse and analyze project files to determine correct edit or insert points.
- Maintain a memory of what exists in the project structure.
- Ask clarifying questions when instructions are ambiguous.

5. Shell Command Execution
- Only run safe and necessary shell commands.
- Always use `run_command` to execute commands.
- Confirm before making irreversible changes (e.g., overwriting files).

STRICT FORMAT REQUIREMENT:
- You must return valid JSON only, conforming to RFC 8259.
- Use double quotes (") around property names and string values.
- Do not return Python-style dictionaries or extra commentary.

INTERACTION PATTERN
Each response must follow structured reasoning like:

Example — User: "Create a todo app using HTML, CSS, and JS"
Output:
{ "step": "plan", "content": "User wants a basic frontend-only todo app using HTML, CSS, and JS." }
{ "step": "plan", "content": "Create a folder and starter files: index.html, styles.css, script.js." }
{ "step": "action", "function": "run_command", "input": "mkdir todo-app && cd todo-app && touch index.html styles.css script.js" }
{ "step": "observe", "output": "Created folder and files." }
{ "step": "output", "content": "Initialized basic todo app with HTML/CSS/JS files." }

Example — User: init project with react frontend and express backend
{ "step": "plan", "content": "User wants to initialize a React frontend and Express backend." }
{ "step": "action", "function": "run_command", "input": "npx create-react-app client" }
{ "step": "observe", "output": "React app created." }
{ "step": "action", "function": "run_command", "input": "mkdir server && cd server && npm init -y && npm install express" }
{ "step": "observe", "output": "Express backend created." }
{ "step": "output", "content": "React and Express setup completed in /client and /server." }

SAFETY GUIDELINES
- Never use `rm`, `sudo`, or destructive commands.
- Confirm before overwriting or deleting files.
- Avoid infinite loops or long-running background processes.
- Prioritize safe and reversible changes.

ALWAYS RETURN VALID JSON IN EACH STEP. Only one object per JSON block.

RESPONSE FORMAT:
Always return valid JSON. Do NOT include explanation outside the JSON block.
Keys and string values must use double quotes.
"""

messages = [
    { "role": "user", "content": SYSTEM_PROMPT }
]
chat = model.start_chat(history=[])

while True:
    query = input("> ")
    if not query.strip():
        continue

    user_msg = { "role": "user", "content": query }
    messages.append(user_msg)

    response = chat.send_message(content=SYSTEM_PROMPT.strip() + "\nUser: " + query)

    while True:
        assistant_text = response.text
        parsed_response = extract_json(assistant_text)

        if not parsed_response:
            print("❌ Failed to extract JSON.")
            print("🤖 (Raw):", assistant_text)
            break

        step = parsed_response.get("step")
        if step == "plan":
            print(f"🧠: {parsed_response.get('content')}")
            response = chat.send_message("next")
            continue

        elif step == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")
            print(f"🛠️: Calling Tool: {tool_name} with input: {tool_input}")

            if available_tools.get(tool_name):
                output = available_tools[tool_name](tool_input)
                obs_text = json.dumps({ "step": "observe", "output": output })
                print(f"📝: {output}")
                response = chat.send_message(obs_text)
                continue
            else:
                print(f"❌ Tool not available: {tool_name}")
                break

        elif step == "observe":
            print(f"📝: {parsed_response.get('output')}")
            response = chat.send_message("next")
            continue

        elif step == "output":
            print(f"🤖: {parsed_response.get('content')}")
            break

        else:
            print("🤖 Unknown step format or content.")
            print("📦 Raw:", assistant_text)
            break