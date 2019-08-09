#%% 모듈 장착

# 기본 모듈
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family = 'Gulim')

#%% 고령자 비율 분석

# 데이터불러오기
gas_household_sort = pd.read_csv('C:/Users/a/Desktop/gas_household_sort.csv')

old = pd.read_excel('C:/Users/a/Desktop/공공데이터/데이터/2018_동별_고령자수.xls',
                    skiprows = [0, 1])

old = old.loc[(old['자치구'] != '합계') &\
              (old['동'] != '합계') &\
              (old['동'] != '소계')]

set(old['동']) - set(gas_household_sort['행정동']) # 염리동 데이터가 가스사용비율 데이터에 없다.

old = old.loc[old['동'] != '염리동']  #염리동 데이터 제거

# old 변수 이름 수정
old = old.rename(columns = {'동' : '행정동',
                            '계' : '전체인구수',
                            '계.1' : '고령자인구수'})

# 필요한 변수만 추출
old = old[['자치구', '행정동', '전체인구수', '고령자인구수']]

# 고령자 비율 변수 추가
old['고령자비율'] = old['고령자인구수'] / old['전체인구수']

seoul = pd.merge(gas_household_sort, old)

seoul.to_csv('seoul.csv',
             index = False,
             encoding = 'cp949')


plt.hist(seoul['고령자비율'])
plt.show()

plt.figure(figsize = (18, 18))
plt.barh(y = seoul['행정동'],
         width= seoul['고령자비율'])
plt.show()

seoul[['가스사용비율', '고령자비율']].corr() # -0.132801 상관성이 별로 없다...

#%% 연령대 비율 분석

#%% 데이터 불러오기
age = pd.read_excel('C:/Users/a/Desktop/공공데이터/데이터/2018_동별_연령대별인구수.xls',
                    na_values = ['-'])

age = age.fillna(0) # 노년인구에서만 보이는 결측값은 0으로 간주하였다.

#%% 데이터 전처리
# 필요없는 데이터 제거(염리동 데이터도 지워줬다.)
age = age.loc[(age['자치구'] != '합계') &\
              (age['동'] != '합계') &\
              (age['동'] != '소계') &\
              (age['구분'] != '남자') &\
              (age['구분'] != '여자') &\
              (age['동'] != '염리동')]

# 연령대 변수 생성(미성년(0~19), 청년(20~34), 장년(35~49), 중년(50~65), 노년(65~))
age['미성년'] = 0
for i in range(4):
    age['미성년'] += age.iloc[:, 5 + i]

age['청년'] = 0
for i in range(3):
    age['청년'] += age.iloc[:, 9 + i]

age['장년'] = 0
for i in range(3):
    age['장년'] += age.iloc[:, 12 + i]

age['중년'] = 0
for i in range(3):
    age['중년'] += age.iloc[:, 15 + i]

age['노년'] = 0
for i in range(8):
    age['노년'] = age['노년'] + age.iloc[:, 18 + i]

age['미성년비율'] = age['미성년'] / age['계']
age['청년비율'] = age['청년'] / age['계']
age['장년비율'] = age['장년'] / age['계']
age['중년비율'] = age['중년'] / age['계']
age['노년비율'] = age['노년'] / age['계']

# 분석에 필요한 변수만 추출
age = age[['자치구', '동', '미성년비율', '청년비율', '장년비율', '중년비율', '노년비율']]

# seoul변수에서 현재분석에 필요없는 지도코드와 주소 변수 제거
del seoul['지도코드'], seoul['주소']

# 변수이름 수정
age = age.rename(columns = {'동' : '행정동'})
seoul = pd.merge(seoul, age, on = ['자치구', '행정동'])

del seoul['고령자인구수'], seoul['고령자비율']
seoul.to_csv('seoul.csv', index = False)

#%% 데이터 분석

corr_df = seoul.corr()
    # 결과 가스사용비율 변수와 각 연령대의 상관계수는 모두 절댓값 0.3 미만으로
    # 가스사용비율이 적은 지역과 연령대와는 별로 상관이 없는것으로 보였다.


#%% 취약지역만 따로 뽑아서 분석
seoul = pd.read_csv('C:/Users/a/Desktop/seoul.csv')
seoul_low = seoul.head(28)
seoul_high = seoul.tail(25)
seoul_outlier = pd.concat([seoul_low, seoul_high])
corr_df = seoul.corr()

plt.scatter(seoul_outlier['1인세대비율'], seoul_outlier['2인세대비율'])
plt.xlabel('1인세대비율')
plt.ylabel('2인세대비율')
plt.show()
seoul.mean()
