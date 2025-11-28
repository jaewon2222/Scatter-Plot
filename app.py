import streamlit as st
import pandas as pd
import altair as alt
import re

st.title("최소 모듈 산점도 (a,b 입력)")

# 1. 데이터 입력
input_text = st.text_area(
    "데이터를 (a,b) 형태로 입력하세요. 한 줄에 하나씩",
    "(1,2)\n(3,4)\n(5,6)"
)

# 2. (a,b) 파싱
data = []
pattern = r"\(\s*([\d\.\-]+)\s*,\s*([\d\.\-]+)\s*\)"

for line in input_text.split("\n"):
    match = re.match(pattern, line.strip())
    if match:
        a, b = float(match.group(1)), float(match.group(2))
        data.append((a, b))

if data:
    df = pd.DataFrame(data, columns=["X", "Y"])
    st.write("입력된 데이터:", df)

    # 3. 산점도 그리기 (Altair 사용)
    chart = alt.Chart(df).mark_circle(size=60).encode(
        x='X',
        y='Y'
    ).interactive()  # <-- 괄호 구조 확인 완료

    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("올바른 (a,b) 형식의 데이터를 입력해주세요.")

