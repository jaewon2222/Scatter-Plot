import streamlit as st
import numpy as np

st.title("Scatter Plot + Regression Line + Correlation (No external libs)")

st.write("X와 Y 값을 쉼표(,)로 구분해 입력하세요.")

# --- 입력 ---
x_input = st.text_area("X 값 입력 (예: 1,2,3,4)")
y_input = st.text_area("Y 값 입력 (예: 2,3,4,5)")

# 데이터 파싱 함수
def parse_numbers(text):
    try:
        return np.array([float(i.strip()) for i in text.split(",") if i.strip() != ""])
    except:
        return None

x = parse_numbers(x_input)
y = parse_numbers(y_input)

if st.button("산점도 그리기"):
    if x is None or y is None:
        st.error("숫자만 입력해야 합니다.")
    else:
        st.write(f"X 개수: {len(x)}개")
        st.write(f"Y 개수: {len(y)}개")

        if len(x) != len(y):
            st.error("X와 Y의 개수가 다릅니다.")
        else:
            if len(x) < 2:
                st.error("최소 2개 이상의 데이터가 필요합니다.")
            else:
                # 중복 횟수 기반 색상 배열 생성
                points = list(zip(x, y))
                unique_pts, counts = np.unique(points, axis=0, return_counts=True)
                count_map = {tuple(pt): c for pt, c in zip(unique_pts, counts)}
                colors = np.array([count_map[(a, b)] for a, b in points])

                # 회귀선 계산 (NaN 대비)
                if np.std(x) == 0 or np.std(y) == 0:
                    slope, intercept = None, None
                    correlation = np.nan
                else:
                    slope, intercept = np.polyfit(x, y, 1)
                    correlation = np.corrcoef(x, y)[0, 1]

                # 산점도 그리기 (Streamlit 기본 API)
                chart_data = {
                    "x": x,
                    "y": y,
                    "color": colors
                }

                st.scatter_chart(chart_data, x="x", y="y", color="color")

                # 회귀선 추가 (Streamlit에는 직접 그릴 수 없으므로 텍스트로 표시)
                if slope is not None:
                    x_line = np.linspace(min(x), max(x), 200)
                    y_line = slope * x_line + intercept

                    reg_data = {"x": x_line, "y": y_line}
                    st.line_chart(reg_data, x="x", y="y")

                # 상관계수 표시
                st.subheader("📌 상관계수")

                if np.isnan(correlation):
                    st.write("상관계수 계산 불가 (데이터가 일정하거나 단조롭지 않음)")
                else:
                    st.write(f"r = **{correlation:.4f}**")

                    # 강도 판단
                    abs_r = abs(correlation)
                    if abs_r < 0.2:
                        strength = "매우 약한"
                        grade = 1
                    elif abs_r < 0.4:
                        strength = "약한"
                        grade = 2
                    elif abs_r < 0.6:
                        strength = "중간 정도의"
                        grade = 3
                    elif abs_r < 0.8:
                        strength = "강한"
                        grade = 4
                    else:
                        strength = "매우 강한"
                        grade = 5

                    # 방향
                    if correlation > 0:
                        direction = "양의 상관관계"
                    elif correlation < 0:
                        direction = "음의 상관관계"
                    else:
                        direction = "상관 없음"

                    st.write(f"➡️ **{strength} {direction}** (등급 {grade})")

                # 회귀식 출력
                st.subheader("📌 회귀식")
                if slope is None:
                    st.write("회귀선을 그릴 수 없습니다.")
                else:
                    st.write(f"y = {slope:.4f}x + {intercept:.4f}")

