import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 다크모드 및 디자인 CSS (중괄호 오류 완벽 방지)
with st.sidebar:
    st.header("🌓 테마 설정")
    dark_mode = st.toggle("흑백 모드 활성화", value=False)

# 테마 색상 설정
if dark_mode:
    bg, txt, card, brd = "#111827", "#f9fafb", "#1f2937", "#374151"
else:
    bg, txt, card, brd = "#f9fafb", "#111827", "#ffffff", "#d1d5db"

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
    /* 복사 버튼 디자인 */
    .stButton>button {{
        width: 100%; background-color: #10b981; color: white;
        border-radius: 12px; border: none; font-weight: bold; height: 3.5em;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)

# 4. 실시간 변환 레이아웃
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 입력")
    # ⚡ 이 부분의 변수(user_input)가 바뀌면 스트림릿은 아래 코드를 '자동으로' 다시 실행합니다.
    user_input = st.text_area("Input", height=550, placeholder="여기에 내용을 붙여넣으세요...", label_visibility="collapsed")

with col_out:
    st.markdown("### ✅ 변환 결과")
    
    # ⚡ [실시간 핵심] user_input에 글자만 있으면 즉시 실행됨 (클릭 불필요)
    if user_input:
        # 서식 제거 (마크다운 기호 등 세탁)
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_input)
        clean_text = re.sub(r'[*_~`]', '', clean_text)
        
        # 실시간 결과창 업데이트
        st.text_area("Output", value=clean_text, height=350, label_visibility="collapsed")
        
        # 📋 복사 버튼 (클릭 시 복사 가능한 코드박스 노출)
        st.markdown("<p style='color: #10b981; font-weight: 700;'>복사 버튼을 누르면 복사 전용 박스가 나타납니다.</p>", unsafe_allow_html=True)
        if st.button("📋 변환 결과 복사하기"):
            st.info("아래 박스 오른쪽의 복사 아이콘을 클릭하세요!")
            st.code(clean_text, language=None)

        # 📊 표 데이터 실시간 감지
        if '|' in user_input:
            try:
                lines = [l.strip() for l in user_input.split('\n') if '|' in l]
                valid = [l for l in lines if '---' not in l]
                if len(valid) > 1:
                    headers = [h.strip() for h in valid[0].split('|') if h.strip()]
                    data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in valid[1:]]
                    df = pd.DataFrame(data, columns=headers)
                    tsv = df.to_csv(index=False, sep='\t', header=False)
                    
                    st.divider()
                    st.markdown("<h4 style='color: #10b981;'>📊 한셀/엑셀용 표 데이터</h4>", unsafe_allow_html=True)
                    st.text_area("Table Output", value=tsv, height=120, label_visibility="collapsed")
            except:
                pass
    else:
        st.info("왼쪽창에 내용을 입력하면 실시간으로 정제됩니다.")

st.markdown("<br><br><hr><p style='text-align: center; opacity: 0.5;'>© 2026 StyleFlow AI.</p>", unsafe_allow_html=True)
