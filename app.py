import streamlit as st
import pandas as pd
import numpy as np

st.title("📈 산점도 + 회귀선 + 상관 분석")

st.write("아래 입력창에 X값들과 Y값들을 넣어주세요.")
st.write("띄어쓰기, 엔터, 콤마 모두 입력 가능!")

# ---------------------------
# 데이터 파싱 함수
# ---------------------------
def parse_input(text):
    # 숫자만 추출
    text = text.replace(",", " ").replace("\n", " ")
    parts = text.split()
    nums = []
    for p in parts:
        try:
            nums.append(float(p))
        except:
            pass
    return nums

# ---------------------------
# 입력
# ---------------------------
x_text = st.text_area("X 값 입력")
y_text = st.text_area("Y 값 입력")

x = parse_input(x_text)
y = parse_input(y_text)

st.write(f"X 개수: {len(x)}개")
st.write(f"Y 개수: {len(y)}개")

# ---------------------------
# 데이터 길이 불일치 처리
# ---------------------------
if len(x) != len(y):
    st.error("⚠️ X와 Y의 개수가 다릅니다. 같은 개수여야 산점도를 그릴 수 있습니다.")
else:
    if len(x) > 1:  # 최소 2개 이상일 때만 처리
        
        df = pd.DataFrame({"x": x, "y": y})

        # ---------------------------
        # 중복 점 강도 표시: 같은 점일수록 color 값 증가
        # ---------------------------
        df["freq"] = df.groupby(["x", "y"])["x"].transform("count")

        # ---------------------------
        # 회귀선 계산
        # ---------------------------
        try:
            coef = np.polyfit(df["x"], df["y"], 1)
            a, b = coef[0], coef[1]
            df["reg"] = a * df["x"] + b
        except:
            a = b = None

        # ---------------------------
        # 상관계수 계산
        # ---------------------------
        try:
            corr = np.corrcoef(df["x"], df["y"])[0, 1]
        except:
            corr = np.nan

        # ---------------------------
        # 상관계수 해석
        # ---------------------------
        def interpret(r):
            if np.isnan(r):
                return "상관계수를 계산할 수 없습니다 (NaN)."

            sign = "양의 상관" if r > 0 else "음의 상관" if r < 0 else "상관 없음"

            strength = abs(r)
            if strength >= 0.8:
                level = "매우 강한"
            elif strength >= 0.6:
                level = "강한"
            elif strength >= 0.4:
                level = "중간"
            elif strength >= 0.2:
                level = "약한"
            else:
                level = "매우 약한 또는 거의 없는"

            return f"{level} {sign} 관계 (r = {r:.3f})"

        st.subheader("📌 상관 분석 결과")
        st.write(interpret(corr))

        # ---------------------------
        # 산점도 (중복점: freq로 색 강하게)
        # ---------------------------
        st.subheader("📊 산점도")
        st.scatter_chart(df, x="x", y="y", color="freq")

        # ---------------------------
        # 회귀선 별도 표시
        # ---------------------------
        if a is not None:
            st.subheader("📐 회귀선")
            st.write(f"회귀식: **y = {a:.4f}x + {b:.4f}**")

            # 회귀선 그리기용
            reg_df = df.sort_values("x")[["x", "reg"]]
            st.line_chart(reg_df, x="x", y="reg")

    else:
        st.warning("데이터가 최소 2개 이상 필요합니다.")
