import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정 및 다크모드 상태 유지
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 사이드바 테마 설정
with st.sidebar:
    st.header("🌓 테마")
    dark_mode = st.toggle("흑백 모드", value=False)
    st.info("💡 팁: 내용을 붙여넣은 후 Ctrl+Enter를 누르면 가장 빠르게 변환됩니다.")

# 테마 색상 (중괄호 오류 방지를 위해 {{ }} 사용)
if dark_mode:
    bg, txt, card, brd = "#111827", "#f9fafb", "#1f2937", "#374151"
else:
    bg, txt, card, brd = "#f9fafb", "#111827", "#ffffff", "#d1d5db"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    .main-title {{
        font-size: 4.8rem; font-weight: 900; color: {txt};
        text-align: center; letter-spacing: -4px; margin-bottom: 2.5rem;
    }}
    .stTextArea textarea {{
        background-color: {card} !important;
        color: {txt} !important;
        border-radius: 16px; border: 1px solid {brd};
        font-size: 16px !important; padding: 22px;
        transition: all 0.2s ease;
    }}
    .stTextArea textarea:focus {{ border-color: #10b981 !important; transform: translateY(-2px); }}
    .result-label {{ color: #10b981; font-weight: 800; font-size: 1.1rem; margin-bottom: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# 2. 헤더
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)

# 3. 레이아웃 (좌: 입력 / 우: 결과)
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 입력")
    # ⚡ 사용자가 붙여넣고 포커스를 옮기면 즉시 실행됩니다.
    raw_text = st.text_area("Input", height=600, placeholder="여기에 내용을 붙여넣으세요...", label_visibility="collapsed")

with col_out:
    st.markdown("### ✅ 변환 결과")
    
    if raw_text:
        # 서식 정제 (불필요한 기호 싹 지우기)
        clean = re.sub(r'(^|\n)[*#>-]\s?', r'\1', raw_text)
        clean = re.sub(r'[*_~`]', '', clean)
        
        # 1. 텍스트 결과 (실시간 업데이트)
        st.text_area("Output", value=clean, height=350, label_visibility="collapsed")
        st.markdown("<p class='result-label'>✔ 위 박스를 클릭 후 Ctrl+A → Ctrl+C 하세요!</p>", unsafe_allow_html=True)
        
        # 2. 표 데이터 감지 (한셀/엑셀용 탭 구분 데이터)
        if '|' in raw_text:
            try:
                lines = [l.strip() for l in raw_text.split('\n') if '|' in l]
                valid = [l for l in lines if '---' not in l]
                if len(valid) > 1:
                    headers = [h.strip() for h in valid[0].split('|') if h.strip()]
                    data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in valid[1:]]
                    df = pd.DataFrame(data, columns=headers)
                    tsv = df.to_csv(index=False, sep='\t', header=False)
                    
                    st.markdown("<hr style='border-top: 1px dashed #10b981;'>", unsafe_allow_html=True)
                    st.markdown("<p class='result-label'>📊 한셀/엑셀용 표 데이터</p>", unsafe_allow_html=True)
                    st.text_area("Table Output", value=tsv, height=150, label_visibility="collapsed")
                    st.caption("박스 내용을 복사해서 엑셀/한셀에 붙여넣으면 격자가 유지됩니다.")
            except:
                pass
    else:
        st.markdown(
            f"""
            <div style="padding: 180px 20px; text-align: center; border: 2px dashed {brd}; border-radius: 16px; color: #9ca3af; background-color: transparent;">
                내용을 붙여넣고 <b>Ctrl + Enter</b>를 누르면<br>마법처럼 결과가 나타납니다.
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("<br><br><hr><p style='text-align: center; opacity: 0.5;'>© 2026 StyleFlow AI. Optimized for Seo-yeon.</p>", unsafe_allow_html=True)
