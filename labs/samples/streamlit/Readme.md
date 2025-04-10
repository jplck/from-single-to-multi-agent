# Joke Bot - A Streamlit AI Demo

A simple and interactive Streamlit application that generates jokes on demand using Azure OpenAI services and Semantic Kernel.

## Overview

This application demonstrates how to build an AI-powered joke bot using:

- **Streamlit**: For the web interface
- **Semantic Kernel**: For orchestrating the AI capabilities
- **Azure OpenAI or GitHub Models**: For generating jokes and handling conversations

The bot uses a custom `JokePlugin` to create family-friendly jokes about any topic that the user provides.

## Features

- Interactive chat interface
- Real-time joke generation based on user input
- Family-friendly content
- Message history with reset capability
- Supports different joke styles (silly, clever, pun, etc.)

## Prerequisites

- Python 3.8+
- An Azure OpenAI account with API access or a GitHub personal access token for Azure AI Inference services
- Required Python packages (see Setup section)

## Setup

1. Install the required packages:
   ```bash
   pip install streamlit semantic-kernel python-dotenv
   ```

## Configuration

Create a `.env` file in the same directory as the application with the following variables:

### For Azure OpenAI:
```
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=your-endpoint-url
AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME=your-deployment-name
```

### For GitHub Token (Alternative):
```
GITHUB_TOKEN=your-github-personal-access-token
```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)
3. Enter a topic in the chat input field and press Enter
4. The application will generate a joke about your topic
5. Use the "Reset Messages" button to clear the chat history

## How It Works

1. The application initializes a Semantic Kernel instance with either Azure OpenAI or Azure AI Inference services
2. A custom `JokePlugin` is registered with the kernel to handle joke generation
3. A `ChatCompletionAgent` is created to manage the conversation
4. When a user inputs a topic, the agent processes it and generates a family-friendly joke
5. The chat history is maintained in the Streamlit session state

## Code Structure

- `init_chat_completion_service()`: Sets up the connection to Azure OpenAI or Azure AI Inference
- `JokePlugin`: A custom plugin with a `generate_joke` function
- `create_kernel()`: Creates and configures the Semantic Kernel
- `create_agent()`: Creates the joke-focused AI agent
- `invoke_agent()`: Handles sending user input to the agent and processing the response
- `run_app()`: The main Streamlit application logic

## Customization

- Modify the system prompt in `run_app()` to change the agent's personality
- Adjust the `JokePlugin.generate_joke()` method to customize joke styles
- Update the Streamlit UI elements in `run_app()` to change the application's appearance


## Acknowledgements

- This demo uses [Semantic Kernel](https://github.com/microsoft/semantic-kernel)
- Built with [Streamlit](https://streamlit.io/)
- Powered by Azure OpenAI or Azure AI Inference services