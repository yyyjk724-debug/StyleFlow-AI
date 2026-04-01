import streamlit as st
import pandas as pd
import re
import base64
from io import BytesIO

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 다크모드 및 통합 디자인 CSS (초록 & 그레이 톤앤매너)
def apply_theme(is_dark):
    bg_color = "#111827" if is_dark else "#f9fafb"
    text_color = "#f9fafb" if is_dark else "#111827"
    card_bg = "#1f2937" if is_dark else "#ffffff"
    border_color = "#374151" if is_dark else "#d1d5db"
    
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {bg_color}; color: {text_color}; }}
        .main-title {{
            font-size: 4rem; font-weight: 900; color: {text_color};
            text-align: center; letter-spacing: -2px; margin-bottom: 0px;
        }}
        .stTextArea textarea {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border-radius: 12px; border: 1px solid {border_color};
            transition: all 0.3s;
        }}
        .stTextArea textarea:focus {{ border-color: #10b981 !important; transform: translateY(-2px); }}
        .copy-btn-hint {{ color: #10b981; font-weight: 600; font-size: 0.9rem; margin-top: 8px; }}
        /* 표 전용 섹션 */
        .table-card {{
            background-color: rgba(16, 185, 129, 0.1);
            padding: 20px; border-radius: 12px; border: 1px solid #10b981; margin-top: 20px;
        }}
        </style>
        """, unsafe_allow_html=True)

# 사이드바 테마 스위치
with st.sidebar:
    st.header("🌓 설정")
    dark_mode = st.toggle("흑백(다크) 모드 활성화")
    st.info("밤에는 다크 모드로 눈을 보호하세요!")

apply_theme(dark_mode)

# 3. 헤더
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; font-size: 1.1rem; opacity: 0.8; margin-bottom: 2rem;">{"어두운 밤에도 편안하게 서식을 세탁하세요." if dark_mode else "AI의 서식을 지우고 당신의 스타일을 입히세요."}</p>', unsafe_allow_html=True)

# 4. 메인 레이아웃
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 AI 답변 붙여넣기")
    user_input = st.text_area("Input", height=500, placeholder="여기에 복사한 내용을 넣으세요...", label_visibility="collapsed")

with col_out:
    st.markdown("### ✅ 변환 결과")
    
    if user_input:
        # 서식 정제 로직 (실시간 자동 변환)
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_input)
        clean_text = re.sub(r'[*_~`]', '', clean_text)
        
        # 결과 출력 박스
        st.text_area("Output", value=clean_text, height=350, label_visibility="collapsed")
        
        # [신규] 복사 버튼 추가 (자바스크립트 우회 방식)
        # 브라우저 보안 때문에 버튼 클릭 시 알림창과 함께 복사하도록 유도
        if st.button("📋 변환 결과 복사하기"):
            st.code(clean_text, language=None)
            st.success("위 박스의 내용을 드래그하여 복사하거나, 오른쪽 아이콘을 눌러주세요!")

        # 5. 표 데이터 처리 (한셀/엑셀 호환성 강화)
        if '|' in user_input:
            st.markdown('<div class="table-card">', unsafe_allow_html=True)
            st.markdown("<h4 style='color: #10b981; margin-top:0;'>📊 표 데이터 감지됨</h4>", unsafe_allow_html=True)
            try:
                lines = [l.strip() for l in user_input.split('\n') if '|' in l]
                valid_lines = [l for l in lines if '---' not in l]
                if len(valid_lines) > 1:
                    headers = [h.strip() for h in valid_lines[0].split('|') if h.strip()]
                    data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in valid_lines[1:]]
                    df = pd.DataFrame(data, columns=headers)
                    
                    # 엑셀/한셀 복사용 TSV 데이터 (탭 구분자)
                    tsv_data = df.to_csv(index=False, sep='\t')
                    
                    st.markdown("**한셀/엑셀용 데이터 (아래 박스 복사 후 바로 붙여넣기)**")
                    st.text_area("Table Copy Area", value=tsv_data, height=120, label_visibility="collapsed")
                    st.caption("💡 이 박스의 내용을 복사해서 엑셀에 붙여넣으면 칸이 딱 맞게 들어갑니다.")
                    
                    with st.expander("데이터 미리보기"):
                        st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error("표 분석 중 오류가 발생했습니다. 형식을 확인해주세요.")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("왼쪽에 내용을 입력하면 실시간으로 서식이 제거됩니다.")

st.markdown("<br><br><hr><p style='text-align: center; opacity: 0.5; font-size: 0.8rem;'>© 2026 StyleFlow AI. Optimized for Academic Success.</p>", unsafe_allow_html=True)
