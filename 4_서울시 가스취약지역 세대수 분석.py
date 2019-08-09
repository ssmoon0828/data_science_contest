#%% 모듈장착

# 기본 모듈
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family = 'Gulim')

#%% 데이터 불러오기
seoul = pd.read_csv('C:/Users/a/Desktop/seoul.csv')
household = pd.read_excel('C:/Users/a/Desktop/공공데이터/데이터/2018_동별_세대수.xls',
                          na_values = ['-'])

#%% 데이터 전처리
household = household.fillna(0)
household = household.loc[(household['자치구'] != '합계') &\
                          (household['행정동'] != '합계') &\
                          (household['행정동'] != '소계') &\
                          (household['행정동'] != '염리동')]
household = household.groupby(['자치구', '행정동']).mean()
household = household.reset_index()
del household['기간']

for i in range(10):
    household[str(i + 1) + '인세대비율'] = 0
    household[str(i + 1) + '인세대비율'] = household.iloc[:, 3 + i] / household['전체세대수']

var_name = list(household.columns)
    
for i in range(10):
    del household[var_name[3 + i]]

seoul = pd.merge(seoul, household, on = ['자치구', '행정동'])
del seoul['전체세대수_y']
seoul = seoul.rename(columns = {'전체세대수_x' : '전체세대수'})

# 변수 정리 : 앞으로는 seoul변수를 이용한다.
seoul = seoul[['자치구', '행정동', 'lat', 'lng', '가정용가스사용량', '가스사용비율',\
               '전체세대수', '1인세대비율', '2인세대비율', '3인세대비율', '4인세대비율',\
                '5인세대비율', '6인세대비율', '7인세대비율', '8인세대비율', '9인세대비율', '10인세대비율',\
                '전체인구수', '미성년비율', '청년비율', '장년비율', '중년비율', '노년비율']]

seoul.to_csv('seoul.csv', index = False)
#%% 데이터분석
corr_df = seoul.corr()
        # 가스사용비율 변수와 세대수 간의 상관관계도 최고가 1인세대 0.25로 별로 상관이 없었다.

plt.scatter(seoul['가스사용비율'], seoul['1인세대비율'])
