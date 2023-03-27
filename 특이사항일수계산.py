import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import scipy.stats as stats
import glob
import re

# 불러올 파일들이 있는 디렉토리 경로
#file_path = 'C:/Users/sang/Desktop/test/*.xlsx'


# 파일불러오기
sdm = pd.read_excel('sdmod.xlsx') #강수량 해상육상특보
sdo = pd.read_excel('sdorg.xlsx') #X
sfm = pd.read_excel('sfmod.xlsx') #해상육상특보
sfo = pd.read_excel('sforg.xlsx') #X
skm = pd.read_excel('skmod.xlsx') #특보
sko = pd.read_excel('skorg.xlsx') #X
srm = pd.read_excel('srmod.xlsx') #해상육상특보
sro = pd.read_excel('srorg.xlsx') #X


sdmA = sdm[["생산일","강수량","해상특보","육상특보"]]
sfmA = sfm[["생산일","해상특보","육상특보"]]
skmA = skm[["생산일","특보"]]
srmA = srm[["생산일","해상특보","육상특보"]]

# 중복 생산일 제거 후 '특보' 값이 '원하는 특보'인 행만 추출
WW_sdmA = sdmA[sdmA['해상특보'].isin(['WW1','WW2','WW3'])].drop_duplicates('생산일')
TY_sdmA = sdmA[sdmA['해상특보'].isin(['TY1','TY2','TY3'])].drop_duplicates('생산일')
RD_sdmA = sdmA[sdmA['강수량'].astype(int) > 0].drop_duplicates('생산일')
WW_sfmA = sfmA[sfmA['해상특보'].isin(['WW1','WW2','WW3'])].drop_duplicates('생산일')
TY_sfmA = sfmA[sfmA['해상특보'].isin(['TY1','TY2','TY3'])].drop_duplicates('생산일')
WW_skmA = skmA[skmA['특보'].isin(['WW1','WW2','WW3'])].drop_duplicates('생산일')
TY_skmA = skmA[skmA['특보'].isin(['TY1','TY2','TY3'])].drop_duplicates('생산일')
WW_srmA = srmA[srmA['해상특보'].isin(['WW1','WW2','WW3'])].drop_duplicates('생산일')
TY_srmA = srmA[srmA['해상특보'].isin(['TY1','TY2','TY3'])].drop_duplicates('생산일')


# 특보일수
print ("SD 풍랑일수", (len(WW_sdmA)))
print ("SD 태풍일수", (len(TY_sdmA)))
print ("SD 강수일수", (len(RD_sdmA)))
print ("SF 풍랑일수", (len(WW_sfmA)))
print ("SF 태풍일수", (len(TY_sfmA)))
print ("SK 풍랑일수", (len(WW_skmA)))
print ("SK 태풍일수", (len(TY_skmA)))
print ("SR 풍랑일수", (len(WW_srmA)))
print ("SR 태풍일수", (len(TY_srmA)))

'''
# 생산일 형식 변환
WW_sdmA['생산일'] = pd.to_datetime(WW_sdmA['생산일'],format='%Y/%m/%d')
TY_sdmA['생산일'] = pd.to_datetime(WW_sdmA['생산일'],format='%Y/%m/%d')
RD_sdmA['생산일'] = pd.to_datetime(WW_sdmA['생산일'],format='%Y/%m/%d')
WW_sfmA['생산일'] = pd.to_datetime(WW_sfmA['생산일'],format='%Y/%m/%d')
TY_sfmA['생산일'] = pd.to_datetime(WW_sfmA['생산일'],format='%Y/%m/%d')
WW_skmA['생산일'] = pd.to_datetime(WW_skmA['생산일'],format='%Y/%m/%d')
TY_skmA['생산일'] = pd.to_datetime(WW_skmA['생산일'],format='%Y/%m/%d')
WW_srmA['생산일'] = pd.to_datetime(WW_srmA['생산일'],format='%Y/%m/%d')
TY_srmA['생산일'] = pd.to_datetime(WW_srmA['생산일'],format='%Y/%m/%d')
'''



# 총 특보 및 강수일수
sdmd=(len(WW_sdmA)+len(TY_sdmA)+len(RD_sdmA))
sfmd=(len(WW_sfmA)+len(TY_sfmA))
skmd=(len(WW_skmA)+len(TY_skmA))
srmd=(len(WW_srmA)+len(TY_srmA))
print()      
print ("SD 총 특보 및 강수일수", sdmd)
print ("SF 총 특보 및 강수일수", sfmd)
print ("SK 총 특보 및 강수일수", skmd)
print ("SR 총 특보 및 강수일수", srmd)

# 총일수에 대한 확률
print()      
#SD
if sdmd != 0:
    sdWWP = len(WW_sdmA) / sdmd * 100
    print("SD풍랑 확률:", sdWWP,'%')
    sdTYP = len(TY_sdmA) / sdmd * 100
    print("SD태픙 확률:", sdTYP,'%')
    sdRDP = len(RD_sdmA) / sdmd * 100
    print("SD강수일 확률:", sdRDP,'%')
#SF
if sfmd != 0:
    sfWWP = len(WW_sfmA) / sfmd * 100
    print("SF풍랑 확률:", sfWWP,'%')
    sfTYP = len(TY_sfmA) / sfmd * 100
    print("SF태풍 확률:", sfTYP,'%')    
#Sk
if skmd != 0:
    skWWP = len(WW_skmA) / skmd * 100
    print("SK풍랑 확률:", skWWP,'%')
    skTYP = len(TY_skmA) / skmd * 100
    print("SK태풍 확률:", skTYP,'%')  
#SR
if srmd != 0:
    srWWP = len(WW_srmA) / srmd * 100
    print("SR풍랑 확률:", srWWP,'%')
    srTYP = len(TY_srmA) / srmd * 100
    print("SR태풍 확률:", srTYP,'%')  






