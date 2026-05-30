"""
실험 결과 분석 및 시각화
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from pathlib import Path
from typing import Dict, List
import numpy as np


class ResultAnalyzer:
    """실험 결과 분석 클래스"""
    
    def __init__(self, results_dir: str = "../results"):
        script_dir = Path(__file__).resolve().parent
        results_path = Path(results_dir)
        self.results_dir = results_path if results_path.is_absolute() else (script_dir / results_path).resolve()
        self.bf_results = None
        self.cms_results = None
        
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10
    
    def load_results(self) -> None:
        """JSON 파일에서 결과 로드"""
        
        bf_path = os.path.join(self.results_dir, "bloom_filter_results.json")
        cms_path = os.path.join(self.results_dir, "count_min_sketch_results.json")
        
        if os.path.exists(bf_path):
            with open(bf_path, 'r', encoding='utf-8') as f:
                self.bf_results = pd.DataFrame(json.load(f))
        
        if os.path.exists(cms_path):
            with open(cms_path, 'r', encoding='utf-8') as f:
                self.cms_results = pd.DataFrame(json.load(f))
    
    def plot_bloom_filter_analysis(self) -> None:
        """Bloom Filter 분석 그래프"""
        if self.bf_results is None:
            print("Bloom Filter 결과를 찾을 수 없습니다")
            return
        
        df = self.bf_results
        
        # 1. 파라미터별 메모리 vs FPR
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        for hash_count in df['hash_count'].unique():
            subset = df[df['hash_count'] == hash_count]
            axes[0].plot(subset['size'], subset['memory_mb'], 
                        marker='o', label=f'hash_count={int(hash_count)}')
        
        axes[0].set_xlabel('비트 배열 크기 (size)')
        axes[0].set_ylabel('메모리 (MB)')
        axes[0].set_title('Bloom Filter: 크기 vs 메모리')
        axes[0].legend()
        axes[0].grid(True)
        
        # FPR vs 크기
        for hash_count in df['hash_count'].unique():
            subset = df[df['hash_count'] == hash_count]
            axes[1].plot(subset['size'], subset['false_positive_rate'], 
                        marker='s', label=f'hash_count={int(hash_count)}')
        
        axes[1].set_xlabel('비트 배열 크기 (size)')
        axes[1].set_ylabel('거짓 긍정율 (FPR)')
        axes[1].set_title('Bloom Filter: 크기 vs FPR')
        axes[1].legend()
        axes[1].grid(True)
        
        charts_dir = self.results_dir / 'charts'
        charts_dir.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(charts_dir / '01_bloom_filter_analysis.png', dpi=150, bbox_inches='tight')
        print("[INFO] 저장됨: 01_bloom_filter_analysis.png")
        plt.close()
    
    def plot_count_min_sketch_analysis(self) -> None:
        """Count-Min Sketch 분석 그래프"""
        if self.cms_results is None:
            print("Count-Min Sketch 결과를 찾을 수 없습니다")
            return
        
        df = self.cms_results
        
        # 1. 파라미터별 메모리 vs 오차
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        for depth in df['depth'].unique():
            subset = df[df['depth'] == depth]
            axes[0].plot(subset['width'], subset['memory_mb'], 
                        marker='o', label=f'depth={int(depth)}')
        
        axes[0].set_xlabel('너비 (width)')
        axes[0].set_ylabel('메모리 (MB)')
        axes[0].set_title('Count-Min Sketch: 너비 vs 메모리')
        axes[0].legend()
        axes[0].grid(True)
        
        # 오차 vs 너비
        for depth in df['depth'].unique():
            subset = df[df['depth'] == depth]
            axes[1].plot(subset['width'], subset['avg_relative_error'], 
                        marker='s', label=f'depth={int(depth)}')
        
        axes[1].set_xlabel('너비 (width)')
        axes[1].set_ylabel('평균 상대 오차')
        axes[1].set_title('Count-Min Sketch: 너비 vs 평균 상대 오차')
        axes[1].legend()
        axes[1].grid(True)
        
        charts_dir = self.results_dir / 'charts'
        charts_dir.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(charts_dir / '02_count_min_sketch_analysis.png', dpi=150, bbox_inches='tight')
        print("[INFO] 저장됨: 02_count_min_sketch_analysis.png")
        plt.close()
    
    def plot_comparison_analysis(self) -> None:
        """두 알고리즘 비교 분석"""
        if self.bf_results is None or self.cms_results is None:
            print("결과를 찾을 수 없습니다")
            return
        
        # 최적 설정 선택 (파라미터별 중간값)
        bf_best = self.bf_results.iloc[self.bf_results['memory_mb'].idxmin()]
        cms_best = self.cms_results.iloc[self.cms_results['memory_mb'].idxmin()]
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 메모리 비교
        algorithms = ['Bloom Filter', 'Count-Min Sketch']
        memories = [bf_best['memory_mb'], cms_best['memory_mb']]
        axes[0, 0].bar(algorithms, memories, color=['#1f77b4', '#ff7f0e'])
        axes[0, 0].set_ylabel('메모리 (MB)')
        axes[0, 0].set_title('알고리즘 메모리 비교')
        axes[0, 0].grid(axis='y')
        for i, v in enumerate(memories):
            axes[0, 0].text(i, v, f'{v:.2f}', ha='center', va='bottom')
        
        # 처리 시간 비교
        times = [bf_best['processing_time_sec'], cms_best['processing_time_sec']]
        axes[0, 1].bar(algorithms, times, color=['#1f77b4', '#ff7f0e'])
        axes[0, 1].set_ylabel('처리 시간 (초)')
        axes[0, 1].set_title('알고리즘 처리 시간 비교')
        axes[0, 1].grid(axis='y')
        for i, v in enumerate(times):
            axes[0, 1].text(i, v, f'{v:.2f}', ha='center', va='bottom')
        
        # 처리량 비교
        throughputs = [bf_best['throughput_records_per_sec'], 
                       cms_best['throughput_records_per_sec']]
        axes[1, 0].bar(algorithms, throughputs, color=['#1f77b4', '#ff7f0e'])
        axes[1, 0].set_ylabel('처리량 (records/sec)')
        axes[1, 0].set_title('알고리즘 처리량 비교')
        axes[1, 0].grid(axis='y')
        for i, v in enumerate(throughputs):
            axes[1, 0].text(i, v, f'{v:.0f}', ha='center', va='bottom')
        
        # 정확도 비교
        bf_fpr = bf_best['false_positive_rate']
        cms_error = cms_best['avg_relative_error']
        
        ax2 = axes[1, 1]
        ax2_twin = ax2.twinx()
        
        bars1 = ax2.bar([0], [bf_fpr], width=0.4, label='BF FPR', color='#1f77b4', alpha=0.7)
        bars2 = ax2_twin.bar([0.5], [cms_error], width=0.4, label='CMS Relative Error', color='#ff7f0e', alpha=0.7)
        
        ax2.set_ylabel('Bloom Filter FPR', color='#1f77b4')
        ax2_twin.set_ylabel('Count-Min Sketch 상대 오차', color='#ff7f0e')
        ax2.set_title('정확도 비교')
        ax2.set_xticks([0.25])
        ax2.set_xticklabels(['정확도'])
        ax2.grid(axis='y')
        
        ax2.text(0, bf_fpr, f'{bf_fpr:.6f}', ha='center', va='bottom', color='#1f77b4')
        ax2_twin.text(0.5, cms_error, f'{cms_error:.6f}', ha='center', va='bottom', color='#ff7f0e')
        
        charts_dir = self.results_dir / 'charts'
        charts_dir.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(charts_dir / '03_algorithm_comparison.png', dpi=150, bbox_inches='tight')
        print("[INFO] 저장됨: 03_algorithm_comparison.png")
        plt.close()
    
    def generate_summary_report(self) -> Dict:
        """요약 리포트 생성"""
        if self.bf_results is None or self.cms_results is None:
            return {}
        
        bf_best = self.bf_results.iloc[self.bf_results['memory_mb'].idxmin()]
        cms_best = self.cms_results.iloc[self.cms_results['memory_mb'].idxmin()]
        
        report = {
            'bloom_filter': {
                'best_config': {
                    'size': int(bf_best['size']),
                    'hash_count': int(bf_best['hash_count'])
                },
                'memory_mb': float(bf_best['memory_mb']),
                'processing_time_sec': float(bf_best['processing_time_sec']),
                'throughput_records_per_sec': float(bf_best['throughput_records_per_sec']),
                'false_positive_rate': float(bf_best['false_positive_rate']),
            },
            'count_min_sketch': {
                'best_config': {
                    'width': int(cms_best['width']),
                    'depth': int(cms_best['depth'])
                },
                'memory_mb': float(cms_best['memory_mb']),
                'processing_time_sec': float(cms_best['processing_time_sec']),
                'throughput_records_per_sec': float(cms_best['throughput_records_per_sec']),
                'avg_relative_error': float(cms_best['avg_relative_error']),
            }
        }
        
        # JSON으로 저장
        summary_path = os.path.join(self.results_dir, "summary_report.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"[INFO] 요약 리포트 저장됨: {summary_path}")
        return report


def main():
    """분석 실행"""
    
    analyzer = ResultAnalyzer("../results")
    analyzer.load_results()
    
    print("[INFO] Bloom Filter 분석 중...")
    analyzer.plot_bloom_filter_analysis()
    
    print("[INFO] Count-Min Sketch 분석 중...")
    analyzer.plot_count_min_sketch_analysis()
    
    print("[INFO] 알고리즘 비교 분석 중...")
    analyzer.plot_comparison_analysis()
    
    print("[INFO] 요약 리포트 생성 중...")
    summary = analyzer.generate_summary_report()
    
    print("\n=== 실험 결과 요약 ===")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
