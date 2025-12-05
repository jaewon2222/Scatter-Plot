import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("산점도 + 회귀선 + 상관계수 분석기 (Altair 기반)")

st.write("X값과 Y값을 줄바꿈 기준으로 입력하세요. 예:")
st.code("1\n2\n3\n4\n5")

# ===== 입력 =====
x_text = st.text_area("X 값 입력", "")
y_text = st.text_area("Y 값 입력", "")

def parse_values(text):
    values = []
    for line in text.splitlines():
        line = line.strip()
        if line == "":
            continue
        try:
            values.append(float(line))
        except:
            pass
    return values

x_list = parse_values(x_text)
y_list = parse_values(y_text)

len_x = len(x_list)
len_y = len(y_list)

st.write(f"X 개수: **{len_x}개**, Y 개수: **{len_y}개**")

if len_x != len_y:
    st.error("❌ X와 Y의 개수가 일치해야 합니다.")
    st.stop()

if len_x < 2:
    st.warning("데이터가 너무 적습니다. 2개 이상 입력해주세요.")
    st.stop()

# ===== DataFrame =====
df = pd.DataFrame({"X": x_list, "Y": y_list})

# 중복 count 계산
counts = df.groupby(["X", "Y"]).size().reset_index(name="count")
counts["count"] = counts["count"].astype(int)

# 0 제거
counts = counts[counts["count"] > 0].copy()

# ===== 상관계수 =====
corr = df["X"].corr(df["Y"])

if np.isnan(corr):
    corr_text = "상관계수: 계산 불가 (모든 값 동일)"
else:
    strength = ""
    abs_corr = abs(corr)

    if abs_corr < 0.2:
        strength = "매우 약한"
    elif abs_corr < 0.4:
        strength = "약한"
    elif abs_corr < 0.6:
        strength = "중간 정도의"
    elif abs_corr < 0.8:
        strength = "강한"
    else:
        strength = "매우 강한"

    direction = "양의" if corr > 0 else "음의"
    corr_text = f"상관계수: **{corr:.4f}** → **{direction} {strength} 상관관계**"

st.markdown(f"### 📊 {corr_text}")

# ===== 회귀선 계산 =====
slope, intercept = np.polyfit(df["X"], df["Y"], 1)
df["regression"] = slope * df["X"] + intercept

# ===== 산점도 + 회귀선 =====
point_chart = (
    alt.Chart(counts)
    .mark_circle()
    .encode(
        x="X:Q",
        y="Y:Q",
        color=alt.Color(
            "count:Q",
            scale=alt.Scale(
                scheme="redyellowblue",
                domain=[counts["count"].min(), counts["count"].max()]
            ),
            legend=alt.Legend(title="중복 개수")
        ),
        size=alt.Size("count:Q", scale=alt.Scale(range=[50, 400]), legend=None),  # 👈 size 범례 제거됨
        tooltip=["X", "Y", "count"]
    )
)

reg_chart = (
    alt.Chart(df)
    .mark_line(color="black")
    .encode(
        x="X:Q",
        y="regression:Q"
    )
)

final_chart = point_chart + reg_chart

st.altair_chart(final_chart, use_container_width=True)

st.write(f"회귀식: **Y = {slope:.4f} X + {intercept:.4f}**")
