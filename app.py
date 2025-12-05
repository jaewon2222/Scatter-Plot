import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("산점도 + 회귀선 + 상관관계 분석")

st.write("X값과 Y값을 각각 줄바꿈으로 입력하세요.")

# -----------------------------
# 입력
# -----------------------------
x_text = st.text_area("X 값 입력 (줄바꿈으로 구분)", height=150)
y_text = st.text_area("Y 값 입력 (줄바꿈으로 구분)", height=150)

if st.button("그래프 그리기"):
    try:
        x_list = [float(i.strip()) for i in x_text.splitlines() if i.strip() != ""]
        y_list = [float(i.strip()) for i in y_text.splitlines() if i.strip() != ""]
    except:
        st.error("숫자만 입력해주세요.")
        st.stop()

    # 길이 체크
    len_x = len(x_list)
    len_y = len(y_list)

    st.write(f"X 개수: **{len_x}개**,  Y 개수: **{len_y}개**")

    if len_x != len_y:
        st.error("X와 Y의 개수가 다릅니다. 동일해야 합니다.")
        st.stop()

    # 데이터프레임 생성
    df = pd.DataFrame({"x": x_list, "y": y_list})

    # -----------------------------
    # 중복 점 강조: 같은 좌표일수록 색 진하게
    # -----------------------------
    df["count"] = df.groupby(["x", "y"])["x"].transform("count")

    # -----------------------------
    # 상관계수 계산
    # -----------------------------
    corr = df["x"].corr(df["y"])

    if pd.isna(corr):
        corr_text = "상관계수를 계산할 수 없습니다 (NaN)."
    else:
        if corr > 0.7:
            level = "강한 양의 상관"
        elif corr > 0.3:
            level = "약한 양의 상관"
        elif corr > 0:
            level = "매우 약한 양의 상관"
        elif corr < -0.7:
            level = "강한 음의 상관"
        elif corr < -0.3:
            level = "약한 음의 상관"
        elif corr < 0:
            level = "매우 약한 음의 상관"
        else:
            level = "상관 없음"

        corr_text = f"상관계수: **{corr:.4f}** → **{level}**"

    st.subheader("📊 상관관계")
    st.write(corr_text)

    # -----------------------------
    # 회귀선 계산
    # -----------------------------
    if len(df) > 1:
        slope, intercept = np.polyfit(df["x"], df["y"], 1)
        df["reg_y"] = df["x"] * slope + intercept
        st.write(f"회귀선:  y = {slope:.4f}x + {intercept:.4f}")
    else:
        st.write("데이터가 너무 적어서 회귀선을 그릴 수 없습니다.")
        df["reg_y"] = np.nan

    # -----------------------------
    # Altair 산점도 + 회귀선
    # -----------------------------
    scatter = (
        alt.Chart(df)
        .mark_circle(size=60)
        .encode(
            x="x",
            y="y",
            color=alt.Color("count:Q", scale=alt.Scale(scheme="redyellowblue")),
            tooltip=["x", "y", "count"]
        )
    )

    regression_line = (
        alt.Chart(df)
        .mark_line(color="black")
        .encode(
            x="x",
            y="reg_y"
        )
    )

    chart = scatter + regression_line

    st.altair_chart(chart, use_container_width=True)
