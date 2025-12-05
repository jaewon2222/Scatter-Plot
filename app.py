import streamlit as st
import pandas as pd
import altair as alt

st.title("좌표 중복 시각화")

# 좌표 입력
user_input = st.text_area(
    "좌표를 입력하세요 (예: 1,2  1,2  3,4)",
    placeholder="예: 1,2  1,2  3,4"
)

# 입력 없으면 종료
if not user_input.strip():
    st.stop()

# 입력 파싱
points = []
for pair in user_input.split():
    if "," in pair:
        try:
            x, y = pair.split(",")
            points.append((float(x), float(y)))
        except:
            pass

df = pd.DataFrame(points, columns=["X", "Y"])

# 중복 카운트 추가
df_count = df.value_counts().reset_index(name="count")

# count 0 제거 필요 없음(애초에 없음)

# 시각화
points_chart = (
    alt.Chart(df_count)
    .mark_circle()
    .encode(
        x="X:Q",
        y="Y:Q",
        size=alt.Size("count:Q", legend=None),  # 🔥 count 범례 제거
        color=alt.Color(
            "count:Q",
            scale=alt.Scale(scheme="yellowred"),
            title="중복 개수"
        ),
        tooltip=["X", "Y", "count"]
    )
)

# 회귀선
reg_line = (
    alt.Chart(df_count)
    .transform_regression("X", "Y")
    .mark_line(color="black")
)

chart = points_chart + reg_line
st.altair_chart(chart, use_container_width=True)
