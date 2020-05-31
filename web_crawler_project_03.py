# -*- coding: utf-8 -*-
"""
Created on Thu May 21 22:30:18 2020

@author: jungho
***************************************
**selenium 및 chrome_driver 설치 필수**
***************************************
"""


from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import numpy as np

bank_list = list() #은행, 저축은행 목록
savingProductTitle_list = list()
interestRate_list = list()
totalInterest_list = list()
financialEvaluation_list = list()
financialEvaluationLink_list = list()
path = 'C:/Users/jungho/Downloads/chromedriver.exe' #chromedriver 경로 pc환경에 맞게 수정필요
savePath = 'C:/Users/jungho/.spyder-py3/금융상품검색결과.csv' #엑셀파일 경로
url_2 = 'https://www.catch.co.kr/' #재무평가 검색 url

def savingOptionSetting():
    if savingOption == 0:
        print('정기예금을 선택하셨습니다.')
        url = 'https://finlife.fss.or.kr/deposit/selectDeposit.do?menuId=2000100'
    if savingOption == 1:
        print('적금을 선택하셨습니다.')
        url = 'https://finlife.fss.or.kr/installment/selectinstallment.do?menuId=2000101'
    return url

def openUrl(path,url): #url open
    driver = webdriver.Chrome(path) #path는 pc환경에 맞춰야함
    driver.get(url)
    return driver
    

def savingAmountSetting():
    selected_tag = driver.find_element_by_css_selector('input#saving-money01.inputContentMoney') #저축금액 입력 
    a = 0
    while a < 8:
        selected_tag.send_keys('\ue003')
        a += 1
    if savingOption == 0:
        deposit = input('저축금액을 입력하세요. (단위: 원)\n')
        print(deposit + '원을 입력하였습니다.')
    if savingOption == 1:
        deposit = input('월 저축금액 입력하세요. (단위: 원)\n')
        print(deposit + '원을 입력하였습니다.\n')
    selected_tag.send_keys(deposit)
    return deposit
    
def savingPeriodSetting():#저축기간 선택
    print(str(savingPeriod) + '개월을 입력하였습니다.\n')
    selected_tag = driver.find_element_by_xpath(("//button[@value={}]").format(savingPeriod))
    '''
    if savingPeriod == 6:
        selected_tag = driver.find_element_by_xpath("//button[@value=6]")
    if savingPeriod == 12:
        selected_tag = driver.find_element_by_xpath("//button[@value=12]")
    if savingPeriod == 24:
        selected_tag = driver.find_element_by_xpath("//button[@value=24]")
    if savingPeriod == 36:
        selected_tag = driver.find_element_by_xpath("//button[@value=36]")
    '''
    selected_tag.click()
    
def bankGroupSetting():    
    if bankGroup == 0:
        print('은행을 입력하였습니다.\n')
        selected_tag = driver.find_element_by_xpath("//button[@value=020000]")
    if bankGroup == 1:
        print('저축은행을 입력하였습니다.\n')
        selected_tag = driver.find_element_by_xpath("//button[@value=030300]")
    selected_tag.click()
    
def productSearching():
    selected_tag = driver.find_element_by_css_selector('button.bank-serch.ajaxFormSearch') #검색
    selected_tag.click()
    
def informationListMaking():
    time.sleep(8)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    temps = soup.find('tbody').findAll('td')
    if savingOption == 0:  #필요한 정보만 list에 저장
        a = 0
        while a < 10 :
            b = 11*a+1#은행명
            c = 11*a+2#상품명
            d = 11*a+3 #세전 이율
            e = 11*a+5 #세후 이자
            bank_list.append(temps[b].get_text())
            savingProductTitle_list.append(temps[c].get_text())
            interestRate_list.append(temps[d].get_text())
            totalInterest_list.append(temps[e].get_text())
            a += 1
    if savingOption == 1:
        a = 0
        while a < 10 :
            b = 12*a+1#은행명
            c = 12*a+2#상품명
            d = 12*a+4 #세전 이율
            e = 12*a+6 #세후 이자
            bank_list.append(temps[b].get_text())
            savingProductTitle_list.append(temps[c].get_text())
            interestRate_list.append(temps[d].get_text())
            totalInterest_list.append(temps[e].get_text())
            a += 1

def printTopTen():
    print('---------------------------------------------------------------------------')
    if bankGroup == 0:
        print('이율 상위 10개 은행:')
    if bankGroup == 1:
        print('이율 상위 10개 저축은행: ')
    print(bank_list)
    print('---------------------------------------------------------------------------')
    
