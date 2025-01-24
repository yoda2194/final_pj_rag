import re
import json 
from datetime import datetime

### 모집공고문 기본 정보 추출하기
# 통합 JSON file 가져오기
with open('./test_result(1~12).json','r', encoding='utf-8') as json_file:
  json_data = json.load(json_file)

### FILTERING
json_list = []
for json_one in json_data:
  if re.search('임의공급', json_one['content']): # 임의공급 모집공고문 제외
    print(json_one['title'])
    continue
  elif re.search('오피스텔', json_one['content']):
    continue
  elif re.search('민간임대', json_one['content']):
    continue
  elif re.search('NO_CONTENT_HERE', json_one['content']):
    continue
  else:
    json_list.append(json_one)

### 날짜 파싱 후 datetime 객체로 변환
def parse_date(date_str, formats):
  for fmt in formats:
      try:
          return datetime.strptime(date_str, fmt).date()
      except ValueError:
          continue

### Markdown에서 기본 정보 추출
def extract_info_content(pdf_json): 
  page_content = pdf_json['content']
  recruit_announce_date = None
  special_supply_apply_date = None
  winner_announce_date = None
  land_type = None

  # 민영 / 공공 추출
  if re.search('무순위', page_content):
      area_local = None
      area_other = None
      apply_type = '무순위'
  else:
    apply_type = 'APT'
    if re.search('민영', page_content):
      land_type = '민영'
    elif re.search('공공', page_content):
      land_type = '공공'
    try:
      # 해당지역, 기타지역 추출
      local = re.findall(r'[가-힣]{2,}\s*\,*[가-힣]*\s*거주자',page_content)

      area_local = local[0][:-3]
      area_other = local[1][:-3]
      if len(area_local) > 10:
        area_local = None
      if len(area_other) > 10:
        area_other = None
    except:
      area_local = None
      area_other = None
  
# 모집공고일, 특별공급 접수일, 당첨자 발표일 추출
  all_date = re.findall(r'[0-9]{2,5}\.[0-9]{2}\.[0-9]{2}\.*\([가-힣]{1}\)',page_content)
  all_date = [date[:-3] for date in all_date]

  # 날짜 파싱
  date_fmt = ['%Y.%m.%d.', '%y.%m.%d.', '%Y.%m.%d', '%y.%m.%d']
  parsed_dates = [parse_date(date, date_fmt) for date in all_date]
  
  try:
  # 택지 유형
    if apply_type == '무순위':
      recruit_announce_date = parsed_dates[1]
      special_supply_apply_date = None
      winner_announce_date = parsed_dates[3]
      land_type = None
    else:
      recruit_announce_date = parsed_dates[0]
      special_supply_apply_date = parsed_dates[1]
      winner_announce_date = parsed_dates[4]    
  except:
    pass
    
  apartment_name = re.match(r'[0-9]{2}월_([a-zA-Z0-9가-힣]{1,}\s*)+', pdf_json['title'])[0][4:]

  # dictionary에 저장  
  pdf_info_extract_dict = {
  'apartment_name' : apartment_name,
  'apply_type' : apply_type,
  'area_local' : area_local,
  'area_other' : area_other,
  'land_type' : land_type,
  'recruit_announce_date' : recruit_announce_date,
  'special_supply_apply_date' : special_supply_apply_date,
  'winner_announce_date' : winner_announce_date
  }
  return pdf_info_extract_dict

### tag key에 dictionary 형태로 추출 데이터 저장 (모집공고문 기본 정보)
for idx, pdf_json in enumerate(json_list):
  pdf_json['tag'] = extract_info_content(pdf_json)