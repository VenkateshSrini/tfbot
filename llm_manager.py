"""LLM manager for handling multi-provider API interactions for Terraform Bot"""
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from config import (
    DEFAULT_MODEL, GPT4_MODEL, DEFAULT_TEMPERATURE, GPT4_TEMPERATURE,
    get_provider_from_model, get_api_key_env_var
)


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, model_name: str, temperature: float):
        self.model_name = model_name
        self.temperature = temperature
        self.setup_api_key()
    
    @abstractmethod
    def setup_api_key(self):
        """Setup API key for the provider"""
        pass
    
    @abstractmethod
    def create_llm_instance(self):
        """Create and return LLM instance"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the provider name"""
        pass


class OpenAILLMProvider(BaseLLMProvider):
    """OpenAI LLM provider implementation"""
    
    def setup_api_key(self):
        """Setup OpenAI API key"""
        env_var = get_api_key_env_var('openai')
        if env_var not in os.environ or not os.environ[env_var]:
            api_key = input("Please enter your OpenAI API key: ").strip()
            os.environ[env_var] = api_key
            print("✅ OpenAI API key is set successfully!")
        else:
            print("✅ OpenAI API key is already set. No need to reconfigure.")
    
    def create_llm_instance(self):
        """Create OpenAI LLM instance"""
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model=self.model_name, temperature=self.temperature)
        except ImportError:
            raise ImportError("langchain_openai is required for OpenAI models. Install with: pip install langchain-openai")
    
    def get_provider_name(self) -> str:
        return "OpenAI"


class AnthropicLLMProvider(BaseLLMProvider):
    """Anthropic LLM provider implementation"""
    
    def setup_api_key(self):
        """Setup Anthropic API key"""
        env_var = get_api_key_env_var('anthropic')
        if env_var not in os.environ or not os.environ[env_var]:
            api_key = input("Please enter your Anthropic API key: ").strip()
            os.environ[env_var] = api_key
            print("✅ Anthropic API key is set successfully!")
        else:
            print("✅ Anthropic API key is already set. No need to reconfigure.")
    
    def create_llm_instance(self):
        """Create Anthropic LLM instance"""
        try:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model=self.model_name, temperature=self.temperature)
        except ImportError:
            raise ImportError("langchain_anthropic is required for Anthropic models. Install with: pip install langchain-anthropic")
    
    def get_provider_name(self) -> str:
        return "Anthropic"


class LLMManager:
    """Enhanced LLM manager with multi-provider support"""
    
    def __init__(self):
        self._llm_cache: Dict[str, Any] = {}
        self._provider_cache: Dict[str, BaseLLMProvider] = {}
        self._setup_initial_provider()
    
    def _setup_initial_provider(self):
        """Setup the initial provider based on default model"""
        provider = self._get_provider(DEFAULT_MODEL)
        provider.setup_api_key()
        print("✅ API key is configured!")
    
    def _get_provider(self, model_name: str) -> BaseLLMProvider:
        """Get or create provider instance for the given model"""
        provider_type = get_provider_from_model(model_name)
        
        if provider_type not in self._provider_cache:
            if provider_type == 'openai':
                self._provider_cache[provider_type] = OpenAILLMProvider(model_name, DEFAULT_TEMPERATURE)
            elif provider_type == 'anthropic':
                self._provider_cache[provider_type] = AnthropicLLMProvider(model_name, DEFAULT_TEMPERATURE)
            else:
                raise ValueError(f"Unsupported provider: {provider_type}")
        
        return self._provider_cache[provider_type]
    
    def get_llm(self, model_name: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE):
        """Get LLM instance (cached) with automatic provider detection"""
        cache_key = f"{model_name}_{temperature}"
        
        if cache_key not in self._llm_cache:
            provider = self._get_provider(model_name)
            # Create a new provider instance with the specific temperature if different
            if temperature != provider.temperature:
                provider_type = get_provider_from_model(model_name)
                if provider_type == 'openai':
                    temp_provider = OpenAILLMProvider(model_name, temperature)
                elif provider_type == 'anthropic':
                    temp_provider = AnthropicLLMProvider(model_name, temperature)
                else:
                    raise ValueError(f"Unsupported provider: {provider_type}")
                
                # Don't setup API key again if already configured
                temp_provider.setup_api_key = lambda: None  # Skip API key setup
                self._llm_cache[cache_key] = temp_provider.create_llm_instance()
            else:
                self._llm_cache[cache_key] = provider.create_llm_instance()
        
        return self._llm_cache[cache_key]
    
    def get_gpt4_llm(self):
        """Get GPT-4 or equivalent LLM instance"""
        return self.get_llm(GPT4_MODEL, GPT4_TEMPERATURE)
    
    def get_default_llm(self):
        """Get default LLM instance"""
        return self.get_llm(DEFAULT_MODEL, DEFAULT_TEMPERATURE)
    
    # Backward compatibility
    def get_gpt35_llm(self):
        """Get LLM instance (returns default model for compatibility)"""
        return self.get_default_llm()
    
    def setup_openai_api(self):
        """Legacy method for backward compatibility"""
        self._setup_initial_provider()
    
    def get_current_provider_info(self) -> Dict[str, str]:
        """Get information about the current provider and model"""
        provider = self._get_provider(DEFAULT_MODEL)
        return {
            "provider": provider.get_provider_name(),
            "model": DEFAULT_MODEL,
            "temperature": str(DEFAULT_TEMPERATURE)
        }
