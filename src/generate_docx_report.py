"""
DOCX 형식의 실험 보고서 자동 생성
Markdown 템플릿을 Word 문서로 변환하고 실험 결과를 포함
"""
import os
import json
from pathlib import Path
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class ReportGenerator:
    """DOCX 보고서 생성 클래스"""
    
    def __init__(self, output_dir: str = "../report"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.doc = Document()
        self.setup_document_style()
    
    def setup_document_style(self) -> None:
        """문서 기본 스타일 설정"""
        # 기본 글꼴 설정
        style = self.doc.styles['Normal']
        style.font.name = 'Calibri'
        style.font.size = Pt(11)
        
        # 문단 설정
        paragraph_format = style.paragraph_format
        paragraph_format.line_spacing = 1.15
        paragraph_format.space_before = Pt(6)
        paragraph_format.space_after = Pt(6)
    
    def add_title(self, title: str) -> None:
        """제목 추가"""
        title_para = self.doc.add_paragraph()
        title_run = title_para.add_run(title)
        title_run.font.size = Pt(24)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(31, 78, 121)  # 진한 파란색
        
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_para.paragraph_format.space_after = Pt(6)
        title_para.paragraph_format.space_before = Pt(6)
        
        # 구분선
        self.add_horizontal_line()
    
    def add_subtitle(self, subtitle: str) -> None:
        """부제목 추가"""
        subtitle_para = self.doc.add_paragraph()
        subtitle_run = subtitle_para.add_run(subtitle)
        subtitle_run.font.size = Pt(12)
        subtitle_run.font.italic = True
        subtitle_run.font.color.rgb = RGBColor(89, 89, 89)
        
        subtitle_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        subtitle_para.paragraph_format.space_after = Pt(24)
    
    def add_heading(self, heading: str, level: int = 1) -> None:
        """제목 추가 (레벨별)"""
        heading_para = self.doc.add_heading(heading, level=level)
        
        # 색상 설정
        for run in heading_para.runs:
            if level == 1:
                run.font.color.rgb = RGBColor(31, 78, 121)
                run.font.size = Pt(18)
            elif level == 2:
                run.font.color.rgb = RGBColor(79, 129, 189)
                run.font.size = Pt(14)
            else:
                run.font.color.rgb = RGBColor(89, 89, 89)
                run.font.size = Pt(12)
        
        heading_para.paragraph_format.space_before = Pt(12)
        heading_para.paragraph_format.space_after = Pt(6)
    
    def add_paragraph(self, text: str, bold: bool = False, italic: bool = False) -> None:
        """문단 추가"""
        para = self.doc.add_paragraph(text)
        if bold or italic:
            for run in para.runs:
                if bold:
                    run.font.bold = True
                if italic:
                    run.font.italic = True
    
    def add_horizontal_line(self) -> None:
        """수평선 추가"""
        para = self.doc.add_paragraph()
        pPr = para._element.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '12')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), '4F81BD')
        pBdr.append(bottom)
        pPr.append(pBdr)
    
    def add_table(self, rows: list, headers: list = None) -> None:
        """표 추가"""
        if headers:
            all_rows = [headers] + rows
        else:
            all_rows = rows
        
        table = self.doc.add_table(rows=len(all_rows), cols=len(all_rows[0]))
        table.style = 'Light Grid Accent 1'
        
        for i, row_data in enumerate(all_rows):
            row = table.rows[i]
            for j, cell_data in enumerate(row_data):
                cell = row.cells[j]
                cell.text = str(cell_data)
                
                # 헤더 스타일
                if i == 0 and headers:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.bold = True
                            run.font.color.rgb = RGBColor(255, 255, 255)
                    # 헤더 배경색
                    shading_elm = OxmlElement('w:shd')
                    shading_elm.set(qn('w:fill'), '4F81BD')
                    cell._element.get_or_add_pPr().append(shading_elm)
    
    def add_image(self, image_path: str, width: float = 6.0) -> None:
        """이미지 추가"""
        if os.path.exists(image_path):
            para = self.doc.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.add_run().add_picture(image_path, width=Inches(width))
            para.paragraph_format.space_before = Pt(6)
            para.paragraph_format.space_after = Pt(6)
    
    def add_info_box(self, title: str, content: str) -> None:
        """정보 상자 추가"""
        para = self.doc.add_paragraph()
        
        # 배경색 설정
        shading_elm = OxmlElement('w:shd')
        shading_elm.set(qn('w:fill'), 'E7E6E6')
        para._element.get_or_add_pPr().append(shading_elm)
        
        # 제목
        title_run = para.add_run(f"▶ {title}\n")
        title_run.font.bold = True
        title_run.font.size = Pt(11)
        
        # 내용
        content_run = para.add_run(content)
        content_run.font.size = Pt(10)
        
        para.paragraph_format.left_indent = Inches(0.3)
        para.paragraph_format.space_before = Pt(6)
        para.paragraph_format.space_after = Pt(6)
    
    def add_page_break(self) -> None:
        """페이지 나누기"""
        self.doc.add_page_break()
    
    def save(self, filename: str) -> None:
        """문서 저장"""
        output_path = os.path.join(self.output_dir, filename)
        self.doc.save(output_path)
        print(f"✅ 보고서 저장됨: {output_path}")


