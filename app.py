import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 산점도 + 상관계수 + 회귀선")

st.write("X와 Y 값을 줄바꿈으로 넣어주세요. (쉼표/공백 입력도 자동 처리됨)")

# -------------------------
# 입력 함수 (유하게 처리)
# -------------------------
def parse_input(text):
    if not text.strip():
        return []
    # 쉼표 / 공백 / 줄바꿈 모두 처리
    items = text.replace(",", " ").split()
    nums = []
    for v in items:
        try:
            nums.append(float(v))
        except:
            pass
    return nums


# -------------------------
# 입력창
# -------------------------
x_input = st.text_area("X값 입력", height=150)
y_input = st.text_area("Y값 입력", height=150)

x = parse_input(x_input)
y = parse_input(y_input)

st.write(f"📌 X 개수: **{len(x)}개**, Y 개수: **{len(y)}개**")

if len(x) != len(y):
    st.error("❗ X와 Y의 개수가 다릅니다. 같은 개수여야 합니다.")
    st.stop()

if len(x) == 0:
    st.warning("값을 입력해주세요.")
    st.stop()

# -------------------------
# 데이터프레임 생성
# -------------------------
df = pd.DataFrame({"x": x, "y": y})

# -------------------------
# 중복 점 카운트
# -------------------------
df["count"] = df.groupby(["x", "y"])["x"].transform("count")

# 색 진하게 하기 위해 count → alpha로 변환
alpha = np.clip(df["count"] / df["count"].max(), 0.3, 1.0)

# -------------------------
# 회귀선 계산
# -------------------------
if len(df) > 1:
    slope, intercept = np.polyfit(df["x"], df["y"], 1)
    df_sorted = df.sort_values("x")  # 회귀선 깨지는 문제 해결
    reg_x = df_sorted["x"]
    reg_y = slope * reg_x + intercept
else:
    slope, intercept = None, None

# -------------------------
# 상관계수 계산
# -------------------------
try:
    corr = np.corrcoef(df["x"], df["y"])[0, 1]
    if np.isnan(corr):
        raise ValueError
except:
    corr = None

# -------------------------
# 상관 해석
# -------------------------
def interpret_corr(c):
    if c is None:
        return "상관관계 계산 불가"

    # 방향
    if c > 0:
        direction = "양의 상관관계"
    elif c < 0:
        direction = "음의 상관관계"
    else:
        direction = "상관 없음"

    # 강도
    ac = abs(c)
    if ac >= 0.8:
        strength = "매우 강한"
    elif ac >= 0.6:
        strength = "강한"
    elif ac >= 0.4:
        strength = "중간"
    elif ac >= 0.2:
        strength = "약한"
    else:
        strength = "매우 약한"

    return f"{strength} {direction}"

interpret_text = interpret_corr(corr)

# -------------------------
# 플롯 그리기
# -------------------------
fig, ax = plt.subplots(figsize=(7, 5))

scatter = ax.scatter(
    df["x"],
    df["y"],
    c=df["count"],          # count 기반 색상
    alpha=alpha,            # 중복 강하게
    cmap="viridis"
)

# 회귀선 추가
if slope is not None:
    ax.plot(reg_x, reg_y, linewidth=2, color="red")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("산점도 (중복 강조 + 회귀선)")

# 필요없는 범례 제거
cb = plt.colorbar(scatter, ax=ax)
cb.set_label("중복 수")

st.pyplot(fig)

# -------------------------
# 결과 텍스트 출력
# -------------------------
if corr is not None:
    st.markdown(f"### 📊 상관계수: **{corr:.4f}**")
else:
    st.markdown("### 📊 상관계수: 계산 불가")

st.markdown(f"### 📘 해석: **{interpret_text}**")
