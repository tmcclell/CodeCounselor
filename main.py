import os
import sys
import asyncio
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import AzureOpenAI
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv(override=True)  # Force override system environment variables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CodeCounselor",
    description="A humorous AI-powered web app that acts as a therapist for code",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    logger.warning("Static directory not found, skipping static file serving")

# Initialize Azure OpenAI client
try:
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    if not all([api_key, azure_endpoint, deployment_name]):
        raise ValueError("Missing required Azure OpenAI environment variables")
    
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint
    )
        
except Exception as e:
    logger.error(f"Failed to initialize Azure OpenAI client: {e}")
    client = None

# Pydantic models
class ChatRequest(BaseModel):
    message: str

def load_therapist_prompt():
    """Load the therapist prompt from the external file."""
    prompt_path = ".github/prompts/CompassionateTherapist.prompt.md"
    
    try:
        if os.path.exists(prompt_path):
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract the prompt content (skip the YAML frontmatter)
                if content.startswith('---'):
                    # Skip YAML frontmatter
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        base_prompt = parts[2].strip()
                    else:
                        base_prompt = content.strip()
                else:
                    base_prompt = content.strip()
                
                # Add the template placeholder for user input
                return base_prompt + "\n\nClient code:\n{user_input}"
        else:
            logger.warning(f"Prompt file not found at {prompt_path}, using fallback prompt")
            # Fallback prompt if file doesn't exist
            return """You are a compassionate but slightly dramatic therapist. Your client is a piece of code. Respond to the code as if it were a person in therapy. Be insightful, humorous, and supportive.

Client code:
{user_input}"""
            
    except Exception as e:
        logger.error(f"Error loading prompt file: {e}")
        # Fallback prompt on error
        return """You are a compassionate but slightly dramatic therapist. Your client is a piece of code. Respond to the code as if it were a person in therapy. Be insightful, humorous, and supportive.

Client code:
{user_input}"""

# Load the therapeutic prompt template from external file
THERAPIST_PROMPT = load_therapist_prompt()

async def generate_therapeutic_response(code: str) -> AsyncGenerator[str, None]:
    """Generate streaming therapeutic response for the given code."""
    try:
        prompt = THERAPIST_PROMPT.format(user_input=code)
        
        # Create chat completion with streaming
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a compassionate code therapist."},
                {"role": "user", "content": prompt}
            ],
            stream=True,
            temperature=0.8,
            max_tokens=1000,
            timeout=30  # Add explicit timeout
        )
        
        # Stream the response
        chunk_count = 0
        
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                chunk_count += 1
                content = chunk.choices[0].delta.content
                yield content
        
        if chunk_count == 0:
            logger.warning("No chunks received from Azure OpenAI")
            yield "🤔 Dr. CodeBot received your code but the response seems to be empty. This might be a configuration issue."
                
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        
        logger.error(f"Error generating response: {error_type}: {error_msg}")
        
        # Provide detailed error messages based on error type and content
        if "Connection error" in error_msg:
            yield "🔌 **Connection Error Detected**\n\n"
            yield "Dr. CodeBot is having trouble connecting to the Azure OpenAI service. This could be due to:\n\n"
            yield "• **Network connectivity issues** - Check your internet connection\n"
            yield "• **Firewall or proxy blocking** - Ensure Azure endpoints are accessible\n"
            yield "• **DNS resolution problems** - Verify the endpoint URL is correct\n"
            yield "• **SSL/TLS certificate issues** - Check if certificates are valid\n\n"
            yield f"**Current Configuration:**\n"
            yield f"• Endpoint: `{azure_endpoint}`\n"
            yield f"• Deployment: `{deployment_name}`\n"
            yield f"• API Version: `{api_version}`\n\n"
            yield "💡 **Troubleshooting Steps:**\n"
            yield "1. Run the advanced debugger: `python advanced_debug.py`\n"
            yield "2. Check Azure OpenAI service status\n"
            yield "3. Verify your network connection\n"
            yield "4. Test the endpoint in a browser or with curl"
            
        elif "401" in error_msg or "authentication" in error_msg.lower():
            yield "🔐 **Authentication Error**\n\n"
            yield "Dr. CodeBot's credentials appear to be invalid. Please check:\n\n"
            yield "• Your API key is correct and hasn't expired\n"
            yield "• The API key has proper permissions for the deployment\n"
            yield "• No extra spaces or characters in the API key\n\n"
            yield f"API Key length: {len(os.getenv('AZURE_OPENAI_API_KEY', ''))} characters"
            
        elif "404" in error_msg or "not found" in error_msg.lower():
            yield "🤖 **Deployment Not Found**\n\n"
            yield f"The deployment '{deployment_name}' doesn't seem to exist. Please verify:\n\n"
            yield "• The deployment name is spelled correctly\n"
            yield "• The deployment exists in your Azure OpenAI resource\n"
            yield "• The deployment is in the 'Succeeded' state\n\n"
            yield "You can check your deployments in the Azure Portal under your OpenAI resource."
            
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            yield "⏰ **Rate Limit Exceeded**\n\n"
            yield "Dr. CodeBot is being rate-limited. Please:\n\n"
            yield "• Wait a moment before trying again\n"
            yield "• Check your quota limits in Azure Portal\n"
            yield "• Consider upgrading your pricing tier if needed"
            
        elif "timeout" in error_msg.lower():
            yield "⏱️ **Request Timeout**\n\n"
            yield "The request to Azure OpenAI timed out. This might be due to:\n\n"
            yield "• High load on the Azure OpenAI service\n"
            yield "• Network latency issues\n"
            yield "• Large request taking too long to process\n\n"
            yield "Try again in a moment with a shorter code snippet."
            
        else:
            yield f"❌ **Unexpected Error**\n\n"
            yield f"Dr. CodeBot encountered an unexpected error:\n\n"
            yield f"**Error Type:** {error_type}\n"
            yield f"**Error Message:** {error_msg}\n\n"
            yield "Please check the server logs for more detailed information, or run the advanced debugger:\n"
            yield "`python advanced_debug.py`"