def load_experimental_results(results_dir: str = "../results") -> dict:
    """실험 결과 로드"""
    results = {
        'bf_results': None,
        'cms_results': None,
        'summary': None
    }
    
    # 결과 파일 로드
    bf_path = os.path.join(results_dir, "bloom_filter_results.json")
    cms_path = os.path.join(results_dir, "count_min_sketch_results.json")
    summary_path = os.path.join(results_dir, "summary_report.json")
    
    try:
        if os.path.exists(bf_path):
            with open(bf_path, 'r') as f:
                results['bf_results'] = json.load(f)
        
        if os.path.exists(cms_path):
            with open(cms_path, 'r') as f:
                results['cms_results'] = json.load(f)
        
        if os.path.exists(summary_path):
            with open(summary_path, 'r') as f:
                results['summary'] = json.load(f)
    except Exception as e:
        print(f"⚠️  결과 로드 실패: {e}")
    
    return results


def generate_template_report(output_dir: str = "../report") -> None:
    """DOCX 보고서 템플릿 생성 (실험 결과 없이)"""
    
    gen = ReportGenerator(output_dir)
    
    # ========== 표지 ==========
    gen.add_title("스트리밍 알고리즘 비교 실험")
    gen.add_subtitle("Bloom Filter와 Count-Min Sketch의 정확도·메모리 트레이드오프 분석")
    
    # 문서 정보
    info_table = [
        ["과제명", "스트리밍 알고리즘 2종 구현 및 정확도·메모리 트레이드오프 분석"],
        ["학생 이름", "[이름 입력]"],
        ["학번", "[학번 입력]"],
        ["제출일", datetime.now().strftime("%Y년 %m월 %d일")],
    ]
    gen.add_table(info_table)
    
    gen.add_page_break()
    
    # ========== 목차 ==========
    gen.add_heading("목차", level=1)
    toc_items = [
        "1. 데이터셋 설명",
        "2. 선택한 알고리즘 개요",
        "3. 구현 방식",
        "4. 실험 환경",
        "5. 파라미터 설정",
        "6. Ground Truth 계산",
        "7. 정확도 비교 결과",
        "8. 메모리 사용량 비교 결과",
        "9. 처리 시간 비교 결과",
        "10. 알고리즘별 장단점 분석",
        "11. 결론 및 최종 분석 질문",
    ]
    for item in toc_items:
        gen.add_paragraph(item)
    
    gen.add_page_break()
    
    # ========== 1. 데이터셋 설명 ==========
    gen.add_heading("1. 데이터셋 설명", level=1)
    
    gen.add_heading("1.1 선택한 데이터셋", level=2)
    gen.add_paragraph("• 이름: Online Retail Dataset (UCI Machine Learning Repository)")
    gen.add_paragraph("• 형식: CSV")
    gen.add_paragraph("• 크기: 약 541,909개 레코드")
    gen.add_paragraph("• 다운로드: https://archive.ics.uci.edu/dataset/352/online+retail")
    
    gen.add_heading("1.2 데이터셋 특성", level=2)
    dataset_table = [
        ["특성", "값"],
        ["시간 범위", "2010-12-01 ~ 2011-12-09"],
        ["고유 상품 수", "약 4,000개"],
        ["고유 고객 수", "약 4,000명"],
        ["형식", "구매 이벤트 스트림"],
    ]
    gen.add_table(dataset_table)
    
    gen.add_heading("1.3 컬럼 설명", level=2)
    columns_table = [
        ["컬럼명", "설명"],
        ["InvoiceNo", "거래 번호"],
        ["StockCode", "상품 코드 (실험의 핵심 대상)"],
        ["Description", "상품 설명"],
        ["Quantity", "구매 수량"],
        ["InvoiceDate", "거래 날짜 및 시간"],
        ["UnitPrice", "단가"],
        ["CustomerID", "고객 ID"],
        ["Country", "거래 국가"],
    ]
    gen.add_table(columns_table)
    
    gen.add_page_break()
    
    # ========== 2. 알고리즘 개요 ==========
    gen.add_heading("2. 선택한 알고리즘 개요", level=1)
    
    gen.add_heading("2.1 Bloom Filter", level=2)
    gen.add_paragraph("목적: 스트림에서 특정 상품 코드가 이전에 나타났는지 빠르게 판정", bold=True)
    
    gen.add_info_box(
        "알고리즘 특징",
        "• 시간 복잡도: 추가 O(k), 조회 O(k)\n"
        "• 공간 복잡도: O(m) (m = 비트 배열 크기)\n"
        "• False Positive 가능 (존재하지 않는 원소를 존재한다고 판정)\n"
        "• False Negative 불가능 (실제 있는 원소는 반드시 참)"
    )
    
    gen.add_heading("2.2 Count-Min Sketch", level=2)
    gen.add_paragraph("목적: 스트림에서 각 상품의 구매 빈도를 효율적으로 추정", bold=True)
    
    gen.add_info_box(
        "알고리즘 특징",
        "• 시간 복잡도: 추가 O(d), 조회 O(d)\n"
        "• 공간 복잡도: O(w × d)\n"
        "• 빈도를 항상 과대추정 (overestimate)\n"
        "• 정확도와 메모리의 트레이드오프 조정 가능"
    )
    
    gen.add_page_break()
    
    # ========== 3. 구현 방식 ==========
    gen.add_heading("3. 구현 방식", level=1)
    
    gen.add_heading("3.1 Bloom Filter 구현", level=2)
    gen.add_info_box(
        "핵심 로직",
        "1. SHA256 기반 다중 해시 함수 사용\n"
        "2. 비트 연산으로 메모리 최적화\n"
        "3. 추가: 모든 해시 값에 대응하는 비트 설정\n"
        "4. 조회: 모든 해시 값의 비트가 설정되어 있는지 확인"
    )
    
    gen.add_heading("3.2 Count-Min Sketch 구현", level=2)
    gen.add_info_box(
        "핵심 로직",
        "1. d개의 해시 함수와 w×d 2D 배열 사용\n"
        "2. 추가: 각 행의 해시 값에 카운트 누적\n"
        "3. 조회: 각 행의 카운트 중 최솟값 반환"
    )
    
    gen.add_page_break()
    
    # ========== 4. 실험 환경 ==========
    gen.add_heading("4. 실험 환경", level=1)
    
    gen.add_heading("4.1 시스템 환경", level=2)
    system_table = [
        ["항목", "값"],
        ["OS", "Ubuntu 24.04 LTS"],
        ["Python", "3.10+"],
        ["메모리", "2GB 이상"],
    ]
    gen.add_table(system_table)
    
    gen.add_heading("4.2 실험 설정", level=2)
    gen.add_info_box(
        "실험 조건",
        "• 전체 데이터 처리: 541,909개 레코드 모두 스트림으로 처리\n"
        "• 메모리 측정: tracemalloc 라이브러리 사용\n"
        "• 시간 측정: time.time() 함수 사용\n"
        "• 반복 실행: 각 파라미터 조합당 1회 실행"
    )
    
    gen.add_page_break()
    
    # ========== 5. 파라미터 설정 ==========
    gen.add_heading("5. 파라미터 설정", level=1)
    
    gen.add_heading("5.1 Bloom Filter", level=2)
    bf_param_table = [
        ["구성", "size", "num_hashes", "메모리"],
        ["소형", "10,000", "3", "~1.2 KB"],
        ["중형", "50,000", "5", "~6.3 KB"],
        ["대형", "100,000", "7", "~12.5 KB"],
    ]
    gen.add_table(bf_param_table)
    
    gen.add_heading("5.2 Count-Min Sketch", level=2)
    cms_param_table = [
        ["구성", "width", "depth", "메모리"],
        ["소형", "500", "3", "~6 KB"],
        ["중형", "1,000", "5", "~20 KB"],
        ["대형", "5,000", "7", "~140 KB"],
    ]
    gen.add_table(cms_param_table)
    
    gen.add_page_break()
    
    # ========== 6. Ground Truth ==========
    gen.add_heading("6. Ground Truth 계산", level=1)
    
    gen.add_heading("6.1 Bloom Filter Ground Truth", level=2)
    gen.add_paragraph("기준: Python set 자료구조를 사용하여 모든 거래에 나타난 상품 기록")
    gen.add_paragraph("총 고유 상품: 약 4,000개")
    
    gen.add_heading("6.2 Count-Min Sketch Ground Truth", level=2)
    gen.add_paragraph("기준: Python dict 자료구조를 사용하여 각 상품의 정확한 거래 횟수 기록")
    gen.add_paragraph("총 거래 수: 541,909개")
    
    gen.add_page_break()
    
    # ========== 7. 정확도 비교 ==========
    gen.add_heading("7. 정확도 비교 결과", level=1)
    
    gen.add_heading("7.1 Bloom Filter 정확도", level=2)
    gen.add_paragraph("정확도 지표: False Positive Rate (FPR)")
    gen.add_info_box(
        "실험 결과 입력 필요",
        "[표 또는 그래프로 size 및 hash_count별 FPR 결과를 입력하세요]\n"
        "예시:\n"
        "• size=10,000: FPR ≈ 0.12 (12%)\n"
        "• size=50,000: FPR ≈ 0.02 (2%)\n"
        "• size=100,000: FPR ≈ 0.006 (0.6%)"
    )
    
    gen.add_heading("7.2 Count-Min Sketch 정확도", level=2)
    gen.add_paragraph("정확도 지표: 상대 오차 (Relative Error)")
    gen.add_info_box(
        "실험 결과 입력 필요",
        "[표 또는 그래프로 width 및 depth별 상대 오차 결과를 입력하세요]\n"
        "예시:\n"
        "• width=500: 평균 오차 ≈ 0.52 (52%)\n"
        "• width=1,000: 평균 오차 ≈ 0.23 (23%)\n"
        "• width=5,000: 평균 오차 ≈ 0.039 (3.9%)"
    )
    
    gen.add_page_break()
    
    # ========== 8. 메모리 사용량 ==========
    gen.add_heading("8. 메모리 사용량 비교 결과", level=1)
    
    gen.add_heading("8.1 Bloom Filter 메모리", level=2)
    gen.add_info_box(
        "실험 결과",
        "[파라미터별 메모리 사용량을 입력하세요]\n"
        "• size=10,000: 1.25 KB\n"
        "• size=50,000: 6.25 KB\n"
        "• size=100,000: 12.50 KB"
    )
    
    gen.add_heading("8.2 Count-Min Sketch 메모리", level=2)
    gen.add_info_box(
        "실험 결과",
        "[파라미터별 메모리 사용량을 입력하세요]\n"
        "• width=500, depth=3: 6 KB\n"
        "• width=1,000, depth=5: 20 KB\n"
        "• width=5,000, depth=7: 140 KB"
    )
    
    gen.add_page_break()
    
    # ========== 9. 처리 시간 ==========
    gen.add_heading("9. 처리 시간 비교 결과", level=1)
    
    gen.add_heading("9.1 전체 처리 시간", level=2)
    gen.add_info_box(
        "실험 결과",
        "[전체 데이터 처리 시간 및 처리량을 입력하세요]\n"
        "예시:\n"
        "• Bloom Filter: 3.45초, 157,000 records/sec\n"
        "• Count-Min Sketch: 4.12초, 131,000 records/sec"
    )
    
    gen.add_heading("9.2 파라미터별 영향", level=2)
    gen.add_paragraph("• Bloom Filter: hash_count 증가 → 처리시간 약간 증가")
    gen.add_paragraph("• Count-Min Sketch: depth 증가 → 처리시간 선형 증가")
    
    gen.add_page_break()
    
    # ========== 10. 장단점 분석 ==========
    gen.add_heading("10. 알고리즘별 장단점 분석", level=1)
    
    gen.add_heading("10.1 Bloom Filter", level=2)
    gen.add_heading("장점", level=3)
    gen.add_paragraph("✅ 매우 적은 메모리 사용 (KB 단위)")
    gen.add_paragraph("✅ 빠른 조회 시간 (O(k))")
    gen.add_paragraph("✅ 구현이 간단")
    gen.add_paragraph("✅ 원소 포함 여부 판정에 최적")
    
    gen.add_heading("단점", level=3)
    gen.add_paragraph("❌ False Positive 불가피")
    gen.add_paragraph("❌ 삭제 불가능 (표준 Bloom Filter)")
    gen.add_paragraph("❌ 확률적 자료구조 (정확도 보장 불가)")
    
    gen.add_heading("10.2 Count-Min Sketch", level=2)
    gen.add_heading("장점", level=3)
    gen.add_paragraph("✅ 항목별 빈도 추정 가능")
    gen.add_paragraph("✅ 정확도 조정 가능 (파라미터)")
    gen.add_paragraph("✅ Sketch 병합 가능")
    gen.add_paragraph("✅ 확장 가능한 구조")
    
    gen.add_heading("단점", level=3)
    gen.add_paragraph("❌ Bloom Filter보다 더 많은 메모리")
    gen.add_paragraph("❌ 과대추정 불가피")
    gen.add_paragraph("❌ 구현이 복잡")
    
    gen.add_page_break()
    
    # ========== 11. 결론 ==========
    gen.add_heading("11. 결론 및 최종 분석 질문", level=1)
    
    gen.add_heading("11.1 주요 발견", level=2)
    gen.add_paragraph("1. 정확도 vs 메모리 트레이드오프 존재", bold=True)
    gen.add_paragraph("   파라미터 증가 → 정확도 향상, 메모리 증가")
    gen.add_paragraph("   명확한 선형/지수 관계 확인")
    
    gen.add_paragraph("2. 파라미터 효과 한계", bold=True)
    gen.add_paragraph("   일정 수준 이상에서 개선 폭 감소")
    gen.add_paragraph("   비용-효과 분석 필요")
    
    gen.add_paragraph("3. 알고리즘 특성 차이", bold=True)
    gen.add_paragraph("   Bloom Filter: 메모리 효율 최우선")
    gen.add_paragraph("   Count-Min Sketch: 정보량 최우선")
    
    gen.add_page_break()
    
    gen.add_heading("11.2 최종 분석 질문", level=2)
    
    gen.add_heading("Q1: 정확도와 메모리 사이의 트레이드오프는?", level=3)
    gen.add_info_box(
        "답변 입력",
        "[실험 결과에 기반하여 구체적인 답변을 입력하세요]\n"
        "\n"
        "예시:\n"
        "명확한 트레이드오프가 존재합니다.\n"
        "- Bloom Filter: 비트 배열 크기 ↑ → FPR ↓, 메모리 ↑\n"
        "- Count-Min Sketch: width/depth ↑ → 오차 ↓, 메모리 ↑"
    )
    
    gen.add_heading("Q2: 파라미터 증가가 항상 성능 향상을 가져오는가?", level=3)
    gen.add_info_box(
        "답변 입력",
        "[실험 데이터를 바탕으로 답변하세요]\n"
        "\n"
        "예시:\n"
        "아니오. 일정 수준 이상에서는 개선 폭이 감소하는 수렴 현상이 관찰됩니다."
    )
    
    gen.add_heading("Q3: 가장 실용적인 알고리즘은?", level=3)
    gen.add_info_box(
        "답변 입력",
        "[장단점 분석과 비즈니스 가치를 고려하여 답변하세요]\n"
        "\n"
        "예시:\n"
        "Count-Min Sketch가 더 실용적입니다.\n"
        "이유: 상품별 빈도 추정으로 인기도 순위 가능, 이상 거래 패턴 탐지 가능"
    )
    
    gen.add_heading("Q4: 실제 서비스 로그 분석에 적용한다면?", level=3)
    gen.add_info_box(
        "답변 입력",
        "[기술적, 운영적 관점을 고려하여 답변하세요]\n"
        "\n"
        "예시:\n"
        "Count-Min Sketch를 선택합니다.\n"
        "이유: 대규모 상품 클릭/구매 로그에서 전체 로그를 저장하지 않고도\n"
        "상품별 빈도 추정이 가능해 실시간 인기 상품 분석에 적합합니다."
    )
    
    gen.add_page_break()
    
    # ========== 참고자료 ==========
    gen.add_heading("참고자료", level=1)
    
    gen.add_heading("논문", level=2)
    gen.add_paragraph("1. Bloom, B. H. (1970). \"Space/time trade-offs in hash coding with allowable errors.\" Communications of the ACM, 13(7), 422-426.")
    gen.add_paragraph("2. Cormode, G., & Muthukrishnan, S. (2005). \"An improved data stream summary: the count-min sketch and its applications.\" Journal of Algorithms, 55(1), 58-75.")
    
    gen.add_heading("온라인 자료", level=2)
    gen.add_paragraph("• Bloom Filter - Wikipedia: https://en.wikipedia.org/wiki/Bloom_filter")
    gen.add_paragraph("• Count-Min Sketch - Wikipedia: https://en.wikipedia.org/wiki/Count%E2%80%93min_sketch")
    gen.add_paragraph("• Online Retail Dataset: https://archive.ics.uci.edu/dataset/352/online+retail")
    
    gen.add_heading("GitHub 저장소", level=2)
    gen.add_paragraph("프로젝트 코드: [GitHub 주소]")
    gen.add_paragraph("실험 결과: results/ 폴더")
    gen.add_paragraph("분석 스크립트: src/ 폴더")
    
    # ========== 저장 ==========
    gen.save("streaming_algorithm_report_template.docx")


