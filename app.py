import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="StyleFlow AI - 실시간 서식 동기화", layout="wide")

# 화면 디자인 최적화 (좌우 배치를 통해 동선을 줄임)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stTextArea textarea { font-size: 15px !important; border-radius: 8px; border: 1px solid #d1d5db; }
    h3 { color: #1f2937; margin-bottom: 10px; font-size: 1.2rem; }
    .status-tag { padding: 4px 10px; background-color: #e5e7eb; border-radius: 15px; font-size: 0.8rem; color: #4b5563; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ StyleFlow AI: 실시간 서식 세탁기")
st.caption("AI 답변을 붙여넣는 즉시 모든 서식이 제거됩니다. 바로 복사해서 PPT에 붙이세요!")

# 좌우 레이아웃 분할 (입력과 출력을 한눈에!)
col_in, col_out = st.columns(2)

with col_in:
    st.markdown("### 📥 AI 답변 붙여넣기")
    # 내용이 변경되면 스트림릿은 자동으로 하단 코드를 재실행합니다.
    user_content = st.text_area(
        "내용 입력 시 즉시 변환됨", 
        height=500, 
        placeholder="ChatGPT나 Gemini의 답변을 여기에 Ctrl+V 하세요...",
        label_visibility="collapsed"
    )

with col_out:
    st.markdown("### 📤 정제된 결과 (PPT/한셀용)")
    
    if user_content:
        # 1. 일반 텍스트 정제 (불필요한 마크다운 기호 제거)
        # 텍스트 앞에 붙는 *, -, # 등을 제거하여 PPT 서식을 방해하지 않게 함
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_content) # 리스트 기호 제거
        clean_text = re.sub(r'[*_~`]', '', clean_text) # 강조 기호 제거
        
        # PPT/워드용 출력 박스
        st.info("💡 아래 내용을 복사해서 PPT에 붙여넣으면 기존 폰트를 그대로 따라갑니다.")
        st.text_area("순수 텍스트 결과:", value=clean_text, height=200)
        
        # 2. 표 데이터 감지 시 자동으로 하단에 노출
        if '|' in user_content:
            st.divider()
            try:
                lines = [l.strip() for l in user_content.split('\n') if '|' in l]
                valid_lines = [l for l in lines if '---' not in l]
                if len(valid_lines) > 1:
                    headers = [h.strip() for h in valid_lines[0].split('|') if h.strip()]
                    data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in valid_lines[1:]]
                    df = pd.DataFrame(data, columns=headers)
                    
                    # 한셀용 탭 데이터
                    tsv_data = df.to_csv(index=False, sep='\t', header=False)
                    
                    st.success("📊 표 데이터 감지 완료! 한셀에 바로 붙여넣으세요.")
                    st.text_area("한셀 전용 데이터:", value=tsv_data, height=150)
            except:
                st.warning("표 데이터를 정리하는 중입니다...")
    else:
        st.write("👈 왼쪽창에 내용을 입력하면 결과가 여기에 나타납니다.")

st.markdown("---")
st.caption("Tip: 이 서비스는 '서식 꼬리표'를 실시간으로 잘라냅니다. 복사 후 PPT에서 '원본 서식 유지'로 붙여넣으면 가장 완벽합니다.")
