import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="StyleFlow AI - 서식 자동 동기화", layout="centered")

# 깔끔한 디자인 설정
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stTextArea textarea { font-size: 16px !important; border-radius: 10px; border: 2px solid #e0e0e0; }
    .copy-box { padding: 20px; background-color: #f9f9f9; border-radius: 10px; border: 1px dashed #ccc; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ StyleFlow AI: 원클릭 서식 동기화")
st.write("AI 답변을 넣으면, 사용 중인 PPT/한셀 서식에 **착!** 달라붙게 정리해 드립니다.")

# 메인 입력창
user_content = st.text_area("AI 답변을 여기에 붙여넣으세요:", height=250, placeholder="여기에 내용을 넣으면 모든 서식이 자동으로 제거됩니다.")

if user_content:
    st.divider()
    
    # 1. 일반 텍스트 정제 (PPT/한글용)
    # 마크다운 기호(#, *, - 등)를 깔끔하게 제거하거나 정리
    clean_text = re.sub(r'[*#_~-]', '', user_content) # 특수문자 제거
    
    st.subheader("📋 1. PPT/한글/워드용 (자동 서식 맞춤)")
    st.info("아래 박스의 내용을 복사해서 PPT에 붙여넣으세요. 기존 PPT의 폰트를 그대로 따라갑니다.")
    st.text_area("서식이 제거된 순수 텍스트:", value=clean_text, height=200, label_visibility="collapsed")
    
    # 2. 표 데이터 정제 (한셀/엑셀용)
    if '|' in user_content:
        st.subheader("📊 2. 한셀/엑셀용 (격자 구조 유지)")
        try:
            lines = [l.strip() for l in user_content.split('\n') if '|' in l]
            # 구분선 제외
            valid_lines = [l for l in lines if '---' not in l]
            headers = [h.strip() for h in valid_lines[0].split('|') if h.strip()]
            data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in valid_lines[1:]]
            
            df = pd.DataFrame(data, columns=headers)
            
            # 한셀용 탭 구분 데이터 생성
            tsv_data = df.to_csv(index=False, sep='\t', header=False)
            
            st.success("표 데이터가 감지되었습니다! 아래 내용을 복사해 한셀에 붙여넣으세요.")
            st.text_area("한셀 전용 복사 영역:", value=tsv_data, height=150)
            st.dataframe(df, use_container_width=True)
        except:
            st.warning("표 데이터를 분석하는 중 오류가 발생했습니다.")
    else:
        st.caption("💡 텍스트 안에 '|' 기호가 포함된 표가 있으면 한셀용 변환기가 자동으로 나타납니다.")

st.markdown("---")
st.caption("Tip: 이 사이트의 출력창에서 복사한 내용은 '순수 텍스트' 상태입니다. PPT에 붙여넣는 즉시 해당 슬라이드의 폰트로 자동 변환됩니다.")
