import os
import json
import nest_asyncio
import dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_parse.base import ResultType

dotenv.load_dotenv()
nest_asyncio.apply()

# LlamaParse 설정
parser = LlamaParse(
    result_type=ResultType.MD,  # 마크다운 형식
    num_workers=4,           # 워커 수 줄임
    verbose=True,            # 로깅 활성화
    language="ko",           # 언어 설정
)

# PDF 파일 추출 설정
file_extraction = {".pdf": parser}

def extract_pdf_content(pdf_path):
    try:
        # PDF 파일 로딩
        documents = SimpleDirectoryReader(
            input_files=[pdf_path],
            file_extractor=file_extraction,
        ).load_data()
        
        # 모든 문서 내용을 하나의 콘텐츠로 결합
        full_content = " ".join([doc.to_langchain_format().page_content for doc in documents])
        return full_content
    
    except Exception as e:
        print(f"Error parsing {pdf_path}: {e}")
        return None

try:
    # PDF 파일이 있는 디렉토리 경로
    pdf_directory = "C:/Users/Admin/Desktop/2. 모집 공고문 Crawling File (Modify)/02월"
    
    # 디렉토리 내 모든 PDF 파일 목록 가져오기
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    
    # JSON으로 저장할 데이터 구조
    json_data = []

    # 각 PDF 파일 처리
    for pdf_filename in pdf_files:
        # 전체 PDF 파일 경로
        pdf_path = os.path.join(pdf_directory, pdf_filename)
        
        # PDF 내용 추출
        full_content = extract_pdf_content(pdf_path)
        
        # 내용 추출에 성공한 경우에만 JSON에 추가
        if full_content:
            json_data.append({
                'title': pdf_filename,
                'content': full_content
            })

    # JSON 파일로 저장
    output_file = "February.json"
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    print(f"JSON 파일이 저장되었습니다: {output_file}")
    print(f"총 {len(json_data)}개의 PDF 파일이 처리되었습니다.")

except Exception as e:
    print(f"Main Error: {e}")