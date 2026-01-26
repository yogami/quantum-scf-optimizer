#!/bin/bash

echo "Installing PLANQK CLI..."
npm install -g @planqk/planqk-cli

printf "$(planqk autocomplete script bash)" >> ~/.bashrc; source ~/.bashrc
planqk autocomplete --refresh-cache
chmod +x -R ~/.cache/planqk/autocomplete

echo
echo "Initializing Python environment..."
uv venv
uv sync
