import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 디자인 고도화 (서연님 스타일 초록 & 그레이)
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
        animation: fadeIn 0.5s ease-in-out;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .success-badge {
        background-color: #10b981; color: white; padding: 4px 12px;
        border-radius: 20px; font-weight: bold; font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 제목 및 안내
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; opacity: 0.7;'>제미나이에서 복사한 표를 그대로 붙여넣고 <b>Ctrl + Enter</b>를 누르세요!</p>", unsafe_allow_html=True)

# 4. 메인 레이아웃
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 붙여넣기")
    # ⚡ 제미나이 표를 드래그해서 바로 붙여넣는 곳
    user_input = st.text_area("Input Area", height=600, placeholder="제미나이 표나 텍스트를 그대로 붙여넣으세요...", label_visibility="collapsed")

with col_out:
    st.markdown("### ✅ 변환 및 표 추출")
    
    if user_input:
        # --- [지능형 표 인식 엔진] ---
        # 탭(\t)이나 공백 2개 이상으로 구분된 데이터를 표로 인식
        lines = user_input.strip().split('\n')
        table_data = []
        
        for line in lines:
            # 1. 마크다운 표 기호(|)가 있는 경우 처리
            if '|' in line:
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if not re.match(r'^[\s|:-]+$', line): # 구분선 제외
                    table_data.append(cells)
            # 2. 제미나이 복사 표(탭 또는 긴 공백) 처리
            else:
                cells = re.split(r'\t| {2,}', line.strip())
                if len(cells) > 1: # 최소 2열 이상일 때만 표로 간주
                    table_data.append(cells)
        
        # 표 데이터가 발견된 경우
        if len(table_data) >= 2:
            st.markdown('<div class="table-card">', unsafe_allow_html=True)
            st.markdown('<span class="success-badge">📊 표 감지 성공</span>', unsafe_allow_html=True)
            st.markdown("<p style='margin-top:10px; font-weight:700;'>한셀/엑셀/PPT용 데이터 (복사해서 붙여넣기):</p>", unsafe_allow_html=True)
            
            # 탭 구분 텍스트 생성
            tsv_output = "\n".join(["\t".join(row) for row in table_data])
            st.text_area("Table Copy Area", value=tsv_output, height=200, label_visibility="collapsed")
            
            # 미리보기 데이터프레임
            try:
                df = pd.DataFrame(table_data[1:], columns=table_data[0])
                st.dataframe(df, use_container_width=True)
            except:
                st.caption("표 구조를 시각화하는 중입니다...")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("표 형태를 찾지 못했습니다. 탭이나 기호가 포함된 내용을 넣어주세요.")

        # --- [텍스트 정제 결과] ---
        st.markdown("<br>🔍 **정제된 텍스트** (기호 제거 완료)", unsafe_allow_html=True)
        # 모든 마크다운 기호 제거
        clean = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_input)
        clean = re.sub(r'[*_~`|]', '', clean)
        st.text_area("Clean Text", value=clean, height=300, label_visibility="collapsed")
    else:
        st.info("왼쪽에 내용을 입력하고 Ctrl + Enter를 눌러주세요.")

st.markdown("<br><hr><p style='text-align: center; opacity: 0.5;'>© 2026 StyleFlow AI. 서연님의 소중한 연구를 응원합니다.</p>", unsafe_allow_html=True)
