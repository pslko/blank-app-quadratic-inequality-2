import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import random

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
