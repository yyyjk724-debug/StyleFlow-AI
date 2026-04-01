import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="StyleFlow AI", layout="wide")

# 초간결 디자인: 불필요한 여백과 라벨 제거
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stTextArea textarea { font-size: 15px !important; border-radius: 8px; border: 1px solid #d1d5db; }
    h3 { color: #1f2937; font-size: 1.1rem; font-weight: 600; margin-bottom: 5px; }
    /* 복사 버튼 스타일 */
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ StyleFlow AI")

# 좌우 레이아웃
col_in, col_out = st.columns(2)

with col_in:
    st.markdown("### 📥 내용을 붙여넣으세요")
    user_content = st.text_area(
        "Input",
        height=500,
        placeholder="AI 답변을 여기에 Ctrl+V 하세요...",
        label_visibility="collapsed"
    )

with col_out:
    st.markdown("### 📤 결과")
    
    if user_content:
        # 1. 서식 제거 로직
        # 리스트 기호 및 마크다운 특수문자 제거
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_content)
        clean_text = re.sub(r'[*_~`]', '', clean_text)
        
        # '변환 결과'라는 이름으로 깔끔하게 출력
        st.markdown("**변환 결과**")
        st.text_area("Output", value=clean_text, height=250, label_visibility="collapsed")
        
        # 2. 원클릭 복사 버튼 (가장 중요한 기능!)
        # 서식 없이 텍스트만 복사되도록 유도
        if st.button("✨ 클릭하여 결과 복사하기"):
            st.write(f'<script>navigator.clipboard.writeText(`{clean_text}`)</script>', unsafe_allow_html=True)
            st.success("클립보드에 복사되었습니다! 이제 PPT나 한글에 붙여넣으세요.")

        # 3. 표 데이터 (있을 경우만 하단에 조용히 표시)
        if '|' in user_content:
            st.divider()
            try:
                lines = [l.strip() for l in user_content.split('\n') if '|' in l]
                valid_lines = [l for l in lines if '---' not in l]
                if len(valid_lines) > 1:
                    headers = [h.strip() for h in valid_lines[0].split('|') if h.strip()]
                    data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in valid_lines[1:]]
                    df = pd.DataFrame(data, columns=headers)
                    tsv_data = df.to_csv(index=False, sep='\t', header=False)
                    
                    st.markdown("**한셀용 데이터**")
                    st.text_area("Table Output", value=tsv_data, height=100, label_visibility="collapsed")
                    st.caption("표 내용은 위 박스를 복사해서 한셀에 붙이시면 됩니다.")
            except:
                pass
    else:
        st.info("왼쪽에 내용을 넣으면 여기에 결과가 나타납니다.")

st.markdown("---")
st.caption("Tip: 복사 버튼을 누르면 서식이 완전히 제거된 상태로 복사되어, 어떤 프로그램이든 '기존 서식'에 맞춰 들어갑니다.")
