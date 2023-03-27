"""
Created on Mon Mar 13 17:03:17 2023

@author: sang
"""

'''
mod=서비스
org=예측
'''
import pandas as pd

# 갈라짐
file_path = r'C:\2023\python test\지역별통계내기\2211\sdmod.xlsx'
file_path2 = r'C:\2023\python test\지역별통계내기\2211\sdorg.xlsx'
sdm = pd.read_excel(file_path)
sdo = pd.read_excel(file_path2)

SD_row = sdm.shape[0]

sdo['해상특보']=''
sdo['육상특보']=''
sdo['특보점수']=''

sdm1 = sdm[["생산일","권역","지역","기온점수","풍속점수","날씨점수","해상특보","육상특보","특보점수","예보지수"]]
sdo1 = sdo[["생산일","권역","지역","기온점수","풍속점수","날씨점수","해상특보","육상특보","특보점수","예보지수"]]

compare = sdm1['예보지수'] == sdo1['예보지수']
csdm = sdm1[~compare]
csdo = sdo1[~compare]

csdm_c = csdm.copy()

csdm_c['강수량']=sdm["강수량"]
csdm_c['강수점수']=sdm["강수점수"]

csdm_c = csdm_c.sort_values(by=['권역','지역'], ascending=[True, True])
csdo = csdo.sort_values(by=['권역','지역'], ascending=[True, True])

csdm_c.rename(columns={'기온점수':'기온점수m'},inplace=True)
csdo.rename(columns={'기온점수':'기온점수o'},inplace=True)
csdm_c.rename(columns={'풍속점수':'풍속점수m'},inplace=True)
csdo.rename(columns={'풍속점수':'풍속점수o'},inplace=True)
csdm_c.rename(columns={'날씨점수':'날씨점수m'},inplace=True)
csdo.rename(columns={'날씨점수':'날씨점수o'},inplace=True)
csdm_c.rename(columns={'예보지수':'예보지수m'},inplace=True)
csdo.rename(columns={'예보지수':'예보지수o'},inplace=True)

sd_result = pd.concat([csdm_c,csdo],axis=1)

# 중복된 열을 제거하여 유일한 값을 가지도록 만듦
sd_result = sd_result.loc[:, ~sd_result.columns.duplicated(keep='first')]

# 컬럼 순서 변경
sd_result = sd_result[['생산일', '권역', '지역', '기온점수m','기온점수o','풍속점수m','풍속점수o','날씨점수m','날씨점수o','강수량','강수점수','해상특보','육상특보','특보점수','예보지수m','예보지수o']]
sd_result = sd_result.reset_index(drop=True)
sd_result.index = sd_result.index + 1

# 셀 색칠 함수
def highlight_diff(x, color):
    style = 'background-color: {}'.format(color)
    if x[0] != x[1]:
        return [style, style]
    else:
        return ['', '']

def highlight_special_R(row):
    if row.name == '강수량':
        return ['background-color: orange' if x != '-' else '' for x in row]
    else:
        return [''] * len(row)

def highlight_special_W(row):
    if row.name == '해상특보':
        return ['background-color: green' if x != '-' else '' for x in row]
    else:
        return [''] * len(row)

# 열 비교하여 값이 다른 경우 해당 셀 색칠
sd_html = sd_result.style.apply(highlight_diff, color='yellow', axis=1, subset=['기온점수m', '기온점수o']) \
              .apply(highlight_diff, color='blue', axis=1, subset=['풍속점수m', '풍속점수o']) \
              .apply(highlight_diff, color='red', axis=1, subset=['날씨점수m', '날씨점수o']) \
              .apply(lambda x: highlight_special_R(x), axis=0) \
              .apply(lambda x: highlight_special_W(x), axis=0) \
              .set_properties(**{'border': '1px solid black'})

# 스타일이 적용된 데이터프레임을 HTML 파일로 저장
with open('갈라짐.html', 'w') as f:
    f.write(sd_html.to_html())
    
# 스타일이 적용된 데이터프레임을 xlsx 파일로 저장
sd_html.to_excel('갈라짐.xlsx', index=True)

#각 권역의 갯수, 각 지역의 갯수, 각 변경요인 갯수
sd_loc = sd_result['권역'].value_counts().sort_index().to_frame(name='횟수').reset_index().rename(columns={'index': '권역'})
sd_locp = sd_result.groupby(['권역', '지역'])['지역'].count().reset_index(name='횟수')

