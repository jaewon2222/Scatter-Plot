import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

st.title("직접 (a,b) 입력 산점도")

# 1. 텍스트 입력
input_text = st.text_area(
    "데이터를 (a,b) 형태로 입력하세요. 한 줄에 하나씩 입력 가능",
    "(1,2)\n(3,4)\n(5,6)"
)

# 2. 입력 파싱
data = []
pattern = r"\(\s*([\d\.\-]+)\s*,\s*([\d\.\-]+)\s*\)"

for line in input_text.split("\n"):
    match = re.match(pattern, line.strip())
    if match:
        a, b = float(match.group(1)), float(match.group(2))
        data.append((a, b))

if data:
    df = pd.DataFrame(data, columns=["X", "Y"])
    st.write("입력된 데이터 미리보기:", df)

    # 3. 산점도 그리기
    if st.button("산점도 그리기"):
        plt.figure(figsize=(8,6))
        sns.scatterplot(data=df, x="X", y="Y")
        st.pyplot(plt)
else:
    st.warning("올바른 (a,b) 형식의 데이터를 입력해주세요.")
