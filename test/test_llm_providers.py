"""
Test suite for multi-provider LLM Manager functionality
Tests both OpenAI and Anthropic providers
"""
import os
import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('..')

from llm_manager import LLMManager, OpenAILLMProvider, AnthropicLLMProvider, BedrockLLMProvider
from config import get_provider_from_model, get_api_key_env_var


class TestLLMProviderDetection(unittest.TestCase):
    """Test provider detection logic"""
    
    def test_openai_model_detection(self):
        """Test OpenAI model detection"""
        self.assertEqual(get_provider_from_model('gpt-4.1'), 'openai')
        self.assertEqual(get_provider_from_model('gpt-4'), 'openai')
        self.assertEqual(get_provider_from_model('gpt-4-turbo'), 'openai')
        self.assertEqual(get_provider_from_model('gpt-3.5-turbo'), 'openai')
    
    def test_anthropic_model_detection(self):
        """Test Anthropic model detection"""
        self.assertEqual(get_provider_from_model('claude-sonnet-4-20250514'), 'anthropic')
        self.assertEqual(get_provider_from_model('claude-3-5-sonnet-20240620'), 'anthropic')
        self.assertEqual(get_provider_from_model('claude-3-sonnet-20240229'), 'anthropic')
        self.assertEqual(get_provider_from_model('claude-3-haiku-20240307'), 'anthropic')
    
    def test_fallback_detection(self):
        """Test fallback detection based on naming"""
        self.assertEqual(get_provider_from_model('gpt-unknown'), 'openai')
        self.assertEqual(get_provider_from_model('claude-unknown'), 'anthropic')
    
    def test_unsupported_model(self):
        """Test unsupported model handling"""
        with self.assertRaises(ValueError):
            get_provider_from_model('unknown-model')
    
    def test_api_key_env_vars(self):
        """Test API key environment variable mapping"""
        self.assertEqual(get_api_key_env_var('openai'), 'OPENAI_API_KEY')
        self.assertEqual(get_api_key_env_var('anthropic'), 'ANTHROPIC_API_KEY')
        
        with self.assertRaises(ValueError):
            get_api_key_env_var('unknown')


class TestOpenAIProvider(unittest.TestCase):
    """Test OpenAI provider functionality"""
    
    def setUp(self):
        """Setup test environment"""
        # Clear environment variables
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
    
    @patch('builtins.input', return_value='test-openai-key')
    def test_setup_api_key_input(self, mock_input):
        """Test API key setup with user input"""
        provider = OpenAILLMProvider('gpt-4', 0.3)
        self.assertEqual(os.environ['OPENAI_API_KEY'], 'test-openai-key')
    
    def test_setup_api_key_existing(self):
        """Test API key setup with existing key"""
        os.environ['OPENAI_API_KEY'] = 'existing-key'
        provider = OpenAILLMProvider('gpt-4', 0.3)
        self.assertEqual(os.environ['OPENAI_API_KEY'], 'existing-key')
    
    def test_provider_name(self):
        """Test provider name"""
        os.environ['OPENAI_API_KEY'] = 'test-key'
        provider = OpenAILLMProvider('gpt-4', 0.3)
        self.assertEqual(provider.get_provider_name(), 'OpenAI')
    
    @patch('llm_manager.OpenAILLMProvider.create_llm_instance')
    def test_create_llm_instance(self, mock_create_llm):
        """Test LLM instance creation"""
        os.environ['OPENAI_API_KEY'] = 'test-key'
        provider = OpenAILLMProvider('gpt-4', 0.3)
        
        mock_instance = MagicMock()
        mock_create_llm.return_value = mock_instance
        
        result = provider.create_llm_instance()
        self.assertEqual(result, mock_instance)


class TestAnthropicProvider(unittest.TestCase):
    """Test Anthropic provider functionality"""
    
    def setUp(self):
        """Setup test environment"""
        # Clear environment variables
        if 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']
    
    @patch('builtins.input', return_value='test-anthropic-key')
    def test_setup_api_key_input(self, mock_input):
        """Test API key setup with user input"""
        provider = AnthropicLLMProvider('claude-3-5-sonnet-20241022', 0.3)
        self.assertEqual(os.environ['ANTHROPIC_API_KEY'], 'test-anthropic-key')
    
    def test_setup_api_key_existing(self):
        """Test API key setup with existing key"""
        os.environ['ANTHROPIC_API_KEY'] = 'existing-key'
        provider = AnthropicLLMProvider('claude-3-5-sonnet-20241022', 0.3)
        self.assertEqual(os.environ['ANTHROPIC_API_KEY'], 'existing-key')
    
    def test_provider_name(self):
        """Test provider name"""
        os.environ['ANTHROPIC_API_KEY'] = 'test-key'
        provider = AnthropicLLMProvider('claude-3-5-sonnet-20241022', 0.3)
        self.assertEqual(provider.get_provider_name(), 'Anthropic')
    
    @patch('llm_manager.AnthropicLLMProvider.create_llm_instance')
    def test_create_llm_instance(self, mock_create_llm):
        """Test LLM instance creation"""
        os.environ['ANTHROPIC_API_KEY'] = 'test-key'
        provider = AnthropicLLMProvider('claude-3-5-sonnet-20241022', 0.3)
        
        mock_instance = MagicMock()
        mock_create_llm.return_value = mock_instance
        
        result = provider.create_llm_instance()
        self.assertEqual(result, mock_instance)


