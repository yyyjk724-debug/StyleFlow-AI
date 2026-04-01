import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="StyleFlow AI", layout="wide")

# 디자인 설정 (더 깔끔하고 직관적으로)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stTextArea textarea { font-size: 16px !important; border-radius: 8px; border: 1px solid #d1d5db; background-color: #fafafa; }
    h3 { color: #1f2937; font-size: 1.2rem; font-weight: 600; margin-bottom: 10px; }
    .copy-hint { font-size: 0.9rem; color: #6366f1; font-weight: bold; margin-bottom: 5px; }
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
        # 1. 서식 제거 로직 (순수 텍스트 추출)
        # AI 특유의 마크다운 기호들을 제거하여 PPT 서식에 맞게 정제
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_content)
        clean_text = re.sub(r'[*_~`]', '', clean_text)
        
        # 2. 변환 결과 출력 (라벨 최소화)
        st.markdown("<p class='copy-hint'>✨ 아래 박스 안을 클릭하고 Ctrl+A -> Ctrl+C 하세요!</p>", unsafe_allow_html=True)
        st.text_area(
            "변환 결과", 
            value=clean_text, 
            height=400, 
            label_visibility="visible"
        )
        
        # 3. 표 데이터 (있을 경우만 하단에 표시)
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
                    
                    st.markdown("**📊 한셀용 데이터**")
                    st.text_area("Table Output", value=tsv_data, height=100, label_visibility="collapsed")
            except:
                pass
    else:
        st.info("왼쪽에 내용을 넣으면 여기에 결과가 나타납니다.")

st.markdown("---")
st.caption("Tip: 결과창의 텍스트는 서식이 완전히 제거된 '순수 상태'입니다. 복사해서 PPT에 붙여넣으면 사용 중인 폰트로 즉시 바뀝니다.")
