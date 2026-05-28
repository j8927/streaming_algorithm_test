# 스트리밍 알고리즘 구현 및 성능 비교

스트리밍 환경에서 대용량 데이터를 효율적으로 처리하기 위한 두 가지 알고리즘(Bloom Filter, Count-Min Sketch)의 구현과 성능 비교 실험입니다.

## 📋 과제 개요

- **과제명**: 스트리밍 알고리즘 2종 구현 및 정확도·메모리 트레이드오프 분석
- **데이터셋**: Online Retail Dataset (UCI)
- **선택 알고리즘**: Bloom Filter, Count-Min Sketch
- **분석 항목**: 정확도, 메모리 사용량, 처리 시간

## 🗂️ 프로젝트 구조

```
streaming-algorithm-assignment/
├─ README.md                          # 프로젝트 설명
├─ requirements.txt                   # Python 의존성
│
├─ data/
│  └─ Online Retail.csv               # 실험 데이터 (541,909개 레코드)
│
├─ src/
│  ├─ bloom_filter.py                 # Bloom Filter 구현
│  ├─ count_min_sketch.py             # Count-Min Sketch 구현
│  ├─ stream_loader.py                # 스트림 데이터 로더
│  ├─ experiment.py                   # 실험 실행 코드
│  └─ analysis.py                     # 결과 분석 및 시각화
│
├─ results/
│  ├─ bloom_filter_results.json       # Bloom Filter 실험 결과
│  ├─ count_min_sketch_results.json   # Count-Min Sketch 실험 결과
│  ├─ summary_report.json             # 요약 리포트
│  └─ charts/                         # 분석 그래프
│     ├─ 01_bloom_filter_analysis.png
│     ├─ 02_count_min_sketch_analysis.png
│     └─ 03_algorithm_comparison.png
│
└─ report/
   └─ streaming_algorithm_report.pdf  # 최종 보고서
```

## 🚀 사용 방법

### 1. 환경 설정

```bash
# 의존성 설치
pip install -r requirements.txt
```

### 2. 데이터 준비

Online Retail 데이터셋 다운로드:
1. https://archive.ics.uci.edu/dataset/352/online+retail 방문
2. "Online Retail.xlsx" 파일 다운로드
3. `data/` 폴더에 저장

또는 CSV로 변환:
```bash
python3 << 'EOF'
import pandas as pd
df = pd.read_excel('data/Online Retail.xlsx')
df.to_csv('data/Online Retail.csv', index=False)
EOF
```

### 3. 실험 실행

```bash
cd src/
python experiment.py
```

실험 실행 시 다음 작업이 수행됩니다:
- Ground Truth 계산 (정확한 고유 상품, 빈도)
- Bloom Filter 파라미터별 실험 (size: 10K, 50K, 100K / hash_count: 3, 5, 7)
- Count-Min Sketch 파라미터별 실험 (width: 500, 1K, 5K / depth: 3, 5, 7)
- 결과를 JSON, CSV 형식으로 저장

### 4. 결과 분석

```bash
python analysis.py
```

분석 결과:
- 알고리즘별 성능 그래프
- 정확도 vs 메모리 트레이드오프 분석
- 최적 파라미터 제시

## 📊 구현한 알고리즘

### 1. Bloom Filter

**목적**: 스트림에서 원소 포함 여부를 O(k) 시간에 판정

**특징**:
- 메모리 효율적 (비트 배열 사용)
- 거짓 긍정(False Positive) 가능
- 거짓 부정(False Negative) 불가능

**성능 지표**:
- 정확도: False Positive Rate (FPR)
- 메모리: 비트 배열 크기
- 처리시간: 초당 처리 레코드 수

**파라미터**:
- `size`: 비트 배열 크기 (10,000 / 50,000 / 100,000)
- `num_hashes`: 해시 함수 개수 (3 / 5 / 7)

### 2. Count-Min Sketch

**목적**: 항목별 빈도를 효율적으로 추정

**특징**:
- 항목별 빈도를 항상 과대추정
- 공간 복잡도: O(w × d)
- 시간 복잡도: 쿼리 O(d)

**성능 지표**:
- 정확도: 상대 오차 (Relative Error)
- 메모리: 2D 배열 크기
- 처리시간: 초당 처리 레코드 수

