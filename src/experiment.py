"""
스트리밍 알고리즘 실험 및 성능 측정
Bloom Filter와 Count-Min Sketch의 정확도, 메모리, 처리시간 비교
"""
import time
import sys
import os
import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple
import tracemalloc

from bloom_filter import BloomFilter
from count_min_sketch import CountMinSketch
from stream_loader import OnlineRetailStreamLoader, load_ground_truth_data


class StreamingAlgorithmExperiment:
    """스트리밍 알고리즘 실험 클래스"""
    
    def __init__(self, data_path: str, output_dir: str = "../results"):
        script_dir = Path(__file__).resolve().parent
        output_path = Path(output_dir)
        self.output_dir = output_path if output_path.is_absolute() else (script_dir / output_path).resolve()
        self.data_path = data_path
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ground Truth 계산
        print("[INFO] Ground Truth 계산 중...")
        self.ground_truth_set, self.ground_truth_counts = load_ground_truth_data(data_path)
        print(f"[INFO] 고유 상품: {len(self.ground_truth_set)}, 총 거래 건수: {sum(self.ground_truth_counts.values())}")
    
    def experiment_bloom_filter(self, 
                               sizes: List[int] = None, 
                               hash_counts: List[int] = None) -> Dict:
        """
        Bloom Filter 실험
        
        Args:
            sizes: 비트 배열 크기 리스트
            hash_counts: 해시 함수 개수 리스트
        
        Returns:
            실험 결과 사전
        """
        if sizes is None:
            sizes = [10000, 50000, 100000]
        if hash_counts is None:
            hash_counts = [3, 5, 7]
        
        results = []
        
        for size in sizes:
            for hash_count in hash_counts:
                print(f"\n[Bloom Filter] size={size}, hash_count={hash_count}")
                
                bf = BloomFilter(size, hash_count)
                loader = OnlineRetailStreamLoader(self.data_path)
                
                # 메모리 추적 시작
                tracemalloc.start()
                start_time = time.time()
                
                # 스트림 처리
                seen_products = set()
                record_count = 0
                for record in loader.stream_records():
                    stock_code = str(record.get('StockCode', ''))
                    if stock_code:
                        bf.add(stock_code)
                        seen_products.add(stock_code)
                        record_count += 1
                
                # 메모리 측정
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                elapsed_time = time.time() - start_time
                throughput = record_count / elapsed_time if elapsed_time > 0 else 0
                
                # 정확도 측정 (False Positive Rate)
                false_positives = 0
                false_positives_count = 0
                
                # 실제로 없는 상품들 테스트
                for actual_product in self.ground_truth_set:
                    if bf.contains(actual_product):
                        # 실제 있는 상품
                        pass
                    else:
                        false_positives += 1
                
                # False Positive Rate 계산
                not_in_bloom = 0
                for i in range(1000):
                    fake_product = f"FAKE_{i}"
                    if bf.contains(fake_product):
                        false_positives_count += 1
                    not_in_bloom += 1
                
                fpr_estimated = false_positives_count / max(not_in_bloom, 1)
                
                result = {
                    'algorithm': 'Bloom Filter',
                    'size': size,
                    'hash_count': hash_count,
                    'memory_mb': peak / (1024 * 1024),
                    'memory_bytes': bf.get_memory_usage(),
                    'processing_time_sec': elapsed_time,
                    'throughput_records_per_sec': throughput,
                    'record_count': record_count,
                    'false_positive_rate': fpr_estimated,
                    'theoretical_fpr': bf.get_false_positive_rate(len(seen_products)),
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                results.append(result)
                print(f"  메모리: {result['memory_mb']:.2f} MB")
                print(f"  시간: {result['processing_time_sec']:.2f}초")
                print(f"  처리량: {result['throughput_records_per_sec']:.0f} records/sec")
                print(f"  FPR: {result['false_positive_rate']:.6f}")
        
        return results
    
    def experiment_count_min_sketch(self,
                                   widths: List[int] = None,
                                   depths: List[int] = None) -> Dict:
        """
        Count-Min Sketch 실험
        
        Args:
            widths: 너비(열) 리스트
            depths: 깊이(행) 리스트
        
        Returns:
            실험 결과 사전
        """
        if widths is None:
            widths = [500, 1000, 5000]
        if depths is None:
            depths = [3, 5, 7]
        
        results = []
        
        for width in widths:
            for depth in depths:
                print(f"\n[Count-Min Sketch] width={width}, depth={depth}")
                
                cms = CountMinSketch(width, depth)
                loader = OnlineRetailStreamLoader(self.data_path)
                
                # 메모리 추적 시작
                tracemalloc.start()
                start_time = time.time()
                
                # 스트림 처리
                record_count = 0
                for record in loader.stream_records():
                    stock_code = str(record.get('StockCode', ''))
                    if stock_code:
                        cms.add(stock_code)
                        record_count += 1
                
                # 메모리 측정
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                elapsed_time = time.time() - start_time
                throughput = record_count / elapsed_time if elapsed_time > 0 else 0
                
                # 정확도 측정 (상대 오차)
                relative_errors = []
                for product, true_count in self.ground_truth_counts.items():
                    estimated_count = cms.query(product)
                    if true_count > 0:
                        relative_error = abs(estimated_count - true_count) / true_count
                        relative_errors.append(relative_error)
                
                avg_relative_error = sum(relative_errors) / len(relative_errors) if relative_errors else 0
                max_relative_error = max(relative_errors) if relative_errors else 0
                
                result = {
                    'algorithm': 'Count-Min Sketch',
                    'width': width,
                    'depth': depth,
                    'memory_mb': peak / (1024 * 1024),
                    'memory_bytes': cms.get_memory_usage(),
                    'processing_time_sec': elapsed_time,
                    'throughput_records_per_sec': throughput,
                    'record_count': record_count,
                    'avg_relative_error': avg_relative_error,
                    'max_relative_error': max_relative_error,
                    'error_bound': cms.get_error_bound(),
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                results.append(result)
                print(f"  메모리: {result['memory_mb']:.2f} MB")
                print(f"  시간: {result['processing_time_sec']:.2f}초")
                print(f"  처리량: {result['throughput_records_per_sec']:.0f} records/sec")
                print(f"  평균 상대 오차: {result['avg_relative_error']:.6f}")
        
        return results
    
    def save_results(self, results: List[Dict], filename: str) -> None:
        """결과를 CSV 파일로 저장"""
        if not results:
            return
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\n[INFO] 결과 저장됨: {output_path}")
    
    def save_json_results(self, results: List[Dict], filename: str) -> None:
        """결과를 JSON 파일로 저장"""
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"[INFO] JSON 결과 저장됨: {output_path}")


def main():
    """메인 실험 함수"""
    
    data_path = "data/Online Retail.csv"
    
    # 데이터 확인
    if not os.path.exists(data_path):
        print(f"[ERROR] 데이터 파일을 찾을 수 없습니다: {data_path}")
        print("\n데이터 다운로드 방법:")
        print("1. https://archive.ics.uci.edu/dataset/352/online+retail 방문")
        print("2. 'Online Retail.xlsx' 다운로드")
        print("3. data/ 폴더에 저장 후 CSV로 변환")
        print("\n또는 다음 코드로 변환:")
        print("  import pandas as pd")
        print("  df = pd.read_excel('data/Online Retail.xlsx')")
        print("  df.to_csv('data/Online Retail.csv', index=False)")
        sys.exit(1)
    
    # 실험 시작
    experiment = StreamingAlgorithmExperiment(data_path)
    
    print("\n" + "="*60)
    print("Bloom Filter 실험 시작")
    print("="*60)
    bf_results = experiment.experiment_bloom_filter()
    experiment.save_results(bf_results, "bloom_filter_results.csv")
    experiment.save_json_results(bf_results, "bloom_filter_results.json")
    
    print("\n" + "="*60)
    print("Count-Min Sketch 실험 시작")
    print("="*60)
    cms_results = experiment.experiment_count_min_sketch()
    experiment.save_results(cms_results, "count_min_sketch_results.csv")
    experiment.save_json_results(cms_results, "count_min_sketch_results.json")
    
    print("\n" + "="*60)
    print("실험 완료")
    print("="*60)


if __name__ == "__main__":
    main()
