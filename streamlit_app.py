#!/usr/bin/env python3
"""
CodeCounselor Streamlit Frontend

A modern Python-native frontend for CodeCounselor that provides an interactive
interface for code therapy sessions with streaming AI responses.
"""

import streamlit as st
import requests
import time
import json
from typing import Optional
import os
from streamlit_ace import st_ace

# Configure page
st.set_page_config(
    page_title="CodeCounselor - AI Code Therapist",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for CodeCounselor branding
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .stTextArea textarea {
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
    }
    
    .therapy-response {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        max-height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
        line-height: 1.6;
        font-size: 15px;
    }
    
    .connection-status {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 6px;
        margin: 8px 0;
    }
    
    .status-connected {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-disconnected {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .bot-message {
        background-color: #f1f8e9;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
DEFAULT_API_URL = "http://localhost:8000"

def get_api_url() -> str:
    """Get the API URL from session state or default."""
    return st.session_state.get('api_url', DEFAULT_API_URL)

def check_backend_health() -> dict:
    """Check if the FastAPI backend is healthy."""
    try:
        api_url = get_api_url()
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            return {"status": "healthy", "data": response.json()}
        else:
            return {"status": "error", "error": f"HTTP {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "error": "Connection failed - is the FastAPI server running?"}
    except requests.exceptions.Timeout:
        return {"status": "error", "error": "Request timeout"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def stream_chat_response(code: str) -> Optional[str]:
    """Send code to the FastAPI backend and stream the response."""
    try:
        api_url = get_api_url()
        response = requests.post(
            f"{api_url}/chat",
            json={"message": code},
            headers={"Content-Type": "application/json"},
            stream=True,
            timeout=30
        )
        
        if response.status_code != 200:
            return f"Error: HTTP {response.status_code} - {response.text}"
        
        # Create a placeholder for streaming response
        response_placeholder = st.empty()
        full_response = ""
        
        # Stream the response
        for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
            if chunk:
                full_response += chunk
                # Update the display in real-time
                response_placeholder.markdown(
                    f'<div class="therapy-response">{full_response}</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.01)  # Small delay for smooth streaming effect
        
        return full_response
        
    except requests.exceptions.ConnectionError:
        return "❌ **Connection Error**: Could not connect to FastAPI backend. Please ensure the server is running on the configured endpoint."
    except requests.exceptions.Timeout:
        return "⏰ **Timeout Error**: The request took too long to complete. Please try again."
    except Exception as e:
        return f"❌ **Unexpected Error**: {str(e)}"

def initialize_session_state():
    """Initialize session state variables."""
    if 'api_url' not in st.session_state:
        st.session_state.api_url = DEFAULT_API_URL
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'backend_status' not in st.session_state:
        st.session_state.backend_status = None

def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 CodeCounselor</h1>
        <p>Your AI-Powered Code Therapist - Now with Streamlit!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # API Configuration
        st.markdown("#### Backend Configuration")
        api_url = st.text_input(
            "FastAPI Backend URL",
            value=st.session_state.api_url,
            help="URL of the CodeCounselor FastAPI backend"
        )
        
        if api_url != st.session_state.api_url:
            st.session_state.api_url = api_url
            st.session_state.backend_status = None
            st.rerun()
        
        # Health Check
        if st.button("🔍 Check Backend Health"):
            with st.spinner("Checking backend connection..."):
                st.session_state.backend_status = check_backend_health()
                st.rerun()
        
        # Display connection status
        if st.session_state.backend_status:
            status = st.session_state.backend_status
            if status["status"] == "healthy":
                st.markdown(
                    '<div class="connection-status status-connected">✅ Backend Connected</div>',
                    unsafe_allow_html=True
                )
                if "data" in status and "azure_openai_configured" in status["data"]:
                    ai_status = "✅ Configured" if status["data"]["azure_openai_configured"] else "❌ Not Configured"
                    st.write(f"Azure OpenAI: {ai_status}")
            else:
                st.markdown(
                    f'<div class="connection-status status-disconnected">❌ {status["error"]}</div>',
                    unsafe_allow_html=True
                )
        
        # Instructions
        st.markdown("---")
        st.markdown("#### 📖 How to Use")
        st.markdown("""
        1. **Check Connection**: Ensure FastAPI backend is running
        2. **Enter Code**: Paste your code in the editor below
        3. **Start Therapy**: Click the button to get AI advice
        4. **View History**: See all your conversations in the chat history
        """)
        
        # Clear history
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💻 Share Your Code with Dr. CodeBot")
        
        # Code input using st_ace for syntax highlighting
        code_input = st_ace(
            placeholder="Paste your troubled code here... Dr. CodeBot is here to help! 🩺",
            language='python',
            theme='monokai',
            height=300,
            auto_update=False,
            font_size=14,
            show_gutter=True,
            show_print_margin=True,
            wrap=True,
            key="code_editor"
        )
        
        # Alternative fallback text area if ace doesn't work
        if not code_input:
            code_input = st.text_area(
                "Code Input (Fallback)",
                placeholder="Paste your troubled code here... Dr. CodeBot is here to help! 🩺",
                height=300,
                help="Enter your code here for therapeutic analysis"
            )
        
        # Submit button
        submit_button = st.button(
            "💊 Start Therapy Session",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        st.markdown("### 🗣️ Dr. CodeBot's Therapeutic Response")
        
        if submit_button:
            if not code_input or not code_input.strip():
                st.error("Please share some code with Dr. CodeBot first! 🩺")
            else:
                # Check backend status first
                health_check = check_backend_health()
                if health_check["status"] != "healthy":
                    st.error(f"Backend connection failed: {health_check['error']}")
                else:
                    with st.spinner("🧠 Dr. CodeBot is analyzing your code..."):
                        # Get streaming response
                        response = stream_chat_response(code_input)
                        
                        if response:
                            # Add to chat history
                            st.session_state.chat_history.append({
                                "timestamp": time.strftime("%H:%M:%S"),
                                "code": code_input,
                                "response": response
                            })
    
    # Chat History
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 💬 Therapy Session History")
        
        # Display chat history in reverse order (newest first)
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Session {len(st.session_state.chat_history) - i} - {chat['timestamp']}", expanded=(i == 0)):
                st.markdown(
                    f'<div class="chat-message user-message"><strong>👤 Your Code:</strong><br><pre><code>{chat["code"]}</code></pre></div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div class="chat-message bot-message"><strong>🧠 Dr. CodeBot:</strong><br>{chat["response"]}</div>',
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()