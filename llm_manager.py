"""LLM manager for handling OpenAI API and LangChain interactions for Terraform Bot"""
import os
from langchain_openai import ChatOpenAI
from config import DEFAULT_MODEL, GPT4_MODEL, DEFAULT_TEMPERATURE, GPT4_TEMPERATURE


class LLMManager:
    def __init__(self):
        self.setup_openai_api()
        self._llm_cache = {}
    
    def setup_openai_api(self):
        """Setup OpenAI API key"""
        if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"]:
            api_key = input("Please enter your OpenAI API key: ").strip()
            os.environ['OPENAI_API_KEY'] = api_key
            print("✅ API key is set successfully!")
        else:
            print("✅ API key is already set. No need to reconfigure.")
        print("✅ API key is configured!")
    
    def get_llm(self, model_name=DEFAULT_MODEL, temperature=DEFAULT_TEMPERATURE):
        """Get LLM instance (cached) - Uses GPT-4.1 by default"""
        cache_key = f"{model_name}_{temperature}"
        if cache_key not in self._llm_cache:
            self._llm_cache[cache_key] = ChatOpenAI(model=model_name, temperature=temperature)
        return self._llm_cache[cache_key]
    
    def get_gpt4_llm(self):
        """Get GPT-4.1 LLM instance"""
        return self.get_llm(GPT4_MODEL, GPT4_TEMPERATURE)
    
    def get_default_llm(self):
        """Get default LLM instance (GPT-4.1)"""
        return self.get_llm(DEFAULT_MODEL, DEFAULT_TEMPERATURE)
    
    # Backward compatibility - now returns GPT-4.1
    def get_gpt35_llm(self):
        """Get LLM instance (now returns GPT-4.1 for compatibility)"""
        return self.get_default_llm()
