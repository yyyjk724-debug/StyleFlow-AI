import streamlit as st
import pandas as pd
import re
from io import BytesIO

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 다크모드 및 디자인 CSS
with st.sidebar:
    st.header("🌓 테마 설정")
    dark_mode = st.toggle("흑백 모드 활성화", value=False)
    st.divider()
    st.warning("⚠️ 필독: 내용을 붙여넣은 후 반드시 'Ctrl + Enter'를 눌러야 결과가 나타납니다!")

bg, txt, card, brd = ("#111827", "#f9fafb", "#1f2937", "#374151") if dark_mode else ("#f9fafb", "#111827", "#ffffff", "#d1d5db")

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
    .highlight-box {{
        background-color: rgba(16, 185, 129, 0.15);
        padding: 20px; border-radius: 16px; border: 2px solid #10b981; margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)

# 4. 메인 레이아웃
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 입력")
    # 사용자가 내용을 입력하는 메인 박스
    user_input = st.text_area("Input", height=600, placeholder="내용을 붙여넣고 Ctrl+Enter를 누르세요!", label_visibility="collapsed")

with col_out:
    st.markdown("### ✅ 변환 및 표 도구")
    
    if user_input:
        # --- [STEP 1: 표 감지 및 데이터 추출] ---
        # 마크다운 표의 핵심인 '|' 기호를 기준으로 행 분리
        lines = [l.strip() for l in user_input.split('\n') if '|' in l]
        
        # 구분선(|---|) 제외하고 실제 데이터 행만 필터링
        table_data = [l for l in lines if not re.match(r'^[\s|:-]+$', l)]
        
        if len(table_data) >= 2: # 헤더 + 최소 1개 행
            try:
                st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                st.success("📊 표 데이터가 감지되었습니다!")
                
                # 표 데이터를 탭(Tab) 구분 형식으로 변환 (한셀/엑셀 붙여넣기용)
                formatted_rows = []
                for line in table_data:
                    # 양 끝의 | 제거 후 분리
                    cells = [c.strip() for c in line.split('|') if c.strip()]
                    formatted_rows.append("\t".join(cells))
                
                tsv_result = "\n".join(formatted_rows)
                
                st.markdown("**한셀/엑셀/PPT 표 삽입용 (복사해서 붙여넣기)**")
                st.text_area("Table Output", value=tsv_result, height=150, label_visibility="collapsed")
                st.caption("💡 이 박스의 내용을 복사해서 PPT의 '표' 안에 붙여넣거나 엑셀에 넣으세요.")
                
                # 데이터프레임 미리보기
                headers = [c.strip() for c in table_data[0].split('|') if c.strip()]
                rows = [[c.strip() for c in l.split('|') if c.strip()] for l in table_data[1:]]
                df = pd.DataFrame(rows, columns=headers)
                st.dataframe(df, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception:
                st.warning("표 형식을 분석하고 있습니다...")

        # --- [STEP 2: 텍스트 서식 제거 결과] ---
        # 마크다운 기호 제거 로직
        clean = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_input)
        clean = re.sub(r'[*_~`]', '', clean)
        
        st.markdown("🔍 **정제된 텍스트 결과**")
        st.text_area("Clean Output", value=clean, height=350, label_visibility="collapsed")
        st.info("💡 위 박스를 클릭하고 Ctrl+A → Ctrl+C로 복사하세요!")

    else:
        st.markdown(
            f"""
            <div style="padding: 180px 20px; text-align: center; border: 2px dashed {brd}; border-radius: 16px; color: #9ca3af;">
                내용을 붙여넣고 <b>Ctrl + Enter</b>를 누르면<br>표 데이터와 정제 결과가 나타납니다.
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("<br><br><hr><p style='text-align: center; opacity: 0.5;'>© 2026 StyleFlow AI. 서연님의 소중한 연구 시간을 아껴드립니다.</p>", unsafe_allow_html=True)
