import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 고급 CSS 디자인
st.markdown("""
    <style>
    .main-title {
        font-size: 4.8rem; font-weight: 900; text-align: center;
        color: #111827; letter-spacing: -4px; margin-bottom: 5px;
    }
    .stTextArea textarea {
        border-radius: 16px; border: 2px solid #10b981;
        font-size: 15px !important; padding: 20px; line-height: 1.6;
    }
    .table-card {
        background-color: #f0fdf4; border: 2px solid #10b981;
        padding: 25px; border-radius: 16px; margin-top: 20px;
    }
    .success-badge {
        background-color: #10b981; color: white; padding: 4px 12px;
        border-radius: 20px; font-weight: bold; font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>제미나이 화면의 표를 그대로 긁어오세요. <b>Ctrl + Enter</b>가 마법의 열쇠입니다!</p>", unsafe_allow_html=True)

# 4. 레이아웃
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 붙여넣기")
    user_input = st.text_area("Input Area", height=600, placeholder="이미지처럼 표를 드래그해서 그대로 붙여넣으세요...", label_visibility="collapsed")

with col_out:
    st.markdown("### ✅ 변환 결과")
    
    if user_input:
        # --- [초정밀 표 추출 엔진] ---
        lines = user_input.strip().split('\n')
        extracted_table = []
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # 패턴 1: 마크다운 기호(|)가 있는 경우
            if '|' in line:
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if not re.match(r'^[\s|:-]+$', line):
                    extracted_table.append(cells)
            
            # 패턴 2: 제미나이 렌더링 표 (탭 또는 2개 이상의 공백)
            else:
                # 탭이나 연속된 공백(2개 이상)을 기준으로 분리
                cells = re.split(r'\t| {2,}', line)
                # 공백이 섞인 경우를 대비해 각 셀 청소
                cells = [c.strip() for c in cells if c.strip()]
                
                if len(cells) > 1: # 최소 2개 열 이상일 때 표로 인정
                    extracted_table.append(cells)
        
        # 표가 감지된 경우 출력
        if len(extracted_table) >= 2:
            st.markdown('<div class="table-card">', unsafe_allow_html=True)
            st.markdown('<span class="success-badge">📊 표 구조 분석 완료</span>', unsafe_allow_html=True)
            
            # 엑셀/PPT용 탭 데이터 생성
            tsv_output = "\n".join(["\t".join(row) for row in extracted_table])
            st.markdown("<p style='margin-top:10px; font-weight:700;'>한셀/엑셀/PPT 복사용 데이터:</p>", unsafe_allow_html=True)
            st.text_area("Table Copy Area", value=tsv_output, height=200, label_visibility="collapsed")
            
            # 데이터프레임 미리보기 (표가 찌그러지지 않게 예외처리)
            try:
                max_cols = max(len(row) for row in extracted_table)
                # 열 개수가 안 맞는 행은 빈칸으로 채움
                padded_table = [row + [""] * (max_cols - len(row)) for row in extracted_table]
                df = pd.DataFrame(padded_table[1:], columns=padded_table[0])
                st.dataframe(df, use_container_width=True)
            except:
                st.info("표 형식이 복잡하여 데이터프레임 대신 텍스트 복사 박스를 활용하세요!")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("표 데이터를 인식하지 못했습니다. 표 전체를 다시 드래그해서 붙여넣어 보세요.")

        # --- [텍스트 정제] ---
        st.markdown("<br>🔍 **정제된 텍스트**", unsafe_allow_html=True)
        # 마크다운 기호 제거
        clean = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_input)
        clean = re.sub(r'[*_~`|]', '', clean)
        st.text_area("Clean Text", value=clean, height=300, label_visibility="collapsed")
    else:
        st.info("왼쪽에 내용을 입력하고 Ctrl + Enter를 눌러주세요.")

st.markdown("<br><hr><p style='text-align: center; opacity: 0.5;'>© 2026 StyleFlow AI. 서연님의 연구를 응원합니다.</p>", unsafe_allow_html=True)
