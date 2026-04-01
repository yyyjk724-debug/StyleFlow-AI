import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정 (파비콘까지 초록색 🌿로 변경)
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 초록색 계열 완벽 통일 CSS 주입
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .main { background-color: #f7faf9; font-family: 'Pretendard', sans-serif; }
    
    /* 입력창 및 결과창 박스 설정: 둥근 모서리, 부드러운 배경색 */
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #cce3d9;
        transition: all 0.3s ease;
        background-color: #ffffff;
        font-size: 16px !important;
        padding: 15px;
    }
    
    /* 🔥 애니메이션: 포커스 시 초록색 강조 및 살짝 떠오름 */
    .stTextArea textarea:focus {
        border-color: #16a34a !important;
        box-shadow: 0 4px 6px -1px rgba(22, 163, 74, 0.1) !important;
        transform: translateY(-2px);
    }

    /* 🔥 애니메이션: 표 감지 뱃지 서서히 나타남 */
    @keyframes fadeInBadge {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .table-badge { 
        padding: 6px 14px; 
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: white; 
        border-radius: 20px; 
        font-size: 0.8rem; 
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
        animation: fadeInBadge 0.6s ease-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* 타이틀 및 가이드 텍스트 색상 설정 */
    .copy-guide {
        color: #15803d;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 5px;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        color: #4b5563;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* 구분선 및 데이터프레임 색상 초록색 포인트 */
    hr { border-top: 2px solid #e2f0e9; }
    .css-1v0609 { border: 1px solid #cce3d9; } /* st.dataframe border */
    
    /* 버튼 호버 시 부드러운 애니메이션 효과 (혹시 버튼 생길 때를 대비) */
    .stButton>button { transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-1px); }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 영역 (
