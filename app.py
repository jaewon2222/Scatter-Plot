import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("📊 산점도 + 중복 점 강조 + 상관계수 계산기")

st.write("X와 Y 값을 각각 입력하세요. 숫자만 자동 인식됩니다.")

# --- 입력 받기 ---
x_text = st.text_area("X 값 (쉼표, 줄바꿈 등 아무 방식 OK)")
y_text = st.text_area("Y 값 (쉼표, 줄바꿈 등 아무 방식 OK)")

def extract_numbers(text):
    # 숫자만 추출
    return [float(x) for x in text.replace("\n", " ").replace(",", " ").split() if x.replace('.','',1).isdigit()]

x_values = extract_numbers(x_text)
y_values = extract_numbers(y_text)

# --- 데이터 길이 안내
st.write(f"X 개수: {len(x_values)}개")
st.write(f"Y 개수: {len(y_values)}개")

if len(x_values) != len(y_values):
    st.error("❗ X와 Y의 개수가 다릅니다. 산점도를 그릴 수 없습니다.")
else:
    if len(x_values) > 0:
        df = pd.DataFrame({"x": x_values, "y": y_values})

        # --- 상관계수 계산 ---
        corr = np.corrcoef(df["x"], df["y"])[0, 1]
        st.subheader(f"📈 상관계수 (Pearson r): **{corr:.4f}**")

        # --- 중복 점 더 잘 보이게 처리 ---
        # jitter 적용: 중복점이 살짝 퍼져 보이게 함
        df["x_jitter"] = df["x"] + np.random.normal(0, 0.02, len(df))
        df["y_jitter"] = df["y"] + np.random.normal(0, 0.02, len(df))

        # --- Altair 산점도 ---
        scatter = (
            alt.Chart(df)
            .mark_circle(size=90, opacity=0.5)  # 투명도 0.5 → 겹칠수록 진하게
            .encode(
                x="x_jitter",
                y="y_jitter",
                tooltip=["x", "y"]
            )
        )

        st.altair_chart(scatter, use_container_width=True)
