import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

st.title("📊 산점도 + 회귀선 + 상관관계 분석기")

st.markdown("X와 Y를 각각 입력하세요. 콤마, 줄바꿈 모두 가능합니다.")

# -----------------------------
# 입력 받기
# -----------------------------
x_text = st.text_area("X 값 입력", height=120)
y_text = st.text_area("Y 값 입력", height=120)

def parse_input(text):
    text = text.replace("\n", ",")
    items = [t.strip() for t in text.split(",") if t.strip() != ""]
    nums = []
    for it in items:
        try:
            nums.append(float(it))
        except:
            pass
    return nums

X = parse_input(x_text)
Y = parse_input(y_text)

st.write(f"X 개수: {len(X)}")
st.write(f"Y 개수: {len(Y)}")

if len(X) != len(Y):
    st.error("❌ X와 Y의 개수가 다릅니다. 동일하게 입력하세요.")
    st.stop()

if len(X) < 2:
    st.warning("데이터가 2개 이상 필요합니다.")
    st.stop()

df = pd.DataFrame({"X": X, "Y": Y})

# -----------------------------
# 중복 감지
# -----------------------------
df["count"] = df.groupby(["X", "Y"])["X"].transform("count")

# 색을 강하게: count>=2는 빨강, 아니면 파랑
colors = df["count"].apply(lambda c: "red" if c >= 2 else "blue")

# -----------------------------
# 회귀선 계산
# -----------------------------
try:
    model = LinearRegression()
    model.fit(df[["X"]], df["Y"])
    slope = model.coef_[0]
    intercept = model.intercept_
    y_pred = model.predict(df[["X"]])
    regression_ok = True
except:
    regression_ok = False

# -----------------------------
# 상관계수 계산
# -----------------------------
corr = np.corrcoef(X, Y)[0, 1]

# NaN 방지
if np.isnan(corr):
    corr_text = "상관계수를 계산할 수 없습니다."
else:
    # 상관 강도 판별
    abs_c = abs(corr)
    if abs_c < 0.2:
        strength = "거의 없음"
    elif abs_c < 0.4:
        strength = "약함"
    elif abs_c < 0.6:
        strength = "중간"
    elif abs_c < 0.8:
        strength = "강함"
    else:
        strength = "매우 강함"

    # 양/음 판별
    direction = "양의 상관" if corr > 0 else "음의 상관"

    corr_text = f"상관계수: **{corr:.4f}**  
➡ {direction}, {strength}"

st.markdown("## 📈 산점도")

# -----------------------------
# 그림 그리기 (matplotlib 사용)
# -----------------------------
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 5))

# 산점도
ax.scatter(df["X"], df["Y"], c=colors, s=60, alpha=0.8)

# 회귀선
if regression_ok:
    x_line = np.linspace(df["X"].min(), df["X"].max(), 200)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, linewidth=2)

# 중복 점 강하게 표시 - 범례 만들기
handles = []

if any(df["count"] >= 2):
    red_patch = plt.Line2D([0], [0], marker='o', color='red', linestyle='None', markersize=8, label='중복 데이터')
    handles.append(red_patch)

blue_patch = plt.Line2D([0], [0], marker='o', color='blue', linestyle='None', markersize=8, label='단일 데이터')
handles.append(blue_patch)

ax.legend(handles=handles)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("산점도 + 회귀선")

st.pyplot(fig)

# -----------------------------
# 결과 출력
# -----------------------------
st.markdown("## 📌 상관계수 분석")
st.markdown(corr_text)

if regression_ok:
    st.markdown(f"### 📐 회귀식  
    **y = {slope:.4f}x + {intercept:.4f}**")
