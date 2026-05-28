# 📄 DOCX 보고서 생성 가이드

Word 형식의 전문적인 보고서를 자동으로 생성합니다.

## 🚀 빠른 시작

### 1단계: 라이브러리 설치

```bash
pip install python-docx Pillow
```

또는:

```bash
pip install -r requirements.txt
```

### 2단계: 템플릿 보고서 생성

```bash
cd src/
python generate_docx_report.py --template
```

**생성 파일**: `report/streaming_algorithm_report_template.docx`

이 파일은:
- ✅ 전체 구조와 섹션이 설정됨
- ✅ 표와 서식이 적용됨
- ✅ 입력 필요 부분이 표시됨
- ⚠️ 실험 데이터는 포함되지 않음

### 3단계: 실험 후 결과 포함 보고서 생성

```bash
cd src/
python experiment.py          # 먼저 실험 실행
python analysis.py            # 결과 분석
python generate_docx_report.py --with-results
```

**생성 파일**: `report/streaming_algorithm_report.docx`

이 파일은:
- ✅ 전체 구조가 설정됨
- ✅ 실험 결과 데이터가 포함됨
- ✅ 그래프 이미지가 삽입됨
- ✅ 요약 리포트가 포함됨

## 📋 보고서 구성

### 자동 생성 부분

- ✅ 표지 (제목, 부제목)
- ✅ 목차
- ✅ 1. 데이터셋 설명
- ✅ 2. 알고리즘 개요
- ✅ 3. 구현 방식
- ✅ 4. 실험 환경
- ✅ 5. 파라미터 설정
- ✅ 6. Ground Truth 계산
- ✅ 7-9. 성능 비교 결과
- ✅ 10. 장단점 분석
- ✅ 11. 결론 (질문 양식 포함)
- ✅ 참고자료

### 수동 입력 필요 부분

다음 섹션은 자신의 실험 결과로 수정하세요:

1. **학생 정보**
   - 학생 이름
   - 학번
   - 제출일

2. **성능 비교 결과**
   - 정확도 수치
   - 메모리 사용량
   - 처리 시간

3. **최종 분석 질문 4가지**
   - Q1: 정확도 vs 메모리 트레이드오프
   - Q2: 파라미터 효과
   - Q3: 가장 실용적인 알고리즘
   - Q4: 서비스 적용 알고리즘

## 💻 고급 사용

### 자신만의 스타일 커스터마이징

`generate_docx_report.py`의 `setup_document_style()` 함수 수정:

```python
def setup_document_style(self) -> None:
    style = self.doc.styles['Normal']
    style.font.name = 'Times New Roman'      # 글꼴 변경
    style.font.size = Pt(12)                 # 크기 변경
    
    # 색상 커스터마이징
    title_run.font.color.rgb = RGBColor(200, 16, 46)  # 빨간색
```

### 색상 코드

```
RGBColor(31, 78, 121)      # 진한 파란색 (제목)
RGBColor(79, 129, 189)     # 중간 파란색 (소제목)
RGBColor(89, 89, 89)       # 회색 (본문)
RGBColor(255, 0, 0)        # 빨간색
RGBColor(0, 128, 0)        # 초록색
```

### 이미지 삽입 커스터마이징

```python
# 그래프 경로 변경
gen.add_image("custom_chart.png", width=6.5)

# 너비 조정
gen.add_image("results/charts/01_bloom_filter_analysis.png", width=5.0)
```

## 📊 결과 파일 경로

생성된 DOCX 파일은 다음 위치에 저장됩니다:

```
streaming_algorithm_test/
└── report/
    ├── streaming_algorithm_report_template.docx    (템플릿)
    └── streaming_algorithm_report.docx             (결과 포함)
```

## 🔄 워크플로우

### 방법 1: 템플릿 생성 후 수동 작성

```bash
# 1. 템플릿 생성
python generate_docx_report.py --template

# 2. Word에서 열어서 수정
# report/streaming_algorithm_report_template.docx 수정
# - 학생 정보 입력
# - 실험 결과 복사-붙여넣기
# - 최종 분석 질문 답변 입력
```

### 방법 2: 자동 생성 후 수정

```bash
# 1. 실험 실행
python experiment.py
python analysis.py

# 2. 결과 포함 보고서 생성
python generate_docx_report.py --with-results

# 3. Word에서 열어서 최종 분석 질문 답변만 입력
# 대부분의 데이터는 자동 포함됨
```

## ✏️ Word에서 편집 팁

### 표 추가

1. **삽입** → **표** → 크기 선택
2. 데이터 입력
3. **표 디자인** 탭에서 스타일 선택

### 이미지 삽입

1. **삽입** → **그림** → 파일 선택
2. 크기 조정: 모서리 드래그
3. 자동 번호 매기기: **참고** → **캡션**

### 수식 삽입

1. **삽입** → **수식**
2. 복잡한 수식은 LaTeX 형식으로 입력 가능

```
FPR = (1 - e^(-k*n/m))^k
상대오차 = |추정값 - 실제값| / 실제값
```

## 📝 최종 체크리스트

DOCX 보고서 완성 체크리스트:

- [ ] 제목 및 부제목 확인
- [ ] 학생 정보 입력 (이름, 학번, 날짜)
- [ ] 모든 표가 정렬되어 있음
- [ ] 모든 그래프가 삽입되어 있음
- [ ] 최종 분석 질문 4가지에 답변
- [ ] 참고자료 업데이트
- [ ] 맞춤법 검사 완료
- [ ] PDF로 내보내기 (선택사항)

## 🎓 제출 전 최종 단계

### 1단계: PDF 변환 (선택사항)

Word에서:
1. **파일** → **다른 이름으로 저장**
2. 파일 형식: **PDF**
3. **저장**

### 2단계: GitHub에 업로드

```bash
git add report/streaming_algorithm_report.docx
git commit -m "최종 보고서 제출"
git push origin main
```

### 3단계: 제출

- 보고서 파일 제출
- GitHub 저장소 링크 포함

## 🆘 문제 해결

### Q: "ModuleNotFoundError: No module named 'docx'"

**A**: python-docx 설치

```bash
pip install python-docx
```

### Q: 이미지가 안 보입니다

**A**: 이미지 경로 확인

```bash
# 그래프 생성 확인
ls results/charts/

# 경로 수정 (src/ 폴더에서 실행 시)
python generate_docx_report.py --with-results
```

### Q: 표의 글꼴이 깨집니다

**A**: 한글 글꼴 설정

```python
# generate_docx_report.py 수정
style.font.name = 'Noto Sans CJK KR'  # 또는 'Gulim'
```

### Q: DOCX 파일이 너무 큽니다

**A**: 이미지 품질 낮추기

```python
# PNG 대신 JPEG 사용
# 또는 이미지 크기 줄이기
gen.add_image("chart.png", width=4.5)  # 너비 감소
```

## 📖 추가 학습

### Python-docx 공식 문서

- 설치: https://python-docx.readthedocs.io/en/latest/
- API 참조: https://python-docx.readthedocs.io/en/latest/api/

### Word 보고서 작성 팁

- 일관된 스타일 사용
- 명확한 구조와 계층
- 시각적 요소 활용 (표, 그래프)
- 간결한 문장

---

**Happy Report Writing! 📝✨**
