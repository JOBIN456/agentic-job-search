from langchain_core.documents.base import Blob
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os
import json
from typing import TypedDict, List, Dict, Any

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=groq_api_key,
    temperature=0
)

class JobfetchState():
    document:any
    resume_json: dict
    path_to_pdf:str
    name:str