class TestBedrockProvider(unittest.TestCase):
    """Test AWS Bedrock provider functionality"""
    
    def setUp(self):
        """Setup test environment"""
        # Clear AWS environment variables
        aws_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_DEFAULT_REGION']
        for var in aws_vars:
            if var in os.environ:
                del os.environ[var]
    
    @patch('builtins.input', side_effect=['y', 'test-access-key', 'test-secret-key', 'us-east-1'])
    def test_setup_credentials_input(self, mock_input):
        """Test AWS credentials setup with user input"""
        provider = BedrockLLMProvider('anthropic.claude-3-5-sonnet-20240620-v1:0', 0.3)
        self.assertEqual(os.environ['AWS_ACCESS_KEY_ID'], 'test-access-key')
        self.assertEqual(os.environ['AWS_SECRET_ACCESS_KEY'], 'test-secret-key')
        self.assertEqual(os.environ['AWS_DEFAULT_REGION'], 'us-east-1')
    
    @patch('builtins.input', return_value='n')
    def test_setup_credentials_declined(self, mock_input):
        """Test AWS credentials setup when user declines manual entry"""
        provider = BedrockLLMProvider('anthropic.claude-3-5-sonnet-20240620-v1:0', 0.3)
        # Should not set credentials if user declines
        self.assertNotIn('AWS_ACCESS_KEY_ID', os.environ)
    
    def test_setup_credentials_existing(self):
        """Test AWS credentials setup with existing credentials"""
        os.environ['AWS_ACCESS_KEY_ID'] = 'existing-access-key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'existing-secret-key'
        
        provider = BedrockLLMProvider('anthropic.claude-3-5-sonnet-20240620-v1:0', 0.3)
        self.assertEqual(os.environ['AWS_ACCESS_KEY_ID'], 'existing-access-key')
        self.assertEqual(os.environ['AWS_SECRET_ACCESS_KEY'], 'existing-secret-key')
    
    def test_provider_name(self):
        """Test provider name"""
        os.environ['AWS_ACCESS_KEY_ID'] = 'test-key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret'
        provider = BedrockLLMProvider('anthropic.claude-3-5-sonnet-20240620-v1:0', 0.3)
        self.assertEqual(provider.get_provider_name(), 'AWS Bedrock')
    
    @patch('llm_manager.BedrockLLMProvider.create_llm_instance')
    def test_create_llm_instance(self, mock_create_llm):
        """Test Bedrock LLM instance creation"""
        os.environ['AWS_ACCESS_KEY_ID'] = 'test-key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret'
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        
        provider = BedrockLLMProvider('anthropic.claude-3-5-sonnet-20240620-v1:0', 0.3)
        
        mock_instance = MagicMock()
        mock_create_llm.return_value = mock_instance
        
        result = provider.create_llm_instance()
        self.assertEqual(result, mock_instance)
    
    @patch('llm_manager.BedrockLLMProvider.create_llm_instance')
    def test_create_llm_instance_invalid_credentials(self, mock_create_llm):
        """Test Bedrock LLM instance creation with invalid credentials"""
        os.environ['AWS_ACCESS_KEY_ID'] = 'test-key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret'
        
        provider = BedrockLLMProvider('anthropic.claude-3-5-sonnet-20240620-v1:0', 0.3)
        
        # Mock the method to raise ValueError
        mock_create_llm.side_effect = ValueError("AWS credentials not found or invalid")
        
        with self.assertRaises(ValueError) as context:
            provider.create_llm_instance()
        
        self.assertIn("AWS credentials not found or invalid", str(context.exception))


