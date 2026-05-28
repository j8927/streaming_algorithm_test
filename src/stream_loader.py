"""
Online Retail Dataset Loader
UCI Online Retail 데이터셋을 스트림 형식으로 로드
"""
import os
import csv
import pandas as pd
from typing import Iterator, Dict, Tuple
import urllib.request
import zipfile
import io


class OnlineRetailStreamLoader:
    """
    Online Retail Dataset 스트림 로더
    데이터: 2010-12-01 ~ 2011-12-09 영국 온라인 소매 거래 (541,909개 레코드)
    """
    
    DATA_URL = "https://archive.ics.uci.edu/static/public/352/data.zip"
    
    def __init__(self, data_path: str = "data/Online Retail.csv"):
        """
        Args:
            data_path: 데이터 파일 경로
        """
        self.data_path = data_path
        self.total_records = 0
        self.columns = ["InvoiceNo", "StockCode", "Description", "Quantity", 
                       "InvoiceDate", "UnitPrice", "CustomerID", "Country"]
    
    def download_data(self) -> None:
        """UCI에서 데이터셋 다운로드"""
        if os.path.exists(self.data_path):
            print(f"[INFO] 데이터 파일이 이미 존재합니다: {self.data_path}")
            return
        
        os.makedirs(os.path.dirname(self.data_path) or ".", exist_ok=True)
        
        try:
            print("[INFO] Online Retail Dataset 다운로드 중...")
            # 원본 URL (UCI Archive)
            url = "https://archive.ics.uci.edu/static/public/352/data.zip"
            
            # 대체 방법: pandas로 직접 읽기 (xlsx 파일)
            print("[INFO] 또는 다음 URL에서 수동으로 다운로드하세요:")
            print("https://archive.ics.uci.edu/dataset/352/online+retail")
            print(f"[INFO] 파일을 {self.data_path}에 저장하세요")
            
        except Exception as e:
            print(f"[ERROR] 다운로드 실패: {e}")
            print("[INFO] 수동으로 다운로드 후 data/ 폴더에 저장하세요")
    
    def convert_xlsx_to_csv(self, xlsx_path: str) -> None:
        """XLSX 파일을 CSV로 변환"""
        if not os.path.exists(xlsx_path):
            print(f"[ERROR] 파일을 찾을 수 없습니다: {xlsx_path}")
            return
        
        print(f"[INFO] XLSX 파일을 CSV로 변환 중... {xlsx_path}")
        df = pd.read_excel(xlsx_path)
        df.to_csv(self.data_path, index=False)
        print(f"[INFO] CSV 파일 저장됨: {self.data_path}")
    
    def stream_records(self) -> Iterator[Dict]:
        """
        데이터를 한 줄씩 스트림 형식으로 로드
        메모리에 전체 데이터를 올리지 않음
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"데이터 파일을 찾을 수 없습니다: {self.data_path}")
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.total_records += 1
                yield row
    
    def get_statistics(self) -> Dict:
        """데이터셋 통계"""
        if not os.path.exists(self.data_path):
            return {}
        
        df = pd.read_csv(self.data_path, dtype={
            'InvoiceNo': str,
            'StockCode': str,
            'Quantity': int,
            'UnitPrice': float,
            'CustomerID': str
        })
        
        return {
            'total_records': len(df),
            'unique_products': df['StockCode'].nunique(),
            'unique_customers': df['CustomerID'].nunique(),
            'unique_invoices': df['InvoiceNo'].nunique(),
            'date_range': (df['InvoiceDate'].min(), df['InvoiceDate'].max()),
            'quantity_range': (df['Quantity'].min(), df['Quantity'].max()),
            'total_revenue': (df['Quantity'] * df['UnitPrice']).sum(),
        }
    
    def sample_stream(self, limit: int = 100) -> Iterator[Dict]:
        """샘플 스트림 데이터 반환 (테스트용)"""
        count = 0
        for record in self.stream_records():
            if count >= limit:
                break
            yield record
            count += 1


def load_ground_truth_data(data_path: str) -> Tuple[set, dict]:
    """
    전체 데이터로부터 Ground Truth 계산
    
    Returns:
        Tuple[set, dict]: (나타난 StockCode 집합, StockCode 빈도 사전)
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"데이터 파일을 찾을 수 없습니다: {data_path}")
    
    product_set = set()
    product_counts = {}
    
    df = pd.read_csv(data_path, dtype={
        'StockCode': str,
        'Quantity': float
    })
    
    for _, row in df.iterrows():
        stock_code = str(row['StockCode'])
        quantity = int(row['Quantity']) if pd.notna(row['Quantity']) else 0
        
        product_set.add(stock_code)
        product_counts[stock_code] = product_counts.get(stock_code, 0) + 1
    
    return product_set, product_counts
