"""
Created on Mon Mar 13 16:07:22 2023
@author: sanghak
"""

import pandas as pd
import numpy as np


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

sdmA = sdmA.replace('-', np.nan)
sfmA= sfmA.replace('-', np.nan)
skmA = skmA.replace('-', np.nan)
srmA  = srmA .replace('-', np.nan)

# 중복 생산일 제거 후 '특보' 값이 '원하는 특보'인 행만 추출
def filter_dataframe(df, condition):
    return df[df.apply(lambda x: condition(x), axis=1)].drop_duplicates('생산일')
WW_sdmA = filter_dataframe(sdmA, lambda x: x['해상특보'] in ['WW1','WW2','WW3'])
TY_sdmA = filter_dataframe(sdmA, lambda x: x['해상특보'] in ['TY1','TY2','TY3'])
RD_sdmA = filter_dataframe(sdmA, lambda x: int(x['강수량']) > 0)
WW_sfmA = filter_dataframe(sfmA, lambda x: x['해상특보'] in ['WW1','WW2','WW3'])
TY_sfmA = filter_dataframe(sfmA, lambda x: x['해상특보'] in ['TY1','TY2','TY3'])
WW_skmA = filter_dataframe(skmA, lambda x: x['특보'] in ['WW1','WW2','WW3'])
TY_skmA = filter_dataframe(skmA, lambda x: x['특보'] in ['TY1','TY2','TY3'])
WW_srmA = filter_dataframe(srmA, lambda x: x['해상특보'] in ['WW1','WW2','WW3'])
TY_srmA = filter_dataframe(srmA, lambda x: x['해상특보'] in ['TY1','TY2','TY3'])

RD_sdmA = RD_sdmA[["생산일","강수량"]]


# 데이터 프레임 합치기 일
merge_WW = pd.merge(WW_sdmA, pd.merge(WW_sfmA, WW_srmA, on='생산일', how='outer'), on='생산일', how='outer')
mWW = pd.merge(WW_skmA, merge_WW, on='생산일', how='outer')
mWW = mWW.sort_values('생산일')
mWW = mWW.reset_index(drop=True)
mWW['해상특보_x'].fillna('', inplace=True)
mWW['해상특보_y'].fillna('', inplace=True)
mWW['특보'].fillna('', inplace=True)
mWW['육상특보_x'].fillna('', inplace=True)
mWW['육상특보_y'].fillna('', inplace=True)
mWW['해상특보WW'] = mWW['해상특보_x'].astype(str) + mWW['해상특보_y'].astype(str) + mWW['특보'].astype(str)
mWW['육상특보WW'] = mWW['육상특보_x'].astype(str) + mWW['육상특보_y'].astype(str)
mWW.drop(['해상특보_x', '해상특보_y','육상특보_x', '육상특보_y','특보','해상특보','육상특보'], axis=1, inplace=True)

##########################################################################################

merge_TY= pd.merge(TY_sdmA, pd.merge(TY_sfmA, TY_srmA, on='생산일', how='outer'), on='생산일', how='outer')
mTY = pd.merge(TY_skmA, merge_TY, on='생산일', how='outer')
mTY = mTY.sort_values('생산일')
mTY = mTY.reset_index(drop=True)
mTY['해상특보_x'].fillna('', inplace=True)
mTY['해상특보_y'].fillna('', inplace=True)
mTY['특보'].fillna('', inplace=True)
mTY['육상특보_x'].fillna('', inplace=True)
mTY['육상특보_y'].fillna('', inplace=True)
mTY['해상특보TY'] = mTY['해상특보_x'].astype(str) + mTY['해상특보_y'].astype(str) + mTY['특보'].astype(str)
mTY['육상특보TY'] = mTY['육상특보_x'].astype(str) + mTY['육상특보_y'].astype(str)
mTY.drop(['해상특보_x', '해상특보_y','육상특보_x', '육상특보_y','특보','해상특보','육상특보'], axis=1, inplace=True)

##########################################################################################

merge_all= pd.merge(RD_sdmA, pd.merge(mWW, mTY, on='생산일', how='outer'), on='생산일', how='outer')
merge_all = merge_all.sort_values('생산일')
merge_all = merge_all.reset_index(drop=True)
mall=merge_all


mall['강수량'].fillna('0', inplace=True)
mall['강수량_x'].fillna('0', inplace=True)
mall['강수량_y'].fillna('0', inplace=True)
mall['강수량_all'] = mall['강수량'].astype(int) + mall['강수량_x'].astype(int) + mall['강수량_y'].astype(int)
mall.drop(['강수량','강수량_x','강수량_y'], axis=1, inplace=True)

##########################################################################################

# 0을 빈문자열로 채우기
def replace_zero_with_empty(df):
    return df.replace(0, '')

mall = replace_zero_with_empty(mall)

def replace_empty_with_nan(df):
    return df.replace('', np.nan)

mall = replace_empty_with_nan(mall)

count_mall = mall.count()

#print(count_mall)

# 특정 열의 원소 개수 세기
count_day = mall['생산일'].count()
count_WW = mall['해상특보WW'].count()
count_TY = mall['해상특보TY'].count()
count_RD = mall['강수량_all'].count()

if count_day != 0:
    perWW = round(count_WW / count_day * 100, 1)
#    print("풍랑 확률:", perWW,'%')
    perTY = round(count_TY / count_day * 100, 1)
#    print("태풍 확률:", perTY,'%')
    perRD = round(count_RD / count_day * 100, 1)
#    print("강수일 확률:", perRD,'%')

print("생산일 :",count_day,"일")
print("태풍 :",count_TY,"일,", "태풍 확률:", perTY,'%')
print("풍랑 :",count_WW,"일,", "풍랑 확률:", perWW,'%')
print("강수일 :",count_RD,"일,", "강수일 확률:", perRD,'%')





