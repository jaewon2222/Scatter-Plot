import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.title("부드러운 산점도 생성기 ✨")

def parse_numbers(text):
    """
    공백, 쉼표, 줄바꿈 모두 허용하는 유연한 파서
    """
    if not text.strip():
        return []
    cleaned = text.replace(",", " ")
    parts = cleaned.split()
    return [float(p) for p in parts]

st.subheader("X 값 입력")
x_raw = st.text_area("X 데이터를 입력하세요 (예: 1 2 3 4 또는 줄바꿈 가능)", height=120)

st.subheader("Y 값 입력")
y_raw = st.text_area("Y 데이터를 입력하세요 (예: 10 20 30 40)", height=120)

X = parse_numbers(x_raw)
Y = parse_numbers(y_raw)

st.write(f"X 개수: {len(X)}개")
st.write(f"Y 개수: {len(Y)}개")

if len(X) != len(Y):
    st.error("❗ X와 Y의 길이가 다릅니다. 그래프를 그릴 수 없습니다.")
else:
    if len(X) > 0:
        X_arr = np.array(X).reshape(-1, 1)
        Y_arr = np.array(Y)

        # 상관계수 계산
        corr = np.corrcoef(X, Y)[0, 1]

        # 선형 회귀
        model = LinearRegression()
        model.fit(X_arr, Y_arr)
        slope = model.coef_[0]
        intercept = model.intercept_

        st.subheader("상관계수와 회귀 결과")
        st.write(f"📎 상관계수 r: **{corr:.4f}**")
        st.write(f"📎 회귀식: **y = {slope:.4f} x + {intercept:.4f}**")

        # 산점도 그리기
        fig, ax = plt.subplots()
        ax.scatter(X, Y, alpha=0.5)  # 중복 점은 자동으로 색이 진해짐

        # 회귀선
        x_line = np.linspace(min(X), max(X), 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("산점도 + 회귀선")

        st.pyplot(fig)