@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Welcome to CodeCounselor - Your AI Code Therapist",
        "docs": "/docs",
        "chat_endpoint": "/chat"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "azure_openai_configured": client is not None
    }

@app.get("/debug")
async def debug_info():
    """Detailed debug information endpoint."""
    return {
        "azure_openai": {
            "client_configured": client is not None,
            "endpoint": azure_endpoint,
            "deployment_name": deployment_name,
            "api_version": api_version,
            "api_key_length": len(os.getenv("AZURE_OPENAI_API_KEY", "")),
            "api_key_starts_with": os.getenv("AZURE_OPENAI_API_KEY", "")[:10] + "..." if os.getenv("AZURE_OPENAI_API_KEY") else None
        },
        "environment": {
            "python_version": sys.version,
            "openai_version": getattr(__import__("openai"), "__version__", "unknown")
        },
        "server": {
            "host": os.getenv("HOST", "0.0.0.0"),
            "port": os.getenv("PORT", 8000)
        }
    }

@app.post("/test-simple")
async def test_simple_request():
    """Test endpoint for simple Azure OpenAI request (non-streaming)."""
    if not client:
        raise HTTPException(
            status_code=500,
            detail="Azure OpenAI client not configured"
        )
    
    try:
        logger.info("Testing simple (non-streaming) request to Azure OpenAI")
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[{"role": "user", "content": "Say 'Hello from Dr. CodeBot!' in exactly those words."}],
            max_tokens=20,
            timeout=30,
            stream=False  # Explicitly disable streaming
        )
        
        result = {
            "status": "success",
            "response": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "model": response.model,
            "created": response.created
        }
        
        logger.info(f"Simple request successful: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Simple request failed: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "endpoint": azure_endpoint,
            "deployment": deployment_name,
            "api_version": api_version
        }

@app.post("/chat")
async def chat_with_therapist(request: ChatRequest):
    """
    Chat endpoint that accepts code snippets and returns streaming therapeutic responses.
    """
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="Azure OpenAI client not configured. Please check your environment variables."
        )
    
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide a code snippet for therapy."
        )
    
    logger.info(f"Received therapy request for code snippet of length: {len(request.message)}")
    
    return StreamingResponse(
        generate_therapeutic_response(request.message),
        media_type="text/plain"
    )

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
