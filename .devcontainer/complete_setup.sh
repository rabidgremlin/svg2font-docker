#!/bin/bash

# install latest node
nvm install --lts && nvm use --lts

# install codex
npm install -g @openai/codex

# Install python 3 font-forge
sudo apt-get update && sudo apt-get -y install python3-fontforge

# Set up .venv with system site packages
uv venv --system-site-packages
uv sync
