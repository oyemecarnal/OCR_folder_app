#!/bin/bash
# Script to create GitHub repository and push code

REPO_NAME="${1:-pdf-monitor}"  # Default to "pdf-monitor" if no name provided

echo "Creating GitHub repository: $REPO_NAME"
echo ""

# Create repository on GitHub
gh repo create "$REPO_NAME" --public --source=. --remote=origin --push 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully created and pushed to: https://github.com/oyemecarnal/$REPO_NAME"
else
    echo ""
    echo "❌ Error creating repository. You may need to:"
    echo "   1. Authenticate: gh auth login"
    echo "   2. Or create the repo manually at https://github.com/new"
    echo "   3. Then run: git remote add origin https://github.com/oyemecarnal/$REPO_NAME.git"
    echo "   4. Then run: git push -u origin main"
fi

