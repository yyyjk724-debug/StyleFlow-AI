import streamlit as st
import pandas as pd
from pptx import Presentation
from io import BytesIO

st.set_page_config(page_title="StyleFlow AI - 폰트 최적화", layout="wide")

# 스타일 설정 (오타 수정됨)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 StyleFlow AI: 폰트 & 서식 동기화")
st.info("AI의 답변을 복사해 넣고, 원하는 폰트를 설정한 뒤 '서식 포함 복사'를 누르세요.")

# 사이드바에서 폰트 설정
st.sidebar.header("⚙️ 마스터 스타일 설정")
target_font = st.sidebar.text_input("적용할 폰트명 (PC에 설치된 이름)", "Gmarket Sans Medium")
font_size = st.sidebar.number_input("폰트 크기 (pt)", value=18)
font_color = st.sidebar.color_picker("글자 색상", "#000000")

# 메인 입력창
user_content = st.text_area("AI 답변(요약 내용 등)을 여기에 붙여넣으세요:", height=300)

if user_content:
    st.subheader("✅ 변환 및 복사 도구")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 1. PPT/워드용 서식 복사")
        styled_html = f"""
            <div style="font-family: '{target_font}'; font-size: {font_size}pt; color: {font_color}; line-height: 1.6; white-space: pre-wrap; padding: 15px; border: 1px solid #ddd; border-radius: 5px;">
            {user_content}
            </div>
        """
        st.markdown("**[미리보기]**")
        st.markdown(styled_html, unsafe_allow_html=True)
        
        st.warning("💡 위 미리보기 내용을 마우스로 드래그해서 복사(Ctrl+C)한 뒤, PPT에 붙여넣기(Ctrl+V) 하세요!")

    with col2:
        st.markdown("### 2. 한셀/엑셀용 표 변환")
        if '|' in user_content:
            try:
                lines = [l.strip() for l in user_content.split('\n') if '|' in l]
                headers = [h.strip() for h in lines[0].split('|') if h.strip()]
                data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in lines[2:]]
                df = pd.DataFrame(data, columns=headers)
                st.dataframe(df)
                tsv_data = df.to_csv(index=False, sep='\t')
                st.download_button("한셀용 데이터 다운로드", tsv_data, "data.tsv")
            except:
                st.warning("표 형식을 인식할 수 없습니다.")
        else:
            st.write("표 데이터가 감지되지 않았습니다.")

st.markdown("---")
st.caption("Tip: PPT에서 붙여넣기 할 때 '원본 서식 유지'를 선택하면 폰트가 더 잘 유지됩니다.")
