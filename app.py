import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 디자인 CSS (심플 & 전문적)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700;900&display=swap');
    .main { font-family: 'Pretendard', sans-serif; background-color: #f9fafb; }
    .main-title {
        font-size: 5rem; font-weight: 900; color: #111827;
        text-align: center; letter-spacing: -4px; margin-bottom: 30px;
    }
    .stTextArea textarea {
        border-radius: 12px; border: 2px solid #d1d5db;
        font-size: 16px !important; padding: 20px;
    }
    .table-box {
        background-color: #ecfdf5; border: 2px solid #10b981;
        padding: 20px; border-radius: 12px; margin-bottom: 20px;
    }
    .result-title { color: #10b981; font-weight: 700; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)

# 4. 레이아웃
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 붙여넣기")
    # ⚡ 팁: 붙여넣고 나서 꼭 Ctrl + Enter를 누르세요!
    user_input = st.text_area("Input", height=600, placeholder="내용을 붙여넣고 'Ctrl + Enter'를 누르세요!", label_visibility="collapsed")

with col_out:
    st.markdown("### ✅ 변환 결과")
    
    if user_input:
        # --- [1. 표 추출 로직] ---
        # 마크다운 표(|...|)를 한 줄씩 읽어서 알맹이만 추출
        lines = [l.strip() for l in user_input.split('\n') if '|' in l]
        # 구분선(|---|) 제외
        table_lines = [l for l in lines if not re.match(r'^[\s|:-]+$', l)]
        
        if len(table_lines) >= 2:
            st.markdown('<div class="table-box">', unsafe_allow_html=True)
            st.markdown('<p class="result-title">📊 표 데이터 감지 완료!</p>', unsafe_allow_html=True)
            
            # 한셀/엑셀/PPT용 탭 구분 텍스트 생성
            formatted_table = []
            for line in table_lines:
                # 양 끝의 | 제거 후 셀 내용만 추출
                cells = [c.strip() for c in line.split('|') if c.strip()]
                formatted_table.append("\t".join(cells))
            
            final_tsv = "\n".join(formatted_table)
            
            st.markdown("**아래 내용을 복사해서 엑셀/한셀에 붙여넣으세요**")
            st.text_area("Table Copy Area", value=final_tsv, height=150, label_visibility="collapsed")
            st.info("💡 이 텍스트를 복사해서 엑셀에 넣으면 칸이 딱 맞습니다.")
            st.markdown('</div>', unsafe_allow_html=True)

        # --- [2. 텍스트 정제 로직] ---
        # 불필요한 마크다운 기호 제거
        clean = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_input)
        clean = re.sub(r'[*_~`]', '', clean)
        
        st.markdown("**🔍 무서식 텍스트 결과**")
        st.text_area("Clean Output", value=clean, height=350, label_visibility="collapsed")
        st.caption("위 내용을 드래그해서 복사하세요.")
    else:
        st.info("왼쪽에 내용을 넣고 Ctrl+Enter를 누르면 결과가 나타납니다.")

st.markdown("<br><hr><p style='text-align: center; opacity: 0.5;'>© 2026 StyleFlow AI. 서연님의 연구를 응원합니다.</p>", unsafe_allow_html=True)
