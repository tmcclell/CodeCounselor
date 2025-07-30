# CodeCounselor

A humorous AI-powered web app that acts as a therapist for code. Submit your code snippets and receive compassionate, streaming responses from Azure OpenAI that help you work through your coding challenges with a therapeutic touch.

## Features

- **Code Therapy Sessions**: Submit code snippets and receive therapeutic advice from an AI counselor
- **Streaming Responses**: Real-time streaming responses from Azure OpenAI for immediate feedback
- **FastAPI Backend**: High-performance API built with FastAPI
- **Azure OpenAI Integration**: Powered by Azure's OpenAI service for reliable and scalable AI responses
- **Simple Frontend**: Basic HTML/JS interface for easy interaction

## Prerequisites

- Python 3.8 or higher
- Azure OpenAI account and API credentials
- Git (for cloning the repository)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tmcclell/CodeCounselor.git
   cd CodeCounselor
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Environment Configuration

Create a `.env` file in the root directory with your Azure OpenAI credentials:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI resource endpoint | `https://my-openai.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | `abc123...` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Name of your deployed model | `gpt-4` |
| `AZURE_OPENAI_API_VERSION` | API version to use | `2024-02-15-preview` |

## Running the Application

1. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the application**
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Frontend (if available): http://localhost:8000/static/index.html

## API Usage

### Chat Endpoint

**POST** `/chat`

Send a code snippet for therapeutic analysis.

#### Request Body
```json
{
  "message": "def broken_function():\n    return 'help me'"
}
```

#### Response
Streaming plain text response with therapeutic advice for your code.

#### Example using curl
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "def my_function():\n    pass  # I don'\''t know what to do here"}'
```

## Project Structure

```
CodeCounselor/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (not in repo)
├── .env.example          # Environment variables template
├── static/               # Frontend files (optional)
│   ├── index.html
│   └── style.css
└── README.md            # This file
```

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --log-level debug
```

### Testing the API

You can test the API using the interactive documentation at `http://localhost:8000/docs` or with tools like curl, Postman, or HTTPie.

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure your virtual environment is activated and dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Azure OpenAI API Error**: Verify your `.env` file has the correct credentials and your Azure OpenAI resource is properly configured

3. **Port Already in Use**: Change the port in the uvicorn command
   ```bash
   uvicorn main:app --reload --port 8001
   ```

### Debug Mode

Run with debug logging to see detailed error messages:
```bash
uvicorn main:app --reload --log-level debug
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- Inspired by the need for therapeutic coding support