def generate_report_with_results(results_dir: str = "../results", 
                                output_dir: str = "../report") -> None:
    """실험 결과를 포함한 DOCX 보고서 생성"""
    
    # 결과 로드
    results = load_experimental_results(results_dir)
    
    # 보고서 생성
    gen = ReportGenerator(output_dir)
    
    # 표지
    gen.add_title("스트리밍 알고리즘 비교 실험")
    gen.add_subtitle("Bloom Filter와 Count-Min Sketch의 정확도·메모리 트레이드오프 분석")
    
    # 요약 섹션
    gen.add_heading("Executive Summary", level=1)
    
    if results['summary']:
        gen.add_paragraph(
            "본 실험에서는 Online Retail Dataset을 대상으로 "
            "Bloom Filter와 Count-Min Sketch 알고리즘을 구현하고 성능을 비교했습니다.",
            bold=True
        )
        
        bf_summary = results['summary'].get('bloom_filter', {})
        cms_summary = results['summary'].get('count_min_sketch', {})
        
        if bf_summary:
            gen.add_paragraph(f"\n[Bloom Filter 최적 설정]", bold=True)
            gen.add_paragraph(f"• 메모리: {bf_summary.get('memory_mb', 'N/A'):.2f} MB")
            gen.add_paragraph(f"• 거짓 긍정율: {bf_summary.get('false_positive_rate', 'N/A'):.6f}")
            gen.add_paragraph(f"• 처리 시간: {bf_summary.get('processing_time_sec', 'N/A'):.2f}초")
        
        if cms_summary:
            gen.add_paragraph(f"\n[Count-Min Sketch 최적 설정]", bold=True)
            gen.add_paragraph(f"• 메모리: {cms_summary.get('memory_mb', 'N/A'):.2f} MB")
            gen.add_paragraph(f"• 상대 오차: {cms_summary.get('avg_relative_error', 'N/A'):.6f}")
            gen.add_paragraph(f"• 처리 시간: {cms_summary.get('processing_time_sec', 'N/A'):.2f}초")
    
    gen.add_page_break()
    
    # 결과 시각화
    charts_dir = os.path.join(results_dir, "charts")
    if os.path.exists(charts_dir):
        gen.add_heading("실험 결과 시각화", level=1)
        
        # 차트 추가
        chart_files = [
            ("01_bloom_filter_analysis.png", "Bloom Filter 분석"),
            ("02_count_min_sketch_analysis.png", "Count-Min Sketch 분석"),
            ("03_algorithm_comparison.png", "알고리즘 비교"),
        ]
        
        for chart_file, description in chart_files:
            chart_path = os.path.join(charts_dir, chart_file)
            if os.path.exists(chart_path):
                gen.add_heading(description, level=2)
                gen.add_image(chart_path)
    
    gen.add_page_break()
    
    # 상세 결과
    if results['bf_results']:
        gen.add_heading("Bloom Filter 상세 결과", level=1)
        
        # 결과 테이블
        table_data = []
        for result in results['bf_results'][:3]:  # 처음 3개만
            table_data.append([
                str(result.get('size', '')),
                str(result.get('hash_count', '')),
                f"{result.get('memory_mb', 0):.2f}",
                f"{result.get('false_positive_rate', 0):.6f}",
                f"{result.get('processing_time_sec', 0):.2f}",
            ])
        
        if table_data:
            headers = ["size", "hash_count", "메모리(MB)", "FPR", "시간(초)"]
            gen.add_table(table_data, headers)
    
    if results['cms_results']:
        gen.add_heading("Count-Min Sketch 상세 결과", level=1)
        
        # 결과 테이블
        table_data = []
        for result in results['cms_results'][:3]:  # 처음 3개만
            table_data.append([
                str(result.get('width', '')),
                str(result.get('depth', '')),
                f"{result.get('memory_mb', 0):.2f}",
                f"{result.get('avg_relative_error', 0):.6f}",
                f"{result.get('processing_time_sec', 0):.2f}",
            ])
        
        if table_data:
            headers = ["width", "depth", "메모리(MB)", "상대오차", "시간(초)"]
            gen.add_table(table_data, headers)
    
    # 저장
    gen.save("streaming_algorithm_report.docx")


