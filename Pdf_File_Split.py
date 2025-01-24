import os 
import shutil
from PyPDF2 import PdfReader

num = 1
page_sum = 0
for month in range(10,13):
  path = f'C:/Users/Admin/Desktop/2. 모집 공고문 Crawling File (Modify)/{month}월'

  file_list = os.listdir(path)
  print(f'파일 번호 : {num}')

  for idx, file in enumerate(file_list):
    file_path = os.path.join(path, file)

    pdf = PdfReader(open(file_path, 'rb'))
    numberPages = len(pdf.pages)

    # print(f'현재 파일명 : {os.path.basename(file)}')
    # print(f'현재 파일의 페이지 수 : {numberPages}')
    page_sum += numberPages
    print(f'{idx}번째 파일')
    print(f'{num}번째 폴더의 페이지 합계 : {page_sum}')

    # 파일마다 총 페이지 수 300까지
    if page_sum >= 900:
      page_sum = 0
      num += 1
      destination_directory = f'C:/Users/Admin/Desktop/2. 모집 공고문 Crawling File (Modify)/모집공고문_file_split/{num}'
      print(f'파일 번호 : {num}')
      try:
        os.makedirs(destination_directory)
      except:
        continue
      shutil.copy2(file_path, destfile_path)

    else:
      destination_directory = f'C:/Users/Admin/Desktop/2. 모집 공고문 Crawling File (Modify)/모집공고문_file_split/{num}'
      if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
      destfile_path = os.path.join(destination_directory, os.path.basename(file))
      shutil.copy2(file_path, destfile_path)