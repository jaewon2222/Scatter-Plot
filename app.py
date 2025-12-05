import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import json
import re  # 정규표현식 사용을 위해 추가

# 애플리케이션 제목
st.set_page_config(page_title="구글 시트 데이터 분석기", layout="wide")
st.title("📊 Google Sheets 연동 산점도/회귀 분석기")

# 사용 설명
with st.expander("ℹ️ 사용 방법 보러가기 (필독)", expanded=True):
    st.write("""
    1. **Google 스프레드시트**를 준비합니다.
    2. 우측 상단 **[공유]** 버튼을 누릅니다.
    3. '일반 액세스'를 **'링크가 있는 모든 사용자'**로 변경합니다 (뷰어 권한).
    4. **[링크 복사]**를 눌러 아래 입력창에 붙여넣으세요.
    """)

# ===== 1. 구글 시트 링크 입력 =====
sheet_url = st.text_input(
    "Google 스프레드시트 링크를 붙여넣으세요", 
    placeholder="https://docs.google.com/spreadsheets/d/..."
)

df_raw = None

if sheet_url:
    try:
        # 정규표현식으로 Sheet ID 추출
        # /d/ 다음에 오는 문자열(알파벳, 숫자, -, _)을 찾음
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', sheet_url)
        
        if match:
            sheet_id = match.group(1)
        else:
            st.error("올바른 구글 스프레드시트 링크 형식이 아닙니다. (ID를 찾을 수 없음)")
            st.stop()
            
        # GID(시트 ID) 추출
        # #gid=숫자 또는 &gid=숫자 형태를 찾음
        gid = "0"
        match_gid = re.search(r'[#&]gid=([0-9]+)', sheet_url)
        if match_gid:
            gid = match_gid.group(1)
            
        # 더 안정적인 gviz 엔드포인트 사용 (export 대신)
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&gid={gid}"
        
        # 데이터 로드
        df_raw = pd.read_csv(csv_url)
        st.success("✅ 데이터를 성공적으로 불러왔습니다!")
        
        # 데이터 미리보기 (상위 5행)
        st.caption("데이터 미리보기:")
        st.dataframe(df_raw.head(), use_container_width=True)

    except Exception as e:
        st.error(f"❌ 데이터를 불러오지 못했습니다. 시트가 '공개' 상태인지 확인해주세요.\n\n(참고: HTTP 400 에러는 링크 형식이 잘못되었을 때 주로 발생합니다.)\n에러 메시지: {e}")
        st.stop()

# 데이터가 로드되었을 때만 실행
if df_raw is not None:
    # ===== 2. X, Y 컬럼 선택 =====
    st.markdown("### 🛠️ 분석할 변수 선택")
    
    columns = df_raw.columns.tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("X축 데이터 선택 (원인)", columns, index=0)
    with col2:
        y_col = st.selectbox("Y축 데이터 선택 (결과)", columns, index=1 if len(columns) > 1 else 0)

    # ===== 데이터 전처리 =====
    # 선택된 컬럼을 숫자형으로 강제 변환 (문자열 등은 NaN 처리)
    x_list = pd.to_numeric(df_raw[x_col], errors='coerce')
    y_list = pd.to_numeric(df_raw[y_col], errors='coerce')
    
    # NaN 값이 있는 행 제거를 위해 임시 DataFrame 생성
    temp_df = pd.DataFrame({'X': x_list, 'Y': y_list})
    
    # 결측치 제거 전 개수
    original_len = len(temp_df)
    
    # 결측치(숫자가 아닌 값 포함) 제거
    temp_df = temp_df.dropna()
    valid_len = len(temp_df)
    
    if original_len != valid_len:
        st.warning(f"⚠️ 숫자가 아닌 데이터 {original_len - valid_len}개를 제외했습니다.")

    len_x = len(temp_df)
    
    # 데이터 부족 체크
    if len_x < 2:
        st.error("데이터가 너무 적습니다 (2개 이상 필요). 숫자 데이터가 포함된 올바른 열을 선택했는지 확인하세요.")
    else:
        st.write(f"분석 데이터 개수: **{len_x}개**")
        
        # 분석을 위한 최종 DataFrame
        df = temp_df.copy()

        # 중복된 (X, Y) 쌍의 개수 계산 (점 크기/색상에 사용)
        counts = df.groupby(["X", "Y"]).size().reset_index(name="count")
        counts["count"] = counts["count"].astype(int)

        # ===== 상관계수 계산 및 해석 (수정됨) =====
        corr = df["X"].corr(df["Y"])

        if np.isnan(corr):
            corr_text = "상관계수: 계산 불가 (모든 값 동일)"
        else:
            abs_corr = abs(corr)
            
            # 1. 상관관계 정도(Strength) 판별 (일반적 통계 기준)
            if abs_corr < 0.1:
                strength = "거의 의미 없음 (관계 없음)"
            elif abs_corr < 0.3:
                strength = "약한 상관관계"
            elif abs_corr < 0.5:
                strength = "중간 정도의 상관관계"
            elif abs_corr < 0.7:
                strength = "강한 상관관계"
            else:
                strength = "매우 강한 상관관계"

            # 2. 방향(Direction) 판별
            direction = "양(+)" if corr > 0 else "음(-)"
            
            # 3. 최종 텍스트 구성
            corr_text = f"상관계수: **{corr:.4f}** → **{direction} 방향의 {strength}**"

        st.markdown(f"### 📊 {corr_text}")

        # ===== 회귀선 계산 및 차트 생성 =====
        try:
            slope, intercept = np.polyfit(df["X"], df["Y"], 1)
            df["regression"] = slope * df["X"] + intercept
            
            st.write(f"회귀식: **Y = {slope:.4f} X + {intercept:.4f}**")

            # 차트: 산점도
            point_chart = (
                alt.Chart(counts)
                .mark_circle()
                .encode(
                    x=alt.X("X:Q", title=f"{x_col} (X)"),
                    y=alt.Y("Y:Q", title=f"{y_col} (Y)"),
                    color=alt.Color("count:Q", scale=alt.Scale(scheme="redyellowblue"), legend=alt.Legend(title="중복")),
                    size=alt.Size("count:Q", scale=alt.Scale(range=[50, 400]), legend=None), 
                    tooltip=[
                        alt.Tooltip("X", title=x_col), 
                        alt.Tooltip("Y", title=y_col), 
                        alt.Tooltip("count", title="개수")
                    ]
                )
                .properties(title=f"{x_col} vs {y_col} 분석")
            )

            # 차트: 회귀선
            reg_chart = (
                alt.Chart(df)
                .mark_line(color="black", strokeDash=[5, 5])
                .encode(
                    x="X:Q",
                    y="regression:Q",
                    tooltip=[
                        alt.Tooltip("X", title=x_col), 
                        alt.Tooltip("regression", format=".4f", title="예측값")
                    ]
                )
            )

            final_chart = point_chart + reg_chart
            st.altair_chart(final_chart, use_container_width=True)

            # ===== 공유 기능 =====
            st.markdown("---")
            st.subheader("🔗 차트 설정 다운로드")
            
            chart_spec = final_chart.to_dict()
            chart_json_string = json.dumps(chart_spec, indent=2, ensure_ascii=False)

            st.download_button(
                label="📥 Altair JSON 다운로드",
                data=chart_json_string,
                file_name="chart_config.json",
                mime="application/json",
            )

        except np.linalg.LinAlgError:
            st.error("❌ 회귀선을 계산할 수 없습니다.")
        except Exception as e:
            st.error(f"❌ 분석 중 오류 발생: {e}")
