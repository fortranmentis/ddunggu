'''
Created on Mon Mar 13 16:07:22 2023
@author: sanghak
'''

import pandas as pd
import numpy as np
import glob
import os



#SD_F
input_file = r'C:\2023\python test\지역별통계내기\SD_F' # csv파일들이 있는 디렉토리 위치
output_file = r'C:\2023\python test\지역별통계내기\SD_F_result.csv' # 병합하고 저장하려는 파일명

allFile_list = glob.glob(os.path.join(input_file, '*')) # glob함수로 파일들을 모은다
print(allFile_list)

allData = [] # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
for file in allFile_list:
    with open(file, encoding='euc-kr') as f:
        df = pd.read_csv(f) # for구문으로 csv파일들을 읽어 들인다
        allData.append(df) # 빈 리스트에 읽어 들인 내용을 추가한다

dataCombine = pd.concat(allData, axis=0, ignore_index=True) # concat함수를 이용해서 리스트의 내용을 병합
# axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
dataCombine.to_csv(output_file, index=False, encoding='euc-kr') # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정



#SD_S
input_file = r'C:\2023\python test\지역별통계내기\SD_S' # csv파일들이 있는 디렉토리 위치
output_file = r'C:\2023\python test\지역별통계내기\SD_S_result.csv' # 병합하고 저장하려는 파일명

allFile_list = glob.glob(os.path.join(input_file, '*')) # glob함수로 파일들을 모은다
print(allFile_list)

allData = [] # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
for file in allFile_list:
    with open(file, encoding='euc-kr') as f:
        df = pd.read_csv(f) # for구문으로 csv파일들을 읽어 들인다
        allData.append(df) # 빈 리스트에 읽어 들인 내용을 추가한다

dataCombine = pd.concat(allData, axis=0, ignore_index=True) # concat함수를 이용해서 리스트의 내용을 병합
# axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
dataCombine.to_csv(output_file, index=False, encoding='euc-kr') # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정



#SF_F
input_file = r'C:\2023\python test\지역별통계내기\SF_F' # csv파일들이 있는 디렉토리 위치
output_file = r'C:\2023\python test\지역별통계내기\SF_F_result.csv' # 병합하고 저장하려는 파일명

allFile_list = glob.glob(os.path.join(input_file, '*')) # glob함수로 파일들을 모은다
print(allFile_list)

allData = [] # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
for file in allFile_list:
    with open(file, encoding='euc-kr') as f:
        df = pd.read_csv(f) # for구문으로 csv파일들을 읽어 들인다
        allData.append(df) # 빈 리스트에 읽어 들인 내용을 추가한다

dataCombine = pd.concat(allData, axis=0, ignore_index=True) # concat함수를 이용해서 리스트의 내용을 병합
# axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
dataCombine.to_csv(output_file, index=False, encoding='euc-kr') # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정



#SF_S
input_file = r'C:\2023\python test\지역별통계내기\SF_S' # csv파일들이 있는 디렉토리 위치
output_file = r'C:\2023\python test\지역별통계내기\SF_S_result.csv' # 병합하고 저장하려는 파일명

allFile_list = glob.glob(os.path.join(input_file, '*')) # glob함수로 파일들을 모은다
print(allFile_list)

allData = [] # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
for file in allFile_list:
    with open(file, encoding='euc-kr') as f:
        df = pd.read_csv(f) # for구문으로 csv파일들을 읽어 들인다
        allData.append(df) # 빈 리스트에 읽어 들인 내용을 추가한다

dataCombine = pd.concat(allData, axis=0, ignore_index=True) # concat함수를 이용해서 리스트의 내용을 병합
# axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
dataCombine.to_csv(output_file, index=False, encoding='euc-kr') # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정



#SK_F
input_file = r'C:\2023\python test\지역별통계내기\SK_F' # csv파일들이 있는 디렉토리 위치
output_file = r'C:\2023\python test\지역별통계내기\SK_F_result.csv' # 병합하고 저장하려는 파일명

allFile_list = glob.glob(os.path.join(input_file, '*')) # glob함수로 파일들을 모은다
print(allFile_list)

allData = [] # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
for file in allFile_list:
    with open(file, encoding='euc-kr') as f:
        df = pd.read_csv(f) # for구문으로 csv파일들을 읽어 들인다
        allData.append(df) # 빈 리스트에 읽어 들인 내용을 추가한다

dataCombine = pd.concat(allData, axis=0, ignore_index=True) # concat함수를 이용해서 리스트의 내용을 병합
# axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
dataCombine.to_csv(output_file, index=False, encoding='euc-kr') # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정



#SK_S
input_file = r'C:\2023\python test\지역별통계내기\SK_S' # csv파일들이 있는 디렉토리 위치
output_file = r'C:\2023\python test\지역별통계내기\SK_S_result.csv' # 병합하고 저장하려는 파일명

allFile_list = glob.glob(os.path.join(input_file, '*')) # glob함수로 파일들을 모은다
print(allFile_list)

allData = [] # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
for file in allFile_list:
    with open(file, encoding='euc-kr') as f:
        df = pd.read_csv(f) # for구문으로 csv파일들을 읽어 들인다
        allData.append(df) # 빈 리스트에 읽어 들인 내용을 추가한다

dataCombine = pd.concat(allData, axis=0, ignore_index=True) # concat함수를 이용해서 리스트의 내용을 병합
# axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
dataCombine.to_csv(output_file, index=False, encoding='euc-kr') # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정



#SR_F
input_file = r'C:\2023\python test\지역별통계내기\SR_F' # csv파일들이 있는 디렉토리 위치
output_file = r'C:\2023\python test\지역별통계내기\SR_F_result.csv' # 병합하고 저장하려는 파일명

allFile_list = glob.glob(os.path.join(input_file, '*')) # glob함수로 파일들을 모은다
print(allFile_list)

allData = [] # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
for file in allFile_list:
    with open(file, encoding='euc-kr') as f:
        df = pd.read_csv(f) # for구문으로 csv파일들을 읽어 들인다
        allData.append(df) # 빈 리스트에 읽어 들인 내용을 추가한다

dataCombine = pd.concat(allData, axis=0, ignore_index=True) # concat함수를 이용해서 리스트의 내용을 병합
# axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
dataCombine.to_csv(output_file, index=False, encoding='euc-kr') # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정



#SR_S
input_file = r'C:\2023\python test\지역별통계내기\SR_S' # csv파일들이 있는 디렉토리 위치
output_file = r'C:\2023\python test\지역별통계내기\SR_S_result.csv' # 병합하고 저장하려는 파일명

allFile_list = glob.glob(os.path.join(input_file, '*')) # glob함수로 파일들을 모은다
print(allFile_list)

allData = [] # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
for file in allFile_list:
    with open(file, encoding='euc-kr') as f:
        df = pd.read_csv(f) # for구문으로 csv파일들을 읽어 들인다
        allData.append(df) # 빈 리스트에 읽어 들인 내용을 추가한다

dataCombine = pd.concat(allData, axis=0, ignore_index=True) # concat함수를 이용해서 리스트의 내용을 병합
# axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
dataCombine.to_csv(output_file, index=False, encoding='euc-kr') # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정





