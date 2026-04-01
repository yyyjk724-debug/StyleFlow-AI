import streamlit as st
import pandas as pd
import re
from pptx import Presentation
from pptx.util import Inches
from io import BytesIO

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 다크모드 및 디자인 CSS
with st.sidebar:
    st.header("🌓 테마")
    dark_mode = st.toggle("흑백 모드 활성화", value=False)
    st.divider()
    st.info("💡 팁: 내용을 붙여넣고 'Ctrl + Enter'를 누르면 즉시 변환됩니다!")

bg, txt, card, brd = ("#111827", "#f9fafb", "#1f2937", "#4b5563") if dark_mode else ("#f9fafb", "#111827", "#ffffff", "#d1d5db")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    .main-title {{
        font-size: 4.8rem; font-weight: 900; color: {txt};
        text-align: center; letter-spacing: -4px; margin-bottom: 20px;
    }}
    .stTextArea textarea {{
        background-color: {card} !important; color: {txt} !important;
        border-radius: 16px; border: 1px solid {brd}; font-size: 16px !important; padding: 22px;
    }}
    /* 강조 섹션 */
    .highlight-box {{
        background-color: rgba(16, 185, 129, 0.15);
        padding: 20px; border-radius: 16px; border: 2px solid #10b981; margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)

# 4. 레이아웃
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 입력")
    # key를 주어 입력 상태를 더 명확히 관리합니다.
    user_input = st.text_area("Input", height=600, placeholder="내용을 붙여넣고 Ctrl+Enter를 누르세요!", label_visibility="collapsed", key="main_input")

with col_out:
    st.markdown("### ✅ 변환 및 도구")
    
    if user_input:
        # --- [STEP 1: PPT 표 생성 로직 (상단 배치)] ---
        if '|' in user_input:
            try:
                lines = [l.strip() for l in user_input.split('\n') if '|' in l]
                # 마크다운 표 구분선(|---|) 제외
                valid_lines = [l for l in lines if not re.match(r'^[\s|:-]+$', l)]
                
                if len(valid_lines) > 1:
                    headers = [c.strip() for c in valid_lines[0].split('|') if c.strip()]
                    rows_data = [[c.strip() for c in l.split('|') if c.strip()] for l in valid_lines[1:]]
                    
                    # PPT 생성
                    prs = Presentation()
                    slide = prs.slides.add_slide(prs.slide_layouts[5])
                    rows, cols = len(rows_data) + 1, len(headers)
                    left, top, width, height = Inches(0.5), Inches(1.2), Inches(9), Inches(0.6 * rows)
                    table = slide.shapes.add_table(rows, cols, left, top, width, height).table
                    
                    # 데이터 채우기
                    for i, h in enumerate(headers): table.cell(0, i).text = h
                    for r_idx, row in enumerate(rows_data):
                        for c_idx, val in enumerate(row):
                            table.cell(r_idx + 1, c_idx).text = str(val)
                    
                    ppt_out = BytesIO()
                    prs.save(ppt_out)
                    
                    # PPT 다운로드 버튼 노출
                    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                    st.success("📊 표 데이터가 감지되었습니다!")
                    st.download_button(
                        label="📂 표 전용 PPT 파일 다운로드",
                        data=ppt_out.getvalue(),
                        file_name="StyleFlow_Table.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception:
                st.warning("표 데이터를 분석하는 중입니다...")

        # --- [STEP 2: 텍스트 정제 결과] ---
        clean = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_input)
        clean = re.sub(r'[*_~`]', '', clean)
        
        st.markdown("🔍 **정제된 텍스트**")
        st.text_area("Clean Output", value=clean, height=350, label_visibility="collapsed")
        st.info("💡 위 박스를 클릭하고 Ctrl+A → Ctrl+C로 복사하세요!")

    else:
        st.markdown(
            f"""
            <div style="padding: 180px 20px; text-align: center; border: 2px dashed {brd}; border-radius: 16px; color: #9ca3af;">
                내용을 붙여넣고 <b>Ctrl + Enter</b>를 누르면<br>PPT 생성 버튼과 정제 결과가 나타납니다.
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("<br><br><hr><p style='text-align: center; opacity: 0.5;'>© 2026 StyleFlow AI. 당신의 연구를 응원합니다.</p>", unsafe_allow_html=True)
