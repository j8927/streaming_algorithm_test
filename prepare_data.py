"""
Online Retail Dataset 다운로드 및 준비 헬퍼 스크립트
"""
import os
import pandas as pd
import urllib.request
import zipfile
from pathlib import Path


def download_and_prepare_data(data_dir: str = "data") -> bool:
    """
    데이터셋 다운로드 및 CSV 변환
    
    Args:
        data_dir: 저장 디렉토리
    
    Returns:
        성공 여부
    """
    
    # 디렉토리 생성
    os.makedirs(data_dir, exist_ok=True)
    
    # 여러 다운로드 방법 시도
    methods = [
        download_from_uci_alternative,
        convert_xlsx_to_csv,
        print_manual_instructions,
    ]
    
    for method in methods:
        if method(data_dir):
            return True
    
    return False


def download_from_uci_alternative(data_dir: str) -> bool:
    """UCI 데이터셋 직접 다운로드 시도"""
    print("[INFO] UCI에서 데이터셋 다운로드 중...")
    
    try:
        # 다운로드 URL (변경될 수 있음)
        url = "https://archive.ics.uci.edu/static/public/352/data.zip"
        zip_path = os.path.join(data_dir, "data.zip")
        csv_path = os.path.join(data_dir, "Online Retail.csv")
        
        # 이미 있으면 스킵
        if os.path.exists(csv_path):
            print(f"[INFO] CSV 파일이 이미 존재합니다: {csv_path}")
            return True
        
        # 다운로드
        print(f"[INFO] 파일 다운로드 중... {url}")
        urllib.request.urlretrieve(url, zip_path)
        print(f"[INFO] 다운로드 완료: {zip_path}")
        
        # 압축 해제
        print("[INFO] 압축 해제 중...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        
        # XLSX 파일 찾기
        xlsx_files = list(Path(data_dir).glob("**/*.xlsx"))
        if xlsx_files:
            xlsx_path = str(xlsx_files[0])
            print(f"[INFO] XLSX 파일 발견: {xlsx_path}")
            
            # CSV로 변환
            print("[INFO] XLSX를 CSV로 변환 중...")
            df = pd.read_excel(xlsx_path)
            df.to_csv(csv_path, index=False)
            print(f"[INFO] CSV 파일 저장됨: {csv_path}")
            
            # 정리
            os.remove(zip_path)
            return True
        
    except Exception as e:
        print(f"[WARNING] 다운로드 실패: {e}")
    
    return False


def convert_xlsx_to_csv(data_dir: str) -> bool:
    """기존 XLSX 파일을 CSV로 변환"""
    print("[INFO] XLSX 파일을 CSV로 변환 시도...")
    
    try:
        # XLSX 파일 찾기
        xlsx_files = list(Path(data_dir).glob("**/*.xlsx"))
        
        for xlsx_path in xlsx_files:
            csv_path = os.path.join(data_dir, "Online Retail.csv")
            
            if not os.path.exists(csv_path):
                print(f"[INFO] XLSX 파일 발견: {xlsx_path}")
                print("[INFO] CSV로 변환 중...")
                
                df = pd.read_excel(xlsx_path)
                df.to_csv(csv_path, index=False)
                
                print(f"[INFO] CSV 파일 저장됨: {csv_path}")
                print(f"[INFO] 레코드 수: {len(df):,}")
                return True
        
    except Exception as e:
        print(f"[WARNING] 변환 실패: {e}")
    
    return False


def print_manual_instructions(data_dir: str) -> bool:
    """수동 다운로드 지침 출력"""
    print("\n" + "=" * 70)
    print("📥 온라인 소매 데이터셋 수동 다운로드 지침")
    print("=" * 70)
    
    print("""
자동 다운로드가 실패했습니다. 다음 단계를 따르세요:

1️⃣  데이터셋 다운로드:
   - 방문: https://archive.ics.uci.edu/dataset/352/online+retail
   - 'Online Retail.xlsx' 파일 다운로드

2️⃣  파일 저장:
   - 다운로드한 파일을 다음 폴더에 저장하세요:
   - {0}/Online Retail.xlsx

3️⃣  CSV로 변환 (선택사항):
   
   다음 Python 코드를 실행하세요:
   
   python3 << 'EOF'
   import pandas as pd
   df = pd.read_excel('{0}/Online Retail.xlsx')
   df.to_csv('{0}/Online Retail.csv', index=False)
   print("✅ CSV 변환 완료!")
   EOF

4️⃣  확인:
   - {0}/Online Retail.csv 파일이 생성되었는지 확인
   - 레코드 수: 약 541,909개

📝 데이터셋 정보:
   - 기간: 2010-12-01 ~ 2011-12-09
   - 고유 상품: ~4,000개
   - 고유 고객: ~4,000명
   - 형식: XLSX 또는 CSV

""".format(data_dir))
    
    return False


def check_data_integrity(data_path: str) -> bool:
    """데이터 무결성 확인"""
    
    if not os.path.exists(data_path):
        print(f"[ERROR] 파일을 찾을 수 없습니다: {data_path}")
        return False
    
    try:
        df = pd.read_csv(data_path)
        
        print("\n✅ 데이터 무결성 확인 완료:")
        print(f"  - 레코드 수: {len(df):,}")
        print(f"  - 컬럼 수: {len(df.columns)}")
        print(f"  - 컬럼명: {', '.join(df.columns)}")
        print(f"  - 메모리 사용: {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")
        
        # 주요 컬럼 확인
        required_columns = ['InvoiceNo', 'StockCode', 'Description', 
                           'Quantity', 'InvoiceDate', 'UnitPrice', 
                           'CustomerID', 'Country']
        
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            print(f"  [WARNING] 누락된 컬럼: {missing}")
            return False
        
        print(f"  - 고유 상품: {df['StockCode'].nunique():,}")
        print(f"  - 고유 고객: {df['CustomerID'].nunique():,}")
        print(f"  - 거래 기간: {df['InvoiceDate'].min()} ~ {df['InvoiceDate'].max()}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 데이터 확인 실패: {e}")
        return False


def main():
    """메인 함수"""
    
    data_dir = "data"
    csv_path = os.path.join(data_dir, "Online Retail.csv")
    
    print("=" * 70)
    print("🔧 Online Retail Dataset 준비")
    print("=" * 70)
    
    # 데이터 다운로드 및 준비
    if download_and_prepare_data(data_dir):
        # 데이터 무결성 확인
        if check_data_integrity(csv_path):
            print("\n" + "=" * 70)
            print("✅ 준비 완료! 다음 명령어로 실험을 시작하세요:")
            print("=" * 70)
            print("\n  cd src/")
            print("  python experiment.py\n")
            return True
    
    # 다운로드 실패
    print("\n" + "=" * 70)
    print("❌ 데이터 준비 실패")
    print("=" * 70)
    print("\n위의 수동 다운로드 지침을 따르세요.\n")
    return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
