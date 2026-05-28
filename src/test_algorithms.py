"""
Bloom Filter와 Count-Min Sketch 단위 테스트
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from bloom_filter import BloomFilter
from count_min_sketch import CountMinSketch


def test_bloom_filter():
    """Bloom Filter 테스트"""
    print("=" * 50)
    print("Bloom Filter 테스트")
    print("=" * 50)
    
    bf = BloomFilter(size=10000, num_hashes=3)
    
    # 1. 원소 추가 및 조회
    test_items = ["apple", "banana", "cherry", "date", "elderberry"]
    
    for item in test_items:
        bf.add(item)
    
    print("\n1. 포함 여부 테스트:")
    for item in test_items:
        result = bf.contains(item)
        print(f"  {item}: {result} (예상: True)")
    
    # 2. 없는 원소 테스트
    print("\n2. 없는 원소 테스트:")
    not_added = ["fig", "grape", "honeydew"]
    for item in not_added:
        result = bf.contains(item)
        print(f"  {item}: {result} (예상: False, False Positive 가능)")
    
    # 3. 메모리 사용량
    print(f"\n3. 메모리 사용량: {bf.get_memory_usage()} bytes")
    
    # 4. 거짓 긍정율
    print(f"\n4. 이론적 거짓 긍정율: {bf.get_false_positive_rate(len(test_items)):.6f}")
    
    print("\n✅ Bloom Filter 테스트 완료\n")


def test_count_min_sketch():
    """Count-Min Sketch 테스트"""
    print("=" * 50)
    print("Count-Min Sketch 테스트")
    print("=" * 50)
    
    cms = CountMinSketch(width=100, depth=3)
    
    # 1. 항목 추가
    items = {
        "apple": 5,
        "banana": 3,
        "cherry": 7,
        "date": 2,
        "elderberry": 4
    }
    
    print("\n1. 항목 추가:")
    for item, count in items.items():
        cms.add(item, count)
        print(f"  {item}: +{count}")
    
    # 2. 빈도 조회
    print("\n2. 빈도 조회:")
    for item, true_count in items.items():
        estimated = cms.query(item)
        error = abs(estimated - true_count) / max(true_count, 1)
        print(f"  {item}: 실제={true_count}, 추정={estimated}, 오차율={error:.2%}")
    
    # 3. 메모리 사용량
    print(f"\n3. 메모리 사용량: {cms.get_memory_usage()} bytes")
    
    # 4. 오차 상한
    print(f"\n4. 오차 상한: {cms.get_error_bound():.6f}")
    
    # 5. 없는 항목 조회
    print("\n5. 없는 항목 조회:")
    not_added = ["fig", "grape"]
    for item in not_added:
        estimated = cms.query(item)
        print(f"  {item}: 추정={estimated} (예상: 0, 과대추정 가능)")
    
    print("\n✅ Count-Min Sketch 테스트 완료\n")


def test_memory_comparison():
    """메모리 비교 테스트"""
    print("=" * 50)
    print("메모리 비교 테스트")
    print("=" * 50)
    
    # Bloom Filter 메모리
    bf_sizes = [1000, 10000, 100000]
    print("\nBloom Filter 메모리:")
    for size in bf_sizes:
        bf = BloomFilter(size=size, num_hashes=3)
        memory_kb = bf.get_memory_usage() / 1024
        print(f"  size={size:6d}: {memory_kb:.2f} KB")
    
    # Count-Min Sketch 메모리
    cms_configs = [(100, 3), (1000, 5), (5000, 7)]
    print("\nCount-Min Sketch 메모리:")
    for width, depth in cms_configs:
        cms = CountMinSketch(width=width, depth=depth)
        memory_kb = cms.get_memory_usage() / 1024
        print(f"  width={width:4d}, depth={depth}: {memory_kb:.2f} KB")
    
    print("\n✅ 메모리 비교 테스트 완료\n")


def test_large_scale():
    """대규모 데이터 테스트"""
    print("=" * 50)
    print("대규모 데이터 테스트")
    print("=" * 50)
    
    # Bloom Filter로 100,000개 원소 처리
    print("\nBloom Filter (100,000개 원소):")
    bf = BloomFilter(size=100000, num_hashes=3)
    
    import time
    start = time.time()
    for i in range(100000):
        bf.add(f"item_{i}")
    elapsed = time.time() - start
    
    print(f"  추가 시간: {elapsed:.3f}초")
    print(f"  처리량: {100000/elapsed:.0f} items/sec")
    
    # Count-Min Sketch로 100,000개 항목 처리
    print("\nCount-Min Sketch (100,000개 항목):")
    cms = CountMinSketch(width=1000, depth=5)
    
    start = time.time()
    for i in range(100000):
        cms.add(f"item_{i}")
    elapsed = time.time() - start
    
    print(f"  추가 시간: {elapsed:.3f}초")
    print(f"  처리량: {100000/elapsed:.0f} items/sec")
    
    print("\n✅ 대규모 데이터 테스트 완료\n")


if __name__ == "__main__":
    test_bloom_filter()
    test_count_min_sketch()
    test_memory_comparison()
    test_large_scale()
    
    print("=" * 50)
    print("모든 테스트 완료! ✅")
    print("=" * 50)
