import streamlit as st
import re

# 1. 페이지 설정 (최대한 단순하게)
st.set_page_config(page_title="StyleFlow AI", layout="wide")

# 2. 디자인 (서연님이 좋아하시던 그 느낌 그대로)
st.markdown("""
    <style>
    .main-title {
        font-size: 4.5rem; font-weight: 900; text-align: center;
        color: #111827; letter-spacing: -4px; margin-bottom: 10px;
    }
    .stTextArea textarea {
        border-radius: 12px; border: 2px solid #10b981;
        font-size: 16px !important; padding: 20px;
    }
    .table-result {
        background-color: #f0fdf4; border: 2px solid #10b981;
        padding: 20px; border-radius: 12px; margin-top: 20px;
    }
    .success-text { color: #10b981; font-weight: 700; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. 제목
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>붙여넣고 <b>Ctrl + Enter</b>를 누르면 표가 즉시 추출됩니다.</p>", unsafe_allow_html=True)

# 4. 레이아웃
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 붙여넣기")
    # ⚡ 핵심: 이 박스에 내용을 넣고 Ctrl + Enter만 치면 됩니다!
    user_input = st.text_area("Input Area", height=600, placeholder="여기에 내용을 붙여넣으세요...", label_visibility="collapsed")

with col_out:
    st.markdown("### ✅ 추출 결과")
    
    if user_input:
        # --- [표 추출 엔진] ---
        # 1. '|'가 포함된 줄만 다 긁어모읍니다.
        lines = [l.strip() for l in user_input.split('\n') if '|' in l]
        # 2. 표 구분선(|---|)은 버리고 알맹이만 남깁니다.
        table_lines = [l for l in lines if not re.match(r'^[\s|:-]+$', l)]
        
        if len(table_lines) >= 1:
            st.markdown('<div class="table-result">', unsafe_allow_html=True)
            st.markdown('<p class="success-text">📊 표 데이터를 찾았습니다!</p>', unsafe_allow_html=True)
            
            # 3. 엑셀/한셀/PPT 표 삽입용 탭(Tab) 데이터 생성
            rows = []
            for line in table_lines:
                cells = [c.strip() for c in line.split('|') if c.strip()]
                rows.append("\t".join(cells))
            
            final_table = "\n".join(rows)
            
            st.markdown("**아래 박스 내용을 복사해서 엑셀/한셀에 붙여넣으세요:**")
            st.text_area("Table Copy", value=final_table, height=200, label_visibility="collapsed")
            st.info("💡 팁: 위 박스 내용을 복사해서 엑셀이나 PPT 표 안에 넣으면 칸이 딱 맞습니다.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("내용 중에 표(|...|) 형식이 보이지 않아요.")

        # --- [텍스트 정제 엔진] ---
        st.markdown("<br>🔍 **기호 제거된 깨끗한 텍스트**", unsafe_allow_html=True)
        clean = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_input)
        clean = re.sub(r'[*_~`]', '', clean)
        st.text_area("Clean Text", value=clean, height=300, label_visibility="collapsed")
    else:
        st.info("왼쪽에 내용을 입력하고 Ctrl + Enter를 눌러주세요.")

st.markdown("<br><hr><p style='text-align: center; opacity: 0.5;'>© 2026 StyleFlow AI. 서연님의 소중한 연구를 응원합니다.</p>", unsafe_allow_html=True)
