import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="자유 식 확인하기", layout="wide")

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

with st.sidebar:
    st.header("📌 학습목표")
    st.write("""
    이차부등식과 이차함수를 연결하여  
    그 관계를 설명하고 이차부등식을 풀 수 있다.
    """)

    st.header("🧭 사용법")
    st.write("""
    1. 수식 버튼으로 이차식을 입력합니다.
    2. 부등호를 선택합니다.
    3. 그래프를 보고 해의 범위를 예상합니다.
    4. 해의 범위를 버튼으로 선택합니다.
    5. 정답을 확인합니다.
    """)

    st.header("💡 입력 예시")
    st.write("""
    x² - 6x + 5  
    x² - 4x + 4  
    x² + 2x + 5
    """)

default_states = {
    "formula": "",
    "ineq": None,
    "selected_range": None,
    "range_checked": False,
    "show_graph": False
}

for k, v in default_states.items():
    if k not in st.session_state:
        st.session_state[k] = v

def add_token(token):
    st.session_state.formula += token
    st.session_state.show_graph = False
    st.session_state.selected_range = None
    st.session_state.range_checked = False

def clear_formula():
    st.session_state.formula = ""
    st.session_state.show_graph = False
    st.session_state.selected_range = None
    st.session_state.range_checked = False
    st.session_state.ineq = None

def clean_expr(text):
    text = text.replace("^", "**")
    text = text.replace(")(", ")*(")
    text = text.replace("x(", "x*(")
    text = text.replace(")x", ")*x")
    text = text.replace("2x", "2*x")
    text = text.replace("3x", "3*x")
    text = text.replace("4x", "4*x")
    text = text.replace("5x", "5*x")
    text = text.replace("6x", "6*x")
    text = text.replace("7x", "7*x")
    text = text.replace("8x", "8*x")
    text = text.replace("9x", "9*x")
    return text

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
    func = sp.lambdify(x, expr, "numpy")
    y_vals = func(x_vals)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x_vals, y_vals, color="#1d4ed8", linewidth=3)
    ax.axhline(0, color="black", linewidth=1.2)
    ax.axvline(0, color="black", linewidth=1.2)

    if ineq in [">", "≥"]:
        ax.fill_between(x_vals, y_vals, 0, where=(y_vals >= 0), color="#93c5fd", alpha=0.35)
    elif ineq in ["<", "≤"]:
        ax.fill_between(x_vals, y_vals, 0, where=(y_vals <= 0), color="#93c5fd", alpha=0.35)

    if roots:
        face = "#1d4ed8" if ineq in ["≥", "≤"] else "white"
        ax.scatter(
            roots,
            [0] * len(roots),
            s=130,
            edgecolors="#1d4ed8",
            facecolors=face,
            linewidths=2
        )

    ymin = min(y_vals) - 5
    ymax = max(y_vals) + 3

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(np.arange(int(np.floor(xmin)), int(np.ceil(xmax)) + 1, 1))
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("이차함수 그래프")
    ax.grid(True, linestyle="--", alpha=0.4)

    return fig

st.markdown("<div class='main-title'>🧪 자유 식 확인하기</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>원하는 이차함수를 만들고 그래프를 보며 이차부등식의 해를 찾아봅시다.</div>", unsafe_allow_html=True)

st.subheader("✏️ 이차식 만들기")

with st.container(border=True):
    if st.session_state.formula:
        latex_formula = format_formula_latex(st.session_state.formula)
        st.latex(f"f(x) = {latex_formula}")
    else:
        st.latex("f(x) =")

st.write("수식 버튼을 눌러 이차식을 만드세요.")

b1, b2, b3, b4, b5, b6, b7, b8 = st.columns([1, 1, 1, 1, 1, 1, 1.4, 1])

with b1:
    st.button("𝑥", use_container_width=True, on_click=add_token, args=("x",))
with b2:
    st.button("²", use_container_width=True, on_click=add_token, args=("^2",))
with b3:
    st.button("+", use_container_width=True, on_click=add_token, args=("+",))
with b4:
    st.button("-", use_container_width=True, on_click=add_token, args=("-",))