#각 권역의 각각의 변경요인 갯수
#각 지역의 각각의 변경요인 갯수
def count_changes_SD(df, groupby_col, warn_col='해상특보', rain_col='강수량'):
    count = df.groupby(groupby_col).apply(lambda x: pd.Series({'기온점수count': (x['기온점수m'] != x['기온점수o']).sum(),
                                                                  '풍속점수count': (x['풍속점수m'] != x['풍속점수o']).sum(),
                                                                  '날씨점수count': (x['날씨점수m'] != x['날씨점수o']).sum()})).reset_index()
    warn = df[df[warn_col] != '-'].groupby(groupby_col + [warn_col]).size().reset_index(name=warn_col+'count')
    pivot = warn.pivot_table(index=groupby_col, columns=warn_col, values=warn_col+'count', fill_value=0).reset_index()
    count = count.merge(pivot, on=groupby_col, how='left').fillna(0)
    rain = df[df[rain_col].astype(int) > 0].groupby(groupby_col + [rain_col]).size().reset_index(name=rain_col+'count')
    count = count.merge(rain, on=groupby_col, how='left').fillna(0)
    return count

count2_sd1 = count_changes_SD(sd_result, ['권역'])
count2_sd2 = count_changes_SD(sd_result, ['권역', '지역'])

# WW2와 WW3열이 모두 존재하는 경우에만 WW2와 WW3열을 합쳐서 WW열로 만듦
# TY2와 TY3열이 모두 존재하는 경우에만 TY2와 TY3열을 합쳐서 TY열로 만듦
def combine_columns(df, col1, col2, new_col):
    if col1 in df.columns and col2 in df.columns:
        df[new_col] = df[col1] + df[col2]
        df.drop([col1, col2], axis=1, inplace=True)
    elif col1 in df.columns:
        df[new_col] = df[col1]
        df.drop([col1], axis=1, inplace=True)
    elif col2 in df.columns:
        df[new_col] = df[col2]
        df.drop([col2], axis=1, inplace=True)
    else:
        df[new_col] = 0
    return df

count2_sd1 = combine_columns(count2_sd1, 'WW2', 'WW3', 'WW')
count2_sd2 = combine_columns(count2_sd2, 'WW2', 'WW3', 'WW')
count2_sd1 = combine_columns(count2_sd1, 'TY2', 'TY3', 'TY')
count2_sd2 = combine_columns(count2_sd2, 'TY2', 'TY3', 'TY')

count2_sd1 = pd.merge(count2_sd1, sd_loc, on='권역')
count2_sd2 = pd.merge(count2_sd2, sd_locp, on='지역')

sd_row_sum = count2_sd2["횟수"].sum()

print('SD 총통계')
sd_sum_all = count2_sd1.sum()
sd_sum_all = pd.DataFrame(sd_sum_all, columns=['변경'])
sd_sum_all = sd_sum_all.drop('권역', axis=0)
sd_sum_all = sd_sum_all.rename(index={'횟수': '총예보지수변경'})
print(sd_sum_all)
sd_sum_all.to_csv('갈라짐_요약.csv', encoding='euc-kr', index=True)

def calculate_percentages(df, row_sum):
    df['기온%'] = round(df['기온점수count'] / row_sum * 100, 1)
    df['풍속%'] = round(df['풍속점수count'] / row_sum * 100, 1)
    df['날씨%'] = round(df['날씨점수count'] / row_sum * 100, 1)
    df['강수량%'] = round(df['강수량count'] / row_sum * 100, 1)
    df['WW%'] = round(df['WW'] / row_sum * 100, 1)
    df['TY%'] = round(df['TY'] / row_sum * 100, 1)
    df['횟수%'] = round(df['횟수'] / row_sum * 100, 1)
    return df

count2_sd1 = calculate_percentages(count2_sd1, sd_row_sum)
count2_sd2 = calculate_percentages(count2_sd2, sd_row_sum)

count2_sd2 = count2_sd2.drop('권역_y', axis=1)
count2_sd2 = count2_sd2.rename(columns={'권역_x':'권역'})

SD_new_order = ['권역', '횟수','횟수%', '강수량count','강수량%','TY','TY%']
count2_sd1 = count2_sd1.reindex(columns=SD_new_order)
SD_new_order2 = ['권역', '지역','횟수','횟수%', '강수량count','강수량%','TY','TY%']
count2_sd2 = count2_sd2.reindex(columns=SD_new_order2)

# 구분열 안의 요소들을 서해, 남해, 동해 순으로 배열
SD_new_order3 = ['황해중부', '황해남부', '제주도','남해서부','남해동부','동해남부','동해중부']
count2_sd1['권역'] = pd.Categorical(count2_sd1['권역'], categories=SD_new_order3, ordered=True)
count2_sd1 = count2_sd1.sort_values('권역').reset_index(drop=True)
count2_sd2['권역'] = pd.Categorical(count2_sd2['권역'], categories=SD_new_order3, ordered=True)
count2_sd2 = count2_sd2.sort_values('권역').reset_index(drop=True)

