#%% 모듈 장착

# 기본 모듈
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family = 'Gulim')

#%% 데이터 불러오기

gas_household_sort = pd.read_csv('C:/Users/a/Desktop/gas_household_sort.csv')

old = pd.read_excel('C:/Users/a/Desktop/공공데이터/데이터/2018_동별_고령자수.xls',
                    skiprows = [0, 1])

old = old.loc[(old['자치구'] != '합계') &\
              (old['동'] != '합계') &\
              (old['동'] != '소계')]

set(old['동']) - set(gas_household_sort['행정동']) # 염리동 데이터가 가스사용비율 데이터에 없다.

old = old.loc[old['동'] != '염리동']  #염리동 데이터 제거

old = old.rename(columns = {'동' : '행정동',
                            '계' : '전체인구수',
                            '계.1' : '고령자인구수'})

old = old[['자치구', '행정동', '전체인구수', '고령자인구수']]

seoul = pd.merge(gas_household_sort, old)

seoul.to_csv('seoul.csv',
             index = False,
             encoding = 'cp949')

plt.hist(seoul['고령자비율'])
plt.show()