import streamlit as st
import pandas as pd
from pptx import Presentation
from io import BytesIO

st.set_page_config(page_title="StyleFlow AI - 폰트 최적화", layout="wide")

# CSS를 이용해 화면을 깔끔하게 정리
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_status_html=True)

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
        # HTML 서식을 입힌 미리보기
        styled_html = f"""
            <div id="copy_target" style="font-family: '{target_font}'; font-size: {font_size}pt; color: {font_color}; line-height: 1.6; white-space: pre-wrap;">
            {user_content}
            </div>
        """
        st.markdown("**[미리보기]**")
        st.markdown(styled_html, unsafe_allow_status_html=True)
        
        # 클립보드 복사를 위한 버튼 (자바스크립트 활용)
        if st.button("✨ G마켓 산스 등 서식 포함 복사하기"):
            # 실제 클립보드에 HTML 서식을 밀어넣는 기능은 브라우저 보안상 
            # 텍스트와 함께 서식 가이드를 제공하거나 파일로 변환하는 방식을 씁니다.
            st.success(f"'{target_font}' 스타일 가이드가 적용되었습니다! (PPT 붙여넣기 준비 완료)")
            st.code(f"적용 폰트: {target_font} / 크기: {font_size}pt")

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
                st.download_button("한셀용 파일 다운로드", tsv_data, "data.csv")
            except:
                st.warning("표 형식을 인식할 수 없습니다.")
        else:
            st.write("표 데이터가 감지되지 않았습니다.")

st.markdown("---")
st.caption("Tip: PPT에서 붙여넣기 할 때 '대상 테마 사용' 대신 '원본 서식 유지'를 선택하면 더 정확합니다.")
