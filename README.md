# DevAgent - AI-Powered Terminal Development Assistant

DevAgent is an advanced terminal-based AI assistant specialized in full-stack application development. It leverages Google's Gemini AI to help developers build, modify, and manage web applications entirely through command-line interactions.

## Features

- **Full-Stack Development Support**: Create and manage React frontends, Express backends, and more
- **Intelligent Project Initialization**: Automatically set up project structures and dependencies
- **Context-Aware Code Generation**: Understands existing codebases and maintains consistency
- **Safe File Operations**: Read, write, and modify files with built-in safety measures
- **Command Execution**: Execute shell commands safely with output capture
- **Structured JSON Communication**: Clear, parseable interaction format

## Prerequisites

- Python 3.7+
- Node.js and npm (for JavaScript/React projects)
- Git (recommended)
- Google Gemini API key

## Installation

1. **Clone or download the script**
   ```bash
    git clone https://github.com/parasmunoli/Terminal-AI.git
   ```

2. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

   Ensure you have the following packages installed:
    ```plaintext 
    google-generative-ai
    python-dotenv
3. **Set up environment variables**
   Create a `.env` file in the same directory as the script:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Get your Gemini API key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

## Usage

### Starting DevAgent

```bash
python main.py
```

The assistant will start with a `>` prompt where you can enter your development requests.

### Example Commands

#### Initialize a new project
```
> Create a TODO app using html, css, and javascript
```

#### Add features to existing project
```
> Add a login feature to the existing html, css, and javascript project
> Implement a user authentication system in the javascript app
> Add and Delete tasks in the todo app
```

#### File operations
```
> Create a new file named `app.js` with the following content:
> console.log('Hello, World!');
> Write a function to fetch data from an API in `app.js`
> Read the contents of `app.js`
```

#### Project setup
```
> Initialize a todo app using HTML, CSS, and JavaScript
> Set up a Django project with PostgreSQL
> Create a Next.js app with TypeScript
```



### Tips for Better Results

- Be specific about your requirements
- Mention the technology stack you prefer
- Ask for clarification when responses seem unclear
- Use follow-up questions to refine implementations

## Limitations

- Requires internet connection for Gemini API calls
- Limited to terminal-based interactions
- Cannot handle GUI applications or browser-based testing
- Responses depend on Gemini API availability and rate limits

## License

This project is provided as-is for educational and development purposes. Please ensure compliance with Google's Gemini API terms of service.

## Support

For issues related to:
- **Gemini API**: Check [Google AI documentation](https://ai.google.dev/)
- **Python dependencies**: Refer to package documentation
- **Development tools**: Consult respective tool documentation

---

**Happy coding with DevAgent! 🚀**