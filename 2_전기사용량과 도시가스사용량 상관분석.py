#%% 모듈 장착

# 기본모듈
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family = 'Gulim')

#%% 데이터 불러오기
elec = pd.read_excel('C:/Users/a/Desktop/공공데이터/데이터/2018_구별_전기사용량.xls',
                     skiprows = [0])

gas = pd.read_excel('C:/Users/a/Desktop/공공데이터/데이터/2018_구별_도시가스사용량.xls')

household = pd.read_excel('C:/Users/a/Desktop/공공데이터/데이터/2018_동별_세대수.xls')
#%% 데이터 전처리
elec = elec[['자치구', '가정용']]
elec = elec.loc[elec['자치구'] != '합계']
elec.rename(columns = {'가정용' : 'elec'}, inplace = True)

gas = gas[['자치구', '가정용']]
gas = gas.loc[gas['자치구'] != '서울시']
gas.rename(columns = {'가정용' : 'gas'}, inplace = True)

set(elec['자치구']) == set(gas['자치구']) # True

energy = pd.merge(elec, gas)

household = household.loc[(household['자치구'] != '합계') &\
                          (household['행정동'] != '합계') &\
                          (household['행정동'] != '소계')]

household = household.groupby('자치구').mean()['전체세대수']
household = household.reset_index()

energy = pd.merge(energy, household)
energy['elec_ratio'] = energy['elec'] / energy['전체세대수']
energy['gas_ratio'] = energy['gas'] / energy['전체세대수']

#%% 확인
energy_scatter = plt.figure(figsize = (12, 12))
plt.scatter(energy['elec'], energy['gas'])
plt.title('구별 전기사용량과 가스사용량의 상관관계')
plt.xlabel('전기사용량')
plt.ylabel('가스사용량')
plt.grid()
plt.show()
energy_scatter.savefig('energy_scatter.png', dpi = 200)

energy_ratio_scatter = plt.figure(figsize = (12, 12))
plt.scatter(energy['elec_ratio'], energy['gas_ratio'])
plt.title('세대별 전기사용량과 가스사용량의 상관관계')
plt.xlabel('전기사용량')
plt.ylabel('가스사용량')
plt.grid()
for i in range(len(energy)):
    plt.text(x = energy['elec_ratio'][i] - 1,
             y = energy['gas_ratio'][i] + 0.1,
             s = energy['자치구'][i])
plt.show()
energy_ratio_scatter.savefig('energy_ratio_scatter.png', dpi = 200)