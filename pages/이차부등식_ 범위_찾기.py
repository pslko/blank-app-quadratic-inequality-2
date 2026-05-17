import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import random

st.set_page_config(page_title="이차부등식 범위 찾기 학습", layout="wide")

x = sp.symbols("x")

st.markdown("""
<style>
.stApp { background-color: #f6f8fb; }

h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #1f2937 !important;
}

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 900;
    margin-top: 20px;
    margin-bottom: 8px;
    color: #111827 !important;
}

.sub-title {
    text-align: center;
    font-size: 21px;
    font-weight: 600;
    color: #4b5563 !important;
    margin-bottom: 28px;
}

.step-box {
    background-color: #eaf4ff;
    border: 2px solid #bfdbfe;
    border-radius: 18px;
    padding: 22px;
    text-align: center;
    font-size: 26px;
    font-weight: 900;
    margin-bottom: 15px;
}

.answer-box {
    background-color: #fff7d6;
    border: 1px solid #facc15;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    font-size: 22px;
    font-weight: 800;
}

.stButton > button {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 2px solid #60a5fa !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    min-height: 52px;
}

.stButton > button:hover {
    background-color: #eaf4ff !important;
    border-color: #2563eb !important;
}

.stButton > button p {
    color: #111827 !important;
    white-space: pre-line !important;
}

/* 사이드바 */
section[data-testid="stSidebar"],
div[data-testid="stSidebar"] {
    background-color: #1f2937 !important;
}

section[data-testid="stSidebar"] *,
div[data-testid="stSidebar"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

problem_bank = {
    "D>0": [
        x**2 - 6*x + 5,
        x**2 - 8*x + 12,
        x**2 - 10*x + 16,
        x**2 - 7*x + 10,
        x**2 - 9*x + 18,
    ],
    "D=0": [
        x**2 - 4*x + 4,
        x**2 + 6*x + 9,
        x**2 - 10*x + 25,
        x**2 + 2*x + 1,
    ],
    "D<0": [
        x**2 + 4,
        x**2 + 2*x + 5,
        x**2 - 4*x + 8,
        x**2 + 6*x + 10,
    ]
}

step_info = {
    "D>0": {"step": "Step 1", "d": "D > 0"},
    "D=0": {"step": "Step 2", "d": "D = 0"},
    "D<0": {"step": "Step 3", "d": "D < 0"}
}

with st.sidebar:
    st.header("📌 학습목표")
    st.write("""
    이차부등식과 이차함수를 연결하여  
    그 관계를 설명하고 이차부등식을 풀 수 있다.
    """)

    st.header("🧭 사용법")
    st.write("""
    1. 단계를 선택합니다.
    2. 수식 버튼으로 인수분해식을 만듭니다.
    3. 정답이면 그래프가 나타납니다.
    4. 부등호를 선택합니다.
    5. 해의 범위를 버튼으로 고릅니다.
    """)

    st.header("💡 핵심")
    st.write("""
    f(x) > 0 : x축보다 위  
    f(x) < 0 : x축보다 아래  
    등호 포함 : x절편 포함
    """)

default_states = {
    "step": None,
    "expr": None,
    "formula": "",
    "factor_correct": False,
    "ineq": None,
    "selected_range": None,
    "range_checked": False
}

for k, v in default_states.items():
    if k not in st.session_state:
        st.session_state[k] = v

def new_problem(step):
    st.session_state.step = step
    st.session_state.expr = random.choice(problem_bank[step])
    st.session_state.formula = ""
    st.session_state.factor_correct = False
    st.session_state.ineq = None
    st.session_state.selected_range = None
    st.session_state.range_checked = False

def add_token(token):
    st.session_state.formula += token

def clear_formula():
    st.session_state.formula = ""

def clean_expr(text):
    text = text.replace("^", "**")
    text = text.replace(")(", ")*(")
    text = text.replace("x(", "x*(")
    text = text.replace(")x", ")*x")
    return text

def check_factor(user_input, expr):
    try:
        parsed = sp.sympify(clean_expr(user_input))
        return sp.expand(parsed) == sp.expand(expr)
    except Exception:
        return False

def format_formula_latex(formula_str):
    try:
        parsed = sp.sympify(clean_expr(formula_str))
        return sp.latex(parsed)
    except Exception:
        return formula_str

def get_roots(expr):
    roots = [r for r in sp.solve(expr, x) if r.is_real]
    roots = sorted(roots, key=lambda r: float(r))
    return roots

def root_text(r):
    if r == int(r):
        return str(int(r))
    return sp.latex(r)

def correct_answer(expr, ineq):
    roots = get_roots(expr)

    if len(roots) == 2:
        r1, r2 = root_text(roots[0]), root_text(roots[1])
        return {
            ">": f"x < {r1} 또는 x > {r2}",
            "<": f"{r1} < x < {r2}",
            "≥": f"x ≤ {r1} 또는 x ≥ {r2}",
            "≤": f"{r1} ≤ x ≤ {r2}"
        }[ineq]

    if len(roots) == 1:
        r = root_text(roots[0])
        return {
            ">": f"x ≠ {r}인 모든 실수",
            "<": "해는 없다",
            "≥": "모든 실수",
            "≤": f"x = {r}"
        }[ineq]

    return {
        ">": "모든 실수",
        "<": "해는 없다",
        "≥": "모든 실수",
        "≤": "해는 없다"
    }[ineq]

def answer_options(expr):
    roots = get_roots(expr)

    if len(roots) == 2:
        r1, r2 = root_text(roots[0]), root_text(roots[1])
        return [
            f"x < {r1} 또는 x > {r2}",
            f"{r1} < x < {r2}",
            f"x ≤ {r1} 또는 x ≥ {r2}",
            f"{r1} ≤ x ≤ {r2}",
            "모든 실수",
            "해는 없다"
        ]

    if len(roots) == 1:
        r = root_text(roots[0])
        return [
            f"x = {r}",
            f"x ≠ {r}인 모든 실수",
            "모든 실수",
            "해는 없다"
        ]

    return [
        "모든 실수",
        "해는 없다",
        "x > 0",
        "x < 0",
        "x ≠ 0",
        "x = 0"
    ]

def draw_graph(expr, ineq=None):
    roots = [float(r) for r in get_roots(expr)]

    if roots:
        xmin = min(roots) - 3
        xmax = max(roots) + 3
    else:
        xmin, xmax = -5, 5

    x_vals = np.linspace(xmin, xmax, 1000)
    f = sp.lambdify(x, expr, "numpy")
    y_vals = f(x_vals)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, y_vals, linewidth=3, color="#1d4ed8")

    ax.axhline(0, color="black", linewidth=1.2)
    ax.axvline(0, color="black", linewidth=1.2)

    if ineq in [">", "≥"]:
        ax.fill_between(x_vals, y_vals, 0, where=(y_vals >= 0), color="#93c5fd", alpha=0.35)
    elif ineq in ["<", "≤"]:
        ax.fill_between(x_vals, y_vals, 0, where=(y_vals <= 0), color="#93c5fd", alpha=0.35)

    if roots:
        face = "#1d4ed8" if ineq in ["≥", "≤"] else "white"
        ax.scatter(roots, [0]*len(roots), s=130, edgecolors="#1d4ed8", facecolors=face, linewidths=2)

    ymin = min(y_vals) - 5
    ymax = max(y_vals) + 3

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(np.arange(int(np.floor(xmin)), int(np.ceil(xmax)) + 1, 1))
    ax.grid(True, alpha=0.3)

    return fig

st.markdown("<div class='main-title'>📈 이차부등식 범위 찾는 학습</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>인수분해 → 그래프 확인 → 부등호 선택 → 해의 범위 찾기</div>", unsafe_allow_html=True)

st.markdown("### 단계를 선택하세요")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Step 1\nD > 0", use_container_width=True):
        new_problem("D>0")

with c2:
    if st.button("Step 2\nD = 0", use_container_width=True):
        new_problem("D=0")

with c3:
    if st.button("Step 3\nD < 0", use_container_width=True):
        new_problem("D<0")

st.divider()

if st.session_state.step is None:
    st.info("위의 단계를 선택하세요.")

else:
    step = st.session_state.step
    expr = st.session_state.expr
    info = step_info[step]

    st.markdown(f"""
    <div class='step-box'>
        {info["step"]}<br>{info["d"]}
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 새 문제 받기", use_container_width=True):
        new_problem(step)
        st.rerun()

    st.subheader("📝 주어진 이차식")
    st.latex(f"f(x) = {sp.latex(expr)}")
    st.write("아래 수식 버튼을 눌러 인수분해 형태를 완성해 보세요.")

    st.subheader("✏️ 인수분해 형태로 변환")

    with st.container(border=True):
        if st.session_state.formula:
            latex_formula = format_formula_latex(st.session_state.formula)
            st.latex(f"f(x) = {latex_formula}")
        else:
            st.latex("f(x) =")

    st.write("블럭을 선택하여 인수분해 형태를 만드세요.")

    b1, b2, b3, b4, b5, b6, b7, b8 = st.columns([1, 1, 1, 1, 1, 1, 1.4, 1])

    with b1:
        st.button("(", use_container_width=True, on_click=add_token, args=("(",))
    with b2:
        st.button("𝑥", use_container_width=True, on_click=add_token, args=("x",))
    with b3:
        st.button("+", use_container_width=True, on_click=add_token, args=("+",))
    with b4:
        st.button("-", use_container_width=True, on_click=add_token, args=("-",))
    with b5:
        st.button(")", use_container_width=True, on_click=add_token, args=(")",))
    with b6:
        st.button("²", use_container_width=True, on_click=add_token, args=("^2",))
    with b7:
        num = st.number_input("숫자 입력", min_value=0, max_value=20, value=1, step=1, label_visibility="collapsed")
    with b8:
        st.button("추가", use_container_width=True, on_click=add_token, args=(str(num),))

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.button("🗑 지우기", use_container_width=True, on_click=clear_formula)

    with col_b:
        check_clicked = st.button("✅ 확인", use_container_width=True)

    if check_clicked:
        if step == "D<0":
            st.error("D < 0인 경우는 실수 범위에서 인수분해되지 않습니다. 아래 버튼을 눌러 확인하세요.")
        else:
            if check_factor(st.session_state.formula, expr):
                st.session_state.factor_correct = True
                st.success("정답입니다! 이제 그래프를 확인해봅시다.")
            else:
                st.error("인수분해가 맞는지 다시 확인해보세요.")

    if step == "D<0":
        if st.button("✅ 실수 범위에서 인수분해 불가", use_container_width=True):
            st.session_state.factor_correct = True
            st.success("정답입니다! D < 0이므로 실근이 없어 실수 범위에서 인수분해되지 않습니다.")

    if st.session_state.factor_correct:
        st.divider()
        st.subheader("📊 그래프 확인하기")

        b1, b2, b3, b4 = st.columns(4)

        with b1:
            if st.button("f(x) > 0", use_container_width=True):
                st.session_state.ineq = ">"
                st.session_state.selected_range = None
                st.session_state.range_checked = False
        with b2:
            if st.button("f(x) < 0", use_container_width=True):
                st.session_state.ineq = "<"
                st.session_state.selected_range = None
                st.session_state.range_checked = False
        with b3:
            if st.button("f(x) ≥ 0", use_container_width=True):
                st.session_state.ineq = "≥"
                st.session_state.selected_range = None
                st.session_state.range_checked = False
        with b4:
            if st.button("f(x) ≤ 0", use_container_width=True):
                st.session_state.ineq = "≤"
                st.session_state.selected_range = None
                st.session_state.range_checked = False

        graph_col, answer_col = st.columns([2, 1])

        with graph_col:
            fig = draw_graph(expr, st.session_state.ineq)
            st.pyplot(fig)

        with answer_col:
            if st.session_state.ineq is None:
                st.info("부등호를 먼저 선택하세요.")
            else:
                st.subheader("✏️ 해의 범위 선택")
                st.latex(f"{sp.latex(expr)} {st.session_state.ineq} 0")

                for opt in answer_options(expr):
                    if st.button(opt, use_container_width=True, key=f"{step}_{expr}_{st.session_state.ineq}_{opt}"):
                        st.session_state.selected_range = opt
                        st.session_state.range_checked = False

                if st.session_state.selected_range:
                    st.info(f"선택한 답: {st.session_state.selected_range}")

                if st.button("🔍 정답 확인", use_container_width=True):
                    st.session_state.range_checked = True

                if st.session_state.range_checked:
                    correct = correct_answer(expr, st.session_state.ineq)

                    if st.session_state.selected_range == correct:
                        st.success("정답입니다!")
                    else:
                        st.error("다시 생각해보세요.")

                    st.markdown("<div class='answer-box'>정답</div>", unsafe_allow_html=True)
                    st.write(correct)

        st.divider()
        st.subheader("💬 생각해보기")
        st.write("1. 그래프가 x축보다 위에 있는 부분은 어느 구간인가요?")
        st.write("2. 그래프가 x축보다 아래에 있는 부분은 어느 구간인가요?")
        st.write("3. 등호가 붙으면 근을 포함해야 하는 이유는 무엇인가요?")