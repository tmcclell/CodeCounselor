# CodeCounselor

A humorous AI-powered web app that acts as a therapist for code. Submit your code snippets and receive compassionate, streaming responses from Azure OpenAI that help you work through your coding challenges with a therapeutic touch.

## Features

- **Code Therapy Sessions**: Submit code snippets and receive therapeutic advice from an AI counselor
- **Streaming Responses**: Real-time streaming responses from Azure OpenAI for immediate feedback
- **FastAPI Backend**: High-performance API built with FastAPI
- **Azure OpenAI Integration**: Powered by Azure's OpenAI service for reliable and scalable AI responses
- **Dual Frontend Options**:
  - **🆕 Streamlit Frontend**: Modern, feature-rich interface with syntax highlighting, chat history, and real-time status monitoring
  - **Classic HTML Frontend**: Simple, lightweight HTML/JS interface for basic interaction

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

### Quick Start (Recommended)
```bash
# Start FastAPI backend
python run_dev.py
```

Then choose your preferred frontend:

#### 🆕 Streamlit Frontend (Recommended)
```bash
# In a new terminal
streamlit run streamlit_app.py
```
- **URL**: http://localhost:8501
- **Features**: Syntax highlighting, chat history, real-time status, debug panel

#### Classic HTML Frontend
- **URL**: http://localhost:8000/static/index.html
- **Features**: Simple, lightweight interface

### Manual Setup
1. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the application**
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Streamlit Frontend: http://localhost:8501 (after running `streamlit run streamlit_app.py`)
   - HTML Frontend: http://localhost:8000/static/index.html

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
├── streamlit_app.py        # 🆕 Streamlit frontend
├── requirements.txt        # Python dependencies (updated with Streamlit)
├── .env                   # Environment variables (not in repo)
├── .env.example          # Environment variables template
├── run_dev.py            # Development server runner
├── STREAMLIT_GUIDE.md    # 🆕 Detailed Streamlit documentation
├── static/               # Classic HTML frontend
│   ├── index.html
│   └── style.css
└── README.md            # This file
```

## Streamlit Frontend Features

The new Streamlit frontend offers enhanced functionality:

### 🎨 Enhanced Code Editor
- **Syntax highlighting** with multiple themes (monokai, github, etc.)
- **Line numbers** and code folding
- **Multi-language support** (Python, JavaScript, etc.)
- **Keyboard shortcuts** (Ctrl+Enter to submit)

### 💬 Session Management
- **Chat history** with expandable sessions
- **Timestamp tracking** for all interactions
- **Code preservation** in conversation history
- **Clear history** functionality

### 🔧 Advanced Monitoring
- **Real-time connection status** indicators
- **API configuration** panel
- **Debug information** with detailed backend status
- **Health checks** with one-click testing

### 📱 Modern UI/UX
- **Responsive design** for mobile and desktop
- **Professional styling** with clean layouts
- **Loading indicators** and progress feedback
- **Error handling** with helpful troubleshooting

For detailed Streamlit documentation, see [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md).

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
