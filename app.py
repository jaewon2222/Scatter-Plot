import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.title("좌표 입력 + 중복 개수 표시 그래프")

# --------------------------
# 데이터 입력
# --------------------------
st.write("좌표를 입력하세요 (예: 1,2)")

points = st.text_area("좌표들 입력 (한 줄에 하나):")

data_list = []
if points.strip():
    for line in points.split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            x, y = line.split(",")
            data_list.append((float(x), float(y)))
        except:
            st.error(f"잘못된 입력: {line}")

df = pd.DataFrame(data_list, columns=["X", "Y"])

# --------------------------
# 중복 count 계산
# --------------------------
if not df.empty:
    count_df = df.groupby(["X", "Y"]).size().reset_index(name="count")

    # count = 0 제거 (원래 생길 일이 없지만 혹시 대비)
    count_df = count_df[count_df["count"] > 0]

    # --------------------------
    # 회귀선 계산
    # --------------------------
    if len(df) >= 2:
        coef = np.polyfit(df["X"], df["Y"], 1)
        poly_fn = np.poly1d(coef)

        reg_x = np.linspace(df["X"].min(), df["X"].max(), 50)
        reg_y = poly_fn(reg_x)

        reg_df = pd.DataFrame({"X": reg_x, "Y": reg_y})
    else:
        reg_df = pd.DataFrame({"X": [], "Y": []})

    # --------------------------
    # Altair 그래프
    # --------------------------
    scatter = (
        alt.Chart(count_df)
        .mark_circle()
        .encode(
            x="X:Q",
            y="Y:Q",
            size=alt.Size("count:Q", legend=None),     # ← 아래 count 범례 제거
            color=alt.Color(
                "count:Q",
                scale=alt.Scale(scheme="yellowred"),
                legend=alt.Legend(title="중복 개수"),   # 색상 범례만 유지
            ),
            tooltip=["X", "Y", "count"]
        )
    )

    regression_line = (
        alt.Chart(reg_df)
        .mark_line(color="black")
        .encode(x="X:Q", y="Y:Q")
    )

    chart = scatter + regression_line

    st.altair_chart(chart, use_container_width=True)

    st.write("### 처리된 데이터 (중복 개수 포함)")
    st.dataframe(count_df)
else:
    st.info("좌표를 입력하세요.")
