"""
Count-Min Sketch Implementation
항목별 빈도를 효율적으로 추정하는 확률적 자료구조
"""
import hashlib
from typing import Any, Dict
import math


class CountMinSketch:
    """
    Count-Min Sketch: 항목별 빈도를 O(d) 시간, O(w*d) 공간에 추정하는 자료구조
    - 빈도를 항상 과대추정(overestimate)
    - 빈도를 과소추정하지 않음
    """
    
    def __init__(self, width: int, depth: int):
        """
        Args:
            width: 각 행의 배열 크기
            depth: 행의 개수 (해시 함수 개수)
        """
        self.width = width
        self.depth = depth
        # 2D 배열 초기화
        self.sketch = [[0] * width for _ in range(depth)]
        self.total_items = 0
        
    def _hash(self, item: Any, row: int) -> int:
        """해시 함수"""
        h = hashlib.sha256(f"{item}_{row}".encode()).digest()
        return int.from_bytes(h[:4], 'big') % self.width
    
    def add(self, item: Any, count: int = 1) -> None:
        """항목 추가 (count만큼 증가)"""
        for row in range(self.depth):
            col = self._hash(item, row)
            self.sketch[row][col] += count
        self.total_items += count
    
    def query(self, item: Any) -> int:
        """항목의 추정 빈도 조회 (최솟값 사용)"""
        min_count = float('inf')
        for row in range(self.depth):
            col = self._hash(item, row)
            min_count = min(min_count, self.sketch[row][col])
        return int(min_count) if min_count != float('inf') else 0
    
    def get_memory_usage(self) -> int:
        """메모리 사용량 (바이트, 정수 기준)"""
        # 각 정수를 4바이트로 가정
        return self.width * self.depth * 4
    
    def get_error_bound(self) -> float:
        """이론적 오차 상한"""
        # 오차 ≤ (2 * N / w) * e^(-depth)
        # 여기서 N은 총 항목 수
        N = self.total_items
        w = self.width
        d = self.depth
        if w == 0:
            return float('inf')
        error = (2 * N / w) * math.exp(-d)
        return error
    
    def merge(self, other: 'CountMinSketch') -> None:
        """두 sketch 병합 (union)"""
        if self.width != other.width or self.depth != other.depth:
            raise ValueError("Sketch dimensions must match")
        for row in range(self.depth):
            for col in range(self.width):
                self.sketch[row][col] += other.sketch[row][col]
        self.total_items += other.total_items
