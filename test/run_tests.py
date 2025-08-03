#!/usr/bin/env python3
"""
Test runner for Terraform Bot tests
Run all tests and demos from a single entry point
"""
import os
import sys
import subprocess

def run_test(test_name, description):
    """Run a single test and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), test_name)
        ], cwd=os.path.dirname(os.path.dirname(__file__)), capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {test_name} PASSED")
            return True
        else:
            print(f"❌ {test_name} FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {test_name}: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 TERRAFORM BOT - TEST SUITE")
    print("=" * 60)
    print("Running all tests and demos...")
    
    tests = [
        ("test_questions.py", "Service-Organized Question System Test"),
        ("demo_workflow.py", "Complete Workflow Demo")
    ]
    
    passed = 0
    total = len(tests)
    
    for test_file, description in tests:
        if run_test(test_file, description):
            passed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests PASSED!")
        return 0
    else:
        print(f"❌ {total - passed} test(s) FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
