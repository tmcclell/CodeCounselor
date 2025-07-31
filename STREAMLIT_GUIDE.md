# Running CodeCounselor with Streamlit

## Overview
CodeCounselor now features a modern Streamlit frontend alongside the original HTML interface, providing enhanced user experience and better functionality.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

### 3. Start Both Applications

#### FastAPI Backend (Required)
```bash
python run_dev.py
```
The FastAPI backend will be available at: http://localhost:8000

#### Streamlit Frontend (New!)
```bash
streamlit run streamlit_app.py
```
The Streamlit frontend will be available at: http://localhost:8501

#### Original HTML Frontend (Still Available)
Visit: http://localhost:8000/static/index.html

## Features Comparison

| Feature | HTML Frontend | Streamlit Frontend |
|---------|---------------|-------------------|
| Code Input | Basic textarea | Syntax-highlighted editor |
| Response Display | Simple text | Markdown with streaming |
| Session History | None | Full chat history |
| Connection Status | None | Real-time status indicators |
| Debug Information | None | JSON debug panel |
| Mobile Responsive | Basic | Advanced |
| Configuration | None | Live API settings |

## Streamlit Frontend Features

### 🎨 Enhanced Code Editor
- Syntax highlighting with multiple themes
- Line numbers and code folding
- Auto-completion support
- Customizable editor settings

### 🔄 Real-time Streaming
- Live streaming of AI responses
- Visual loading indicators
- Proper error handling and recovery

### 💬 Session Management
- Complete chat history with timestamps
- Expandable session details
- Code snippet preservation
- Clear history functionality

### 🔧 Advanced Configuration
- Live connection status monitoring
- API endpoint configuration
- Debug information panel
- Health check utilities

### 📱 Mobile-Responsive Design
- Adaptive layout for all screen sizes
- Touch-friendly interface
- Optimized for tablets and phones

## API Endpoints Used

The Streamlit frontend communicates with the FastAPI backend through:

- `GET /health` - Connection and health status
- `GET /debug` - Detailed debug information
- `POST /chat` - Streaming therapeutic responses

## Development

### Running in Development Mode
Both frontends can run simultaneously for testing and comparison:

1. **FastAPI Backend**: `python run_dev.py` (port 8000)
2. **Streamlit Frontend**: `streamlit run streamlit_app.py` (port 8501)
3. **Original Frontend**: http://localhost:8000/static/index.html

### Hot Reloading
- FastAPI: Automatic reload on file changes
- Streamlit: Automatic reload on file save

## Deployment

### Streamlit Cloud (Recommended for Streamlit)
1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Set environment variables in Streamlit Cloud dashboard
4. Deploy automatically

### Traditional Deployment
- FastAPI: Use uvicorn with production settings
- Streamlit: Use streamlit run with production configuration

## Troubleshooting

### Connection Issues
1. Ensure FastAPI backend is running on port 8000
2. Check API endpoint URL in Streamlit sidebar
3. Use the "Check Connection" button for diagnostics
4. Review debug information for detailed error messages

### Azure OpenAI Issues
1. Verify credentials in .env file
2. Check endpoint URL and deployment name
3. Ensure proper API key permissions
4. Use the debug panel for configuration verification

## Migration from HTML Frontend

The Streamlit frontend is designed to be a drop-in replacement for the HTML frontend:

1. All existing functionality is preserved
2. API compatibility is maintained
3. Both frontends can coexist
4. No backend changes required

## Support

For issues specific to:
- **Streamlit Frontend**: Check the sidebar debug panel and connection status
- **FastAPI Backend**: Review server logs and /debug endpoint
- **Azure OpenAI**: Verify credentials and check service status