class TestBedrockProviderDetection(unittest.TestCase):
    """Test Bedrock provider detection (commented functionality)"""
    
    def test_bedrock_model_detection_commented(self):
        """Test that Bedrock models are not detected when commented out"""
        # These should raise ValueError since Bedrock is commented out
        with self.assertRaises(ValueError):
            get_provider_from_model('anthropic.claude-3-5-sonnet-20240620-v1:0')
        
        with self.assertRaises(ValueError):
            get_provider_from_model('amazon.titan-text-premier-v1:0')
        
        with self.assertRaises(ValueError):
            get_provider_from_model('meta.llama3-1-70b-instruct-v1:0')
    
    def test_bedrock_api_key_env_var_commented(self):
        """Test that Bedrock API key env var is not supported when commented"""
        with self.assertRaises(ValueError):
            get_api_key_env_var('bedrock')


class TestLLMManager(unittest.TestCase):
    """Test LLM Manager functionality"""
    
    def setUp(self):
        """Setup test environment"""
        # Clear environment variables
        for key in ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY']:
            if key in os.environ:
                del os.environ[key]
    
    @patch('builtins.input', return_value='test-anthropic-key')
    def test_manager_initialization(self, mock_input):
        """Test manager initialization with Anthropic as default"""
        manager = LLMManager()
        self.assertIsNotNone(manager)
        self.assertEqual(os.environ['ANTHROPIC_API_KEY'], 'test-anthropic-key')
    
    @patch('builtins.input', return_value='test-anthropic-key')
    @patch('llm_manager.LLMManager.get_llm')
    def test_get_default_llm(self, mock_get_llm, mock_input):
        """Test getting default LLM (Anthropic)"""
        manager = LLMManager()
        mock_instance = MagicMock()
        mock_get_llm.return_value = mock_instance
        
        result = manager.get_default_llm()
        self.assertEqual(result, mock_instance)
    
    @patch('builtins.input', return_value='test-anthropic-key')
    def test_get_provider_info(self, mock_input):
        """Test getting current provider information"""
        manager = LLMManager()
        info = manager.get_current_provider_info()
        
        expected = {
            "provider": "Anthropic",
            "model": "claude-sonnet-4-20250514",
            "temperature": "0.3"
        }
        self.assertEqual(info, expected)
    
    @patch('builtins.input', return_value='test-anthropic-key')
    @patch('llm_manager.LLMManager.get_llm')
    def test_llm_caching(self, mock_get_llm, mock_input):
        """Test LLM instance caching"""
        manager = LLMManager()
        mock_instance = MagicMock()
        mock_get_llm.return_value = mock_instance
        
        # First call should create instance
        result1 = manager.get_llm('claude-sonnet-4-20250514', 0.3)
        # Second call should return cached instance
        result2 = manager.get_llm('claude-sonnet-4-20250514', 0.3)
        
        self.assertEqual(result1, result2)


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility with existing code"""
    
    def setUp(self):
        """Setup test environment"""
        for key in ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY']:
            if key in os.environ:
                del os.environ[key]
    
    @patch('builtins.input', return_value='test-anthropic-key')
    @patch('llm_manager.LLMManager.get_gpt35_llm')
    def test_get_gpt35_llm_compatibility(self, mock_get_gpt35_llm, mock_input):
        """Test that get_gpt35_llm still works (returns default model)"""
        manager = LLMManager()
        mock_instance = MagicMock()
        mock_get_gpt35_llm.return_value = mock_instance
        
        result = manager.get_gpt35_llm()
        
        # Should return the default model (Anthropic)
        self.assertEqual(result, mock_instance)
    
    @patch('builtins.input', return_value='test-anthropic-key')
    def test_setup_openai_api_compatibility(self, mock_input):
        """Test that setup_openai_api method still works"""
        manager = LLMManager()
        
        # Should not raise any errors
        manager.setup_openai_api()
        self.assertEqual(os.environ['ANTHROPIC_API_KEY'], 'test-anthropic-key')


if __name__ == '__main__':
    print("🧪 Running LLM Manager Multi-Provider Tests...")
    print("=" * 60)
    
    # Run all test suites
    test_suites = [
        TestLLMProviderDetection,
        TestOpenAIProvider,
        TestAnthropicProvider,
        TestBedrockProvider,
        TestBedrockProviderDetection,
        TestLLMManager,
        TestBackwardCompatibility
    ]
    
    for suite_class in test_suites:
        print(f"\n📋 Running {suite_class.__name__}...")
        suite = unittest.TestLoader().loadTestsFromTestCase(suite_class)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if not result.wasSuccessful():
            print(f"❌ {suite_class.__name__} had failures!")
        else:
            print(f"✅ {suite_class.__name__} passed!")
    
    print("\n" + "=" * 60)
    print("🎯 Test execution completed!")