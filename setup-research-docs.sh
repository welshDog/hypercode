#!/bin/bash

# HyperCode Research Docs Setup Script
# Version 1.0.0
# "The Fastest Way to Organized Knowledge"

echo "🚀 HyperCode Research Setup Initiated..."
echo "----------------------------------------"

# 1. Create Directory
if [ ! -d "docs/RESEARCH" ]; then
    echo "📂 Creating docs/RESEARCH directory..."
    mkdir -p docs/RESEARCH
else
    echo "✅ Directory docs/RESEARCH exists."
fi

# 2. Check/Move Files (Self-Healing)
# If files are in root, move them. If in docs/RESEARCH, keep them.

FILES=(
    "HyperCode_Project_Understanding.md"
    "HyperCode_DEEP_DIVE.md"
    "QUANTUM_ALGORITHMS_SUPER_DEEP_DIVE.md"
    "QUANTUM_QUICK_REFERENCE.md"
    "GITHUB_SETUP_GUIDE.md"
    "INTEGRATION_READY_SUMMARY.md"
    "README_FOR_GITHUB_PUSH.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "📦 Moving $file to docs/RESEARCH/..."
        mv "$file" "docs/RESEARCH/"
    elif [ -f "docs/RESEARCH/$file" ]; then
        echo "✅ $file is correctly placed."
    else
        echo "⚠️  Warning: $file not found!"
    fi
done

# 3. Final Verification
echo "----------------------------------------"
echo "🔍 Verifying Manifest..."
COUNT=$(ls docs/RESEARCH/*.md 2>/dev/null | wc -l)
echo "📊 Found $COUNT research documents."

if [ $COUNT -ge 4 ]; then
    echo "🎉 SETUP COMPLETE! Your research docs are ready."
    echo "👉 Next Step: git add docs/RESEARCH/ && git commit"
else
    echo "❌ something went wrong. Please check file list."
fi
