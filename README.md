# 영동고속도로 교통 데이터 분석 - Streamlit Portfolio

## 프로젝트 소개
2024년 10월 영동고속도로 서창JC-신갈JC 구간의 평균속도 및 교통량 데이터를 분석한 Python 데이터 분석 프로젝트입니다.

## 실행 방법
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 배포
1. 이 폴더 전체를 GitHub repository에 업로드합니다.
2. Streamlit Community Cloud에서 해당 repository를 연결합니다.
3. Main file path로 `app.py`를 선택한 뒤 Deploy 합니다.

## 현재 버전
현재 첨부된 Jupyter Notebook에 저장된 그래프를 이미지로 추출해 포트폴리오 페이지로 구성했습니다.
원본 Excel 데이터까지 repository에 추가하면 Streamlit의 selectbox, slider, Plotly 등을 이용해 인터랙티브 분석 페이지로 확장할 수 있습니다.


## 포트폴리오 소스 구성
- `app.py`: Streamlit 포트폴리오 화면
- `assets/`: 분석 결과 그래프
- `Term_module.py`: 직접 작성한 데이터 통합/전처리/분석 모듈
- `Term_Project_2020104218.ipynb`: 분석 결과가 저장된 노트북

현재 앱은 저장된 결과 그래프를 표시하므로 원본 Excel 파일이 없어도 배포됩니다.
