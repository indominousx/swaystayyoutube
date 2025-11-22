# import streamlit as st
# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate
# from langchain_community.vectorstores import FAISS
# from dotenv import load_dotenv
# import os

# load_dotenv()

# st.title("🎥 YouTube Transcript Summarizer with RAG")

# video_id = st.text_input("Enter YouTube Video ID:", "1rObihO_seo")

# if st.button("Summarize"):
#     with st.spinner("Fetching transcript..."):
#         try:
#             ytapi = YouTubeTranscriptApi()
#             transcript_list = ytapi.fetch(video_id=video_id, languages=['en'])
#             transcript = " ".join([t.text for t in transcript_list])
#         except TranscriptsDisabled:
#             st.error("Transcripts are disabled for this video.")
#             transcript = ""

#     if transcript:
#         st.success("Transcript fetched successfully!")

#         splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         tt = splitter.create_documents([transcript])
#         st.write(f" Number of chunks: {len(tt)}")

#         embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#         vector_store = FAISS.from_documents(tt, embedding_model)
#         retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})

#         prompt = PromptTemplate(
#             template = """
# You are an expert AI assistant.
# Context:{context}

# Based on the above context, answer the question clearly:

# Question: {question}
# """,
#             input_variables=["context", "question"]
#         )

#         question = "Summarize the main points of the transcript."

#         retrieved_docs = retriever.invoke(question)
#         context_text = " ".join([doc.page_content for doc in retrieved_docs])
#         final_prompt = prompt.format(context=context_text, question=question)

#         llm = ChatGoogleGenerativeAI(
#             model="gemini-2.5-flash",
#             api_key=os.getenv("GOOGLE_API_KEY")
#         )

#         summary = llm.invoke(final_prompt)

#         st.subheader("📝 Summary")
#         st.write(summary)
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
import time
import requests
from datetime import datetime

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="YouTube Transcript Summarizer",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'summary_history' not in st.session_state:
    st.session_state.summary_history = []
if 'retriever' not in st.session_state:
    st.session_state.retriever = None
if 'current_video' not in st.session_state:
    st.session_state.current_video = None
if 'video_metadata' not in st.session_state:
    st.session_state.video_metadata = None

# Function to get video metadata
def get_video_metadata(video_id):
    """Fetch video metadata using YouTube oEmbed API"""
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'title': data.get('title', 'N/A'),
                'author': data.get('author_name', 'N/A'),
                'thumbnail': data.get('thumbnail_url', ''),
                'thumbnail_hq': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            }
    except:
        pass
    
    # Fallback metadata
    return {
        'title': f'Video ID: {video_id}',
        'author': 'Unknown',
        'thumbnail': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        'thumbnail_hq': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    }

