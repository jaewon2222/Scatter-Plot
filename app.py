import streamlit as st
import pandas as pd

st.title("🎯 간단 산점도 도구 (모듈 설치 필요 없음)")

st.write("X값과 Y값을 각각 입력하세요. 쉼표(,) 또는 공백으로 구분할 수 있습니다.")

# 입력 받기
x_input = st.text_area("X 값 입력", placeholder="예: 1, 2, 3, 4, 5")
y_input = st.text_area("Y 값 입력", placeholder="예: 2, 4, 5, 7, 10")

def parse_values(text):
    if not text.strip():
        return []
    text = text.replace(",", " ")
    parts = text.split()
    values = []
    for p in parts:
        try:
            values.append(float(p))
        except:
            pass
    return values

x_list = parse_values(x_input)
y_list = parse_values(y_input)

# 길이 표시
st.write(f"X 개수: {len(x_list)}")
st.write(f"Y 개수: {len(y_list)}")

# 개수 다르면 경고
if len(x_list) != len(y_list):
    st.error("❌ X와 Y의 개수가 다릅니다. 동일한 개수를 입력하세요.")
else:
    if len(x_list) > 0:
        df = pd.DataFrame({'X': x_list, 'Y': y_list})
        
        st.write("### 📌 산점도")
        st.scatter_chart(df, x='X', y='Y')

        # 중복 여부 표시
        duplicated = df.duplicated().sum()
        if duplicated > 0:
            st.warning(f"⚠ 중복된 점 {duplicated}개 있음")
        else:
            st.success("✔ 중복된 점 없음")
