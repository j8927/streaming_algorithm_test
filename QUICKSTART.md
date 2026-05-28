# 🚀 빠른 시작 가이드

스트리밍 알고리즘 실험을 빠르게 시작하는 방법입니다.

## ⚡ 5분 안에 시작하기

### 1단계: 데이터 준비 (2분)

```bash
# 작업 디렉토리로 이동
cd /workspaces/streaming_algorithm_test

# 의존성 설치
pip install -r requirements.txt

# 데이터 다운로드 및 준비
python prepare_data.py
```

**수동 다운로드** (자동 실패 시):
1. https://archive.ics.uci.edu/dataset/352/online+retail 방문
2. "Online Retail.xlsx" 다운로드
3. `data/` 폴더에 저장

### 2단계: 실험 실행 (3분+)

```bash
# Python 워크플로우 실행 (모든 단계 자동 실행)
python run_workflow.py

# 또는 각 단계별 수동 실행
cd src/
python test_algorithms.py      # 알고리즘 테스트
python experiment.py           # 메인 실험
python analysis.py             # 결과 분석
```

**또는 Bash 스크립트 사용**:
```bash
chmod +x run_experiment.sh
./run_experiment.sh
```

## 📊 결과 확인

실험 완료 후 생성되는 파일들:

```
results/
├── bloom_filter_results.json        ← Bloom Filter 결과
├── count_min_sketch_results.json    ← Count-Min Sketch 결과
├── summary_report.json              ← 요약 리포트
└── charts/
    ├── 01_bloom_filter_analysis.png
    ├── 02_count_min_sketch_analysis.png
    └── 03_algorithm_comparison.png
```

## 🔍 결과 분석

### 요약 리포트 확인

```bash
# JSON 포맷 보기
cat results/summary_report.json

# 또는 Python으로 확인
python3 << 'EOF'
import json
with open('results/summary_report.json', 'r') as f:
    data = json.load(f)
    print(json.dumps(data, indent=2, ensure_ascii=False))
EOF
```

### 상세 결과 비교

```bash
# CSV 파일로 비교 (Excel에서도 열 수 있음)
cat results/bloom_filter_results.csv
cat results/count_min_sketch_results.csv
```

## 📝 보고서 작성

### 1단계: 템플릿 확인

```bash
cat report/REPORT_TEMPLATE.md
```

### 2단계: 최종 분석 질문 답변

템플릿의 다음 섹션을 작성하세요:

```markdown
## 11.3 최종 답변: 최종 분석 질문

#### Q1: 정확도와 메모리 사이의 트레이드오프는?
[실험 결과에 기반해 답변]

#### Q2: 파라미터 증가가 항상 성능 향상을 가져오는가?
[실험 그래프 분석]

#### Q3: 가장 실용적인 알고리즘은?
[장단점 분석]

#### Q4: 실제 서비스 로그 분석에는?
[비즈니스 가치 분석]
```

### 3단계: PDF 변환

Markdown → PDF 변환 방법:

```bash
# 방법 1: Pandoc 사용
pandoc report/REPORT_TEMPLATE.md -o report/streaming_algorithm_report.pdf

# 방법 2: 온라인 도구
# - https://pandoc.org/try/
# - REPORT_TEMPLATE.md 업로드 → PDF 다운로드

# 방법 3: Google Docs/Word
# - Markdown 내용 복사
# - Google Docs/Word에 붙여넣기
# - PDF로 내보내기
```

## ⚙️ 파라미터 변경

### Bloom Filter 파라미터 수정

`src/experiment.py`의 `experiment_bloom_filter` 호출:

```python
# 기본값
experiment.experiment_bloom_filter(
    sizes=[10000, 50000, 100000],
    hash_counts=[3, 5, 7]
)

# 커스텀 설정
experiment.experiment_bloom_filter(
    sizes=[5000, 10000, 20000],      # 더 작은 크기
    hash_counts=[2, 3, 4]             # 더 적은 해시
)
```

### Count-Min Sketch 파라미터 수정

```python
# 기본값
experiment.experiment_count_min_sketch(
    widths=[500, 1000, 5000],
    depths=[3, 5, 7]
)

# 커스텀 설정
experiment.experiment_count_min_sketch(
    widths=[100, 500, 1000],          # 더 작은 너비
    depths=[1, 2, 3]                   # 더 적은 깊이
)
```

## 🐛 문제 해결

### Q: 데이터 파일을 찾을 수 없습니다

**A**: 다음 단계를 따르세요:

```bash
# 1. 데이터 폴더 생성
mkdir -p data

# 2. 수동으로 파일 다운로드
# https://archive.ics.uci.edu/dataset/352/online+retail
# Online Retail.xlsx 다운로드

# 3. data/ 폴더에 저장 후 CSV 변환
python3 << 'EOF'
import pandas as pd
df = pd.read_excel('data/Online Retail.xlsx')
df.to_csv('data/Online Retail.csv', index=False)
print("✅ 변환 완료!")
EOF
```

### Q: 메모리 부족 오류

**A**: 더 작은 데이터로 테스트하세요:

```python
# src/stream_loader.py 수정
def sample_stream(self, limit: int = 10000):  # 100 → 10000
    # ...
```

또는 파라미터를 줄이세요:

```python
# src/experiment.py 수정
experiment.experiment_bloom_filter(
    sizes=[10000],      # 1개만 테스트
    hash_counts=[3]
)
```

### Q: 실험 시간이 너무 오래 걸립니다

**A**: 다음 방법 중 하나를 선택하세요:

```bash
# 방법 1: 배경에서 실행
python run_workflow.py &

# 방법 2: 더 빠른 설정으로 테스트
# 파라미터 개수를 줄임
```

### Q: Python 버전 오류

**A**: Python 3.7+ 필요:

```bash
python3 --version
python3 run_workflow.py
```

## 📋 체크리스트

실험 완료 체크리스트:

- [ ] 의존성 설치 완료 (`pip install -r requirements.txt`)
- [ ] 데이터 파일 준비 (`data/Online Retail.csv`)
- [ ] 알고리즘 테스트 통과 (`test_algorithms.py`)
- [ ] 메인 실험 완료 (`experiment.py`)
- [ ] 결과 파일 생성 (`results/`)
- [ ] 분석 그래프 생성 (`results/charts/`)
- [ ] 보고서 템플릿 작성 (`report/REPORT_TEMPLATE.md`)
- [ ] 최종 분석 질문 답변 작성
- [ ] PDF 보고서 생성
- [ ] GitHub 업로드

## 🎯 다음 단계

1. **결과 분석**
   - results/summary_report.json 확인
   - 각 알고리즘의 성능 비교

2. **보고서 작성**
   - report/REPORT_TEMPLATE.md 참고
   - 자신의 실험 결과로 채우기

3. **GitHub 업로드**
   ```bash
   git add .
   git commit -m "스트리밍 알고리즘 실험 완료"
   git push origin main
   ```

4. **제출**
   - PDF 보고서 제출
   - GitHub 저장소 링크 포함

## 📞 도움말

- 알고리즘 이론: `src/bloom_filter.py`, `src/count_min_sketch.py` 주석 참고
- 실험 방법: `report/REPORT_TEMPLATE.md` 의 "구현 방식" 섹션
- 파라미터 튜닝: `report/REPORT_TEMPLATE.md` 의 "파라미터 설정" 섹션

---

**Happy Experimenting! 🚀**
