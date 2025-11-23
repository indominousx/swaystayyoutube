from flask import Flask, redirect
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>SwayStay YouTube Lite</title>
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
                color: #f0f0f0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                text-align: center;
            }
            .container {
                padding: 3rem;
                background: rgba(20, 20, 20, 0.8);
                border-radius: 24px;
                border: 2px solid rgba(16, 185, 129, 0.3);
                max-width: 600px;
            }
            h1 {
                color: #10b981;
                margin-bottom: 1rem;
            }
            p {
                color: #6b7280;
                margin-bottom: 2rem;
                line-height: 1.6;
            }
            .note {
                background: rgba(251, 191, 36, 0.1);
                padding: 1rem;
                border-radius: 12px;
                border: 1px solid rgba(251, 191, 36, 0.3);
                margin-top: 2rem;
            }
            a {
                color: #10b981;
                text-decoration: none;
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎥 SwayStay YouTube Lite</h1>
            <p>This Streamlit application cannot run directly on Vercel.</p>
            <p><strong>Streamlit apps require a persistent server</strong>, which Vercel's serverless architecture doesn't support.</p>
            <div class="note">
                <p><strong>✅ Recommended Deployment Options:</strong></p>
                <ul style="text-align: left; color: #f0f0f0;">
                    <li><a href="https://render.com" target="_blank">Render</a> - Free tier available</li>
                    <li><a href="https://streamlit.io/cloud" target="_blank">Streamlit Cloud</a> - Purpose-built for Streamlit</li>
                    <li><a href="https://railway.app" target="_blank">Railway</a> - Easy deployment</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)))
