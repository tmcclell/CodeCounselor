---
applyTo: '**'
---
Project Goal
Create a humorous AI-powered web app that acts as a therapist for code. The app should accept code snippets from users and return streaming responses from Azure OpenAI using a therapist-style prompt.

Set up the project
- Create a new Python project using FastAPI.
- Add a requirements.txt file with dependencies: fastapi, uvicorn, openai, python-dotenv, and httpx.

Create the FastAPI app
-Build a /chat POST endpoint that accepts a JSON payload with a message field.
-Use Azure OpenAI’s ChatCompletion API with stream=True to return a streaming response.
-Use a prompt template that makes the AI respond like a compassionate therapist for code.
-Use an existing Azure Open AI endpoint identified in the .env file.
-Load API credentials and endpoint from environment variables using dotenv.
-Use the openai.AzureOpenAI client to connect to the Azure endpoint.

Implement streaming
-Use FastAPI’s StreamingResponse to stream the LLM’s output token-by-token.
-Ensure the response is returned as plain text.
-Add a simple frontend (optional)
-Create a basic HTML/JS page or use Streamlit to send code snippets and display the streamed response.

Add a README
-Include setup instructions, environment variable configuration, and how to run the app locally.