count2_sd1.to_csv('갈라짐_권역_사유.csv', encoding='euc-kr', index=False)
count2_sd2.to_csv('갈라짐_지역_사유.csv', encoding='euc-kr', index=False)

##################################################################
##################################################################
##################################################################
##################################################################

#바다낚시
file_path3 = r'C:\2023\python test\지역별통계내기\2211\sfmod.xlsx'
file_path4 = r'C:\2023\python test\지역별통계내기\2211\sforg.xlsx'
sfm = pd.read_excel(file_path3)
sfo = pd.read_excel(file_path4)

# 행의 갯수
SF_row = sfm.shape[0]

sfo['해상특보']=''
sfo['육상특보']=''
sfo['특보점수']=''

sfm1 = sfm[["생산일","권역","지역","최대파고","평균수온","기온점수","풍속점수","해상특보","육상특보","특보점수","예보지수"]]
sfo1 = sfo[["생산일","권역","지역","최대파고","평균수온","기온점수","풍속점수","해상특보","육상특보","특보점수","예보지수"]]

compare = sfm1['예보지수'] == sfo1['예보지수']
csfm = sfm1[~compare]
csfo = sfo1[~compare]

csfm_c = csfm.copy()

csfm_c = csfm_c.sort_values(by=['권역','지역'], ascending=[True, True])
csfo = csfo.sort_values(by=['권역','지역'], ascending=[True, True])

csfm_c.rename(columns={'최대파고':'최대파고m'},inplace=True)
csfo.rename(columns={'최대파고':'최대파고o'},inplace=True)
csfm_c.rename(columns={'평균수온':'평균수온m'},inplace=True)
csfo.rename(columns={'평균수온':'평균수온o'},inplace=True)
csfm_c.rename(columns={'기온점수':'기온점수m'},inplace=True)
csfo.rename(columns={'기온점수':'기온점수o'},inplace=True)
csfm_c.rename(columns={'풍속점수':'풍속점수m'},inplace=True)
csfo.rename(columns={'풍속점수':'풍속점수o'},inplace=True)
csfm_c.rename(columns={'예보지수':'예보지수m'},inplace=True)
csfo.rename(columns={'예보지수':'예보지수o'},inplace=True)

sf_result = pd.concat([csfm_c,csfo],axis=1)

# 중복된 열을 제거하여 유일한 값을 가지도록 만듦
sf_result = sf_result.loc[:, ~sf_result.columns.duplicated(keep='first')]

# 컬럼 순서 변경
sf_result = sf_result[['생산일', '권역', '지역', '최대파고m','최대파고o','평균수온m','평균수온o','기온점수m','기온점수o','풍속점수m','풍속점수o','해상특보','육상특보','특보점수','예보지수m','예보지수o']]
sf_result = sf_result.reset_index(drop=True)
sf_result.index = sf_result.index + 1

# 셀 색칠 함수
def highlight_diff(x, color):
    style = 'background-color: {}'.format(color)
    if x[0] != x[1]:
        return [style, style]
    else:
        return ['', '']

def highlight_special(row):
    if row.name == '해상특보':
        return ['background-color: orange' if x != '-' else '' for x in row]
    else:
        return [''] * len(row)

# 열 비교하여 값이 다른 경우 해당 셀 색칠
sf_html = sf_result.style.apply(highlight_diff, color='yellow', axis=1, subset=['최대파고m', '최대파고o']) \
              .apply(highlight_diff, color='blue', axis=1, subset=['평균수온m', '평균수온o']) \
              .apply(highlight_diff, color='red', axis=1, subset=['기온점수m', '기온점수o']) \
              .apply(highlight_diff, color='green', axis=1, subset=['풍속점수m', '풍속점수o']) \
              .apply(lambda x: highlight_special(x), axis=0) \
              .set_properties(**{'border': '1px solid black'})


# 스타일이 적용된 데이터프레임을 HTML 파일로 저장
with open('바다낚시.html', 'w') as f:
    f.write(sf_html.to_html())

# 스타일이 적용된 데이터프레임을 xlsx 파일로 저장
sf_html.to_excel('바다낚시.xlsx', index=True)