def main():
    """메인 함수"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="DOCX 보고서 생성")
    parser.add_argument(
        "--template",
        action="store_true",
        help="템플릿만 생성 (실험 결과 없이)"
    )
    parser.add_argument(
        "--with-results",
        action="store_true",
        help="실험 결과를 포함하여 생성"
    )
    parser.add_argument(
        "--results-dir",
        default="../results",
        help="결과 디렉토리 경로"
    )
    parser.add_argument(
        "--output-dir",
        default="../report",
        help="출력 디렉토리 경로"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("DOCX 보고서 생성")
    print("=" * 60)
    
    if args.template or (not args.with_results):
        print("\n[1/1] 템플릿 생성 중...")
        generate_template_report(args.output_dir)
        print("✅ 템플릿 보고서 생성 완료!")
        print("    파일: report/streaming_algorithm_report_template.docx")
    
    if args.with_results:
        print("\n[1/1] 결과 포함 보고서 생성 중...")
        generate_report_with_results(args.results_dir, args.output_dir)
        print("✅ 결과 포함 보고서 생성 완료!")
        print("    파일: report/streaming_algorithm_report.docx")
    
    print("\n💡 팁: 생성된 DOCX 파일을 열어서 최종 분석 질문 답변을 작성하세요.")


if __name__ == "__main__":
    main()
