import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 다크모드 및 실시간 UI 디자인 CSS
with st.sidebar:
    st.header("🌓 설정")
    dark_mode = st.toggle("흑백(다크) 모드 활성화", value=False)
    st.info("밤에는 다크 모드로 눈을 보호하세요!")

if dark_mode:
    bg_color, text_color, card_bg, border_color = "#111827", "#f9fafb", "#1f2937", "#374151"
else:
    bg_color, text_color, card_bg, border_color = "#f9fafb", "#111827", "#ffffff", "#d1d5db"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color} !important; color: {text_color} !important; }}
    .main-title {{
        font-size: 4.2rem; font-weight: 900; color: {text_color};
        text-align: center; letter-spacing: -3px; margin-bottom: 2rem;
    }}
    .stTextArea textarea {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border-radius: 16px; border: 1px solid {border_color};
        transition: all 0.3s ease; font-size: 16px !important; padding: 20px;
    }}
    /* 복사 버튼 스타일 커스텀 */
    .stButton>button {{
        width: 100%; background-color: #10b981; color: white;
        border-radius: 10px; border: none; font-weight: bold; height: 3em;
        transition: 0.3s;
    }}
    .stButton>button:hover {{ background-color: #059669; transform: translateY(-2px); }}
    
    .table-section {{
        background-color: rgba(16, 185, 129, 0.1);
        padding: 25px; border-radius: 16px; border: 1px solid #10b981; margin-top: 30px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)

# 4. 실시간 변환 메인 레이아웃
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 입력")
    # key를 지정하여 상태 변화를 즉각 반영 (실시간 변환 핵심)
    user_input = st.text_area("Input", height=500, placeholder="여기에 내용을 붙여넣으세요...", label_visibility="collapsed")

with col_out:
    st.markdown("### ✅ 변환 결과")
    
    # ⚡ [실시간 엔진] 입력창에 글자가 들어오는 즉시 실행됩니다.
    if user_input:
        # 서식 정제 (마크다운 기호 제거)
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_input)
        clean_text = re.sub(r'[*_~`]', '', clean_text)
        
        # 정제된 텍스트 출력
        st.text_area("Output", value=clean_text, height=350, label_visibility="collapsed")
        
        # 📋 [복사 버튼 부활] 클릭 시 복사가 용이하도록 코드 블록 형태로 노출
        st.markdown("<p style='color: #10b981; font-weight: 700; margin-top: 10px;'>복사하려면 아래 버튼을 누르거나 박스를 클릭하세요.</p>", unsafe_allow_html=True)
        if st.button("📋 변환 결과 복사하기 (클릭)"):
            st.code(clean_text, language=None)
            st.success("위 박스의 복사 아이콘을 누르면 클립보드에 저장됩니다!")

        # 5. 표 데이터 자동 처리
        if '|' in user_input:
            st.markdown('<div class="table-section">', unsafe_allow_html=True)
            st.markdown("<h4 style='color: #10b981; margin-top:0;'>📊 표 데이터 감지 완료</h4>", unsafe_allow_html=True)
            try:
                lines = [l.strip() for l in user_input.split('\n') if '|' in l]
                valid_lines = [l for l in lines if '---' not in l]
                if len(valid_lines) > 1:
                    headers = [h.strip() for h in valid_lines[0].split('|') if h.strip()]
                    data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in valid_lines[1:]]
                    df = pd.DataFrame(data, columns=headers)
                    tsv_data = df.to_csv(index=False, sep='\t', header=False)
                    
                    st.markdown("**한셀/엑셀용 데이터**")
                    st.text_area("Table Copy", value=tsv_data, height=100, label_visibility="collapsed")
                    st.caption("💡 위 박스를 복사해서 엑셀에 붙여넣으면 칸이 완벽히 맞습니다.")
            except:
                pass
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("왼쪽창에 내용을 입력하면 실시간으로 서식이 정제됩니다.")

st.markdown("<br><br><hr><p style='text-align: center; opacity: 0.5; font-size: 0.8rem;'>© 2026 StyleFlow AI.</p>", unsafe_allow_html=True)
