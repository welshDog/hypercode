#!/bin/bash
# 🚀 HyperCode ANTLR Setup Script
# Automates grammar generation and validation
# Usage: bash setup_antlr.sh

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🔥 HYPERCODE ANTLR GRAMMAR SETUP SCRIPT 🔥               ║"
echo "║  Automated Grammar Generation & Validation                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# =============================================================================
# STEP 1: CHECK PREREQUISITES
# =============================================================================

echo "📋 STEP 1: Checking Prerequisites..."

# Check for Java
if ! command -v java &> /dev/null; then
    echo "❌ Java not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install openjdk
    else
        sudo apt-get update && sudo apt-get install -y default-jdk
    fi
else
    JAVA_VERSION=$(java -version 2>&1 | head -1)
    echo "✅ Java found: $JAVA_VERSION"
fi

# Check for ANTLR
if ! command -v antlr4 &> /dev/null; then
    echo "❌ ANTLR4 not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install antlr
    else
        echo "⚠️  Manual installation needed for Linux."
        echo "    Visit: https://www.antlr.org/download"
    fi
else
    ANTLR_VERSION=$(antlr4 2>&1 | head -1)
    echo "✅ ANTLR4 found: $ANTLR_VERSION"
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found."
    exit 1
else
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python 3 found: $PYTHON_VERSION"
fi

echo ""

# =============================================================================
# STEP 2: CREATE DIRECTORY STRUCTURE
# =============================================================================

echo "📁 STEP 2: Creating directory structure..."

GRAMMAR_DIR="hypercode-core/grammar"
mkdir -p "$GRAMMAR_DIR"
echo "✅ Created: $GRAMMAR_DIR"

echo ""

# =============================================================================
# STEP 3: COPY GRAMMAR FILE
# =============================================================================

echo "📄 STEP 3: Placing HyperCode.g4..."

if [ -f "HyperCode.g4" ]; then
    cp HyperCode.g4 "$GRAMMAR_DIR/"
    echo "✅ Copied: HyperCode.g4 → $GRAMMAR_DIR/"
else
    echo "⚠️  HyperCode.g4 not found in current directory."
    echo "   Expected at: $(pwd)/HyperCode.g4"
fi

echo ""

# =============================================================================
# STEP 4: GENERATE PARSER & LEXER
# =============================================================================

echo "⚙️  STEP 4: Generating parser and lexer from grammar..."

cd "$GRAMMAR_DIR"

antlr4 -Dlanguage=Python3 -visitor -no-listener HyperCode.g4

if [ $? -eq 0 ]; then
    echo "✅ Grammar generation successful!"
    echo ""
    echo "Generated files:"
    ls -1 HyperCode*.py 2>/dev/null || echo "   ❌ No files generated"
else
    echo "❌ Grammar generation failed!"
    exit 1
fi

cd - > /dev/null

echo ""

# =============================================================================
# STEP 5: CREATE __init__.py
# =============================================================================

echo "🐍 STEP 5: Creating Python module..."

cat > "$GRAMMAR_DIR/__init__.py" << 'EOF'
"""
HyperCode ANTLR4 Grammar Module
Auto-generated from HyperCode.g4
"""

from antlr4 import *
from .HyperCodeLexer import HyperCodeLexer
from .HyperCodeParser import HyperCodeParser
from .HyperCodeVisitor import HyperCodeVisitor

__all__ = [
    'HyperCodeLexer',
    'HyperCodeParser',
    'HyperCodeVisitor',
    'InputStream',
    'CommonTokenStream',
]
EOF

echo "✅ Created: $GRAMMAR_DIR/__init__.py"

echo ""

# =============================================================================
# STEP 6: INSTALL ANTLR RUNTIME
# =============================================================================

echo "📦 STEP 6: Installing ANTLR4 Python runtime..."

pip3 install antlr4-python3-runtime 2>/dev/null || \
python3 -m pip install antlr4-python3-runtime

if [ $? -eq 0 ]; then
    echo "✅ ANTLR4 Python runtime installed"
else
    echo "⚠️  Could not install ANTLR4 runtime. Try manual: pip3 install antlr4-python3-runtime"
fi

echo ""

# =============================================================================
# STEP 7: QUICK VALIDATION
# =============================================================================

echo "✅ STEP 7: Validating setup..."

python3 << 'VALIDATE_SCRIPT'
import sys

try:
    from antlr4 import *
    from hypercode.grammar import HyperCodeLexer, HyperCodeParser
    
    print("   ✅ Imports successful!")
    
    # Test parsing a simple program
    code = "init(5);"
    input_stream = InputStream(code)
    lexer = HyperCodeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = HyperCodeParser(stream)
    tree = parser.program()
    
    print(f"   ✅ Sample parse successful: '{code}'")
    
except Exception as e:
    print(f"   ❌ Validation failed: {e}")
    sys.exit(1)
VALIDATE_SCRIPT

echo ""

# =============================================================================
# SUMMARY
# =============================================================================

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ SETUP COMPLETE!                                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Summary:"
echo "   - Grammar file: $GRAMMAR_DIR/HyperCode.g4"
echo "   - Generated lexer: $GRAMMAR_DIR/HyperCodeLexer.py"
echo "   - Generated parser: $GRAMMAR_DIR/HyperCodeParser.py"
echo "   - Module imports: hypercode.grammar"
echo ""
echo "🚀 Next steps:"
echo "   1. Review generated files: ls -la $GRAMMAR_DIR/"
echo "   2. Run tests: pytest hypercode-core/tests/"
echo "   3. Compare with hand-written parser (Task 1.2)"
echo ""
echo "📖 More info: See ANTLR_IMPLEMENTATION.md"
echo ""
