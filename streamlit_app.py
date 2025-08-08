#!/usr/bin/env python3
"""
Streamlit frontend for CodeCounselor - AI Code Therapist
"""

import streamlit as st
import requests
import json
import time
from streamlit_ace import st_ace
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="CodeCounselor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
FASTAPI_BASE_URL = "http://localhost:8000"
DEFAULT_CODE = """# Paste your troubled code here...
def my_problematic_function():
    # This function doesn't work as expected
    pass
"""

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "api_status" not in st.session_state:
    st.session_state.api_status = "unknown"

def check_api_status() -> dict:
    """Check if FastAPI backend is running and healthy."""
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            st.session_state.api_status = "healthy"
            return health_data
        else:
            st.session_state.api_status = "unhealthy"
            return {"status": "unhealthy", "azure_openai_configured": False}
    except requests.exceptions.RequestException:
        st.session_state.api_status = "offline"
        return {"status": "offline", "azure_openai_configured": False}

def get_debug_info() -> Optional[dict]:
    """Get debug information from FastAPI backend."""
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/debug", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def stream_therapeutic_response(code: str):
    """Stream therapeutic response from FastAPI backend."""
    try:
        response = requests.post(
            f"{FASTAPI_BASE_URL}/chat",
            json={"message": code},
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            # Create a placeholder for streaming text
            response_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
                if chunk:
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                    time.sleep(0.02)  # Small delay for better visual effect
            
            # Final response without cursor
            response_placeholder.markdown(full_response)
            return full_response
        else:
            error_msg = f"Error {response.status_code}: {response.text}"
            st.error(error_msg)
            return error_msg
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Connection error: {str(e)}"
        st.error(error_msg)
        return error_msg

def main():
    """Main Streamlit application."""
    
    # Header
    st.title("🧠 CodeCounselor")
    st.markdown("### Your AI-Powered Code Therapist")
    st.markdown("Share your code with Dr. CodeBot and receive compassionate, humorous therapeutic advice!")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Settings & Status")
        
        # Check API status
        if st.button("🔄 Check Connection", type="secondary"):
            with st.spinner("Checking FastAPI backend..."):
                health_data = check_api_status()
        else:
            health_data = check_api_status()
        
        # Display connection status
        if st.session_state.api_status == "healthy":
            st.success("✅ Backend Connected")
            if health_data.get("azure_openai_configured"):
                st.success("✅ Azure OpenAI Configured")
            else:
                st.warning("⚠️ Azure OpenAI Not Configured")
        elif st.session_state.api_status == "unhealthy":
            st.error("❌ Backend Unhealthy")
        else:
            st.error("❌ Backend Offline")
            st.markdown("**Make sure to start FastAPI backend:**")
            st.code("python run_dev.py", language="bash")
        
        # API Configuration
        st.subheader("📡 API Configuration")
        api_url = st.text_input("FastAPI URL:", value=FASTAPI_BASE_URL)
        if api_url != FASTAPI_BASE_URL:
            st.warning("Custom API URL set. Click 'Check Connection' to test.")
        
        # Debug Information
        if st.checkbox("🐛 Show Debug Info"):
            debug_info = get_debug_info()
            if debug_info:
                st.json(debug_info)
            else:
                st.error("Could not fetch debug info")
        
        # Clear Chat History
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("💻 Code Input")
        
        # Code input using streamlit-ace for syntax highlighting
        code_input = st_ace(
            value=DEFAULT_CODE,
            language="python",
            theme="monokai",
            key="code_editor",
            height=300,
            font_size=14,
            tab_size=4,
            wrap=False,
            show_gutter=True,
            show_print_margin=True,
            annotations=None,
            placeholder="Paste your troubled code here... Dr. CodeBot is here to help! 🩺"
        )
        
        # Submit button
        submit_button = st.button("💊 Start Therapy Session", type="primary", use_container_width=True)
        
        # Keyboard shortcut hint
        st.caption("💡 Tip: Use Ctrl+Enter in the editor to quickly submit!")
    
    with col2:
        st.subheader("🗣️ Dr. CodeBot's Response")
        
        # Show current response
        if submit_button and code_input.strip():
            if st.session_state.api_status != "healthy":
                st.error("❌ Cannot start therapy session: Backend is not available")
            else:
                with st.spinner("🧠 Dr. CodeBot is analyzing your code..."):
                    response = stream_therapeutic_response(code_input)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "code": code_input,
                        "response": response,
                        "timestamp": time.time()
                    })
        
        elif submit_button and not code_input.strip():
            st.warning("⚠️ Please share some code with Dr. CodeBot first!")
        
        # If no current session, show welcome message
        if not submit_button:
            st.info("""
            👋 **Welcome to CodeCounselor!**
            
            Dr. CodeBot is ready to help you work through your coding challenges.
            
            **How it works:**
            1. Paste your code in the editor on the left
            2. Click "Start Therapy Session"
            3. Receive compassionate, humorous advice from Dr. CodeBot
            
            **Features:**
            - 🎨 Syntax highlighting for better code readability
            - 📱 Mobile-responsive design
            - 💬 Chat history to track your sessions
            - 🔄 Real-time streaming responses
            """)
    
    # Chat History Section
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("📜 Chat History")
        
        # Show recent sessions in reverse chronological order
        for i, session in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Session {len(st.session_state.chat_history) - i} - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session['timestamp']))}"):
                st.subheader("Code:")
                st.code(session["code"], language="python")
                st.subheader("Dr. CodeBot's Response:")
                st.markdown(session["response"])
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8em;'>
            Built with ❤️ and a lot of debugging sessions | 
            <a href="http://localhost:8000/docs" target="_blank">FastAPI Docs</a> | 
            <a href="http://localhost:8000/static/index.html" target="_blank">Original Frontend</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()