import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="StyleFlow AI", layout="wide")

# 디자인 설정: 불필요한 라벨 제거 및 시인성 향상
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    /* 입력창과 결과창의 폰트 및 테두리 설정 */
    .stTextArea textarea { font-size: 16px !important; border-radius: 8px; border: 1px solid #d1d5db; background-color: #fafafa; }
    h3 { color: #1f2937; font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; }
    .copy-msg { font-size: 0.85rem; color: #4f46e5; font-weight: 600; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ StyleFlow AI")

# 좌우 레이아웃 배치
col_in, col_out = st.columns(2)

with col_in:
    st.markdown("### 📥 내용을 붙여넣으세요")
    # 아래의 value가 변하는 순간, 스트림릿은 전체 코드를 다시 실행(실시간 변환)합니다.
    user_content = st.text_area(
        "Input",
        height=500,
        placeholder="AI 답변을 여기에 Ctrl+V 하세요...",
        label_visibility="collapsed"
    )

with col_out:
    st.markdown("### 📤 결과")
    
    if user_content:
        # 1. 서식 제거 로직 (순수 텍스트 정제)
        # AI가 사용하는 마크다운 기호(*, #, - 등)를 제거하여 순수 텍스트만 추출
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_content)
        clean_text = re.sub(r'[*_~`]', '', clean_text)
        
        # 2. 변환 결과 즉시 출력 (버튼 없이 실시간 반영)
        st.markdown("**변환 결과**")
        st.text_area(
            "Output", 
            value=clean_text, 
            height=300, 
            label_visibility="collapsed"
        )
        st.markdown("<p class='copy-msg'>💡 위 박스를 클릭 후 Ctrl+A → Ctrl+C 하여 PPT에 붙여넣으세요!</p>", unsafe_allow_html=True)
        
        # 3. 표 데이터 감지 시 하단 노출
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
                    
                    st.markdown("**한셀 전용 데이터**")
                    st.text_area("Table Output", value=tsv_data, height=100, label_visibility="collapsed")
            except:
                pass
    else:
        st.info("왼쪽에 내용을 넣으면 여기에 즉시 나타납니다.")

st.markdown("---")
st.caption("Tip: 이 사이트의 결과는 '무서식' 상태입니다. 복사해서 PPT에 붙여넣으면 사용 중인 서식에 자동으로 맞춰집니다.")
