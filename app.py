import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 다크모드 및 디자인 CSS
with st.sidebar:
    st.header("🌓 테마 설정")
    dark_mode = st.toggle("흑백 모드 활성화", value=False)

# 테마 색상 설정
bg, txt, card, brd = ("#111827", "#f9fafb", "#1f2937", "#374151") if dark_mode else ("#f9fafb", "#111827", "#ffffff", "#d1d5db")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    .main-title {{
        font-size: 4.5rem; font-weight: 900; color: {txt};
        text-align: center; letter-spacing: -3px; margin-bottom: 2rem;
    }}
    .stTextArea textarea {{
        background-color: {card} !important;
        color: {txt} !important;
        border-radius: 16px; border: 1px solid {brd};
        font-size: 16px !important; padding: 20px;
    }}
    .stButton>button {{
        width: 100%; background-color: #10b981; color: white;
        border-radius: 12px; border: none; font-weight: bold; height: 3.5em;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)

# 4. 실시간 변환 로직 (핵심: 세션 상태와 on_change 활용)
if 'clean_output' not in st.session_state:
    st.session_state.clean_output = ""

def transform():
    # 입력값이 들어오면 즉시 서식을 정제하여 저장함
    raw = st.session_state.user_input
    if raw:
        # 서식 제거 로직
        clean = re.sub(r'(^|\n)[*#>-]\s?', r'\1', raw)
        clean = re.sub(r'[*_~`]', '', clean)
        st.session_state.clean_output = clean

col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 입력")
    # ⚡ on_change를 통해 입력이 감지되는 즉시 transform 함수를 실행함
    st.text_area(
        "Input", 
        height=550, 
        placeholder="내용을 붙여넣으면 즉시 변환됩니다...", 
        label_visibility="collapsed",
        key="user_input",
        on_change=transform
    )

with col_out:
    st.markdown("### ✅ 변환 결과")
    
    # ⚡ 변환된 결과를 실시간으로 노출함
    st.text_area(
        "Output", 
        value=st.session_state.clean_output, 
        height=350, 
        label_visibility="collapsed",
        key="display_output"
    )
    
    if st.session_state.clean_output:
        st.markdown("<p style='color: #10b981; font-weight: 700;'>복사 버튼을 눌러서 간편하게 복사하세요.</p>", unsafe_allow_html=True)
        if st.button("📋 변환 결과 복사하기"):
            st.code(st.session_state.clean_output, language=None)

st.markdown("<br><br><hr><p style='text-align: center; opacity: 0.5;'>© 2026 StyleFlow AI.</p>", unsafe_allow_html=True)
