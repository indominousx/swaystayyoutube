# SwayStay YouTube Lite

A Streamlit application for summarizing YouTube video transcripts using AI with RAG (Retrieval Augmented Generation).

## Features

- 🎥 Extract and summarize YouTube video transcripts
- 🤖 Multiple summary types (Concise, Detailed, Key Points, Action Items)
- 💬 Interactive Q&A about video content
- 📊 Transcript analytics
- 📝 Download summaries
- 🕐 Summary history tracking

## Deployment on Render

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
