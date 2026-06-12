import streamlit as st
import sys
import os
import importlib.util
from pathlib import Path

# ============================================================================
# DYNAMIC IMPORT WORKAROUND
# ============================================================================
def load_module(module_name, file_path):
    """Load a module dynamically using importlib."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Load agent dynamically
agent_path = Path(__file__).parent / "src" / "agent.py"
agent_module = load_module("agent", agent_path)
ReActAgent = agent_module.ReActAgent

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="ReAct Research Copilot",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    h1 {
        color: #1f77b4;
        font-weight: 700;
    }
    h2 {
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("### 🔬 ReAct Research Copilot")
    st.markdown("---")
    
    st.markdown("#### 📚 About")
    st.info(
        "An AI research assistant using **ReAct** (Reasoning + Acting) "
        "combined with **RAG** to answer AI/ML research questions."
    )
    
    st.markdown("#### 🎯 How It Works")
    st.markdown("1. **Think** 🤔 - Plan search strategy\n"
                "2. **Search** 🔍 - Find documents\n"
                "3. **Read** 📖 - Extract info\n"
                "4. **Answer** 💬 - Synthesize response")
    
    st.markdown("#### 📊 Knowledge Base")
    st.metric("Documents", "36")
    
    st.markdown("#### 🔧 Tech Stack")
    st.markdown("- **LLM**: Groq (LLaMA 3.3 70B)\n"
                "- **Embeddings**: Sentence-Transformers\n"
                "- **Frontend**: Streamlit")
    
    st.markdown("---")
    st.markdown("**[GitHub](https://github.com/Akshay-Sharma354/ReAct_Research_Copilot)**")

# ============================================================================
# MAIN CONTENT
# ============================================================================
st.markdown("""
# 🔬 ReAct Research Copilot

**Your AI-Powered Research Assistant**

Ask questions about AI, machine learning, or research concepts.
""")

st.markdown("---")

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    with st.spinner("🤖 Initializing ReAct agent..."):
        try:
            st.session_state.agent = ReActAgent()
            st.session_state.agent_ready = True
        except Exception as e:
            st.error(f"❌ Failed to initialize: {str(e)}")
            st.session_state.agent_ready = False

# ============================================================================
# QUERY INPUT
# ============================================================================
st.markdown("### 💬 Ask Your Question")

col1, col2 = st.columns([0.85, 0.15])

with col1:
    user_query = st.text_input(
        "What would you like to know?",
        placeholder="e.g., What are transformers?",
        label_visibility="collapsed"
    )

with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

# ============================================================================
# PROCESS QUERY
# ============================================================================
if search_button and user_query:
    if not st.session_state.agent_ready:
        st.error("❌ Agent not ready. Please refresh.")
    else:
        with st.spinner("🔄 Searching..."):
            try:
                response = st.session_state.agent.query(user_query)
                
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_query
                })
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============================================================================
# DISPLAY CONVERSATION
# ============================================================================
st.markdown("---")
st.markdown("### 📖 Conversation")

if st.session_state.messages:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <strong>🧠 Your Question:</strong><br>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: #f0fff4; border-left: 4px solid #2ca02c; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <strong>🤖 Response:</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(message["content"])
else:
    st.info("👆 Start by asking a question above!")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    <p>🚀 Built with Streamlit | Powered by Groq</p>
</div>
""", unsafe_allow_html=True)