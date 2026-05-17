import streamlit as st
import urllib.parse

st.set_page_config(
    page_title="이차부등식 학습",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    if hasattr(st, "experimental_get_query_params"):
        query_params = st.experimental_get_query_params()
    else:
        query_params = {}
except Exception:
    query_params = {}

# 사이드바: 항상 표시하되, 루트 페이지일 땐 설명 없이 다른 페이지 목록만 보입니다.
with st.sidebar:
    try:
        pages = {}
        if hasattr(st, "experimental_get_pages"):
            pages = st.experimental_get_pages() or {}

        if pages:
            st.markdown("**다른 페이지**")
            for _, p in pages.items():
                display_name = p.display_name if hasattr(p, "display_name") else p.get("display_name", str(p))
                btn_key = f"nav_{display_name}"
                try:
                    if st.button(display_name, key=btn_key):
                        # set query param if available, then rerun to navigate
                        try:
                            if hasattr(st, "experimental_set_query_params"):
                                st.experimental_set_query_params(page=display_name)
                        except Exception:
                            pass
                        try:
                            st.experimental_rerun()
                        except Exception:
                            pass
                except Exception:
                    st.markdown(f"- {display_name}")
        else:
            # experimental_get_pages가 없거나 빈 경우: pages 디렉터리의 파일명으로 폴백
            import os
            page_files = []
            try:
                for fname in sorted(os.listdir("pages")):
                    if fname.endswith(".py") and not fname.startswith("__"):
                        page_files.append(fname)
            except Exception:
                page_files = []

            if page_files:
                st.markdown("**다른 페이지**")
                for fname in page_files:
                    label = os.path.splitext(fname)[0].replace("_", " ")
                    btn_key = f"nav_{fname}"
                    try:
                        if st.button(label, key=btn_key):
                            try:
                                if hasattr(st, "experimental_set_query_params"):
                                    st.experimental_set_query_params(page=label)
                            except Exception:
                                pass
                            try:
                                st.experimental_rerun()
                            except Exception:
                                pass
                    except Exception:
                        st.write(f"- {label}")
            else:
                st.write("(페이지 없음)")

    except Exception:
        # 사이드바 렌더링에서 치명적 오류가 나지 않도록 무시
        pass


st.markdown("""
<style>
.stApp {
    background-color: #f6f8fb;
}

.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    margin-top: 40px;
    margin-bottom: 10px;
    color: #111827;
}

.sub-title {
    text-align: center;
    font-size: 22px;
    font-weight: 600;
    color: #4b5563;
    margin-bottom: 40px;
}

.info-card {
    background-color: #ffffff;
    border: 1px solid #dbe4f0;
    border-radius: 20px;
    padding: 28px;
    min-height: 260px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.info-card h3 {
    color: #111827;
    font-size: 25px;
    margin-bottom: 18px;
}

.info-card p, .info-card li {
    color: #1f2937;
    font-size: 18px;
    line-height: 1.8;
}

.guide-box {
    background-color: #eaf4ff;
    border: 2px solid #bfdbfe;
    border-radius: 18px;
    padding: 24px;
    margin-top: 40px;
    text-align: center;
    color: #1f2937;
    font-size: 20px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<div class='main-title'>📈 이차부등식 범위 찾는 학습</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>이차함수 그래프와 연결하여 이차부등식의 해를 찾아봅시다.</div>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>📌 학습목표</h3>
        <p>
        이차부등식과 이차함수를 연결하여<br>
        그 관계를 설명하고<br>
        이차부등식을 풀 수 있다.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>🧭 사용법</h3>
        <ol>
            <li>왼쪽 페이지 목록에서 학습 페이지를 선택합니다.</li>
            <li>단계별 학습 또는 자유 식 확인을 진행합니다.</li>
            <li>수식 버튼으로 식을 입력합니다.</li>
            <li>그래프를 보고 해의 범위를 찾습니다.</li>
            <li>정답 확인을 통해 풀이를 점검합니다.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h3>💡 핵심</h3>
        <p>
        f(x) &gt; 0<br>
        → 그래프가 x축보다 위<br><br>
        f(x) &lt; 0<br>
        → 그래프가 x축보다 아래<br><br>
        등호 포함<br>
        → x절편 포함
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="guide-box">
왼쪽 사이드바에서 원하는 학습 페이지를 선택해 시작하세요.
</div>
""", unsafe_allow_html=True)