# Enhanced CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
        --bg: #000000;
        --fg: #f0f0f0;
        --card: rgba(20, 20, 20, 0.8);
        --primary: #10b981;
        --secondary: #fbbf24;
        --accent: #f97316;
        --muted: #6b7280;
        --border: rgba(255, 255, 255, 0.1);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: var(--fg);
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 { color: var(--fg) !important; font-weight: 700; }
    
    .title-box {
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(251, 191, 36, 0.1));
        backdrop-filter: blur(20px);
        border: 2px solid rgba(16, 185, 129, 0.3);
        border-radius: 24px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        animation: fadeIn 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .title-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 4px;
        background: linear-gradient(90deg, transparent, var(--primary), var(--secondary), var(--accent), transparent);
        animation: shimmer 3s linear infinite;
    }
    
    .title-box h1 {
        margin: 0;
        font-size: 3rem;
        background: linear-gradient(135deg, #10b981, #fbbf24, #f97316);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient 5s ease infinite;
    }
    
    .title-box p {
        color: var(--muted);
        margin-top: 1rem;
        font-size: 1.2rem;
    }
    
    .stTextInput > div > div > input {
        background: rgba(20, 20, 20, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        color: var(--fg) !important;
        border: 2px solid var(--border) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2), 0 0 30px rgba(16, 185, 129, 0.3);
    }
    
    .stSelectbox > div > div {
        background: rgba(20, 20, 20, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid var(--border) !important;
        border-radius: 16px !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), #059669) !important;
        color: #000 !important;
        border-radius: 16px !important;
        padding: 1.25rem 2.5rem !important;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        transition: all 0.4s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 40px rgba(16, 185, 129, 0.6);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--secondary), #d97706) !important;
        color: #000 !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        font-weight: 600;
        box-shadow: 0 8px 20px rgba(251, 191, 36, 0.4);
    }
    
    .content-box {
        background: rgba(20, 20, 20, 0.6);
        backdrop-filter: blur(20px);
        padding: 3rem;
        border-radius: 24px;
        border: 1px solid var(--border);
        margin: 1.5rem 0;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        animation: fadeIn 0.6s ease-out;
    }
    
    .video-card {
        background: rgba(20, 20, 20, 0.8);
        backdrop-filter: blur(20px);
        border: 2px solid var(--border);
        border-radius: 20px;
        overflow: hidden;
        margin: 2rem 0;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
        animation: fadeIn 0.8s ease-out;
        transition: all 0.4s ease;
    }
    
    .video-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6), 0 0 0 2px var(--primary);
    }
    
    .video-thumbnail {
        width: 100%;
        height: auto;
        display: block;
    }
    
    .video-info {
        padding: 2rem;
    }
    
    .video-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--fg);
        margin: 0 0 1rem 0;
    }
    
    .video-author {
        color: var(--muted);
        font-size: 1.05rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    .video-meta-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .meta-item {
        background: rgba(16, 185, 129, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        transition: all 0.3s ease;
    }
    
    .meta-item:hover {
        transform: translateY(-5px);
        border-color: var(--primary);
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
    }
    
    .meta-label {
        font-size: 0.85rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .meta-value {
        font-size: 1.3rem;
        color: var(--fg);
        font-weight: 700;
    }
    
    .info-card {
        background: rgba(251, 191, 36, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        margin: 2rem 0;
        border: 2px solid rgba(251, 191, 36, 0.3);
        box-shadow: 0 10px 30px rgba(251, 191, 36, 0.2);
    }
    
    .info-card strong {
        color: var(--secondary);
        font-size: 1.2rem;
    }
    
    .success-message {
        background: rgba(16, 185, 129, 0.1);
        backdrop-filter: blur(10px);
        color: var(--fg);
        padding: 1.5rem;
        border-radius: 16px;
        border: 2px solid var(--primary);
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    }
    
    .success-message strong {
        color: var(--primary);
        font-size: 1.1rem;
    }
    
    .error-message {
        background: rgba(239, 68, 68, 0.1);
        backdrop-filter: blur(10px);
        color: var(--fg);
        padding: 1.5rem;
        border-radius: 16px;
        border: 2px solid #ef4444;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
    }
    
    .stat-badge {
        background: linear-gradient(135deg, var(--primary), #059669);
        color: #000;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        display: inline-block;
        font-weight: 700;
        margin: 0.5rem 0.5rem 0 0;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        transition: all 0.3s ease;
    }
    
    .stat-badge:hover {
        transform: translateY(-2px);
    }
    
    .stat-badge a {
        color: inherit !important;
        text-decoration: none !important;
    }
    
    .summary-box {
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.1), rgba(251, 191, 36, 0.1));
        backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 20px;
        border: 2px solid var(--accent);
        margin-top: 2rem;
        box-shadow: 0 20px 60px rgba(249, 115, 22, 0.3);
        animation: fadeIn 1s ease-out;
    }
    
    .summary-box h3 {
        margin: 0 0 1.5rem 0;
        color: var(--accent) !important;
        font-size: 1.8rem;
    }
    
    .result-box {
        background: rgba(10, 10, 10, 0.8);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid var(--border);
        color: var(--fg);
        margin-top: 1.5rem;
        line-height: 1.9;
        font-size: 1.1rem;
        animation: fadeIn 0.8s ease-out;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(20, 20, 20, 0.6);
        backdrop-filter: blur(20px);
        padding: 0.75rem;
        border-radius: 16px;
        border: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--muted);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), #059669) !important;
        color: #000 !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    .divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--primary), var(--secondary), var(--accent), transparent);
        margin: 3rem 0;
        border-radius: 2px;
    }
    
    .footer-text {
        text-align: center;
        color: var(--muted);
        padding: 3rem 2rem;
        font-size: 1rem;
        background: rgba(20, 20, 20, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        margin-top: 4rem;
        border: 1px solid var(--border);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Title section
st.markdown("""
    <div class="title-box">
        <h1>🎥 SwayStay Youtube Lite </h1>
        <p>Extract sustainble insights from any YouTube video instantly</p>
    </div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs([" Summarize", " Ask Questions", " History"])

with tab1:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("###  Enter Video Details")
        
        video_input = st.text_input(
            "YouTube Video URL or ID",
            "1rObihO_seo",
            help="Paste the full YouTube URL or just the video ID"
        )
        
        def extract_video_id(input_str):
            import re
            input_str = input_str.strip()
            patterns = [
                r'(?:youtube\.com\/watch\?v=)([^&\s]+)',
                r'(?:youtube\.com\/embed\/)([^?\s]+)',
                r'(?:youtu\.be\/)([^?\s]+)',
                r'(?:youtube\.com\/v\/)([^?\s]+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, input_str)
                if match:
                    return match.group(1)
            return input_str
        
        video_id = extract_video_id(video_input)
        
        summary_type = st.selectbox(
            " Summary Type",
            ["Concise Summary", "Detailed Summary", "Key Points", "Action Items"],
            help="Choose how you want the transcript to be summarized"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button(" Generate Summary"):
            start_time = time.time()
            
            with st.spinner("📹 Fetching video information..."):
                metadata = get_video_metadata(video_id)
                st.session_state.video_metadata = metadata
                
                st.markdown(f"""
                    <div class="video-card">
                        <img src="{metadata['thumbnail_hq']}" class="video-thumbnail" alt="Video Thumbnail">
                        <div class="video-info">
                            <h2 class="video-title">{metadata['title']}</h2>
                            <div class="video-author">
                                <span></span>
                                <span>{metadata['author']}</span>
                            </div>
                            <div>
                                <span class="stat-badge"> {video_id}</span>
                                <span class="stat-badge"><a href="https://youtube.com/watch?v={video_id}" target="_blank"> Watch</a></span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with st.spinner(" Fetching transcript..."):
                try:
                    ytapi = YouTubeTranscriptApi()
                    transcript_list = ytapi.fetch(video_id=video_id, languages=['en'])
                    transcript = " ".join([t.text for t in transcript_list])
                except TranscriptsDisabled:
                    st.markdown("""
                        <div class="error-message">
                            <strong> Error:</strong> Transcripts are disabled for this video.
                        </div>
                    """, unsafe_allow_html=True)
                    transcript = ""

            if transcript:
                st.markdown("""
                    <div class="success-message">
                        <strong>Success!</strong> Transcript fetched successfully!
                    </div>
                """, unsafe_allow_html=True)

                with st.spinner(" Processing with AI..."):
                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1500, 
                        chunk_overlap=300,
                        length_function=len,
                        separators=["\n\n", "\n", ". ", " ", ""]
                    )
                    tt = splitter.create_documents([transcript])
                    
                    word_count = len(transcript.split())
                    estimated_time = round(word_count / 150, 1)
                    char_count = len(transcript)
                    
                    st.markdown(f"""
                        <div class="info-card">
                            <strong> Transcript Analytics</strong><br><br>
                            <div class="video-meta-grid">
                                <div class="meta-item">
                                    <div class="meta-label">Chunks</div>
                                    <div class="meta-value"> {len(tt)}</div>
                                </div>
                                <div class="meta-item">
                                    <div class="meta-label">Total Words</div>
                                    <div class="meta-value">{word_count:,}</div>
                                </div>
                                <div class="meta-item">
                                    <div class="meta-label">Characters</div>
                                    <div class="meta-value">{char_count:,}</div>
                                </div>
                                <div class="meta-item">
                                    <div class="meta-label">Read Time</div>
                                    <div class="meta-value"> ~{estimated_time} min</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                    vector_store = FAISS.from_documents(tt, embedding_model)
                    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})
                    
                    st.session_state.retriever = retriever
                    st.session_state.current_video = video_id

                    question_map = {
                        "Concise Summary": "Provide a concise summary of the main points in 3-4 sentences.",
                        "Detailed Summary": "Provide a detailed summary covering all major topics and key insights in a table format with headings add sustainability travel insights where applicable.",
                        "Key Points": "Extract and list the key points and main takeaways in bullet format add suastainability insights where applicable.",
                        "Action Items": "Identify actionable items, recommendations, or steps mentioned in the content."
                    }
                    
                    prompt = PromptTemplate(
                        template = """
You are an expert AI assistant.
Context:{context}

Based on the above context, answer the question clearly:

Question: {question}
""",
                        input_variables=["context", "question"]
                    )

                    question = question_map[summary_type]
                    retrieved_docs = retriever.invoke(question)
                    context_text = " ".join([doc.page_content for doc in retrieved_docs])
                    final_prompt = prompt.format(context=context_text, question=question)

                    llm = ChatGoogleGenerativeAI(
                        model="gemini-2.5-flash",
                        api_key=os.getenv("GOOGLE_API_KEY")
                    )

                    summary = llm.invoke(final_prompt)
                    
                    processing_time = round(time.time() - start_time, 2)
                    st.session_state.summary_history.append({
                        'video_id': video_id,
                        'summary_type': summary_type,
                        'summary': summary.content,
                        'time': processing_time,
                        'metadata': metadata,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="summary-box">
                        <h3>📝 {summary_type}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="result-box">
                        {summary.content}
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="text-align: right; color: var(--muted); margin-top: 1rem;">
                        ⚡ Processed in {processing_time}s
                    </div>
                """, unsafe_allow_html=True)
                
                st.download_button(
                    label="📥 Download Summary",
                    data=summary.content,
                    file_name=f"summary_{video_id}.txt",
                    mime="text/plain"
                )
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("###  Ask Questions About the Travel Video")
        
        if st.session_state.retriever is None:
            st.info(" Please generate a summary first in the 'Summarize' tab to enable Q&A features.")
        else:
            if st.session_state.video_metadata:
                metadata = st.session_state.video_metadata
                st.markdown(f"""
                    <div class="video-card">
                        <div style="display: flex; gap: 1.5rem; align-items: center; padding: 1.5rem;">
                            <img src="{metadata['thumbnail']}" style="width: 180px; border-radius: 16px; border: 2px solid var(--primary);" alt="Thumbnail">
                            <div>
                                <h3 style="margin: 0 0 0.5rem 0;">{metadata['title']}</h3>
                                <p style="color: var(--muted); margin: 0;">by {metadata['author']}</p>
                                <span class="stat-badge" style="margin-top: 1rem;">🎬 {st.session_state.current_video}</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.success(f" Ready to answer questions!")
            
            user_question = st.text_input("Ask anything about the video:", placeholder="What are the main topics discussed?")
            
            if st.button(" Get Answer") and user_question:
                with st.spinner(" Thinking..."):
                    prompt = PromptTemplate(
                        template = """
You are an expert AI assistant.
Context:{context}

Based on the above context, answer the question clearly and concisely:

Question: {question}
""",
                        input_variables=["context", "question"]
                    )
                    
                    retrieved_docs = st.session_state.retriever.invoke(user_question)
                    context_text = " ".join([doc.page_content for doc in retrieved_docs])
                    final_prompt = prompt.format(context=context_text, question=user_question)
                    
                    llm = ChatGoogleGenerativeAI(
                        model="gemini-2.5-flash",
                        api_key=os.getenv("GOOGLE_API_KEY")
                    )
                    
                    answer = llm.invoke(final_prompt)
                    
                    st.markdown(f"""
                        <div class="result-box">
                            <strong style="color: var(--primary);">Q:</strong> {user_question}<br><br>
                            <strong style="color: var(--accent);">A:</strong> {answer.content}
                        </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("###  Summary History")
        
        if len(st.session_state.summary_history) == 0:
            st.info("No summaries generated yet. Start by summarizing a video!")
        else:
            st.markdown(f"**Total Summaries:** {len(st.session_state.summary_history)}")
            
            for idx, item in enumerate(reversed(st.session_state.summary_history)):
                metadata = item.get('metadata', {})
                timestamp = item.get('timestamp', 'N/A')
                
                with st.expander(f"🎥 {metadata.get('title', item['video_id'])} | {item['summary_type']} (⚡{item['time']}s)"):
                    if metadata:
                        st.markdown(f"""
                            <div style="display: flex; gap: 1rem; margin-bottom: 1rem; background: var(--card); padding: 1rem; border-radius: 16px;">
                                <img src="{metadata.get('thumbnail', '')}" style="width: 120px; border-radius: 12px;" alt="Thumbnail">
                                <div>
                                    <strong style="color: var(--primary);">{metadata.get('title', 'N/A')}</strong><br>
                                    <span style="color: var(--muted); font-size: 0.9rem;">by {metadata.get('author', 'N/A')}</span><br>
                                    <span style="color: var(--muted); font-size: 0.85rem;"> {timestamp}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="result-box">
                            {item['summary']}
                        </div>
                    """, unsafe_allow_html=True)
            
            if st.button(" Clear History"):
                st.session_state.summary_history = []
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer-text">
        <p> Tip: Paste any YouTube URL (youtube.com/watch?v=..., youtu.be/...) or just the video ID</p>
        <p style="margin-top: 1rem; opacity: 0.7;"> Features: Multiple summary types • Q&A mode • History tracking • Download summaries</p>
    </div>
""", unsafe_allow_html=True)