import streamlit as st
import pandas as pd
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from io import BytesIO

st.set_page_config(page_title="StyleFlow AI", layout="wide")

st.title("🚀 StyleFlow AI: 오피스 최적화 도구")
st.markdown("AI 답변을 복사해 넣으면 한셀/PPT 맞춤형으로 변환해 드립니다.")

# 사이드바 설정
st.sidebar.header("🎨 스타일 설정")
font_name = st.sidebar.text_input("적용할 폰트명", "맑은 고딕")
font_size = st.sidebar.slider("폰트 크기", 10, 24, 12)

# 메인 입력창
raw_input = st.text_area("AI가 생성한 마크다운 표나 텍스트를 붙여넣으세요:", height=200)

if raw_input:
    try:
        # 데이터프레임 변환 (간단한 예시)
        lines = [line.strip() for line in raw_input.split('\n') if '|' in line]
        if lines:
            headers = [h.strip() for h in lines[0].split('|') if h.strip()]
            data = []
            for line in lines[2:]:
                data.append([cell.strip() for cell in line.split('|') if cell.strip()])
            df = pd.DataFrame(data, columns=headers)
            
            st.subheader("📊 데이터 미리보기")
            st.table(df)

            col1, col2 = st.columns(2)
            
            with col1:
                st.info("한셀/엑셀용 (탭 구분)")
                tsv_data = df.to_csv(index=False, sep='\t')
                st.text_area("이 내용을 복사해서 한셀에 붙여넣으세요:", tsv_data, height=150)

            with col2:
                st.success("PPT 차트 생성")
                prs = Presentation()
                slide = prs.slides.add_slide(prs.slide_layouts[5])
                chart_data = CategoryChartData()
                chart_data.categories = df.iloc[:, 0].tolist()
                chart_data.add_series('데이터', (pd.to_numeric(df.iloc[:, 1], errors='coerce').fillna(0).tolist()))
                
                x, y, cx, cy = 1000000, 1000000, 7000000, 4500000
                slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data)
                
                ppt_out = BytesIO()
                prs.save(ppt_out)
                st.download_button("PPTX 파일 다운로드", data=ppt_out.getvalue(), file_name="styleflow_chart.pptx")
    except Exception as e:
        st.error("표 형식 분석에 실패했습니다. 올바른 마크다운 표인지 확인해주세요.")
