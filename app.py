import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 사이드바 테마 설정
with st.sidebar:
    st.header("🌓 테마")
    dark_mode = st.toggle("흑백 모드", value=False)
    st.info("💡 팁: 붙여넣고 빈 화면을 클릭하거나 Ctrl+Enter를 누르면 즉시 변환됩니다.")

# 테마 색상 (중괄호 오류 방지 처리)
if dark_mode:
    bg, txt, card, brd = "#111827", "#f9fafb", "#1f2937", "#4b5563"
else:
    bg, txt, card, brd = "#f9fafb", "#111827", "#ffffff", "#d1d5db"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    .main-title {{
        font-size: 4.8rem; font-weight: 900; color: {txt};
        text-align: center; letter-spacing: -4px; margin-bottom: 2rem;
    }}
    .stTextArea textarea {{
        background-color: {card} !important;
        color: {txt} !important;
        border-radius: 16px; border: 1px solid {brd};
        font-size: 16px !important; padding: 22px;
    }}
    .stTextArea textarea:focus {{ border-color: #10b981 !important; }}
    .result-label {{ color: #10b981; font-weight: 800; font-size: 1.1rem; margin-bottom: 8px; }}
    .table-section {{
        background-color: rgba(16, 185, 129, 0.08);
        padding: 20px; border-radius: 12px; border: 1px solid #10b981; margin-top: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. 헤더
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)

# 3. 레이아웃
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 입력")
    # ⚡ 실시간 입력을 받는 메인 박스
    raw_text = st.text_area("Input", height=600, placeholder="내용을 붙여넣으세요...", label_visibility="collapsed")

with col_out:
    st.markdown("### ✅ 변환 결과")
    
    if raw_text:
        # 1. 텍스트 정제 (불필요한 마크다운 기호 제거)
        clean = re.sub(r'(^|\n)[*#>-]\s?', r'\1', raw_text)
        clean = re.sub(r'[*_~`]', '', clean)
        
        # 텍스트 결과창
        st.text_area("Output", value=clean, height=300, label_visibility="collapsed")
        st.markdown("<p class='result-label'>✔ 위 박스 클릭 후 Ctrl+A → Ctrl+C로 복사하세요!</p>", unsafe_allow_html=True)
        
        # 2. 표 데이터 추출 로직 (더 정교하게 수정)
        # 마크다운 표 형식(|...|)을 찾아내어 리스트로 변환
        table_lines = [line.strip() for line in raw_text.split('\n') if '|' in line]
        
        if len(table_lines) >= 2: # 헤더와 내용이 있어야 함
            try:
                # 구분선(|---|) 제외하고 알맹이만 추출
                content_lines = [l for l in table_lines if not re.match(r'^[\s|:-]+$', l)]
                
                if content_lines:
                    # 각 행을 탭(Tab)으로 구분된 텍스트로 변환 (한셀/엑셀용)
                    formatted_rows = []
                    for line in content_lines:
                        cells = [c.strip() for c in line.split('|') if c.strip()]
                        formatted_rows.append("\t".join(cells))
                    
                    final_table_text = "\n".join(formatted_rows)
                    
                    # 표 전용 섹션 표시
                    st.markdown('<div class="table-section">', unsafe_allow_html=True)
                    st.markdown("<p class='result-label'>📊 한셀/엑셀용 표 데이터</p>", unsafe_allow_html=True)
                    st.text_area("Table Output", value=final_table_text, height=150, label_visibility="collapsed")
                    st.caption("위 박스의 내용을 복사해서 엑셀/한셀에 붙여넣으면 칸이 완벽히 정렬됩니다.")
                    st.markdown('</div>', unsafe_allow_html=True)
            except:
                st.caption("표 형식을 분석하고 있습니다...")
    else:
        st.markdown(
            f"""
            <div style="padding: 180px 20px; text-align: center; border: 2px dashed {brd}; border-radius: 16px; color: #9ca3af;">
                내용을 붙여넣고 <b>Ctrl + Enter</b>를 누르거나<br>빈 공간을 클릭하면 결과가 즉시 나타납니다.
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("<br><br><hr><p style='text-align: center; opacity: 0.5;'>© 2026 StyleFlow AI. Built for Seo-yeon.</p>", unsafe_allow_html=True)
