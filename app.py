import streamlit as st
from graph.agent_graph import analyze_code
from utils.file_handler import cleanup_temp
import os

st.set_page_config(page_title="Local AI Bug Hunter", layout="wide")
st.title("🔒 Local AI Bug Hunter – Agentic RAG Edition (Jan 2026)")

st.info("Fully offline • deepseek-r1:8b + Semgrep + RAG • Ethical use only")

code_input = st.text_area("Paste source code here", height=400, placeholder="Enter code to scan...")
uploaded = st.file_uploader("Or upload a file", type=["py", "js", "java", "cpp", "go", "c", "php"])

if uploaded:
    code_input = uploaded.read().decode("utf-8")

if st.button("🚀 Scan for Vulnerabilities") and code_input.strip():
    with st.spinner("Agent running hybrid analysis (Semgrep → RAG → LLM)..."):
        cleanup_temp()
        report = analyze_code(code_input)
    st.success("Analysis Complete!")
    st.markdown("### 📊 Vulnerability Report")
    st.markdown(report)

st.caption("Built with Ollama, LangGraph, Chroma, and Semgrep • January 2026")