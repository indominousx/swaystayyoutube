#!/bin/bash

# Create .streamlit directory if it doesn't exist
mkdir -p ~/.streamlit/

# Create Streamlit credentials file
cat > ~/.streamlit/credentials.toml << EOF
[general]
email = ""
EOF

# Create Streamlit config file
cat > ~/.streamlit/config.toml << EOF
[server]
headless = true
enableXsrfProtection = false
enableCORS = false
EOF
