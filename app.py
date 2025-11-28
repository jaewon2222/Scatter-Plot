import streamlit as st
import pandas as pd
import altair as alt

st.title("x 값, y 값 별도 입력 산점도")

# 1. x 값 입력
x_input = st.text_area(
    "X 값들을 콤마(,)로 구분하여 입력하세요",
    "1,2,3,4,5,6,7,8,9,10"
)

# 2. y 값 입력
y_input = st.text_area(
    "Y 값들을 콤마(,)로 구분하여 입력하세요",
    "2,3,4,5,6,7,8,9,10,11"
)

try:
    # 3. 문자열 → 숫자 리스트로 변환
    x_values = [float(x.strip()) for x in x_input.split(",") if x.strip() != ""]
    y_values = [float(y.strip()) for y in y_input.split(",") if y.strip() != ""]

    # 4. 길이 확인
    if len(x_values) != len(y_values):
        st.error("X와 Y 값의 개수가 다릅니다. 동일한 개수로 입력해주세요.")
    else:
        # 5. DataFrame 생성
        df = pd.DataFrame({"X": x_values, "Y": y_values})
        st.write("데이터 미리보기:", df)

        # 6. 산점도 그리기
        chart = alt.Chart(df).mark_circle(size=60).encode(
            x='X',
            y='Y'
        ).interactive()

        st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error(f"입력값을 확인해주세요: {e}")