#각 권역의 갯수, 각 지역의 갯수, 각 변경요인 갯수
sf_loc = sf_result['권역'].value_counts().sort_index().to_frame(name='횟수').reset_index().rename(columns={'index': '권역'})
sf_locp = sf_result.groupby(['권역', '지역'])['지역'].count().reset_index(name='횟수')

#각 권역의 각각의 변경요인 갯수
#각 지역의 각각의 변경요인 갯수
def count_changes_SF(df, groupby_col, warn_col='해상특보'):
    count = df.groupby(groupby_col).apply(lambda x: pd.Series({'최대파고count': (x['최대파고m'] != x['최대파고o']).sum(),
                                                                  '평균수온count': (x['평균수온m'] != x['평균수온o']).sum(),
                                                                  '기온점수count': (x['기온점수m'] != x['기온점수o']).sum(),
                                                                  '풍속점수count': (x['풍속점수m'] != x['풍속점수o']).sum()})).reset_index()
    warn = df[df[warn_col] != '-'].groupby(groupby_col + [warn_col]).size().reset_index(name=warn_col+'count')
    pivot = warn.pivot_table(index=groupby_col, columns=warn_col, values=warn_col+'count', fill_value=0).reset_index()
    count = count.merge(pivot, on=groupby_col, how='left').fillna(0)
    return count

count_sf1 = count_changes_SF(sf_result, ['권역'])
count_sf2 = count_changes_SF(sf_result, ['권역', '지역'])

# WW2와 WW3열이 모두 존재하는 경우에만 WW2와 WW3열을 합쳐서 WW열로 만듦
# TY2와 TY3열이 모두 존재하는 경우에만 TY2와 TY3열을 합쳐서 TY열로 만듦
def combine_columns(df, col1, col2, new_col):
    if col1 in df.columns and col2 in df.columns:
        df[new_col] = df[col1] + df[col2]
        df.drop([col1, col2], axis=1, inplace=True)
    elif col1 in df.columns:
        df[new_col] = df[col1]
        df.drop([col1], axis=1, inplace=True)
    elif col2 in df.columns:
        df[new_col] = df[col2]
        df.drop([col2], axis=1, inplace=True)
    else:
        df[new_col] = 0
    return df

count_sf1 = combine_columns(count_sf1, 'WW2', 'WW3', 'WW')
count_sf2 = combine_columns(count_sf2, 'WW2', 'WW3', 'WW')
count_sf1 = combine_columns(count_sf1, 'TY2', 'TY3', 'TY')
count_sf2 = combine_columns(count_sf2, 'TY2', 'TY3', 'TY')

count_sf1 = pd.merge(count_sf1, sf_loc, on='권역')
count_sf2 = pd.merge(count_sf2, sf_locp, on='지역')

sf_row_sum = count_sf1["횟수"].sum()

print()
print('SF 총통계')
sf_sum_all = count_sf1.sum()
sf_sum_all = pd.DataFrame(sf_sum_all, columns=['변경'])
sf_sum_all = sf_sum_all.drop('권역', axis=0)
sf_sum_all = sf_sum_all.rename(index={'횟수': '총예보지수변경'})
print(sf_sum_all)
sf_sum_all.to_csv('바다낚시_요약.csv', encoding='euc-kr', index=True)

def calculate_percentages(df, row_sum):
    df['최대파고%'] = round(df['최대파고count'] / row_sum * 100, 1)
    df['평균수온%'] = round(df['평균수온count'] / row_sum * 100, 1)
    df['기온%'] = round(df['기온점수count'] / row_sum * 100, 1)
    df['풍속%'] = round(df['풍속점수count'] / row_sum * 100, 1)
    df['WW%'] = round(df['WW'] / row_sum * 100, 1)
    df['TY%'] = round(df['TY'] / row_sum * 100, 1)
    df['횟수%'] = round(df['횟수'] / row_sum * 100, 1)
    return df

count_sf1 = calculate_percentages(count_sf1, sf_row_sum)
count_sf2 = calculate_percentages(count_sf2, sf_row_sum)

count_sf2 = count_sf2.drop('권역_y', axis=1)
count_sf2 = count_sf2.rename(columns={'권역_x':'권역'})

SF_new_order = ['권역', '횟수','횟수%', '최대파고count', '최대파고%','평균수온count','평균수온%','WW','WW%','TY','TY%']
count_sf1 = count_sf1.reindex(columns=SF_new_order)
SF_new_order2 = ['권역', '지역','횟수','횟수%', '최대파고count', '최대파고%','평균수온count','평균수온%','WW','WW%','TY','TY%']
count_sf2 = count_sf2.reindex(columns=SF_new_order2)

