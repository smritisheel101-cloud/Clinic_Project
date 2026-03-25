"""
Streamlit UI for WellCare Plus Clinic
Imports the LangGraph graph directly (no API calls).
Run: streamlit run app.py
"""
import asyncio
import uuid
import streamlit as st
from langchain_core.messages import AIMessage
from graph.workflow import build_faq_only_workflow, build_workflow


def _extract_text(messages) -> str:
    """Extract text from the last AI message, handling Bedrock's list content format."""
    for msg in reversed(messages):
        if not isinstance(msg, AIMessage):
            continue
        content = msg.content
        if isinstance(content, str) and content.strip():
            return content
        if isinstance(content, list):
            parts = [b["text"] for b in content if isinstance(b, dict) and b.get("type") == "text"]
            if parts:
                return "\n".join(parts)
    return "I'm sorry, I couldn't generate a response. Please try again."

# --- Page Config ---
st.set_page_config(
    page_title="WellCare Plus Clinic",
    page_icon="🌿",
    layout="wide",
)

# --- Custom Header ---
st.markdown(
    "<h1 style='text-align: center; color: #2E8B57;'>🌿 WellCare Plus Clinic 🌿</h1>",
    unsafe_allow_html=True
)
st.markdown("<p style='text-align:center;color:gray;'>Your trusted partner in health and wellness</p>", unsafe_allow_html=True)

# --- Session State Init ---
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]
if "user_id" not in st.session_state:
    st.session_state.user_id = "demo_user"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "faq_only"
if "graph" not in st.session_state:
    st.session_state.graph = build_faq_only_workflow()
if "mcp_client" not in st.session_state:
    st.session_state.mcp_client = None


def connect_full_system():
    """Try to connect to Composio MCP and build the full multi-agent graph."""
    try:
        graph, client = asyncio.run(build_workflow())
        st.session_state.graph = graph
        st.session_state.mcp_client = client
        st.session_state.mode = "full"
        return True
    except Exception as e:
        st.error(f"Could not connect to MCP server: {e}")
        return False


# --- Sidebar ---
with st.sidebar:
    st.success("Welcome to WellCare Plus!")

    st.divider()

    # Mode selector
    st.subheader("Mode")
    if st.session_state.mode == "faq_only":
        st.info("FAQ Only (no MCP)")
        if st.button("Connect Full System"):
            with st.spinner("Connecting to Composio MCP..."):
                if connect_full_system():
                    st.success("Connected! Full system active.")
                    st.rerun()
    else:
        st.success("Full Multi-Agent System")

    st.divider()

    # User ID
    st.subheader("User")
    new_user = st.text_input("User ID", value=st.session_state.user_id)
    if new_user != st.session_state.user_id:
        st.session_state.user_id = new_user

    st.divider()

    # Session info
    st.subheader("Session")
    st.text(f"Thread: {st.session_state.thread_id}")
    st.text(f"User: {st.session_state.user_id}")

    if st.button("New Conversation"):
        st.session_state.thread_id = str(uuid.uuid4())[:8]
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("Try asking:")
    if st.session_state.mode == "full":
        st.markdown("""
        - 🌿 What are your clinic hours?
        - 🩺 I'd like to book an appointment
        - 👩‍⚕️ Which doctors are available?
        - 📋 What's the cancellation policy?
        - 📅 Book me with Dr. Chen tomorrow at 10 AM
        """)
    else:
        st.markdown("""
        - 🌿 What are your clinic hours?
        - 👩‍⚕️ Which doctors work here?
        - 📋 What's the cancellation policy?
        - 💳 Do you accept insurance?
        - 📍 Where is the clinic located?
        """)

    st.divider()
    st.caption("Powered by LangGraph + AWS Bedrock")

# --- Main Chat Area ---
if st.session_state.mode == "full":
    st.caption("💬 Ask questions, book appointments, or request confirmations. The supervisor routes automatically.")
else:
    st.caption("💬 Ask me anything about our clinic, doctors, policies, and services.")

# Display chat history with styled bubbles
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='background-color:#E0F7FA;padding:10px;border-radius:10px;margin:5px 0;text-align:right;'>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='background-color:#FFF3E0;padding:10px;border-radius:10px;margin:5px 0;text-align:left;'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(
        f"<div style='background-color:#E0F7FA;padding:10px;border-radius:10px;margin:5px 0;text-align:right;'>{prompt}</div>",
        unsafe_allow_html=True
    )

    # Get agent response
    config = {
        "configurable": {
            "thread_id": st.session_state.thread_id,
            "user_id": st.session_state.user_id,
        }
    }

    graph = st.session_state.graph

    with st.spinner("Thinking..."):
        if st.session_state.mode == "full":
            result = asyncio.run(graph.ainvoke(
                {"messages": [("user", prompt)]},
                config,
            ))
        else:
            result = graph.invoke(
                {"messages": [("user", prompt)]},
                config,
            )
        response = _extract_text(result["messages"])
        st.markdown(
            f"<div style='background-color:#FFF3E0;padding:10px;border-radius:10px;margin:5px 0;text-align:left;'>{response}</div>",
            unsafe_allow_html=True
        )

    st.session_state.messages.append({"role": "assistant", "content": response})

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align:center;color:gray;'>📞 Call us at 123-456-7890 | 📍 123 Wellness Street</p>", unsafe_allow_html=True)
