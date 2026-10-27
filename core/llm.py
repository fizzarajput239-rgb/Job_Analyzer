"""LLM factory: Groq ya Gemini, .env se select hota hai."""
import os
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider == "groq":
        from langchain_groq import ChatGroq
        if not os.getenv("GROQ_API_KEY"):
            raise RuntimeError("GROQ_API_KEY .env file mein set nahi hai.")
        return ChatGroq(model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"), temperature=0)

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        if not os.getenv("GOOGLE_API_KEY"):
            raise RuntimeError("GOOGLE_API_KEY .env file mein set nahi hai.")
        return ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), temperature=0)

    raise RuntimeError(f"Unknown LLM_PROVIDER '{provider}'. 'groq' ya 'gemini' use karein.")
