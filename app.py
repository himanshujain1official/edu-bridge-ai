import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from gtts import gTTS
import os
import time

# --- CONFIGURATION ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- PROFESSIONAL UI STYLING (Emerald & Slate) ---
st.set_page_config(page_title="Edu-Bridge AI", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #f8fafc; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #064e3b !important; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* Custom Card Design */
    .feature-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #10b981;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* 3D Flashcard Effect Simulation */
    .flashcard {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
with st.sidebar:
    st.title("🌿 Edu-Bridge")
    st.markdown("---")
    page = st.radio("Navigate", ["🏠 Home", "📖 Interactive Learning", "🗂️ Flashcards", "📝 Quiz Mode"])
    st.markdown("---")
    st.caption("AI for Inclusive Education")

# --- HOME PAGE ---
if page == "🏠 Home":
    st.title("Welcome to Edu-Bridge")
    st.subheader("Bridging the gap for students with learning disabilities.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Our Mission</h3>
            <p>To convert complex, high-level textbooks into simplified audio-visual experiences for students with Dyslexia and Cognitive challenges.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ AI Powered</h3>
            <p>Using Google Gemini 2.5 Flash to process PDFs, simplify language, and generate interactive quizzes instantly.</p>
        </div>
        """, unsafe_allow_html=True)

# --- INTERACTIVE LEARNING (PDF TO AUDIO) ---
elif page == "📖 Interactive Learning":
    st.title("Interactive Learning Module")
    uploaded_file = st.file_uploader("Upload your Textbook/PDF", type="pdf")
    
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        text = "".join([p.extract_text() for p in reader.pages])
        
        if st.button("🚀 Process Material"):
            with st.spinner("Simplifying for you..."):
                prompt = f"Simplify this for a 10-year old with short sentences and bullets: {text[:3000]}"
                res = model.generate_content(prompt).text
                
                st.markdown(f'<div class="feature-card">{res}</div>', unsafe_allow_html=True)
                
                # Audio Generation
                tts = gTTS(text=res, lang='en')
                tts.save("edu_audio.mp3")
                st.audio("edu_audio.mp3")
                st.success("Audio Lesson Ready! Click play above.")

# --- FLASHCARDS ---
elif page == "🗂️ Flashcards":
    st.title("3D Flashcards (AI Generated)")
    topic = st.text_input("Enter a topic (e.g. DNA, Photosynthesis)")
    
    if topic:
        if st.button("Generate Flashcard"):
            flash_prompt = f"Define {topic} in exactly 15 simple words for a flashcard."
            def_text = model.generate_content(flash_prompt).text
            st.markdown(f'<div class="flashcard">{topic.upper()}<br><hr style="border:1px solid white"><small>{def_text}</small></div>', unsafe_allow_html=True)

# --- QUIZ MODE ---
elif page == "📝 Quiz Mode":
    st.title("Knowledge Check")
    st.write("Test your understanding with a quick 3-question quiz.")
    
    if st.button("Generate New Quiz"):
        quiz_prompt = "Generate 3 Multiple Choice Questions about General Science. Format: Q, A, B, C, D and Correct Answer."
        quiz_res = model.generate_content(quiz_prompt).text
        st.session_state['quiz'] = quiz_res
        st.info("Quiz Generated! See below:")
        st.write(quiz_res)
    
    # Progress Bar (Your requirement)
    st.write("Progress:")
    st.progress(33) # Example static progress