# 구분열 안의 요소들을 서해, 남해, 동해 순으로 배열
SF_new_order3 = ['황해중부', '황해남부', '제주도','남해서부','남해동부','동해남부','동해중부']
count_sf1['권역'] = pd.Categorical(count_sf1['권역'], categories=SF_new_order3, ordered=True)
count_sf1 = count_sf1.sort_values('권역').reset_index(drop=True)
count_sf2['권역'] = pd.Categorical(count_sf2['권역'], categories=SF_new_order3, ordered=True)
count_sf2 = count_sf2.sort_values('권역').reset_index(drop=True)

count_sf1.to_csv('바다낚시_권역_사유.csv', encoding='euc-kr', index=False)
count_sf2.to_csv('바다낚시_지역_사유.csv', encoding='euc-kr', index=False)

##################################################################
##################################################################
##################################################################
##################################################################

#뱃멀미
file_path5 = r'C:\2023\python test\지역별통계내기\2211\skmod.xlsx'
file_path6 = r'C:\2023\python test\지역별통계내기\2211\skorg.xlsx'
skm = pd.read_excel(file_path5)
sko = pd.read_excel(file_path6)

# 행의 갯수
SK_row = skm.shape[0]

#sko['해상특보']=''
sko['특보']=''
sko['특보점수']=''

skm1 = skm[["생산일","항로명","선박명","최대파고","풍속점수","특보","특보점수","예보지수"]]
sko1 = sko[["생산일","항로명","선박명","최대파고","풍속점수","특보","특보점수","예보지수"]]

compare = skm1['예보지수'] == sko1['예보지수']
cskm = skm1[~compare]
csko = sko1[~compare]

cskm_c = cskm.copy()

cskm_c = cskm_c.sort_values(by=['항로명','선박명'], ascending=[True, True])
csko = csko.sort_values(by=['항로명','선박명'], ascending=[True, True])

cskm_c.rename(columns={'최대파고':'최대파고m'},inplace=True)
csko.rename(columns={'최대파고':'최대파고o'},inplace=True)
cskm_c.rename(columns={'풍속점수':'풍속점수m'},inplace=True)
csko.rename(columns={'풍속점수':'풍속점수o'},inplace=True)
cskm_c.rename(columns={'예보지수':'예보지수m'},inplace=True)
csko.rename(columns={'예보지수':'예보지수o'},inplace=True)

sk_result = pd.concat([cskm_c,csko],axis=1)

# 중복된 열을 제거하여 유일한 값을 가지도록 만듦
sk_result = sk_result.loc[:, ~sk_result.columns.duplicated(keep='first')]

# 컬럼 순서 변경
sk_result = sk_result[['생산일', '항로명', '선박명', '최대파고m','최대파고o','풍속점수m','풍속점수o','특보','특보점수','예보지수m','예보지수o']]
sk_result = sk_result.reset_index(drop=True)
sk_result.index = sk_result.index + 1

# 셀 색칠 함수
def highlight_diff(x, color):
    style = 'background-color: {}'.format(color)
    if x[0] != x[1]:
        return [style, style]
    else:
        return ['', '']

def highlight_special(row):
    if row.name == '특보':
        return ['background-color: orange' if x != '-' else '' for x in row]
    else:
        return [''] * len(row)

# 열 비교하여 값이 다른 경우 해당 셀 색칠
sk_html = sk_result.style.apply(highlight_diff, color='yellow', axis=1, subset=['최대파고m', '최대파고o']) \
              .apply(highlight_diff, color='blue', axis=1, subset=['풍속점수m', '풍속점수o']) \
              .apply(lambda x: highlight_special(x), axis=0) \
              .set_properties(**{'border': '1px solid black'})

# 스타일이 적용된 데이터프레임을 HTML 파일로 저장
with open('뱃멀미.html', 'w') as f:
    f.write(sk_html.to_html())

# 스타일이 적용된 데이터프레임을 xlsx 파일로 저장
sk_html.to_excel('뱃멀미.xlsx', index=True)

#각 권역의 갯수, 각 지역의 갯수, 각 변경요인 갯수
sk_loc = sk_result['항로명'].value_counts().sort_index().to_frame(name='횟수').reset_index().rename(columns={'index': '항로명'})
sk_locp = sk_result.groupby(['항로명', '선박명'])['선박명'].count().reset_index(name='횟수')

