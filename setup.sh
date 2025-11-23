#!/bin/bash

# Create .streamlit directory if it doesn't exist
mkdir -p ~/.streamlit/

# Create Streamlit config file
echo "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableXsrfProtection = false\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml
