import streamlit as st
import plotly.express as px
import pandas as pd

st.title("산점도 입력기 (Plotly 버전)")

# 입력을 좀 유하게: 콤마, 공백, 엔터 모두 허용
x_raw = st.text_area("X 값들을 입력하세요 (쉼표, 공백, 줄바꿈 모두 가능)")
y_raw = st.text_area("Y 값들을 입력하세요 (쉼표, 공백, 줄바꿈 모두 가능)")

def parse_values(text):
    if not text.strip():
        return []
    # 공백, 콤마, 엔터 모두 가능하게 분리
    return [float(v) for v in text.replace(',', ' ').split()]

x = parse_values(x_raw)
y = parse_values(y_raw)

# 개수 다르면 알려주기
if len(x) != len(y):
    st.warning(f"⚠ X={len(x)}개, Y={len(y)}개 로 개수가 다릅니다.")
else:
    if len(x) > 0:
        df = pd.DataFrame({"X": x, "Y": y})

        # 중복 점 카운트
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            st.info(f"🔁 중복된 점이 {duplicates}개 있습니다.")

        # 산점도 그리기
        fig = px.scatter(
            df,
            x="X",
            y="Y",
            title="산점도 (중복 점 포함)",
            opacity=0.8,       # 중복점 겹치면 진해져서 자연스럽게 표시됨
            width=700,
            height=500,
        )
        st.plotly_chart(fig)