def printInformation():
    i = 0
    for bank in bank_list:
        selected_tag = driver.find_element_by_css_selector('input.inp') #은행명 입력
        time.sleep(5) #delay 주어야함 제대로 수행 안될시 시간을 늘린다.
        selected_tag.send_keys(bank)
        selected_tag = driver.find_element_by_css_selector('#header div div p a img') #재무평가 태그 선택
        selected_tag.click()
        time.sleep(8) #delay 주어야함 제대로 수행 안될시 시간을 늘린다.
        print('---------------------------------------------------------------------------')
        #print(driver.current_url) 에러 발생시 url이 일치하는지 확인
        try: #재무평가 있을 때
            soup = BeautifulSoup(driver.page_source, 'html.parser') #은행재무평가점수 태그 가져옴
            financialEvaluation = soup.find('span', {'class': 'pointc_3'}).get_text()
            financialEvaluation_list.append(financialEvaluation)
            financialEvaluationLink = soup.find('a', {'href': re.compile('^(/Comp/CompInfo).*')}).attrs['href']#재무평가 상세링크 가져옴
            financialEvaluationLink_list.append(('https://www.catch.co.kr{}').format(financialEvaluationLink))#재무평가 상세링크 저장
            print(bank) #필요한 정보 출력 부분
            print(savingProductTitle_list[i])
            print('세전 이율: ' + interestRate_list[i])
            print(('세후 이자: ' + totalInterest_list[i] + '원 ({}개월 후)').format(str(savingPeriod)))
            print('재무평가 점수: ' + financialEvaluation)
            print(('재무평가 상세 링크: https://www.catch.co.kr{}').format(financialEvaluationLink))
        except Exception: #재무평가 없을 때 예외처리
            financialEvaluation_list.append('재무평가 정보를 찾을 수 없습니다.')
            financialEvaluationLink_list.append('')
            print(bank)
            print(savingProductTitle_list[i])
            print('세전 이율: ' + interestRate_list[i])
            print(('세후 이자: ' + totalInterest_list[i] + '원 ({}개월 후)').format(str(savingPeriod)))
            print('재무평가 정보를 찾을 수 없습니다.')
        i+=1
        time.sleep(8) #delay 주어야함 제대로 수행 안될시 시간을 늘린다.
        selected_tag = driver.find_element_by_css_selector('div#header_wrap div#gnb2 div.inner h1 a')
        selected_tag.click()
        time.sleep(8) #delay 주어야함 제대로 수행 안될시 시간을 늘린다.
        
def saveAsExcelFile(path):
    if savingOption == 0:
        data = {
            '은행명' : bank_list,
            '상품명' : savingProductTitle_list,
            '저축금액' : deposit,
            '저축기간' : savingPeriod,
            '세전 이율' : interestRate_list,
            '세후 이자' : totalInterest_list,
            '재무평가 점수' : financialEvaluation_list,
            '재무평가 상세 링크' : financialEvaluationLink_list
        }
    if savingOption == 1:
        data = {
            '은행명' : bank_list,
            '상품명' : savingProductTitle_list,
            '월 저축금액' : deposit,
            '저축기간' : savingPeriod,
            '세전 이율' : interestRate_list,
            '세후 이자' : totalInterest_list,
            '재무평가 점수' : financialEvaluation_list,
            '재무평가 상세 링크' : financialEvaluationLink_list
        }
    df = pd.DataFrame(data ,index = np.arange(1,11))
    df.to_csv(path,encoding='cp949') #경로는 pc환경에 맞춰야함

savingOption = int(input('상품을 선택하세요. (정기예금은 0, 적금은 1)\n')) #예금 방식(정기예금, 적금) 선택, Url 실행
url_1 = savingOptionSetting() #정기예금, 적금을 선택하여 url 받아옴
driver = openUrl(path,url_1) #받은 url로 chrome 실행
deposit = savingAmountSetting() #저축금액 설정
savingPeriod = int(input('저축 기간을 입력하세요. (6, 12 , 24, 36) (단위: 개월)\n')) #저축 기간 입력
savingPeriodSetting() #저축기간 설정
bankGroup = int(input('금융권역을 선택하세요. (은행 0, 저축은행 1)\n')) #금융권역 선택
bankGroupSetting() #금융권역 설정
productSearching() #금융상품 검색
informationListMaking() #정보리스트 만듦
printTopTen() #이율 기준 상위 10개 출력
driver.close() #은행 검색 완료
driver = openUrl(path,url_2)
printInformation() #정보 출력
driver.close() #은행 재무평가 검색 완료
saveAsExcelFile(savePath) #엑셀 파일로 저장, 엑셀 파일이 열려 있으면 저장안 됨