**파라미터**:
- `width`: 각 행의 크기 (500 / 1,000 / 5,000)
- `depth`: 행의 개수 (3 / 5 / 7)

## 📈 실험 설계

### Ground Truth 계산

- **Bloom Filter 비교 기준**: Python `set`을 이용한 실제 포함 여부
- **Count-Min Sketch 비교 기준**: Python `dict`를 이용한 정확한 빈도

### 성능 측정 항목

| 항목 | 설명 | 측정 방식 |
|------|------|---------|
| **정확도** | Bloom Filter: FPR / Count-Min: 상대 오차 | 테스트 데이터셋 기준 |
| **메모리** | 실제 메모리 사용량 또는 자료구조 크기 | `tracemalloc` / 수동 계산 |
| **시간** | 전체 처리 시간, 초당 처리량 | `time.time()` 측정 |

### 데이터셋 특성

```
Online Retail Dataset
- 기간: 2010-12-01 ~ 2011-12-09
- 레코드 수: 541,909개
- 고유 상품: ~4,000개
- 형식: CSV
```

## 🔍 주요 발견 사항

### 정확도 vs 메모리 트레이드오프

- **Bloom Filter**: 비트 배열 크기 증가 → FPR 감소, 메모리 증가
- **Count-Min Sketch**: width/depth 증가 → 상대 오차 감소, 메모리 증가

### 파라미터 효과

- 파라미터 증가가 항상 성능 향상으로 이어지지는 않음
- 일정 수준 이상에서는 개선 폭이 감소 (수렴)

### 실용성 평가

- **Count-Min Sketch**가 더 실용적 (상품별 빈도 추정)
- 상품 클릭/구매 로그 분석에 직접 활용 가능

## 💻 시스템 요구사항

- Python 3.7+
- 메모리: 2GB 이상 권장
- 디스크: 100MB 이상 권장

## 📝 출력 파일

### 실험 결과
- `results/bloom_filter_results.json`: Bloom Filter 파라미터별 결과
- `results/count_min_sketch_results.json`: Count-Min Sketch 파라미터별 결과
- `results/summary_report.json`: 최적 설정 요약

### 분석 그래프
- `results/charts/01_bloom_filter_analysis.png`: BF 파라미터 분석
- `results/charts/02_count_min_sketch_analysis.png`: CMS 파라미터 분석
- `results/charts/03_algorithm_comparison.png`: 알고리즘 비교

## 🎓 최종 분석 질문

### Q1: 정확도와 메모리 사이의 트레이드오프

**A**: 명확한 트레이드오프가 존재했습니다.
- Bloom Filter: 비트 배열 크기 ↑ → FPR ↓, 메모리 ↑
- Count-Min Sketch: width/depth ↑ → 오차 ↓, 메모리 ↑

### Q2: 파라미터 증가가 항상 성능 향상을 가져오는가?

**A**: 아니오. 일정 수준 이상에서는 개선 폭이 감소하는 수렴 현상 관찰

### Q3: 가장 실용적인 알고리즘

**A**: **Count-Min Sketch**
- 상품별 빈도 추정으로 인기 상품 분석 가능
- 이상 거래 패턴 탐지 가능
- 실시간 분석에 적합

### Q4: 실제 서비스 로그 분석 시 선택 알고리즘

**A**: **Count-Min Sketch**
- 대규모 상품 클릭/구매 로그 분석에 최적
- 전체 로그 저장 없이 빈도 추정 가능
- 메모리 효율성과 정확도의 좋은 균형

## 📖 참고 자료

### Bloom Filter
- "Space/Time Trade-offs in Hash Coding with Allowable Errors" (Bloom, 1970)
- [Bloom Filter - Wikipedia](https://en.wikipedia.org/wiki/Bloom_filter)

### Count-Min Sketch
- "An Improved Data Stream Summary: The Count-Min Sketch and its Applications" (Cormode & Muthukrishnan, 2005)
- [Count-Min Sketch - Wikipedia](https://en.wikipedia.org/wiki/Count%E2%80%93min_sketch)

### Online Retail Dataset
- [UCI Machine Learning Repository - Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

---

**제출일**: 2024년 6월 14일 이전
**작성자**: [학생 이름]