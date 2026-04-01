import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 고도화된 디자인 & 애니메이션 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .main { background-color: #f9fafb; font-family: 'Pretendard', sans-serif; }
    
    /* 메인 타이틀: 폰트 크기 대폭 확대 및 볼드 처리 */
    .main-title {
        font-size: 3.8rem;
        font-weight: 900;
        color: #111827;
        letter-spacing: -2px;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .sub-title {
        color: #4b5563;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 3rem;
    }

    /* 입력/결과 박스 디자인 */
    .stTextArea textarea {
        border-radius: 16px;
        border: 1px solid #d1d5db;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background-color: #ffffff;
        font-size: 16px !important;
        padding: 20px;
    }
    
    /* 포커스 애니메이션 */
    .stTextArea textarea:focus {
        border-color: #10b981 !important;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.1) !important;
        transform: translateY(-4px);
    }

    /* 표 감지 섹션 애니메이션 및 스타일 */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .table-section {
        background-color: #ecfdf5;
        border-radius: 16px;
        padding: 25px;
        border: 1px solid #10b981;
        margin-top: 30px;
        animation: slideUp 0.5s ease-out;
    }

    .table-header {
        color: #065f46;
        font-size: 1.1rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 15px;
    }

    .copy-guide {
        color: #059669;
        font-weight: 700;
        font-size: 0.95rem;
        margin-top: 10px;
    }

    /* 레이블 스타일 */
    .input-label {
        font-size: 1.1rem;
        font-weight: 700;
        color: #374151;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    hr { border-top: 1px solid #e5e7eb; margin: 40px 0; }
    </style>
    """, unsafe_allow_html=True)

# 3. 중앙 집중형 헤더
st.markdown('<h1 class="main-title">StyleFlow AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AI의 복잡한 서식을 지우고, 당신의 문서 스타일로 즉시 동기화합니다.</p>', unsafe_allow_html=True)

# 좌우 레이아웃 배치
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown('<div class="input-label">📥 AI 답변 붙여넣기</div>', unsafe_allow_html=True)
    user_content = st.text_area(
        "Input Area",
        height=550,
        placeholder="ChatGPT나 Gemini의 답변(텍스트 또는 표)을 여기에 Ctrl+V 하세요...",
        label_visibility="collapsed"
    )

with col_out:
    st.markdown('<div class="input-label">✅ 무서식 변환 결과</div>', unsafe_allow_html=True)
    
    if user_content:
        # 서식 제거 로직
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_content)
        clean_text = re.sub(r'[*_~`]', '', clean_text)
        
        # 즉시 변환 출력
        st.text_area("Output Area", value=clean_text, height=350, label_visibility="collapsed")
        st.markdown('<p class="copy-guide">✔ 박스 클릭 후 전체 선택(Ctrl+A) → 복사(Ctrl+C) 하세요!</p>', unsafe_allow_html=True)
        
        # 표 데이터 감지 시 전용 섹션 노출
        if '|' in user_content:
            st.markdown('<div class="table-section">', unsafe_allow_html=True)
            st.markdown('<div class="table-header">📊 표 데이터 완벽 감지됨</div>', unsafe_allow_html=True)
            try:
                lines = [l.strip() for l in user_content.split('\n') if '|' in l]
                valid_lines = [l for l in lines if '---' not in l]
                if len(valid_lines) > 1:
                    headers = [h.strip() for h in valid_lines[0].split('|') if h.strip()]
                    data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in valid_lines[1:]]
                    df = pd.DataFrame(data, columns=headers)
                    tsv_data = df.to_csv(index=False, sep='\t', header=False)
                    
                    st.markdown("<p style='font-size: 0.9rem; color: #065f46; font-weight: 600;'>한셀/엑셀에 바로 붙여넣을 데이터:</p>", unsafe_allow_html=True)
                    st.text_area("Table Output", value=tsv_data, height=120, label_visibility="collapsed")
                    st.caption("위 박스를 복사해 한셀에 붙이면 칸이 완벽하게 정렬됩니다.")
                    
                    with st.expander("변환된 데이터 미리보기", expanded=True):
                        st.dataframe(df, use_container_width=True)
            except:
                pass
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div style="padding: 150px 20px; text-align: center; border: 2px dashed #d1d5db; border-radius: 16px; color: #9ca3af; background-color: #ffffff; margin-top: 10px;">
                내용을 입력하는 즉시<br>텍스트와 표가 자동으로 변환됩니다.
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #9ca3af; font-size: 0.85rem;">© 2026 StyleFlow AI. Academic & Professional Document Sync Tool.</p>', unsafe_allow_html=True)
