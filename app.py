import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="StyleFlow AI", layout="wide")

# 디자인 설정: 표 감지 시 하이라이트 효과 추가
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stTextArea textarea { font-size: 16px !important; border-radius: 8px; border: 1px solid #d1d5db; background-color: #fafafa; }
    h3 { color: #1f2937; font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; }
    .table-badge { 
        padding: 5px 12px; 
        background-color: #e0e7ff; 
        color: #4338ca; 
        border-radius: 20px; 
        font-size: 0.85rem; 
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .copy-msg { font-size: 0.85rem; color: #4f46e5; font-weight: 600; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ StyleFlow AI")

# 좌우 레이아웃
col_in, col_out = st.columns(2)

with col_in:
    st.markdown("### 📥 내용을 붙여넣으세요")
    # Placeholder에 표 예시를 넣어 사용자가 "표도 되는구나"를 알게 함
    example_placeholder = (
        "AI 답변을 여기에 Ctrl+V 하세요...\n\n"
        "💡 표 예시:\n"
        "| 구분 | 내용 |\n"
        "| --- | --- |\n"
        "| 명승 | 낙산사 의상대 |"
    )
    user_content = st.text_area(
        "Input",
        height=500,
        placeholder=example_placeholder,
        label_visibility="collapsed"
    )

with col_out:
    st.markdown("### 📤 결과")
    
    if user_content:
        # 1. 일반 텍스트 정제
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_content)
        clean_text = re.sub(r'[*_~`]', '', clean_text)
        
        st.markdown("**텍스트 결과**")
        st.text_area("Output", value=clean_text, height=250, label_visibility="collapsed")
        st.markdown("<p class='copy-msg'>💡 위 박스를 클릭 후 Ctrl+A → Ctrl+C 하여 PPT에 붙여넣으세요!</p>", unsafe_allow_html=True)
        
        # 2. 표 데이터 감지 및 시각화 (이 부분이 핵심!)
        if '|' in user_content:
            st.divider()
            # 표가 감지되었다는 시각적 뱃지 노출
            st.markdown('<div class="table-badge">📊 표 데이터 자동 감지됨</div>', unsafe_allow_html=True)
            try:
                lines = [l.strip() for l in user_content.split('\n') if '|' in l]
                valid_lines = [l for l in lines if '---' not in l]
                if len(valid_lines) > 1:
                    headers = [h.strip() for h in valid_lines[0].split('|') if h.strip()]
                    data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in valid_lines[1:]]
                    df = pd.DataFrame(data, columns=headers)
                    tsv_data = df.to_csv(index=False, sep='\t', header=False)
                    
                    st.markdown("**한셀/엑셀 전용 데이터**")
                    st.text_area("Table Output", value=tsv_data, height=120, label_visibility="collapsed")
                    st.caption("위 박스를 복사해서 한셀에 붙여넣으면 격자가 완벽하게 유지됩니다.")
                    
                    # 실제 표 모양을 미리보기로 보여줌 (신뢰도 상승!)
                    with st.expander("데이터 미리보기", expanded=True):
                        st.dataframe(df, use_container_width=True)
            except:
                st.caption("표 형식을 분석 중입니다...")
    else:
        st.info("왼쪽에 내용을 넣으면 텍스트와 표가 즉시 변환됩니다.")

st.markdown("---")
st.caption("Tip: 이 사이트는 AI 답변의 '서식 꼬리표'를 제거하여 사용 중인 PPT/한셀 서식에 자동으로 맞춥니다.")
