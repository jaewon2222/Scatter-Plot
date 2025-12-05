import streamlit as st
import pandas as pd
import numpy as np

st.title("📈 산점도 (중복 강조 + 상관계수)")

st.write("X값과 Y값을 줄바꿈으로 입력해주세요.")

# --- 입력 영역 ---
x_input = st.text_area("X 값 입력 (한 줄에 하나씩)")
y_input = st.text_area("Y 값 입력 (한 줄에 하나씩)")

if st.button("산점도 그리기"):
    try:
        # 입력 파싱
        x_list = [float(x.strip()) for x in x_input.splitlines() if x.strip() != ""]
        y_list = [float(y.strip()) for y in y_input.splitlines() if y.strip() != ""]

        # 길이가 다를 경우 안내
        if len(x_list) != len(y_list):
            st.error(f"⚠️ X 개수: {len(x_list)}, Y 개수: {len(y_list)} — 개수가 다릅니다.")
            st.stop()

        # DataFrame 생성
        df = pd.DataFrame({"x": x_list, "y": y_list})

        # 중복 체크 count 컬럼 생성
        df["count"] = df.groupby(["x", "y"])["x"].transform("count")

        # *** 색 강하게: count값이 높을수록 색이 진해진다고 생각하면 됨 ***
        st.write("중복 값이 많을수록 점 색이 진하게 보입니다.")

        st.scatter_chart(df, x="x", y="y", color="count")

        # --- 상관계수 ---
        corr = np.corrcoef(df["x"], df["y"])[0, 1]
        st.subheader("📊 상관계수 (Pearson r)")
        st.write(f"**r = {corr:.4f}**")

        # 해석 자동 출력
        if abs(corr) < 0.2:
            desc = "거의 없음"
        elif abs(corr) < 0.4:
            desc = "약함"
        elif abs(corr) < 0.6:
            desc = "보통"
        elif abs(corr) < 0.8:
            desc = "강함"
        else:
            desc = "매우 강함"

        trend = "양의 상관" if corr > 0 else "음의 상관"

        st.write(f"➡️ **{trend} + {desc} 상관관계**")

    except:
        st.error("입력값을 숫자로 변환할 수 없습니다. 줄바꿈으로 숫자만 입력해주세요.")
