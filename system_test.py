#!/usr/bin/env python3
"""
🔥 HYPERCODE FULL SYSTEM TEST SUITE

Comprehensive testing of all components:
- Parser
- Compiler
- Type Checker
- IR & Backend
- API Server
- Documentation

Run: python system_test.py
"""

import sys
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# ============================================================================
# TEST CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent
HYPERCODE_CORE = PROJECT_ROOT / "hypercode-core"
TESTS_DIR = HYPERCODE_CORE / "tests"

# Ensure hypercode-core is in python path
sys.path.insert(0, str(HYPERCODE_CORE))

# ============================================================================
# TEST RESULTS TRACKING
# ============================================================================

class TestResults:
    """Track test results across all suites"""
    
    def __init__(self):
        self.suites = {}
        self.total_passed = 0
        self.total_failed = 0
        self.total_skipped = 0
        self.start_time = time.time()
    
    def add_suite(self, name: str, passed: int, failed: int, skipped: int = 0):
        """Add results from a test suite"""
        self.suites[name] = {
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'total': passed + failed + skipped
        }
        self.total_passed += passed
        self.total_failed += failed
        self.total_skipped += skipped
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time"""
        return time.time() - self.start_time
    
    def summary(self) -> str:
        """Generate summary"""
        elapsed = self.get_elapsed_time()
        total = self.total_passed + self.total_failed + self.total_skipped
        
        summary = f"\n{'='*70}\n"
        summary += f"HYPERCODE FULL SYSTEM TEST RESULTS\n"
        summary += f"{'='*70}\n\n"
        
        for suite_name, results in self.suites.items():
            status = "✅ PASS" if results['failed'] == 0 else "❌ FAIL"
            summary += f"{status} | {suite_name:<30} | {results['passed']}/{results['total']}\n"
        
        summary += f"\n{'─'*70}\n"
        summary += f"Total: {self.total_passed} passed, {self.total_failed} failed, {self.total_skipped} skipped\n"
        summary += f"Time: {elapsed:.2f}s\n"
        summary += f"Coverage Target: >85%\n"
        summary += f"{'='*70}\n"
        
        return summary

# ============================================================================
# TEST SUITE 1: PARSER TESTS
# ============================================================================

def test_parser() -> Tuple[int, int]:
    """Test HyperCode Parser"""
    print("\n🧪 TIER 1: PARSER TESTS")
    print("─" * 70)
    
    passed = 0
    failed = 0
    
    test_cases = [
        ("init(5);", "Basic init"),
        ("@init: q = QReg(2);", "V3 init with directive"),
        ("hadamard(q0);", "Single qubit gate"),
        ("cnot(q0, q1);", "Two qubit gate"),
        ("measure(q0);", "Measurement"),
        ("let x: int = 5;", "Variable declaration"),
        ("let q: qubit[2];", "Qubit array declaration"),
        ("# Comment\ninit(3);", "Comments"),
        ("init(5);\nhadamard(q0);\nmeasure(q0);", "Multi-statement"),
    ]
    
    try:
        from hypercode.parser.parser import HyperCodeParser
        
        for code, desc in test_cases:
            try:
                parser = HyperCodeParser(code)
                ast = parser.parse()
                print(f"  ✅ {desc:<30} PASS")
                passed += 1
            except Exception as e:
                print(f"  ❌ {desc:<30} FAIL: {str(e)[:50]}")
                failed += 1
    
    except Exception as e:
        print(f"  ❌ Parser import failed: {e}")
        failed = len(test_cases)
    
    return passed, failed

# ============================================================================
# TEST SUITE 2: COMPILER TESTS
# ============================================================================

def test_compiler() -> Tuple[int, int]:
    """Test HyperCode Compiler"""
    print("\n🔧 TIER 2: COMPILER TESTS")
    print("─" * 70)
    
    passed = 0
    failed = 0
    
    test_cases = [
        ("@init: q = QReg(2)", "V3 code generation"),
        ("@init: q = QReg(3)\n@hadamard: q[0]", "Quantum gates"),
        ("@init: q = QReg(2)\n@cnot: q[0], q[1]", "Multi-qubit gates"),
        ("@init: q = QReg(1)\n@init: c = CReg(1)\n@measure: q[0] -> c[0]", "Measurement operations"),
    ]
    
    try:
        from hypercode.parser.parser import HyperCodeParser
        from hypercode.compiler import compile_to_v3
        
        for code, desc in test_cases:
            try:
                parser = HyperCodeParser(code)
                ast = parser.parse()
                v3_code = compile_to_v3(ast)
                
                # Verify output is valid V3
                assert "@" in v3_code or "init" in v3_code.lower(), "Invalid V3 output"
                print(f"  ✅ {desc:<30} PASS")
                passed += 1
            except Exception as e:
                print(f"  ❌ {desc:<30} FAIL: {str(e)[:50]}")
                failed += 1
    
    except Exception as e:
        print(f"  ❌ Compiler import failed: {e}")
        failed = len(test_cases)
    
    return passed, failed

# ============================================================================
# TEST SUITE 3: TYPE CHECKER TESTS
# ============================================================================

def test_type_checker() -> Tuple[int, int]:
    """Test Type Checking System"""
    print("\n🛡️  TIER 3: TYPE CHECKER TESTS")
    print("─" * 70)
    
    passed = 0
    failed = 0
    
    try:
        from hypercode.ir.types import (
            QubitType, IntType, AnyType, QubitArrayType, 
            are_compatible, is_array_type, array_size
        )
        from hypercode.ir.type_checker import TypeChecker
        
        # Test 1: Type system exists
        try:
            assert QubitType() is not None
            assert IntType() is not None
            print(f"  ✅ Type system definition        PASS")
            passed += 1
        except Exception as e:
            print(f"  ❌ Type system definition        FAIL: {e}")
            failed += 1
        
        # Test 2: Type compatibility
        try:
            assert are_compatible(IntType(), IntType())
            assert are_compatible(AnyType(), IntType())
            print(f"  ✅ Type compatibility            PASS")
            passed += 1
        except Exception as e:
            print(f"  ❌ Type compatibility            FAIL: {e}")
            failed += 1
        
        # Test 3: Type checker initialization
        try:
            checker = TypeChecker()
            assert checker.symbols == {}
            assert checker.errors == []
            print(f"  ✅ Type checker initialization   PASS")
            passed += 1
        except Exception as e:
            print(f"  ❌ Type checker initialization   FAIL: {e}")
            failed += 1
        
        # Test 4: Gate arity detection
        try:
            checker = TypeChecker()
            assert checker.gate_arity('h') == 1
            assert checker.gate_arity('cx') == 2
            assert checker.gate_arity('ccx') == 3
            print(f"  ✅ Gate arity detection          PASS")
            passed += 1
        except Exception as e:
            print(f"  ❌ Gate arity detection          FAIL: {e}")
            failed += 1
        
        # Test 5: Array type detection
        try:
            t = QubitArrayType(5)
            assert is_array_type(t)
            assert array_size(t) == 5
            print(f"  ✅ Array type detection          PASS")
            passed += 1
        except Exception as e:
            print(f"  ❌ Array type detection          FAIL: {e}")
            failed += 1
    
    except Exception as e:
        print(f"  ❌ Type checker import failed: {e}")
        failed = 5
    
    return passed, failed

# ============================================================================
# TEST SUITE 4: IR & BACKEND TESTS
# ============================================================================

def test_ir_backend() -> Tuple[int, int]:
    """Test IR Lowering and Quantum Backend"""
    print("\n⚙️  TIER 4: IR & BACKEND TESTS")
    print("─" * 70)
    
    passed = 0
    failed = 0
    
    try:
        from hypercode.parser.parser import HyperCodeParser
        from hypercode.compiler import compile_to_v3
        from hypercode.interpreter.evaluator import evaluate
        
        # Test 1: Simple initialization
        try:
            code = "@init: q = QReg(2)"
            parser = HyperCodeParser(code)
            ast = parser.parse()
            v3_code = compile_to_v3(ast)
            result = evaluate(ast)
            assert result is not None
            print(f"  ✅ IR generation (init)          PASS")
            passed += 1
        except Exception as e:
            print(f"  ❌ IR generation (init)          FAIL: {str(e)[:40]}")
            failed += 1
        
        # Test 2: Hadamard gate
        try:
            code = "@init: q = QReg(1)\n@hadamard: q[0]\n@init: c = CReg(1)\n@measure: q[0] -> c[0]"
            parser = HyperCodeParser(code)
            ast = parser.parse()
            result = evaluate(ast)
            assert result is not None
            print(f"  ✅ Quantum gate execution        PASS")
            passed += 1
        except Exception as e:
            print(f"  ❌ Quantum gate execution        FAIL: {str(e)[:40]}")
            failed += 1
        
        # Test 3: CNOT gate
        try:
            code = "@init: q = QReg(2)\n@cnot: q[0], q[1]\n@init: c = CReg(2)\n@measure: q[0] -> c[0]"
            parser = HyperCodeParser(code)
            ast = parser.parse()
            result = evaluate(ast)
            assert result is not None
            print(f"  ✅ Multi-qubit gate (CNOT)       PASS")
            passed += 1
        except Exception as e:
            print(f"  ❌ Multi-qubit gate (CNOT)       FAIL: {str(e)[:40]}")
            failed += 1
    
    except Exception as e:
        print(f"  ❌ IR/Backend import failed: {e}")
        failed = 3
    
    return passed, failed

# ============================================================================
# TEST SUITE 5: API SERVER TESTS
# ============================================================================

def test_api_server() -> Tuple[int, int]:
    """Test API Server and HTTP Endpoints"""
    print("\n🌐 TIER 5: API SERVER TESTS")
    print("─ " * 70)
    
    passed = 0
    failed = 0
    
    try:
        import requests
        
        # Test 1: Server health check
        try:
            response = requests.get("http://127.0.0.1:8000/health", timeout=2)
            assert response.status_code == 200
            print(f"  ✅ Server health check           PASS")
            passed += 1
        except requests.exceptions.ConnectionError:
            print(f"  ⚠️  Server not running (skipped)")
            failed += 1
        except Exception as e:
            print(f"  ❌ Server health check           FAIL: {e}")
            failed += 1
        
        # Test 2: Compile endpoint
        try:
            payload = {
                "nodes": [
                    {"id": "1", "type": "init", "data": {"qubits": 2}},
                    {"id": "2", "type": "gate", "data": {"gate": "hadamard", "target": 0}},
                ],
                "edges": []
            }
            response = requests.post("http://127.0.0.1:8000/compile", json=payload, timeout=5)
            if response.status_code == 200:
                print(f"  ✅ Compile endpoint             PASS")
                passed += 1
            else:
                print(f"  ❌ Compile endpoint             FAIL: {response.status_code}")
                failed += 1
        except requests.exceptions.ConnectionError:
            print(f"  ⚠️  Server not running (skipped)")
            failed += 1
        except Exception as e:
            print(f"  ❌ Compile endpoint              FAIL: {str(e)[:40]}")
            failed += 1
    
    except ImportError:
        print(f"  ⚠️  requests library not installed (skipped)")
        failed = 2
    
    return passed, failed

# ============================================================================
# TEST SUITE 6: PYTEST SUITE
# ============================================================================

def test_pytest() -> Tuple[int, int]:
    """Run pytest test suite"""
    print("\n🧬 TIER 6: PYTEST COMPREHENSIVE SUITE")
    print("─" * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
            cwd=HYPERCODE_CORE,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse pytest output
        output = result.stdout + result.stderr
        
        # Extract counts
        if "passed" in output:
            import re
            match = re.search(r'(\d+) passed', output)
            if match:
                passed = int(match.group(1))
            else:
                passed = 0
            
            match = re.search(r'(\d+) failed', output)
            failed = int(match.group(1)) if match else 0
            
            # Display summary
            if failed == 0:
                print(f"  ✅ All pytest tests              PASS ({passed} tests)")
            else:
                print(f"  ⚠️  Pytest results: {passed} passed, {failed} failed")
                print(f"\n{output}")
            
            return passed, failed
        else:
            print(f"  ⚠️  Could not parse pytest output")
            return 0, 0
    
    except subprocess.TimeoutExpired:
        print(f"  ❌ Pytest timeout")
        return 0, 1
    except Exception as e:
        print(f"  ⚠️  Pytest execution failed: {e}")
        return 0, 1

# ============================================================================
# TEST SUITE 7: DOCUMENTATION TESTS
# ============================================================================

def test_documentation() -> Tuple[int, int]:
    """Verify documentation completeness"""
    print("\n📚 TIER 7: DOCUMENTATION TESTS")
    print("─" * 70)
    
    passed = 0
    failed = 0
    
    required_files = [
        ("README.md", "Project README"),
        ("CHANGELOG.md", "Change log"),
        ("docs/GETTING_STARTED.md", "Getting started guide"),
        ("docs/ARCHITECTURE.md", "Architecture docs"),
        ("CONTRIBUTING.md", "Contribution guide"),
    ]
    
    for filename, description in required_files:
        # Check in hypercode-core first (standard repo structure)
        filepath = HYPERCODE_CORE / filename
        if not filepath.exists():
             # Fallback to project root
             filepath = PROJECT_ROOT / filename
            
        if filepath.exists():
            # Check file has content
            content = filepath.read_text(encoding='utf-8')
            if len(content) > 100:
                print(f"  ✅ {description:<30} PASS")
                passed += 1
            else:
                print(f"  ❌ {description:<30} FAIL (empty or too small)")
                failed += 1
        else:
            print(f"  ❌ {description:<30} FAIL (missing)")
            failed += 1
    
    return passed, failed

# ============================================================================
# TEST SUITE 8: CODE QUALITY TESTS
# ============================================================================

def test_code_quality() -> Tuple[int, int]:
    """Test code quality metrics"""
    print("\n✨ TIER 8: CODE QUALITY TESTS")
    print("─" * 70)
    
    passed = 0
    failed = 0
    
    # Test 1: Check for type hints
    try:
        parser_file = HYPERCODE_CORE / "hypercode" / "parser" / "parser.py"
        content = parser_file.read_text()
        
        type_hints_count = content.count(": ")
        if type_hints_count > 20:
            print(f"  ✅ Type hints present            PASS ({type_hints_count} hints)")
            passed += 1
        else:
            print(f"  ❌ Type hints insufficient       FAIL")
            failed += 1
    except Exception as e:
        print(f"  ❌ Type hints check failed       FAIL: {e}")
        failed += 1
    
    # Test 2: Check for docstrings
    try:
        compiler_file = HYPERCODE_CORE / "hypercode" / "compiler.py"
        content = compiler_file.read_text()
        
        docstring_count = content.count('"""') // 2
        if docstring_count > 5:
            print(f"  ✅ Docstrings present            PASS ({docstring_count} docstrings)")
            passed += 1
        else:
            print(f"  ❌ Docstrings insufficient       FAIL")
            failed += 1
    except Exception as e:
        print(f"  ❌ Docstring check failed        FAIL: {e}")
        failed += 1
    
    # Test 3: Check for error handling
    try:
        evaluator_file = HYPERCODE_CORE / "hypercode" / "interpreter" / "evaluator.py"
        content = evaluator_file.read_text()
        
        try_blocks = content.count("try:")
        if try_blocks > 3:
            print(f"  ✅ Error handling present        PASS ({try_blocks} try blocks)")
            passed += 1
        else:
            print(f"  ❌ Error handling insufficient   FAIL")
            failed += 1
    except Exception as e:
        print(f"  ❌ Error handling check failed   FAIL: {e}")
        failed += 1
    
    return passed, failed

# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

def main():
    """Execute all test suites"""
    
    print("\n" + "="*70)
    print("🔥 HYPERCODE FULL SYSTEM TEST SUITE 🔥")
    print("="*70)
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project Root: {PROJECT_ROOT}")
    
    results = TestResults()
    
    # Run all test suites
    p1, f1 = test_parser()
    results.add_suite("Parser Tests", p1, f1)
    
    p2, f2 = test_compiler()
    results.add_suite("Compiler Tests", p2, f2)
    
    p3, f3 = test_type_checker()
    results.add_suite("Type Checker Tests", p3, f3)
    
    p4, f4 = test_ir_backend()
    results.add_suite("IR & Backend Tests", p4, f4)
    
    p5, f5 = test_api_server()
    results.add_suite("API Server Tests", p5, f5)
    
    p6, f6 = test_pytest()
    results.add_suite("Pytest Suite", p6, f6)
    
    p7, f7 = test_documentation()
    results.add_suite("Documentation Tests", p7, f7)
    
    p8, f8 = test_code_quality()
    results.add_suite("Code Quality Tests", p8, f8)
    
    # Print summary
    print(results.summary())
    
    # Determine pass/fail
    if results.total_failed == 0:
        print("✅ ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION!\n")
        return 0
    else:
        print(f"❌ {results.total_failed} TEST(S) FAILED - REVIEW REQUIRED\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
