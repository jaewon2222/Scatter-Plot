import streamlit as st
import numpy as np
import pandas as pd

st.title("📈 산점도 + 상관계수 + 회귀선 시각화")

st.write("X값과 Y값을 각각 줄바꿈으로 입력하세요.")

# 입력 UI
x_input = st.text_area("X 값 (줄바꿈으로 분리)", height=150)
y_input = st.text_area("Y 값 (줄바꿈으로 분리)", height=150)

if st.button("산점도 그리기"):

    try:
        # 문자열을 줄바꿈 기준으로 분리하고 숫자로 변환
        x_list = [float(v) for v in x_input.split() if v.strip() != ""]
        y_list = [float(v) for v in y_input.split() if v.strip() != ""]

        len_x = len(x_list)
        len_y = len(y_list)

        # 개수 표시
        st.write(f"🔢 X 개수: **{len_x}**, Y 개수: **{len_y}**")

        # 개수가 다르면 경고
        if len_x != len_y:
            st.error("⚠️ X와 Y의 개수가 다릅니다. 동일한 개수여야 합니다.")
            st.stop()

        # DataFrame 생성
        df = pd.DataFrame({"X": x_list, "Y": y_list})

        # 중복 데이터 개수 계산
        df['count'] = df.groupby(['X', 'Y'])['X'].transform('count')

        # 색상: count가 높을수록 더 진하게(=중복 강조)
        # 대신 matplotlib 없이 Streamlit 기본 scatter 사용
        # Streamlit 내장 chart는 색 설정 X → 우리가 직접 색 배열 생성
        max_count = df['count'].max()
        df['color'] = df['count'] / max_count  # 0~1 사이로 정규화

        # 회귀선 계산
        try:
            slope, intercept = np.polyfit(df["X"], df["Y"], 1)
            df["reg_y"] = df["X"] * slope + intercept
            reg_available = True
        except Exception:
            slope = None
            intercept = None
            reg_available = False

        # 상관계수 계산
        corr = np.corrcoef(df["X"], df["Y"])[0, 1]
        if np.isnan(corr):
            corr_text = "상관계수: 계산 불가 (NaN)"
            corr_strength = "데이터가 모두 같거나 변화가 없어 상관관계를 판단할 수 없습니다."
        else:
            corr_text = f"상관계수: **{corr:.4f}**"

            # 상관관계 해석 (양/음 + 강도)
            if corr > 0:
                direction = "양의 상관관계"
            elif corr < 0:
                direction = "음의 상관관계"
            else:
                direction = "상관 없음"

            abs_corr = abs(corr)

            if abs_corr >= 0.8:
                strength = "강한"
            elif abs_corr >= 0.5:
                strength = "중간"
            elif abs_corr >= 0.3:
                strength = "약한"
            elif abs_corr > 0:
                strength = "매우 약한"
            else:
                strength = ""

            if abs_corr == 0:
                corr_strength = "상관 없음"
            else:
                corr_strength = f"{strength} {direction}"

        # 결과 출력
        st.subheader("📌 상관계수 분석")
        st.write(corr_text)
        st.write(corr_strength)

        # Streamlit 내장 scatter_chart 사용 → 색을 직접 배열로 전달
        st.subheader("📊 산점도 (중복 강조 + 회귀선 포함)")

        # 산점도용 데이터
        scatter_df = df[["X", "Y", "color"]]

        # 스트림릿 기본 차트는 color label 못 쓰므로 이렇게 변환
        st.scatter_chart(
            scatter_df,
            x="X",
            y="Y",
            color="color",
            size=None,
        )

        # 회귀선 표시 (Table로 표시 — 기본 차트엔 Overlay 불가)
        if reg_available:
            st.subheader("📉 회귀선")
            st.write(f"**회귀식:**  y = {slope:.4f}x + {intercept:.4f}")

            # 회귀선 선형 데이터 표시
            st.line_chart(
                df[["X", "reg_y"]].sort_values("X"),
                x="X",
                y="reg_y"
            )

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