#각 권역의 각각의 변경요인 갯수
#각 지역의 각각의 변경요인 갯수
def count_changes_SK(df, groupby_col, warn_col='특보'):
    count = df.groupby(groupby_col).apply(lambda x: pd.Series({'최대파고count': (x['최대파고m'] != x['최대파고o']).sum(),
                                                                  '풍속점수count': (x['풍속점수m'] != x['풍속점수o']).sum()})).reset_index()
    warn = df[df[warn_col] != '-'].groupby(groupby_col + [warn_col]).size().reset_index(name=warn_col+'count')
    pivot = warn.pivot_table(index=groupby_col, columns=warn_col, values=warn_col+'count', fill_value=0).reset_index()
    count = count.merge(pivot, on=groupby_col, how='left').fillna(0)
    return count

count_sk1 = count_changes_SK(sk_result, ['항로명'])
count_sk2 = count_changes_SK(sk_result, ['항로명', '선박명'])

# WW2와 WW3열이 모두 존재하는 경우에만 WW2와 WW3열을 합쳐서 WW열로 만듦
# TY2와 TY3열이 모두 존재하는 경우에만 TY2와 TY3열을 합쳐서 TY열로 만듦
def combine_columns(df, col1, col2, new_col):
    if col1 in df.columns and col2 in df.columns:
        df[new_col] = df[col1] + df[col2]
        df.drop([col1, col2], axis=1, inplace=True)
    elif col1 in df.columns:
        df[new_col] = df[col1]
        df.drop([col1], axis=1, inplace=True)
    elif col2 in df.columns:
        df[new_col] = df[col2]
        df.drop([col2], axis=1, inplace=True)
    else:
        df[new_col] = 0
    return df

count_sk1 = combine_columns(count_sk1, 'WW2', 'WW3', 'WW')
count_sk2 = combine_columns(count_sk2, 'WW2', 'WW3', 'WW')
count_sk1 = combine_columns(count_sk1, 'TY2', 'TY3', 'TY')
count_sk2 = combine_columns(count_sk2, 'TY2', 'TY3', 'TY')

count_sk1 = pd.merge(count_sk1, sk_loc, on='항로명')
count_sk2 = pd.merge(count_sk2, sk_locp, on='선박명')

sk_row_sum = count_sk1["횟수"].sum()

print()
print('SK 총통계')
sk_sum_all = count_sk1.sum()
sk_sum_all = pd.DataFrame(sk_sum_all, columns=['변경'])
sk_sum_all = sk_sum_all.drop('항로명', axis=0)
sk_sum_all = sk_sum_all.rename(index={'횟수': '총예보지수변경'})
print(sk_sum_all)
sk_sum_all.to_csv('뱃멀미_요약.csv', encoding='euc-kr', index=True)

def calculate_percentages(df, row_sum):
    df['최대파고%'] = round(df['최대파고count'] / row_sum * 100, 1)
    df['풍속%'] = round(df['풍속점수count'] / row_sum * 100, 1)
    df['WW%'] = round(df['WW'] / row_sum * 100, 1)
    df['TY%'] = round(df['TY'] / row_sum * 100, 1)
    df['횟수%'] = round(df['횟수'] / row_sum * 100, 1)
    return df

count_sk1 = calculate_percentages(count_sk1, sk_row_sum)
count_sk2 = calculate_percentages(count_sk2, sk_row_sum)

count_sk2 = count_sk2.drop('항로명_y', axis=1)
count_sk2 = count_sk2.rename(columns={'항로명_x':'항로명'})

SK_new_order = ['항로명', '횟수','횟수%', '최대파고count', '최대파고%','WW','WW%','TY','TY%']
count_sk1 = count_sk1.reindex(columns=SK_new_order)
SK_new_order2 = ['항로명', '선박명','횟수','횟수%', '최대파고count', '최대파고%','WW','WW%','TY','TY%']
count_sk2 = count_sk2.reindex(columns=SK_new_order2)

count_sk1.to_csv('뱃멀미_항로_사유.csv', encoding='euc-kr', index=False)
count_sk2.to_csv('뱃멀미_선박_사유.csv', encoding='euc-kr', index=False)

##################################################################
##################################################################
##################################################################
##################################################################

# 서핑
file_path7 = r'C:\2023\python test\지역별통계내기\2211\srmod.xlsx'
file_path8 = r'C:\2023\python test\지역별통계내기\2211\srorg.xlsx'
srm = pd.read_excel(file_path7)
sro = pd.read_excel(file_path8)

# 행의 갯수
SR_row = srm.shape[0]

sro['해상특보']=''
sro['육상특보']=''
sro['특보점수']=''

srm1 = srm[["생산일","구분","지역","유의파고","풍속점수","파향점수","파주기점수","수온점수","해상특보","육상특보","특보점수","예보지수"]]
sro1 = sro[["생산일","구분","지역","유의파고","풍속점수","파향점수","파주기점수","수온점수","해상특보","육상특보","특보점수","예보지수"]]

