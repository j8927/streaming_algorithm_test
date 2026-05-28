#!/usr/bin/env python3
"""
스트리밍 알고리즘 실험 메인 워크플로우
Bloom Filter와 Count-Min Sketch 성능 비교 실험
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(title: str, level: int = 1) -> None:
    """헤더 출력"""
    if level == 1:
        print("\n" + "=" * 70)
        print(title.center(70))
        print("=" * 70)
    else:
        print(f"\n{'=' * 50}")
        print(f"▶ {title}")
        print(f"{'=' * 50}")


def check_dependencies() -> bool:
    """의존성 확인"""
    print_header("의존성 확인", level=2)
    
    try:
        import pandas
        import numpy
        import matplotlib
        import seaborn
        print("✅ 모든 의존성이 설치되어 있습니다")
        return True
    except ImportError as e:
        print(f"❌ 누락된 패키지: {e}")
        print("\n다음 명령어를 실행하세요:")
        print("  pip install -r requirements.txt")
        return False


def prepare_data() -> bool:
    """데이터 준비"""
    print_header("데이터 준비", level=2)
    
    try:
        result = subprocess.run(
            [sys.executable, "prepare_data.py"],
            capture_output=False,
            timeout=300
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ 타임아웃: 데이터 준비가 너무 오래 걸렸습니다")
        return False
    except Exception as e:
        print(f"❌ 데이터 준비 실패: {e}")
        return False


def run_tests() -> bool:
    """알고리즘 단위 테스트 실행"""
    print_header("알고리즘 단위 테스트", level=2)
    
    try:
        src_dir = Path(__file__).parent / "src"
        result = subprocess.run(
            [sys.executable, "test_algorithms.py"],
            cwd=src_dir,
            capture_output=False,
            timeout=60
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ 타임아웃: 테스트가 너무 오래 걸렸습니다")
        return False
    except Exception as e:
        print(f"❌ 테스트 실행 실패: {e}")
        return False


def run_experiments() -> bool:
    """메인 실험 실행"""
    print_header("메인 실험 실행", level=2)
    print("(이 과정은 3-5분 정도 소요될 수 있습니다)\n")
    
    try:
        src_dir = Path(__file__).parent / "src"
        result = subprocess.run(
            [sys.executable, "experiment.py"],
            cwd=src_dir,
            capture_output=False,
            timeout=600  # 10분 타임아웃
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ 타임아웃: 실험이 너무 오래 걸렸습니다")
        return False
    except Exception as e:
        print(f"❌ 실험 실행 실패: {e}")
        return False


def run_analysis() -> bool:
    """결과 분석 및 시각화"""
    print_header("결과 분석 및 시각화", level=2)
    
    try:
        src_dir = Path(__file__).parent / "src"
        result = subprocess.run(
            [sys.executable, "analysis.py"],
            cwd=src_dir,
            capture_output=False,
            timeout=120
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⚠️  타임아웃: 분석이 너무 오래 걸렸습니다")
        return False
    except Exception as e:
        print(f"⚠️  분석 실패: {e}")
        # 분석 실패는 경고만 하고 계속 진행
        return True


def show_results() -> None:
    """결과 요약 출력"""
    print_header("실험 결과 요약", level=2)
    
    results_dir = Path(__file__).parent / "results"
    
    # 결과 파일 목록
    print("\n📁 생성된 파일:")
    result_files = [
        ("Bloom Filter 결과", results_dir / "bloom_filter_results.json"),
        ("Count-Min Sketch 결과", results_dir / "count_min_sketch_results.json"),
        ("요약 리포트", results_dir / "summary_report.json"),
    ]
    
    for name, path in result_files:
        status = "✅" if path.exists() else "❌"
        print(f"  {status} {name}: {path.name}")
    
    # 그래프
    charts_dir = results_dir / "charts"
    if charts_dir.exists():
        chart_files = list(charts_dir.glob("*.png"))
        print(f"\n📊 분석 그래프 ({len(chart_files)}개):")
        for chart in sorted(chart_files):
            print(f"  ✅ {chart.name}")


def show_next_steps() -> None:
    """다음 단계 안내"""
    print_header("다음 단계", level=2)
    
    print("""
✅ 실험이 완료되었습니다!

📋 다음으로 할 일:

1. 결과 확인
   - results/summary_report.json 파일 확인
   - results/charts/ 폴더의 그래프 확인

2. 보고서 작성
   - report/ 폴더에 보고서 PDF 작성
   - 다음 항목 포함:
     * 데이터셋 설명
     * 선택한 알고리즘 개요
     * 구현 방식 및 실험 환경
     * 정확도/메모리/처리시간 비교 결과
     * 알고리즘별 장단점 분석
     * 최종 분석 질문에 대한 답변

3. GitHub 업로드 (선택)
   - git add .
   - git commit -m "스트리밍 알고리즘 실험 완료"
   - git push origin main

💡 팁:
   - 결과 파일은 JSON 형식이므로 Python으로 쉽게 분석 가능
   - matplotlib 그래프를 보고서에 포함시킬 수 있음
   - 다시 실험하려면: python run_workflow.py
""")


def main() -> int:
    """메인 워크플로우"""
    
    print_header("스트리밍 알고리즘 비교 실험 워크플로우")
    
    # 1. 의존성 확인
    if not check_dependencies():
        return 1
    
    # 2. 데이터 준비
    if not prepare_data():
        return 1
    
    # 3. 알고리즘 테스트
    if not run_tests():
        print("\n⚠️  테스트 실패했지만 계속 진행합니다...")
    
    # 4. 메인 실험
    if not run_experiments():
        return 1
    
    # 5. 결과 분석
    run_analysis()
    
    # 6. 결과 표시
    show_results()
    show_next_steps()
    
    print_header("✅ 워크플로우 완료!", level=1)
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
