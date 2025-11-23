# SwayStay YouTube Lite

A Streamlit application for summarizing YouTube video transcripts using AI with RAG (Retrieval Augmented Generation).

## Features

- 🎥 Extract and summarize YouTube video transcripts
- 🤖 Multiple summary types (Concise, Detailed, Key Points, Action Items)
- 💬 Interactive Q&A about video content
- 📊 Transcript analytics
- 📝 Download summaries
- 🕐 Summary history tracking

## Deployment on Streamlit Community Cloud (Recommended)

### Quick Deploy Steps

1. **Push your code to GitHub** (Already done! ✅)

2. **Go to Streamlit Community Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Deploy New App**
   - Click "New app" button
   - Select repository: `indominousx/swaystay_youtube`
   - Branch: `krishna` (or `main` after merging)
   - Main file path: `app.py`
   - Click "Deploy"

4. **Add Secrets**
   - Go to your app settings (⚙️ icon)
   - Click "Secrets" in the sidebar
   - Add your secret:
     ```toml
     GOOGLE_API_KEY = "your_google_api_key_here"
     ```
   - Click "Save"

5. **Done!** 🎉
   - Your app will be live at: `https://[your-app-name].streamlit.app`

### Get Your Google API Key
- Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- Sign in and create an API key
- Copy the key and add it to Streamlit secrets

## Alternative Deployment - Render

### Prerequisites
- A [Render](https://render.com) account
- A Google API key for Gemini API

### Deployment Steps

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Create a New Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure the Web Service**
   - **Name**: `swaystay-youtube-lite` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

4. **Add Environment Variables**
   - Click "Advanced" or go to "Environment" tab
   - Add the following environment variable:
     - Key: `GOOGLE_API_KEY`
     - Value: Your Google Gemini API key

5. **Deploy**
   - Click "Create Web Service"
   - Wait for the deployment to complete (5-10 minutes)
   - Your app will be available at: `https://your-app-name.onrender.com`

### Environment Variables Required

- `GOOGLE_API_KEY` - Your Google Gemini API key (Get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On Mac/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: 
  - LangChain
  - Google Gemini (gemini-2.5-flash)
  - HuggingFace Embeddings
  - FAISS Vector Store
- **Data**: YouTube Transcript API

## License

MIT License