compare = srm1['예보지수'] == sro1['예보지수']
csrm = srm1[~compare]
csro = sro1[~compare]

csrm_c = csrm.copy()

csrm_c = csrm_c.sort_values(by=['구분','지역'], ascending=[True, True])
csro = csro.sort_values(by=['구분','지역'], ascending=[True, True])

csrm_c.rename(columns={'유의파고':'유의파고m'},inplace=True)
csro.rename(columns={'유의파고':'유의파고o'},inplace=True)
csrm_c.rename(columns={'풍속점수':'풍속점수m'},inplace=True)
csro.rename(columns={'풍속점수':'풍속점수o'},inplace=True)
csrm_c.rename(columns={'파향점수':'파향점수m'},inplace=True)
csro.rename(columns={'파향점수':'파향점수o'},inplace=True)
csrm_c.rename(columns={'파주기점수':'파주기점수m'},inplace=True)
csro.rename(columns={'파주기점수':'파주기점수o'},inplace=True)
csrm_c.rename(columns={'수온점수':'수온점수m'},inplace=True)
csro.rename(columns={'수온점수':'수온점수o'},inplace=True)
csrm_c.rename(columns={'예보지수':'예보지수m'},inplace=True)
csro.rename(columns={'예보지수':'예보지수o'},inplace=True)

sr_result = pd.concat([csrm_c,csro],axis=1)

# 중복된 열을 제거하여 유일한 값을 가지도록 만듦
sr_result = sr_result.loc[:, ~sr_result.columns.duplicated(keep='first')]

# 컬럼 순서 변경
sr_result = sr_result[['생산일', '구분', '지역', '유의파고m','유의파고o','풍속점수m','풍속점수o','파향점수m','파향점수o','파주기점수m','파주기점수o','수온점수m','수온점수o','해상특보','육상특보','특보점수','예보지수m','예보지수o']]

sr_result = sr_result.reset_index(drop=True)
sr_result.index = sr_result.index + 1

# 셀 색칠 함수
def highlight_diff(x, color):
    style = 'background-color: {}'.format(color)
    if x[0] != x[1]:
        return [style, style]
    else:
        return ['', '']
def highlight_special(row):
    if row.name == '해상특보':
        return ['background-color: orange' if x != '-' else '' for x in row]
    else:
        return [''] * len(row)    

# 열 비교하여 값이 다른 경우 해당 셀 색칠
sr_html = sr_result.style.apply(highlight_diff, color='yellow', axis=1, subset=['유의파고m', '유의파고o']) \
              .apply(highlight_diff, color='blue', axis=1, subset=['풍속점수m', '풍속점수o']) \
              .apply(highlight_diff, color='red', axis=1, subset=['파향점수m', '파향점수o']) \
              .apply(highlight_diff, color='green', axis=1, subset=['파주기점수m', '파주기점수o']) \
              .apply(highlight_diff, color='pink', axis=1, subset=['수온점수m', '수온점수o']) \
              .apply(lambda x: highlight_special(x), axis=0) \
              .set_properties(**{'border': '1px solid black'})


# 스타일이 적용된 데이터프레임을 HTML 파일로 저장
with open('서핑.html', 'w') as f:
    f.write(sr_html.to_html())

# 스타일이 적용된 데이터프레임을 xlsx 파일로 저장
sr_html.to_excel('서핑.xlsx', index=True)

#각 권역의 갯수, 각 지역의 갯수, 각 변경요인 갯수
sr_loc = sr_result['구분'].value_counts().sort_index().to_frame(name='횟수').reset_index().rename(columns={'index': '구분'})
sr_locp = sr_result.groupby(['구분', '지역'])['지역'].count().reset_index(name='횟수')

#각 권역의 각각의 변경요인 갯수
#각 지역의 각각의 변경요인 갯수
def count_changes_SR(df, groupby_col, warn_col='해상특보'):
    count = df.groupby(groupby_col).apply(lambda x: pd.Series({'유의파고count': (x['유의파고m'] != x['유의파고o']).sum(),
                                                                  '풍속점수count': (x['풍속점수m'] != x['풍속점수o']).sum(),
                                                                  '파향점수count': (x['파향점수m'] != x['파향점수o']).sum(),
                                                                  '파주기점수count': (x['파주기점수m'] != x['파주기점수o']).sum(),
                                                                  '수온점수count': (x['수온점수m'] != x['수온점수o']).sum()})).reset_index()
    warn = df[df[warn_col] != '-'].groupby(groupby_col + [warn_col]).size().reset_index(name=warn_col+'count')
    pivot = warn.pivot_table(index=groupby_col, columns=warn_col, values=warn_col+'count', fill_value=0).reset_index()
    count = count.merge(pivot, on=groupby_col, how='left').fillna(0)
    return count

