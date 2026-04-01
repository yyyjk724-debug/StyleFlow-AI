import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정 (파비콘까지 초록색 🌿로 변경)
st.set_page_config(page_title="StyleFlow AI", page_icon="🌿", layout="wide")

# 2. 초록색 계열 완벽 통일 CSS 주입
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .main { background-color: #f7faf9; font-family: 'Pretendard', sans-serif; }
    
    /* 입력창 및 결과창 박스 설정: 둥근 모서리, 부드러운 배경색 */
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #cce3d9;
        transition: all 0.3s ease;
        background-color: #ffffff;
        font-size: 16px !important;
        padding: 15px;
    }
    
    /* 🔥 애니메이션: 포커스 시 초록색 강조 및 살짝 떠오름 */
    .stTextArea textarea:focus {
        border-color: #16a34a !important;
        box-shadow: 0 4px 6px -1px rgba(22, 163, 74, 0.1) !important;
        transform: translateY(-2px);
    }

    /* 🔥 애니메이션: 표 감지 뱃지 서서히 나타남 */
    @keyframes fadeInBadge {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .table-badge { 
        padding: 6px 14px; 
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: white; 
        border-radius: 20px; 
        font-size: 0.8rem; 
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
        animation: fadeInBadge 0.6s ease-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* 타이틀 및 가이드 텍스트 색상 설정 */
    .copy-guide {
        color: #15803d;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 5px;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        color: #4b5563;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* 구분선 및 데이터프레임 색상 초록색 포인트 */
    hr { border-top: 2px solid #e2f0e9; }
    .css-1v0609 { border: 1px solid #cce3d9; } /* st.dataframe border */
    
    /* 버튼 호버 시 부드러운 애니메이션 효과 (혹시 버튼 생길 때를 대비) */
    .stButton>button { transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-1px); }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 영역 (아이콘까지 초록색 계열로 🌿 완벽 통일)
st.markdown('<h1 class="main-title">🌿 StyleFlow AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AI 답변의 서식을 세탁하여 당신의 문서에 완벽하게 동기화합니다.</p>', unsafe_allow_html=True)

# 좌우 레이아웃 gap을 줘서 더 시원하게 배치
col_in, col_out = st.columns(2, gap="large")

with col_in:
    # 파란색 트레이 아이콘 -> 초록색 이모지 📩로 변경하여 완벽 통일
    st.markdown("<h3 style='color: #374151;'>📩 AI 답변 입력</h3>", unsafe_allow_html=True)
    # 내용 입력 시 무클릭 실시간 변환 핵심 코드
    user_content = st.text_area(
        "Input",
        height=550,
        placeholder="ChatGPT나 Gemini의 답변을 붙여넣으세요...\n자동으로 모든 서식이 제거됩니다.",
        label_visibility="collapsed"
    )

with col_out:
    # 파란색 트레이 아이콘 -> 초록색 이모지 ✅로 변경하여 완벽 통일
    st.markdown("<h3 style='color: #374151;'>✅ 무서식 결과 (PPT/한글용)</h3>", unsafe_allow_html=True)
    
    if user_content:
        # 1. 서식 제거 및 텍스트 정제 로직
        # AI 특유의 마크다운 기호들을 깔끔하게 제거
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_content)
        clean_text = re.sub(r'[*_~`]', '', clean_text)
        
        # 즉시 변환된 결과 출력 박스 (초록색 포커스 테두리 적용됨)
        st.text_area("Cleaned Content", value=clean_text, height=320, label_visibility="collapsed")
        st.markdown('<p class="copy-guide">✨ 박스 클릭 후 Ctrl+A → Ctrl+C 하여 PPT에 붙여넣으세요!</p>', unsafe_allow_html=True)
        
        # 2. 표 데이터 자동 감지 (뱃지 애니메이션 포함)
        if '|' in user_content:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown('<div class="table-badge">📊 표 데이터 자동 감지됨</div>', unsafe_allow_html=True)
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
                    
                    # 실제 표 미리보기 (데이터프레임 색상까지 초록색 계열로 다듬음)
                    with st.expander("데이터 미리보기", expanded=True):
                        st.dataframe(df, use_container_width=True)
            except:
                pass
    else:
        # 비어있을 때의 안내 박스 디자인 (초록 계열)
        st.markdown(
            """
            <div style="padding: 130px 20px; text-align: center; border: 2px dashed #cce3d9; border-radius: 12px; color: #9ca3af; background-color: #ffffff; margin-top: 10px;">
                왼쪽창에 내용을 입력하면<br>결과가 실시간으로 나타납니다.
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("<br><br><br><hr>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #9ca3af; font-size: 0.8rem;">© 2026 StyleFlow AI. Built for Academic & Research efficiency.</p>', unsafe_allow_html=True)
