import streamlit as st
import pandas as pd
import re

# 1. 페이지 설정 및 파비콘(아이콘) 설정
st.set_page_config(page_title="StyleFlow AI", page_icon="⚡", layout="wide")

# 2. 고급 CSS 애니메이션 및 디자인 주입
st.markdown("""
    <style>
    /* 폰트 및 배경 설정 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    .main { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* 입력창 및 결과창 박스 디자인 */
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        background-color: #ffffff;
    }
    
    /* 포커스 시 부드러운 애니메이션 효과 */
    .stTextArea textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        transform: translateY(-2px);
    }

    /* 표 감지 뱃지 애니메이션 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .table-badge { 
        padding: 6px 14px; 
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white; 
        border-radius: 20px; 
        font-size: 0.8rem; 
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
        animation: fadeIn 0.5s ease-out;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* 가이드 텍스트 스타일 */
    .copy-guide {
        color: #6366f1;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* 헤더 스타일 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#1e293b, #64748b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 영역
st.markdown('<h1 class="main-title">⚡ StyleFlow AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;">AI 답변의 서식을 세탁하여 당신의 문서에 완벽하게 동기화합니다.</p>', unsafe_allow_html=True)

# 좌우 레이아웃
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("### 📥 Input")
    user_content = st.text_area(
        "AI 내용을 붙여넣으세요",
        height=500,
        placeholder="ChatGPT나 Gemini의 답변을 여기에 붙여넣으세요...\n자동으로 모든 서식이 제거됩니다.",
        label_visibility="collapsed"
    )

with col_out:
    st.markdown("### 📤 Output")
    
    if user_content:
        # 1. 텍스트 정제 로직
        clean_text = re.sub(r'(^|\n)[*#>-]\s?', r'\1', user_content)
        clean_text = re.sub(r'[*_~`]', '', clean_text)
        
        st.markdown("**변환된 결과**")
        st.text_area("Cleaned Content", value=clean_text, height=280, label_visibility="collapsed")
        st.markdown('<p class="copy-guide">✨ 박스 클릭 후 Ctrl+A → Ctrl+C 하여 PPT에 붙여넣으세요!</p>', unsafe_allow_html=True)
        
        # 2. 표 감지 및 애니메이션 효과
        if '|' in user_content:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="table-badge">📊 표 데이터 자동 감지됨</div>', unsafe_allow_html=True)
            try:
                lines = [l.strip() for l in user_content.split('\n') if '|' in l]
                valid_lines = [l for l in lines if '---' not in l]
                if len(valid_lines) > 1:
                    headers = [h.strip() for h in valid_lines[0].split('|') if h.strip()]
                    data = [[cell.strip() for cell in l.split('|') if cell.strip()] for l in valid_lines[1:]]
                    df = pd.DataFrame(data, columns=headers)
                    tsv_data = df.to_csv(index=False, sep='\t', header=False)
                    
                    st.markdown("**한셀/엑셀 전용**")
                    st.text_area("Table Output", value=tsv_data, height=120, label_visibility="collapsed")
                    
                    with st.expander("데이터 미리보기", expanded=True):
                        st.dataframe(df, use_container_width=True)
            except:
                pass
    else:
        st.markdown(
            """
            <div style="padding: 100px 20px; text-align: center; border: 2px dashed #e2e8f0; border-radius: 12px; color: #94a3b8;">
                왼쪽창에 내용을 입력하면<br>결과가 실시간으로 나타납니다.
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("---")
st.markdown('<p style="text-align: center; color: #94a3b8; font-size: 0.8rem;">© 2026 StyleFlow AI. Built for Academic & Research efficiency.</p>', unsafe_allow_html=True)
