#!/bin/sh

chmod +x .githooks/commit-msg

if git config core.hooksPath .githooks; then
    echo "✅ Git hooks path configured to .githooks successfully."
else
    echo "❌ Failed to configure git hooks path."
    exit 1
fi
