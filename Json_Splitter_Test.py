import pandas as pd
import numpy as np
from collections import defaultdict
import re
import json 
from langchain_text_splitters import MarkdownHeaderTextSplitter

### 통합 JSON file 가져오기
with open('./test_result(1~12).json','r', encoding='utf-8') as json_file:
  json_data = json.load(json_file)

### TEXT SPLIT AND GET TABLE DATA AS CSV TYPE 
def get_table_csv(one_json):
  headers_to_split_on = [
      ("#", "Header 1")
  ]
  md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, strip_headers=True, return_each_line=True)

  txt_doc_split = md_splitter.split_text(one_json['content'])
  pdf_metadata_csv = defaultdict(list)
  for idx, line in enumerate(txt_doc_split):
    
    header = line.metadata['Header 1']
    content = line.page_content

    if re.search(r'\|+\n+', content):
      # print(f'\ncontent ---------------------------------------\n{content}')
      cell_list = [cell for cell in content.split('|')[1:-1]]
      if ('공급대상' in cell_list) and ('주택관리번호' in cell_list):
        num_columns = cell_list.index('\n')
        new_count = cell_list.count('\n')
        # print(f'\nHeader : {header} ------------------------------------- ')
        # print(f'cell : {cell_list}')
        # print(f'num_columns : {num_columns}\nlength of list : {len(cell_list)}\nnum of newline : {new_count}')
        try:
          arr_list = []
          for t in range(2, len(cell_list)//num_columns - (new_count//num_columns)):
            arr = np.array(cell_list[t*num_columns+t:(t+1)*num_columns+t])
            arr_list.append(arr)
          
          info_extract_df = pd.DataFrame(arr_list, columns = cell_list[:num_columns])
          pdf_metadata_csv['공급대상'].append(info_extract_df)
        except:
          print(f"\n{one_json['title']}파일에서 markdown 오류로 인해 삽입하지 못했습니다.\n{content}")
        # print(f'\nextracted dataframe ---------------------------------------\n{info_extract_df}')
      elif ('공급금액' in cell_list) and ('약식표기' in cell_list):
        num_columns = cell_list.index('\n')
        new_count = cell_list.count('\n')
        # print(f'\nHeader : {header} ------------------------------------- ')
        # print(f'cell : {cell_list}')
        # print(f'num_columns : {num_columns}\nlength of list : {len(cell_list)}\nnum of newline : {new_count}')
        try:
          arr_list = []
          for t in range(2, len(cell_list)//num_columns - (new_count//num_columns)):
            arr = np.array(cell_list[t*num_columns+t:(t+1)*num_columns+t])
            arr_list.append(arr)
          
          info_extract_df = pd.DataFrame(arr_list, columns = cell_list[:num_columns])
          pdf_metadata_csv['분양금액'].append(info_extract_df)
        except:
          print(f"\n{one_json['title']}파일에서 markdown 오류로 인해 삽입하지 못했습니다.\n{content}")
      
      elif ('청약예끔' in cell_list) and ('예치금액' in cell_list):
        num_columns = cell_list.index('\n')
        new_count = cell_list.count('\n')
        # print(f'\nHeader : {header} ------------------------------------- ')
        # print(f'cell : {cell_list}')
        # print(f'num_columns : {num_columns}\nlength of list : {len(cell_list)}\nnum of newline : {new_count}')
        try:
          arr_list = []
          for t in range(2, len(cell_list)//num_columns - (new_count//num_columns)):
            arr = np.array(cell_list[t*num_columns+t:(t+1)*num_columns+t])
            arr_list.append(arr)
          
          info_extract_df = pd.DataFrame(arr_list, columns = cell_list[:num_columns])
          pdf_metadata_csv['분양금액'].append(info_extract_df)
        except:
          print(f"\n{one_json['title']}파일에서 markdown 오류로 인해 삽입하지 못했습니다.\n{content}")
      
    else:
      continue
  return pdf_metadata_csv


for idx, json_file in enumerate(json_data):
  try:
    json_file['metacsv'] = get_table_csv(json_file)
  except:
    print(f"extracted text에 오류가 존재합니다 : {idx}번째 파일 {json_file['title']}")


# 통합 JSON file 저장하기 : Object of type DataFrame is not JSON serializable
# with open('./result_with_metadata.json','w', encoding='utf-8') as f:
#  json.dump(json_data, f, indent=4)

### json(markdown)에 있는 table 웬만해서는 다 추출 가능한데 여기서 유용한 데이터만 뽑는건 그냥 키워드 중심으로 뽑아야 될지 모르겠음
### 유용한 데이터 필터링만 되면 csv로 뽑아서 바로 db로 넣으면 될듯
    