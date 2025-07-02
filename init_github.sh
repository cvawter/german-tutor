#!/bin/bash

# Detect GitHub username
GITHUB_USERNAME=$(gh api user --jq .login)
REPO_NAME="german-tutor"

echo "Creating GitHub repo '$REPO_NAME' for user '$GITHUB_USERNAME'..."

# Initialize git and create repo via GitHub CLI
git init
gh repo create "$GITHUB_USERNAME/$REPO_NAME" --source=. --private --push
git add .
git commit -m "Initial commit with Streamlit, Ollama, and ChromaDB memory"
git branch -M main
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git
git push -u origin main

echo "✅ Repo created and pushed: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
