#!/bin/sh

# Configure git to use hooks from the .githooks directory
git config core.hooksPath .githooks

chmod +x .githooks/commit-msg

if git config core.hooksPath .githooks; then
    echo "✅ Git hooks path configured to .githooks successfully."
else
    echo "❌ Failed to configure git hooks path."
    exit 1
fi
