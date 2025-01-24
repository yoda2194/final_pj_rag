from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def get_pdf_lh(startDt, endDt, list_len):
  driver = webdriver.Chrome()
  url = "https://apply.lh.or.kr/lhapply/apply/wt/wrtanc/selectWrtancList.do?mi=1027"
  driver.get(url)

  driver.find_element(By.ID, "panSs").send_keys("전체")  
  driver.find_element(By.ID, "startDt").send_keys(str(startDt))  
  driver.find_element(By.ID, "endDt").send_keys(str(endDt))    
  driver.find_element(By.ID, "btnSah").click()  # 검색 버튼 클릭
  time.sleep(5)

  driver.find_element(By.ID, "listWt").send_keys(f"{list_len}건")    
  time.sleep(5)
  page_len = len(driver.find_elements(By.CSS_SELECTOR, "#sub_container > form:nth-child(7) > div > a.bbs_pge_num")) + 1
  
  for t in range(1,page_len):
    houses = driver.find_elements(By.CSS_SELECTOR, "table > tbody > tr")
  
    for i in range(len(houses)):
      houses = driver.find_elements(By.CSS_SELECTOR, "table > tbody > tr")
      house = houses[i]
      
      house_title = house.find_element(By.CSS_SELECTOR, "td.mVw.bbs_tit > a").text
      print(f"{i+1}번째 모집공고 : {house_title}")

      house_link = house.find_element(By.CSS_SELECTOR, "td.mVw.bbs_tit > a") 
      house_link.click() # 표에서 해당 분양 공고 클릭
      time.sleep(8)

      # pdf 파일 다운로드
      pdf_load = driver.find_element(By.CSS_SELECTOR, 'div.bbsV_atchmnfl > dl.col_red > dd > ul > li') 
      pdf_load.find_element(By.XPATH, "//a[contains(text(), '.pdf')]").click()
      
      # 이전 탭으로 이동하기
      driver.back()
      time.sleep(5)

    # 다음 페이지로 이동
    if (t+1) % 10 == 1:
      driver.find_element(By.XPATH, "//a[contains(text(), '다음 페이지')]").click() 
    try:
      driver.find_element(By.XPATH, f"//a[contains(text(), '{t+1}')]").click()
    except:
      continue
      


get_pdf_lh("2024-01-01", "2025-01-01", 100)