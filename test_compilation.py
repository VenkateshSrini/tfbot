#!/usr/bin/env python3
"""
Compilation and Import Test Script
Tests all modules and dependencies to ensure everything compiles correctly
"""
import sys
import os
import importlib.util

def test_import(module_name, file_path=None):
    """Test if a module can be imported successfully"""
    try:
        if file_path:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
        else:
            __import__(module_name)
        print(f"✅ {module_name}: Import successful")
        return True
    except Exception as e:
        print(f"❌ {module_name}: Import failed - {e}")
        return False

def test_syntax(file_path):
    """Test if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        compile(content, file_path, 'exec')
        print(f"✅ {os.path.basename(file_path)}: Syntax valid")
        return True
    except SyntaxError as e:
        print(f"❌ {os.path.basename(file_path)}: Syntax error - {e}")
        return False
    except Exception as e:
        print(f"❌ {os.path.basename(file_path)}: Error - {e}")
        return False

def main():
    """Run all compilation and import tests"""
    print("🔍 Testing Terraform Bot API - Compilation and Import Verification")
    print("=" * 70)
    
    # Test core dependencies
    print("\n📦 Testing Core Dependencies:")
    dependencies = [
        'fastapi', 'uvicorn', 'pydantic', 'os', 'sys', 'typing',
        'contextlib', 'tempfile', 'json'
    ]
    
    dep_results = []
    for dep in dependencies:
        dep_results.append(test_import(dep))
    
    # Test main project files syntax
    print("\n📝 Testing Python File Syntax:")
    project_files = [
        'tf-bot.py',
        'config.py',
        'llm_manager.py',
        'terraform_generator.py',
        'terraform_parser.py',
        'terraform_question_manager.py',
        'api/main.py',
        'api/models.py',
        'api/utils.py'
    ]
    
    syntax_results = []
    for file_path in project_files:
        if os.path.exists(file_path):
            syntax_results.append(test_syntax(file_path))
        else:
            print(f"⚠️  {file_path}: File not found")
            syntax_results.append(False)
    
    # Test API module imports
    print("\n🔌 Testing API Module Imports:")
    
    # Add paths for imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    api_dir = os.path.join(current_dir, 'api')
    sys.path.insert(0, current_dir)
    sys.path.insert(0, api_dir)
    
    api_modules = []
    
    # Test core modules
    core_modules = [
        'config', 'llm_manager', 'terraform_generator', 
        'terraform_parser', 'terraform_question_manager'
    ]
    
    for module in core_modules:
        api_modules.append(test_import(module))
    
    # Test API modules
    api_files = ['models', 'utils']
    for module in api_files:
        module_path = os.path.join(api_dir, f'{module}.py')
        if os.path.exists(module_path):
            api_modules.append(test_import(module, module_path))
        else:
            print(f"⚠️  {module}: File not found")
            api_modules.append(False)
    
    # Test main API app
    try:
        main_path = os.path.join(api_dir, 'main.py')
        if os.path.exists(main_path):
            api_modules.append(test_import('main_api', main_path))
        else:
            print("⚠️  main.py: File not found")
            api_modules.append(False)
    except Exception as e:
        print(f"❌ main.py: Import failed - {e}")
        api_modules.append(False)
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 40)
    
    total_deps = len(dependencies)
    passed_deps = sum(dep_results)
    print(f"Dependencies: {passed_deps}/{total_deps} passed")
    
    total_syntax = len(syntax_results)
    passed_syntax = sum(syntax_results)
    print(f"Syntax Tests: {passed_syntax}/{total_syntax} passed")
    
    total_imports = len(api_modules)
    passed_imports = sum(api_modules)
    print(f"Module Imports: {passed_imports}/{total_imports} passed")
    
    total_tests = total_deps + total_syntax + total_imports
    total_passed = passed_deps + passed_syntax + passed_imports
    
    print(f"\n🎯 Overall: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 All tests passed! The application is ready to run.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
