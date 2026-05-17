import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

x = sp.symbols("x")

st.markdown("<div class='main-title'>🧪 자유 식 확인하기</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>원하는 이차함수를 입력하고 그래프와 해를 확인해 봅시다.</div>", unsafe_allow_html=True)

st.subheader("✏️ 이차식 입력")

user_expr = st.text_input(
    "이차식을 입력하세요",
    placeholder="예: x^2 - 6*x + 5",
    value="x^2 - 6*x + 5"
)

ineq = st.radio(
    "부등호 선택",
    [">", "<", "≥", "≤"],
    horizontal=True
)


def clean_expr(text):
    text = text.replace("^", "**")
    text = text.replace(")(", ")*(")
    text = text.replace("x(", "x*(")
    text = text.replace(")x", ")*x")
    return text


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

    return "해를 찾을 수 없습니다. 식을 확인해주세요."


def draw_graph(expr, ineq):
    func = sp.lambdify(x, expr, "numpy")
    x_vals = np.linspace(-10, 10, 800)
    y_vals = func(x_vals)

    fig, ax = plt.subplots()
    ax.axhline(0, color="black", linewidth=1)
    ax.plot(x_vals, y_vals, color="#1f77b4", linewidth=2)

    if ineq in [">", "≥"]:
        mask = y_vals > 0 if ineq == ">" else y_vals >= 0
        ax.fill_between(x_vals, y_vals, 0, where=mask, interpolate=True, color="#c6f6d5", alpha=0.45)
    else:
        mask = y_vals < 0 if ineq == "<" else y_vals <= 0
        ax.fill_between(x_vals, y_vals, 0, where=mask, interpolate=True, color="#fed7d7", alpha=0.45)

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("이차 함수 그래프")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_xlim(x_vals.min(), x_vals.max())

    return fig


try:
    expr = sp.sympify(clean_expr(user_expr))

    st.subheader("📝 입력한 이차부등식")
    st.latex(f"{sp.latex(expr)} {ineq} 0")

    st.subheader("📊 그래프")
    fig = draw_graph(expr, ineq)
    st.pyplot(fig)

    st.subheader("✅ 해")
    answer = correct_answer(expr, ineq)
    st.success(answer)

    st.subheader("🔍 판별식 확인")
    expanded = sp.expand(expr)
    a = expanded.coeff(x, 2)
    b = expanded.coeff(x, 1)
    c = expanded.coeff(x, 0)
    D = b**2 - 4*a*c

    st.latex(f"D = b^2 - 4ac = {sp.latex(D)}")

    if D > 0:
        st.info("D > 0 이므로 그래프는 x축과 서로 다른 두 점에서 만납니다.")
    elif D == 0:
        st.info("D = 0 이므로 그래프는 x축에 한 점에서 접합니다.")
    else:
        st.info("D < 0 이므로 그래프는 x축과 만나지 않습니다.")
except Exception:
    st.error("식을 다시 확인해 주세요. 예: x^2 - 6*x + 5 또는 x**2 - 6*x + 5")