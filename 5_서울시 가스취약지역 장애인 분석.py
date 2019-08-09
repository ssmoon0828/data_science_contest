#%% 모듈 장착

# 기본모듈
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family = 'Gulim')

#%% 데이터 불러오기
seoul = pd.read_csv('seoul.csv')
disability = pd.read_excel('C:/Users/a/Desktop/공공데이터/데이터/2018년_동별_급별_장애인수.xls',
                           skiprows = [0, 1],
                           na_values = ['-'])

#%% 데이터 전처리

disability = disability.fillna(0)

# 변수 이름 변경
disability = disability.rename(columns = {'동' : '행정동',
                                          '계' : '전체_장애인수',
                                          '계.1' : '1급_장애인수',
                                          '계.2' : '2급_장애인수',
                                          '계.3' : '3급_장애인수',
                                          '계.4' : '4급_장애인수',
                                          '계.5' : '5급_장애인수',
                                          '계.6' : '6급_장애인수'})


set(disability['행정동']) - set(seoul['행정동'])

# 필요없는 행 제거
disability = disability.loc[(disability['자치구'] != '합계') &\
                            (disability['행정동'] != '합계') &\
                            (disability['행정동'] != '소계') &\
                            (disability['행정동'] != '염리동') &\
                            (disability['행정동'] != '기타')]

# 필요한 변수 추출
disability = disability[['자치구', '행정동', '전체_장애인수', '1급_장애인수', '2급_장애인수',
                         '3급_장애인수', '4급_장애인수', '5급_장애인수', '6급_장애인수']]


#%% 데이터 결합
seoul = pd.merge(seoul, disability, on = ['자치구', '행정동'])

seoul['장애인_비율'] = seoul['전체_장애인수'] / seoul['전체인구수']

for i in range(6):
    seoul[str(i + 1) + '급_장애인비율'] = seoul.iloc[:, 24 + i] / seoul['전체인구수']

corr_df = seoul.corr() # 상관계수가 낮게나와 가스취약지역과 장애인 인구비율과는 상관이 없는것으로 결정 짓는다.
