import streamlit as st

st.set_page_config(
    page_title="이차부등식 학습",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("""
### 📌 학습 페이지 선택
왼쪽 사이드바 상단의 페이지 버튼을 눌러
학습 페이지를 선택하세요.

- 이차부등식 범위 찾기
- 자유식 확인하기
""")

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