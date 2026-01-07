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

def scanner_node(state):

    temp_dir= "temp"

    temp_path = os.path.join(temp_dir, "scanned_code")
    os.makedirs(temp_dir, exist_ok=True)


    with open(temp_path, "w") as f:
        f.write(state["code"])
    findings = run_semgrep_scan(temp_path)
    os.remove(temp_path)


    return {"semgrep_findings": findings, "iterations": 1}

def retrieval_node(state): #Retrieves relevant context from the RAG knowledge base

    findings = state.get("semgrep_findings", [])[:5]
    code_snippet = state.get("code", "")[:1000]

    query = ( f"Security vulnerabilities and remediation guidance related to the following findings:\n"
        f"{json.dumps(findings, indent=2)}\n\n"
        f"Code context:\n{code_snippet}")


    docs = retriever.invoke(query)


    if not docs:
        context = "No relevant vulnerability references found in the knowledge base."

        
    context ="\n\n---\n\n".join([f"{doc.page_content}\n(Source: {doc.metadata.get('source', 'KB')})" 
                for doc in docs])

    return {"retrieved_context": context}

def analysis_node(state):
    prompt = f"""
    Knowledge Base Context:

    {state['retrieved_context']}

    Semgrep Findings(raw):

    {json.dumps(state['semgrep_findings'], indent=2)}

    Code Analysis:

    {state['code']}

    Task: Produce  a professional vulnerability report in Markdown.
    Include:
    - Severity (Critical, High, Medium, Low, Informational)
    - Location (line numbers if possible)
    - Explanation with evidence  from KB
    - Proof-of-Concept if applicable
    - Remediation steps


    if no vulberabilities are present, state that.
    """
    response= llm.invoke([HumanMessage(content=prompt)])
    return {"report": response.content}

def decide_continue(state):
    if state["iterations"] >= config["max_iterations"]:
        return END
    return "retriever"


graph = StateGraph(AgentState)
graph.add_node("scanner", scanner_node)
graph.add_node("retrieval", retrieval_node)
graph.add_node("analysis", analysis_node)

graph.set_entry_point("scanner")
graph.add_edge("scanner", "retrieval")
graph.add_edge("retrieval", "analysis")
graph.add_conditional_edges("analysis", decide_continue)


agent = graph.compile()

def analyze_code(code: str):
    initial_state = {
        "code": code,
        "semgrep_findings": [],
        "retrieved_context": "",
        "report": "",
        "iterations": 0
    }
    result = agent.invoke(initial_state)
    return result["report"]