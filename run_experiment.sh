#!/bin/bash
# 전체 실험 워크플로우 실행 스크립트

set -e  # 에러 발생 시 중단

echo "=================================="
echo "스트리밍 알고리즘 실험 워크플로우"
echo "=================================="

# 1. 환경 설정
echo ""
echo "📦 [1/4] 의존성 설치 중..."
pip install -r requirements.txt > /dev/null 2>&1 || {
    echo "⚠️  pip install 실패 - 수동으로 설치하세요"
    echo "pip install -r requirements.txt"
    exit 1
}
echo "✅ 의존성 설치 완료"

# 2. 데이터 준비
echo ""
echo "📥 [2/4] 데이터 준비 중..."
python prepare_data.py || {
    echo "❌ 데이터 준비 실패"
    exit 1
}

# 3. 알고리즘 테스트
echo ""
echo "🧪 [3/4] 알고리즘 단위 테스트 중..."
cd src/
python test_algorithms.py || {
    echo "❌ 테스트 실패"
    exit 1
}

# 4. 메인 실험 실행
echo ""
echo "🔬 [4/4] 메인 실험 실행 중..."
echo "(이 과정은 2-5분 정도 소요됩니다)"
python experiment.py || {
    echo "❌ 실험 실행 실패"
    exit 1
}

# 5. 결과 분석
echo ""
echo "📊 결과 분석 및 시각화 중..."
python analysis.py || {
    echo "⚠️  분석 중 오류 발생"
}

cd ..

# 완료
echo ""
echo "=================================="
echo "✅ 실험 완료!"
echo "=================================="
echo ""
echo "📁 생성된 파일:"
echo "  - results/bloom_filter_results.json"
echo "  - results/count_min_sketch_results.json"
echo "  - results/summary_report.json"
echo "  - results/charts/*.png"
echo ""
echo "다음 단계:"
echo "  - 결과 파일 확인: cat results/summary_report.json"
echo "  - 그래프 확인: results/charts/ 폴더"
echo "  - 보고서 작성: report/ 폴더"
