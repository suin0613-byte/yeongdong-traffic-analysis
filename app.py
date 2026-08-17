from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="영동고속도로 교통 데이터 분석",
    page_icon="🚗",
    layout="wide",
)

ASSETS = Path(__file__).parent / "assets"

st.title("🚗 영동고속도로 교통 데이터 분석")
st.caption("서창JC ↔ 신갈JC 구간 · 2024년 10월 데이터 기반 Python 데이터 분석 프로젝트")

st.markdown(
    """
인천에서 학교까지 차량으로 통학하며 영동고속도로의 반복적인 정체를 체감한 경험에서 출발한 프로젝트입니다.
실제 교통 데이터를 이용해 **어디서, 언제 가장 정체가 심한지**를 확인하고,
요일·휴일·교통량이 정체와 어떤 관계를 갖는지 검증했습니다.
"""
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("하행 최다 정체 구간", "2개 구간 공동", "각 15일")
m2.metric("상행 최다 정체 구간", "동수원IC→북수원IC", "21일")
m3.metric("하행 최저 속도 시간대", "10시")
m4.metric("상행 최저 속도 시간대", "17시")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["프로젝트 개요", "핵심 분석", "가설 검증", "교통량 분석", "결론·기술"]
)

with tab1:
    st.subheader("1. 문제 정의")
    st.markdown(
        """
- 영동선 하행에서 가장 자주 막히는 구간은 어디인가?
- 영동선 상행에서 가장 자주 막히는 구간은 어디인가?
- 하행·상행에서 가장 정체가 심한 시간대는 언제인가?
- 월요일 출근시간, 금요일 퇴근시간, 평일/주말/공휴일에 차이가 있는가?
- 교통량이 많을수록 평균속도가 낮아지는가?
"""
    )

    st.subheader("2. 데이터")
    st.markdown(
        """
- 경기도 교통정보센터에서 영동고속도로 구간별 통계정보 수집
- 2024년 10월 1일~31일 상·하행 데이터 활용
- 교통량 데이터와 평균속도 데이터를 추가로 결합
- 원본 파일 호환 문제로 데이터를 직접 정리한 뒤 Python 분석용 Excel 형태로 가공
"""
    )

    st.subheader("3. 분석 과정")
    st.markdown(
        """
`os.listdir()`로 날짜별 파일을 통합하고, `pandas`로 필요한 구간·시간대를 필터링했습니다.
`mean()`, `idxmin()`, `value_counts()`, `isin()` 등을 사용해 평균속도와 빈도수를 계산했으며,
반복되는 전처리 로직은 클래스로 구성해 별도 모듈로 정리했습니다.

**사용 기술:** Python · Pandas · NumPy · Matplotlib · Excel 데이터 전처리
"""
    )

with tab2:
    st.subheader("가장 자주 막히는 구간")
    c1, c2 = st.columns(2)
    with c1:
        st.image(str(ASSETS / "downstream_sections.png"), use_container_width=True)
        st.markdown(
            """
**하행(서창JC → 신갈JC)**  
동군포IC→부곡IC와 군포IC→동군포IC가 각각 15일로 가장 자주 정체되었습니다.
두 구간 모두 차로 수가 4차로에서 3차로로 감소한다는 공통점이 있습니다.
"""
        )
    with c2:
        st.image(str(ASSETS / "upstream_sections.png"), use_container_width=True)
        st.markdown(
            """
**상행(신갈JC → 서창JC)**  
동수원IC→북수원IC가 21일로 가장 자주 정체된 구간으로 나타났습니다.
"""
        )

    st.subheader("가장 정체가 심한 시간대")
    c3, c4 = st.columns(2)
    with c3:
        st.image(str(ASSETS / "downstream_time.png"), use_container_width=True)
        st.markdown("**하행:** 평균속도가 가장 낮은 시간대는 **10시**였습니다.")
    with c4:
        st.image(str(ASSETS / "upstream_time.png"), use_container_width=True)
        st.markdown("**상행:** 평균속도가 가장 낮은 시간대는 **17시**였습니다.")

with tab3:
    st.subheader("가설 1 · 하행 출근시간은 월요일이 가장 막힐 것이다")
    st.image(str(ASSETS / "monday_commute.png"), use_container_width=True)
    st.success("분석 결과, 10월 출근시간대 평균속도가 월요일에 가장 낮아 가설과 일치했습니다.")

    st.subheader("가설 2 · 상행 퇴근시간은 금요일이 가장 막힐 것이다")
    st.image(str(ASSETS / "friday_commute.png"), use_container_width=True)
    st.success("분석 결과, 10월 퇴근시간대 평균속도가 금요일에 가장 낮아 가설과 일치했습니다.")

    st.subheader("가설 3 · 공휴일과 주말은 평일보다 덜 막힐 것이다")
    st.image(str(ASSETS / "weekday_weekend_holiday.png"), use_container_width=True)
    st.success("평일의 평균속도가 가장 낮게 나타나 가설과 일치했습니다.")

with tab4:
    st.subheader("가설 4 · 교통량이 많을수록 평균속도는 낮아질 것이다")

    st.markdown("#### 구간별 비교")
    st.image(str(ASSETS / "traffic_vs_speed_section.png"), use_container_width=True)
    st.markdown(
        """
대부분의 구간에서 교통량 증가와 평균속도 감소가 함께 나타났습니다.
다만 일부 구간은 같은 패턴을 보이지 않아, 사고·진출입 교통·도로 구조 등
추가 변수를 함께 고려할 필요가 있음을 확인했습니다.
"""
    )

    st.markdown("#### 시간대별 비교")
    st.image(str(ASSETS / "traffic_vs_speed_time.png"), use_container_width=True)
    st.markdown(
        """
시간대별 그래프에서도 전반적으로 교통량과 평균속도가 반대 방향으로 움직이는 경향을 확인했습니다.
이 분석은 단순 상관관계 관찰이며, 교통량만으로 정체의 인과관계를 단정하지 않았습니다.
"""
    )

with tab5:
    st.subheader("프로젝트에서 확인한 점")
    st.markdown(
        """
1. **정체는 특정 구간에 집중되었습니다.** 하행은 차로 감소 구간, 상행은 동수원IC→북수원IC에서 빈도가 높았습니다.
2. **방향별 피크 시간이 달랐습니다.** 하행은 10시, 상행은 17시에 평균속도가 가장 낮았습니다.
3. **요일 특성이 확인되었습니다.** 월요일 출근시간과 금요일 퇴근시간의 평균속도가 가장 낮았습니다.
4. **교통량과 속도 사이에는 전반적인 반비례 경향이 있었습니다.** 다만 예외 구간이 있어 다른 변수의 영향도 고려해야 합니다.
"""
    )

    st.subheader("배운 점")
    st.markdown(
        """
- 실제 생활에서 느낀 문제를 데이터 기반 질문과 가설로 구체화했습니다.
- 여러 Excel 파일을 날짜·방향별로 통합하고 분석 목적에 맞게 재구성했습니다.
- 반복되는 전처리 로직을 클래스와 모듈 형태로 정리해 코드 재사용성을 높였습니다.
- 그래프만 제시하는 데 그치지 않고, 예외 사례와 분석 한계까지 함께 해석했습니다.
"""
    )

    st.info(
        "이 포트폴리오 버전은 원본 Jupyter Notebook에 저장된 결과 그래프를 이용해 구성했습니다. "
        "원본 Excel 데이터까지 함께 배포하면 필터·선택 기능이 있는 인터랙티브 버전으로 확장할 수 있습니다."
    )
