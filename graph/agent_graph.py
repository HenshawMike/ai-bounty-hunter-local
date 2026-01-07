from langgraph.graph import StateGraph , END
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from rag.retriever import get_retriever
from scanners.semgrep_scanner import  run_semgrep_scan
from typing import TypedDict, Annotated
import operator 
import yaml
import os
import json 

with open("config.yaml") as f:
    config = yaml.safe_load(f)

llm = ChatOllama(model=config["llm_model"], temperature=0.7) 

retriever = get_retriever()

class AgentState(TypedDict):
    code: str
    semgrep_findings: list
    retrieved_context: str 
    report: str
    iterations: Annotated[int, operator.add]
    