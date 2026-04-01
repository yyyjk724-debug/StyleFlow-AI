import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 초록 & 회색 계열의 디자인 주입 (애니메이션 포함)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .main { background-color: #f3f4f6; font-family: 'Pretendard', sans-serif; }
    
    /* 입력창 및 결과창 박스 */
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #d1d5db;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
        transition: all 0.2s ease-in-out;
        background-color: #ffffff;
        font-size: 15px !important;
    }
    
    /* 포커스 시 초록색 강조 */
    .stTextArea textarea:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
    }

    /* 표 감지 뱃지 (초록 계열) */
    .table-badge { 
        padding: 5px 12px; 
        background-color: #10b981;
        color: white; 
        border-radius: 6px; 
        font-size: 0.8rem; 
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* 가이드 텍스트 */
    .copy-guide {
        color: #059669;
        font-weight: 600;
        font-size: 0.85rem;
        margin-top: 5px;
    }

    /* 메인 타이틀 */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.2rem;
    }
    
    /* 서브 타이틀 */
    .sub-title {
        color: #4b5563;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* 구분선 초록색 포인트 */
    hr { border-top: 2px solid #e5e7eb; }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 영역
st.markdown('<h1 class="main-title">🌿 StyleFlow AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AI 답변의 서식을 세탁하여 문서의 본래 스타일을 지켜드립니다.</p>', unsafe_allow_html=True)

# 좌우 레이아웃 배치
col_in, col_out = st.columns(2, gap="medium")

with col_in:
    st.markdown("<h3 style='color: #374151;'>📥 AI 답변 입력</h3>", unsafe_allow_html=True)
    # value가 변하면 버튼 클릭 없이 전체 코드가 즉시 재실행됩니다 (실시간 변환 핵심)
    user_content = st.text_area(
        "Input Area",
        height=550,
        placeholder="ChatGPT나 Gemini의 답변을 붙여넣으세요. 즉시 서식이 제거됩니다.",
        label_visibility="collapsed"
    )

with col_out:
    st.markdown("<h3 style='color: #374151;'>📤 변환 결과</h3>", unsafe_allow_html=True)
    
    if user_content:
        # 1. 서식 제거 및 텍스트 정제
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_content)
        clean_text = re.sub(r'[*_~`]', '', clean_text)
        
        # 즉시 출력되는 텍스트 박스
        st.text_area("Output Area", value=clean_text, height=300, label_visibility="collapsed")
        st.markdown('<p class="copy-guide">✔ 위 박스를 클릭 후 Ctrl+A → Ctrl+C 하여 PPT에 붙여넣으세요!</p>', unsafe_allow_html=True)
        
        # 2. 표 데이터 자동 감지
        if '|' in user_content:
            st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
            st.markdown('<div class="table-badge">📊 표 데이터 감지됨</div>', unsafe_allow_html=True)
            try:
                lines = [l.strip() for l in user_content.split('\n') if '|' in l]
                valid_lines = [l for l in lines if '---' not in l]
                if len(valid_lines) > 1:
                    headers = [h.strip() for h in valid_lines[0].split('|') if h.strip()]
                    data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in valid_lines[1:]]
                    df = pd.DataFrame(data, columns=headers)
                    tsv_data = df.to_csv(index=False, sep='\t', header=False)
                    
                    st.markdown("<p style='font-size: 0.9rem; font-weight: 600; color: #374151;'>한셀/엑셀 전용 복사</p>", unsafe_allow_html=True)
                    st.text_area("Table Output", value=tsv_data, height=120, label_visibility="collapsed")
                    
                    with st.expander("데이터 미리보기", expanded=True):
                        st.dataframe(df, use_container_width=True)
            except:
                pass
    else:
        st.markdown(
            """
            <div style="padding: 120px 20px; text-align: center; border: 2px dashed #d1d5db; border-radius: 10px; color: #9ca3af; background-color: #ffffff;">
                왼쪽창에 내용을 입력하면<br>결과가 실시간으로 나타납니다.
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #9ca3af; font-size: 0.8rem;">© 2026 StyleFlow AI. Optimized for Academic Efficiency.</p>', unsafe_allow_html=True)
