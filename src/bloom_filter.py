"""
Bloom Filter Implementation
스트림에서 원소 포함 여부를 효율적으로 판정하는 확률적 자료구조
"""
import hashlib
from typing import Any
import sys


class BloomFilter:
    """
    Bloom Filter: 원소 포함 여부를 O(k) 시간에 판정하는 확률적 자료구조
    - 거짓 긍정(False Positive) 가능
    - 거짓 부정(False Negative) 불가능
    """
    
    def __init__(self, size: int, num_hashes: int):
        """
        Args:
            size: 비트 배열 크기
            num_hashes: 해시 함수 개수
        """
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bytearray((size + 7) // 8)  # 비트를 바이트로 변환
        self.num_elements = 0
        
    def _hash(self, item: Any, seed: int) -> int:
        """해시 함수"""
        h = hashlib.sha256(f"{item}_{seed}".encode()).digest()
        return int.from_bytes(h[:4], 'big') % self.size
    
    def add(self, item: Any) -> None:
        """원소 추가"""
        for i in range(self.num_hashes):
            hash_value = self._hash(item, i)
            # 비트 설정
            byte_index = hash_value // 8
            bit_index = hash_value % 8
            self.bit_array[byte_index] |= (1 << bit_index)
        self.num_elements += 1
    
    def contains(self, item: Any) -> bool:
        """원소 포함 여부 판정 (False Positive 가능)"""
        for i in range(self.num_hashes):
            hash_value = self._hash(item, i)
            # 비트 확인
            byte_index = hash_value // 8
            bit_index = hash_value % 8
            if not (self.bit_array[byte_index] & (1 << bit_index)):
                return False
        return True
    
    def get_memory_usage(self) -> int:
        """메모리 사용량 (바이트)"""
        return len(self.bit_array)
    
    def get_false_positive_rate(self, actual_count: int) -> float:
        """이론적 거짓 긍정 확률 (정확한 계산)"""
        if actual_count == 0:
            return 0.0
        # FPR ≈ (1 - e^(-k*n/m))^k
        import math
        m = self.size
        k = self.num_hashes
        n = actual_count
        try:
            return (1 - math.exp(-k * n / m)) ** k
        except:
            return 1.0