count_sr1 = count_changes_SR(sr_result, ['구분'])
count_sr2 = count_changes_SR(sr_result, ['구분', '지역'])

# WW2와 WW3열이 모두 존재하는 경우에만 WW2와 WW3열을 합쳐서 WW열로 만듦
# TY2와 TY3열이 모두 존재하는 경우에만 TY2와 TY3열을 합쳐서 TY열로 만듦

def combine_columns(df, col1, col2, new_col):
    if col1 in df.columns and col2 in df.columns:
        df[new_col] = df[col1] + df[col2]
        df.drop([col1, col2], axis=1, inplace=True)
    elif col1 in df.columns:
        df[new_col] = df[col1]
        df.drop([col1], axis=1, inplace=True)
    elif col2 in df.columns:
        df[new_col] = df[col2]
        df.drop([col2], axis=1, inplace=True)
    else:
        df[new_col] = 0
    return df

count_sr1 = combine_columns(count_sr1, 'WW2', 'WW3', 'WW')
count_sr2 = combine_columns(count_sr2, 'WW2', 'WW3', 'WW')
count_sr1 = combine_columns(count_sr1, 'TY2', 'TY3', 'TY')
count_sr2 = combine_columns(count_sr2, 'TY2', 'TY3', 'TY')

count_sr1 = pd.merge(count_sr1, sr_loc, on='구분')
count_sr2 = pd.merge(count_sr2, sr_locp, on='지역')

sr_row_sum = count_sr1["횟수"].sum()

print()
print('SR 총통계')
sr_sum_all = count_sr1.sum()
sr_sum_all = pd.DataFrame(sr_sum_all, columns=['변경'])
sr_sum_all = sr_sum_all.drop('구분', axis=0)
sr_sum_all = sr_sum_all.rename(index={'횟수': '총예보지수변경'})
print(sr_sum_all)
sr_sum_all.to_csv('서핑_요약.csv', encoding='euc-kr', index=True)

def calculate_percentages(df, row_sum):
    df['유의파고%'] = round(df['유의파고count'] / row_sum * 100, 1)
    df['풍속%'] = round(df['풍속점수count'] / row_sum * 100, 1)
    df['파향%'] = round(df['파향점수count'] / row_sum * 100, 1)
    df['파주기%'] = round(df['파주기점수count'] / row_sum * 100, 1)
    df['수온%'] = round(df['수온점수count'] / row_sum * 100, 1)
    df['WW%'] = round(df['WW'] / row_sum * 100, 1)
    df['TY%'] = round(df['TY'] / row_sum * 100, 1)
    df['횟수%'] = round(df['횟수'] / row_sum * 100, 1)
    return df

count_sr1 = calculate_percentages(count_sr1, sr_row_sum)
count_sr2 = calculate_percentages(count_sr2, sr_row_sum)

count_sr2 = count_sr2.drop('구분_y', axis=1)
count_sr2 = count_sr2.rename(columns={'구분_x':'구분'})

SR_new_order = ['구분', '횟수','횟수%', '유의파고count', '유의파고%','파향점수count','파향%','파주기점수count','파주기%','수온점수count','수온%','WW','WW%','TY','TY%']
count_sr1 = count_sr1.reindex(columns=SR_new_order)
SR_new_order2 = ['구분', '지역','횟수','횟수%', '유의파고count', '유의파고%','파향점수count','파향%','파주기점수count','파주기%','수온점수count','수온%','WW','WW%','TY','TY%']
count_sr2 = count_sr2.reindex(columns=SR_new_order2)

# 구분열 안의 요소들을 서해, 남해, 동해 순으로 배열
SR_new_order3 = ['태안', '부산', '동해','양양']
count_sr1['구분'] = pd.Categorical(count_sr1['구분'], categories=SR_new_order3, ordered=True)
count_sr1 = count_sr1.sort_values('구분').reset_index(drop=True)
count_sr2['구분'] = pd.Categorical(count_sr2['구분'], categories=SR_new_order3, ordered=True)
count_sr2 = count_sr2.sort_values('구분').reset_index(drop=True)

#print(count_sr2)
count_sr1.to_csv('서핑_구분_사유.csv', encoding='euc-kr', index=False)
count_sr2.to_csv('서핑_지역_사유.csv', encoding='euc-kr', index=False)