with b5:
    st.button("(", use_container_width=True, on_click=add_token, args=("(",))
with b6:
    st.button(")", use_container_width=True, on_click=add_token, args=(")",))
with b7:
    num = st.number_input("숫자 입력", min_value=0, max_value=30, value=1, step=1, label_visibility="collapsed")
with b8:
    st.button("추가", use_container_width=True, on_click=add_token, args=(str(num),))

c1, c2 = st.columns([1, 1])

with c1:
    st.button("🗑 지우기", use_container_width=True, on_click=clear_formula)

with c2:
    if st.button("✅ 식 확인", use_container_width=True):
        st.session_state.show_graph = True
        st.session_state.selected_range = None
        st.session_state.range_checked = False

if st.session_state.show_graph:
    try:
        expr = sp.sympify(clean_expr(st.session_state.formula))
        expanded = sp.expand(expr)

        a = expanded.coeff(x, 2)
        b = expanded.coeff(x, 1)
        c = expanded.coeff(x, 0)

        if a == 0:
            st.error("이차식이 아닙니다. x²항이 있는 식을 만들어 주세요.")
        else:
            st.divider()

            st.subheader("📝 만든 이차함수")
            st.latex(f"f(x) = {sp.latex(expanded)}")

            D = b**2 - 4*a*c

            st.subheader("🔍 판별식 확인")
            st.latex(f"D = b^2 - 4ac = {sp.latex(D)}")

            if D > 0:
                st.info("D > 0 이므로 그래프는 x축과 서로 다른 두 점에서 만납니다.")
            elif D == 0:
                st.info("D = 0 이므로 그래프는 x축에 한 점에서 접합니다.")
            else:
                st.info("D < 0 이므로 그래프는 x축과 만나지 않습니다.")

            st.subheader("📌 부등호 선택")

            i1, i2, i3, i4 = st.columns(4)

            with i1:
                if st.button("f(x) > 0", use_container_width=True):
                    st.session_state.ineq = ">"
                    st.session_state.selected_range = None
                    st.session_state.range_checked = False
            with i2:
                if st.button("f(x) < 0", use_container_width=True):
                    st.session_state.ineq = "<"
                    st.session_state.selected_range = None
                    st.session_state.range_checked = False
            with i3:
                if st.button("f(x) ≥ 0", use_container_width=True):
                    st.session_state.ineq = "≥"
                    st.session_state.selected_range = None
                    st.session_state.range_checked = False
            with i4:
                if st.button("f(x) ≤ 0", use_container_width=True):
                    st.session_state.ineq = "≤"
                    st.session_state.selected_range = None
                    st.session_state.range_checked = False

            graph_col, answer_col = st.columns([2, 1])

            with graph_col:
                st.subheader("📊 그래프")
                fig = draw_graph(expanded, st.session_state.ineq)
                st.pyplot(fig)

            with answer_col:
                if st.session_state.ineq is None:
                    st.info("부등호를 먼저 선택하세요.")
                else:
                    st.subheader("✏️ 해의 범위 선택")
                    st.latex(f"{sp.latex(expanded)} {st.session_state.ineq} 0")

                    for opt in answer_options(expanded):
                        if st.button(
                            opt,
                            use_container_width=True,
                            key=f"free_{expanded}_{st.session_state.ineq}_{opt}"
                        ):
                            st.session_state.selected_range = opt
                            st.session_state.range_checked = False

                    if st.session_state.selected_range:
                        st.info(f"선택한 답: {st.session_state.selected_range}")

                    if st.button("🔍 정답 확인", use_container_width=True):
                        st.session_state.range_checked = True

                    if st.session_state.range_checked:
                        correct = correct_answer(expanded, st.session_state.ineq)

                        if st.session_state.selected_range == correct:
                            st.success("정답입니다!")
                        else:
                            st.error("다시 생각해보세요.")

                        st.markdown("<div class='answer-box'>정답</div>", unsafe_allow_html=True)
                        st.write(correct)

    except Exception:
        st.error("식이 완성되지 않았습니다. 예: x² - 6x + 5 형태가 되도록 다시 만들어 주세요.")