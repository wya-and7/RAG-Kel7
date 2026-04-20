"""
=============================================================
ANTARMUKA STREAMLIT — RAG UTS Data Engineering
=============================================================

Jalankan dengan: streamlit run ui/app.py
=============================================================
"""

import sys
import os
from pathlib import Path

# Agar bisa import dari folder src/
sys.path.append(str(Path(__file__).parent.parent / "src"))

import streamlit as st
from dotenv import load_dotenv
import requests
from streamlit_lottie import st_lottie

load_dotenv()

# ─── Konfigurasi Halaman (Ekstrem) ────────────────────────────────────────────
st.set_page_config(
    page_title="AgriBot - Premium AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Injeksi Extreme Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Global Typography */
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }
    
    /* 1. HIDE DEFAULT STREAMLIT ELEMENTS (BREAKING THE TEMPLATE) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove default layout paddings */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px;
    }

    /* 2. LIVING GRADIENT BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    }

    /* 3. FLOATING SIDEBAR EXPERIMENT */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.45) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        margin-top: 2rem !important;
        margin-bottom: 2rem !important;
        margin-left: 1rem !important;
        height: calc(100vh - 4rem) !important;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 15px 35px rgba(22, 160, 133, 0.1);
        overflow: hidden;
    }

    /* Sidebar Resizer line */
    [data-testid="stSidebarResizer"] {
        display: none !important;
    }
    
    /* 4. PREMIUM HERO BANNER HTML CUSTOM */
    .hero-banner {
        background: linear-gradient(120deg, #10b981 0%, #059669 100%);
        border-radius: 30px;
        padding: 40px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(5, 150, 105, 0.2);
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .hero-banner::after {
        content: '';
        position: absolute;
        top: -50px;
        right: -50px;
        width: 200px;
        height: 200px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
    }

    .hero-banner h1 {
        font-size: 3.5rem;
        margin: 0;
        font-weight: 800;
        color: white !important;
        line-height: 1.1;
        letter-spacing: -1px;
    }
    
    .hero-banner p {
        font-size: 1.1rem;
        margin-top: 15px;
        opacity: 0.95;
        font-weight: 400;
    }

    /* 5. MODERN CHAT BUBBLES WITH SHADOWS */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
        border: 1px solid rgba(16, 185, 129, 0.15);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(16, 185, 129, 0.08);
        background-color: rgba(255, 255, 255, 1);
    }
    
    /* Text in chat */
    div[data-testid="stChatMessageContent"] {
        color: #1f2937;
        font-size: 1.05rem;
    }

    /* 6. FLOATING NEON CHAT INPUT */
    [data-testid="stChatInput"] {
        background: white !important;
        border: 2px solid rgba(16, 185, 129, 0.1) !important;
        border-radius: 30px !important;
        box-shadow: 0 10px 40px rgba(5, 150, 105, 0.08) !important;
        transition: all 0.3s ease;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #10b981 !important;
        box-shadow: 0 15px 50px rgba(16, 185, 129, 0.2) !important;
    }

    /* 7. QUICK ACTION BUTTONS AND PRIMARY BUTTONS */
    button[kind="primary"] {
        background: linear-gradient(to right, #10b981, #059669) !important;
        border-radius: 25px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        color: white !important;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(16, 185, 129, 0.45) !important;
    }
    
    /* General transparent/quick action buttons */
    div.stButton > button {
        border-radius: 18px;
        background: white;
        border: 2px solid transparent;
        color: #059669;
        font-weight: 500;
        transition: all 0.2s cubic-bezier(0.4, 0.0, 0.2, 1);
        height: auto;
        padding: 18px 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    }
    div.stButton > button:hover {
        background: #f0fdf4;
        border: 2px solid #10b981;
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(16, 185, 129, 0.15);
    }
    
    /* 8. CONTEXT CARD (EXPANDER UPGRADE) */
    .context-card {
        background-color: white;
        border-left: 5px solid #10b981;
        padding: 1.5rem;
        border-radius: 8px 12px 12px 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .context-card b { color: #059669; font-size: 1.1rem; }
    
    hr {
        border-color: rgba(16, 185, 129, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ─── Lottie Fetcher ───────────────────────────────────────────────────────────
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# URL lottie animasi tanaman yang estetik
lottie_plant = load_lottieurl("https://lottie.host/80998f48-356a-4c28-be94-e3db78a571da/1A3oG5Fp7Y.json")

# ─── Load Vector Store (Backend logic intact) ──────────────────────────────────
@st.cache_resource
def load_vs():
    """Load vector store sekali saja, di-cache untuk performa."""
    try:
        from query import load_vectorstore
        return load_vectorstore(), None
    except FileNotFoundError as e:
        return None, str(e)
    except Exception as e:
        return None, f"Error: {e}"

# ─── Eksekusi Load ─────────────────────────────────────────────────────────────
vectorstore, error = load_vs()

if error:
    st.error(f" {error}")
    st.info("Jalankan terlebih dahulu: `python src/indexing.py`")
    st.stop()

# ─── Start UI Layout ──────────────────────────────────────────────────────────
if "app_loaded" not in st.session_state:
    st.toast("AgriBot siap membantu! 🌱", icon="✨")
    st.session_state.app_loaded = True

# ─── SIDEBAR FLOATING KUSTOM ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Engine RAG")
    
    top_k = st.slider(
        "Jumlah dokumen relevan",
        min_value=1, max_value=10, value=3
    )
    
    show_context = st.checkbox("Tampilkan rujukan konteks", value=True)
    show_prompt = st.checkbox("Tampilkan prompt orisinal", value=False)
    
    st.divider()
    st.markdown("### 🌿 Info Sistem")
    
    st.markdown("""
    **Kelompok:** *(nama)*  
    **Framework RAG:** LangChain  
    **Vector DB:** ChromaDB  
    **Embedding:** MiniLM 
    """)
    st.divider()
    if lottie_plant:
        st_lottie(lottie_plant, height=150, key="sidebar_plant")

# ─── HERO BANNER ────────────────────────────────────────────────────────────
# Membuat layout container banner di atas dengan flex
st.markdown("""
<div class="hero-banner">
    <h1>AgriBot</h1>
    <p>Asisten AI Pertanian Premium — Tingkatkan panen dan rawat tanaman Anda dengan panduan instan dari sistem cerdas RAG.</p>
</div>
""", unsafe_allow_html=True)

# ─── KONTROL STATE CHAT ───────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat dengan custom styling & avatars
for msg in st.session_state.messages:
    avatar = "🧑‍🌾" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        
        # Format Konteks Card
        if msg["role"] == "assistant" and show_context and "contexts" in msg:
            with st.expander("📚 Rujukan Dokumen"):
                for i, ctx in enumerate(msg["contexts"], 1):
                    st.markdown(f"""
                    <div class="context-card">
                        <b>[{i}] Skor Presisi: {ctx['score']:.4f}</b><br/>
                        <small style="color: #6b7280; font-family: monospace;">{ctx['source']}</small><br/><br/>
                        <span style="color: #4b5563; font-size: 0.95rem;">{ctx['content'][:300]}...</span>
                    </div>
                    """, unsafe_allow_html=True)

# ─── EMPTY STATE & QUICK ACTIONS ──────────────────────────────────────────────
quick_action_clicked = None
if len(st.session_state.messages) == 0:
    st.markdown("<h3 style='text-align: center; color: #059669; font-weight: 700; margin-bottom: 2rem;'>Coba tanyakan sesuatu:</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    if c1.button("🪴 Cara budidaya selada hidroponik", use_container_width=True):
        quick_action_clicked = "Bagaimana tahapan menanam selada menggunakan sistem hidroponik?"
    if c2.button("🐛 Solusi penyakit wereng coklat", use_container_width=True):
        quick_action_clicked = "Apa obat atau cara ampuh untuk membasmi hama wereng coklat pada tanaman?"
    if c3.button("💧 Panduan penyiraman bunga hias", use_container_width=True):
        quick_action_clicked = "Kapan jadwal dan cara menyiram tanaman hias yang benar agar tidak layu?"
        
    st.markdown("<br><br>", unsafe_allow_html=True)

# ─── FRONTEND INPUT & BACKEND CALL ──────────────────────────────────────────────
user_input = st.chat_input("Ketik pertanyaan seputar botani, tanaman basah, hidroponik...")
question = quick_action_clicked or user_input

if question:
    # 1. Catat input user dan render
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑‍🌾"):
        st.write(question)
    
    # 2. Render dan generate respon Assistant
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Merumuskan jawaban terbaik..."):
            try:
                from query import answer_question
                # Pastikan backend tetap berkerja persis seperti versi awal
                result = answer_question(question, vectorstore)
                
                # Tampilkan hasil
                st.write(result["answer"])
                
                # Tampilkan Expandable Konteks Card
                if show_context:
                    with st.expander("📚 Rujukan Dokumen"):
                        for i, ctx in enumerate(result["contexts"], 1):
                            st.markdown(f"""
                            <div class="context-card">
                                <b>[{i}] Skor Presisi: {ctx['score']:.4f}</b><br/>
                                <small style="color: #6b7280; font-family: monospace;">{ctx['source']}</small><br/><br/>
                                <span style="color: #4b5563; font-size: 0.95rem;">{ctx['content'][:300]}...</span>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Tampilkan prompt orisinal jika di-toggle
                if show_prompt:
                    with st.expander("🔧 Internal LLM Prompt"):
                        st.code(result["prompt"], language="text")
                
                # Simpan metadata ke log percakapan
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "contexts": result["contexts"]
                })
                
            except Exception as e:
                error_msg = f"Gangguan Sistem: {e}\n\nPastikan API Key LLM yang digunakan sudah tervalidasi."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# ─── TOMBOL RESET CHAT ────────────────────────────────────────────────────────
if st.session_state.messages:
    st.markdown("<hr style='margin-top: 40px;'>", unsafe_allow_html=True)
    colA, colB, colC = st.columns([1,2,1])
    with colB:
        if st.button("🧹 Hapus Sesi Percakapan", type="primary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
