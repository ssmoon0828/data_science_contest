#%% 모듈 장착

# 기본 모듈
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family = 'Gulim')

# 통계모듈
import scipy as sp
import scipy.stats

# 지도 시각화 모듈
import googlemaps
import folium

#%% 데이터불러오기

# 동별 세대수 데이터
raw_household = pd.read_excel('C:/Users/ssmoo/Desktop/공공데이터/데이터/2018_동별_세대수.xls',
                              na_values = ['-'])

# 동별 가스 사용 데이터
raw_gas = pd.read_excel('C:/Users/ssmoo/Desktop/공공데이터/데이터/2018_동별_도시가스사용량.xls',
                        skiprows = [0, 1],
                        na_values = ['-'])

# 동별 연령대 데이터
raw_age = pd.read_excel('C:/Users/ssmoo/Desktop/공공데이터/데이터/2018_동별_연령대별인구수.xls',
                        na_values = ['-'])

# 동별 장애인수 데이터
raw_disability = pd.read_excel('C:/Users/ssmoo/Desktop/공공데이터/데이터/2018년_동별_급별_장애인수.xls',
                               skiprows = [0, 1],
                               na_values = ['-'])

# 동별 기초생활수급자 데이터
raw_baselife = pd.read_excel('C:/Users/a/Desktop/data_science_contest/원래데이터/2018_동별_국민기초생활보장수급자.xls',
                             skiprows = [0],
                             na_values = '-')
#%% 데이터 전처리

#%%동별 세대수 데이터 전처리
household = raw_household.copy()
household = household.fillna(0)

# 필요없는 데이터 제거
household = household.loc[(household['자치구'] != '합계') &\
                          (household['행정동'] != '합계') &\
                          (household['행정동'] != '소계') &\
                          (household['행정동'] != '염리동')] # 다른 데이터에는 염리동, 둔촌1동 데이터가 없다.

# 분리되어 있는 기간들을 평균으로 통일
household = household.groupby(['자치구', '행정동']).mean()

# n인세대별 비율 추출
for i in range(9):
    household[str(i + 1) + '인세대비율'] = household.iloc[:, i + 2] / household['전체세대수']

household['10세대이상비율'] = household['10인세대 이상'] / household['전체세대수']

# 필요한 변수 추출
household = household.iloc[:, [1, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]]

# 인덱스 -> 변수 변환
household = household.reset_index()

# csv파일로 저장
household.to_csv('household.csv', index = False)

#%% 동별 가스 사용 데이터 전처리
gas = raw_gas.copy()

# 변수 이름 수정
gas = gas.rename(columns = {'동' : '행정동',
                                '소계' : '가스사용량'})

# 필요없는 데이터 제거
gas = gas.loc[(gas['자치구'] != '합계') &\
              (gas['행정동'] != '합계') &\
              (gas['행정동'] != '소계')]

# 가스사용량 / 세대수 를 이용한 가스사용비율 변수 추가
gas = pd.merge(gas, household, on = ['자치구', '행정동'])
gas['가스사용비율'] = gas['가스사용량'] / gas['전체세대수']

# 필요한 변수 추출
gas = gas[['자치구', '행정동', '가스사용량', '가스사용비율']]

# 자치구 행정동 가나다 순 배열
gas = gas.sort_values(['자치구', '행정동'])

# csv파일로 저장
gas.to_csv('gas.csv', index = False)
#%% 동별 연령대 데이터 전처리
age = raw_age.copy()
age = age.fillna(0)

# 변수 이름 수정
age = age.rename(columns = {'동' : '행정동',
                            '계' : '전체인구수'})

# 필요없는 데이터 제거
age = age.loc[(age['자치구'] != '합계') &\
              (age['행정동'] != '합계') &\
              (age['행정동'] != '소계') &\
              (age['행정동'] != '염리동') &\
              (age['구분'] == '계')]

# 연령대 새로운 범주 변수 생성
# 미성년(0~19), 청년(20~34), 장년(35~49), 중년(50~65), 노년(65~)
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

age['미성년비율'] = age['미성년'] / age['전체인구수']
age['청년비율'] = age['청년'] / age['전체인구수']
age['장년비율'] = age['장년'] / age['전체인구수']
age['중년비율'] = age['중년'] / age['전체인구수']
age['노년비율'] = age['노년'] / age['전체인구수']

# 필요한 변수 추출
age = age[['자치구', '행정동', '전체인구수', '미성년비율', '청년비율', '장년비율', '중년비율', '노년비율']]

# 자치구 행정동 가나다순 배열
age = age.sort_values(['자치구', '행정동'])

# csv파일로 저장
age.to_csv('age.csv', index = False)
#%% 동별 장애인수 데이터 전처리
disability = raw_disability.copy()
disability = disability.fillna(0)

# 변수 이름 변경
disability = disability.rename(columns = {'동' : '행정동',
                                          '계' : '전체장애인수',
                                          '계.1' : '1급장애인수',
                                          '계.2' : '2급장애인수',
                                          '계.3' : '3급장애인수',
                                          '계.4' : '4급장애인수',
                                          '계.5' : '5급장애인수',
                                          '계.6' : '6급장애인수'})

# 필요없는 행 제거
disability = disability.loc[(disability['자치구'] != '합계') &\
                            (disability['행정동'] != '합계') &\
                            (disability['행정동'] != '소계') &\
                            (disability['행정동'] != '염리동') &\
                            (disability['행정동'] != '기타')]

# 필요한 변수 추출
disability = disability[['자치구', '행정동', '전체장애인수', '1급장애인수', '2급장애인수',
                         '3급장애인수', '4급장애인수', '5급장애인수', '6급장애인수']]

# 비율 변수 생성
disability = pd.merge(disability, age, on = ['자치구', '행정동'])

disability['전체장애인비율'] = disability['전체장애인수'] / disability['전체인구수']

for i in range(6):
    disability[str(i + 1) + '급장애인비율'] = disability.iloc[:, i + 3] / disability['전체인구수']
    
# 필요한 변수 추출
disability = disability[['자치구', '행정동', '전체장애인비율', '1급장애인비율', '2급장애인비율',
                         '3급장애인비율', '4급장애인비율', '5급장애인비율', '6급장애인비율']]

# 자취구 행정동 가나다순 배열
disability = disability.sort_values(['자치구', '행정동'])

# csv파일로 저장
disability.to_csv('disability.csv', index = False)

#%% 동별 기초생활 수급자 데이터 전처리
baselife = raw_baselife.copy()

# 변수 이름 수정
baselife = baselife.rename(columns = {'동' : '행정동',
                                      '가구' : '기초생활수급가구수',
                                      '인원' : '기초생활수급인원수'})
# 필요없는 데이터 제거
baselife = baselife.loc[(baselife['자치구'] != '합계') &\
                        (baselife['자치구'] != '본청') &\
                        (baselife['행정동'] != '합계') &\
                        (baselife['행정동'] != '본청') &\
                        (baselife['행정동'] != '소계') &\
                        (baselife['행정동'] != '기타') &\
                        (baselife['행정동'] != '염리동')]

# 필요한 변수 추출
baselife = baselife[['자치구', '행정동', '기초생활수급가구수', '기초생활수급인원수']]

# 비율변수를 계산하기 위한 merge
baselife = pd.merge(baselife, household, on = ['자치구', '행정동'])
baselife = pd.merge(baselife, age, on = ['자치구', '행정동'])
baselife['기초생활수급가구비율'] = baselife['기초생활수급가구수'] / baselife['전체세대수']
baselife['기초생활수급인원비율'] = baselife['기초생활수급인원수'] / baselife['전체인구수']

# 필요한 변수 추출
baselife = baselife[['자치구', '행정동', '기초생활수급가구비율', '기초생활수급인원비율']]

# 자치구 행정동 가나다순 배열
baselife = baselife.sort_values(['자치구', '행정동'])

# csv파일로 저장
baselife.to_csv('baselife.csv', index = False)

#%% 데이터 통합

dong = pd.merge(gas, household, on = ['자치구', '행정동'])
dong = pd.merge(dong, age, on = ['자치구', '행정동'])
dong = pd.merge(dong, disability, on = ['자치구', '행정동'])
dong = pd.merge(dong, baselife, on = ['자치구', '행정동'], how = 'left') # 둔촌1동 데이터를 지우지 않기 위해 left join

# 가스사용비율이 적은 순으로 sorting
dong = dong.sort_values('가스사용비율')

dong.to_csv('dong.csv', index = False)

#%% 데이터 분석
dong = pd.read_csv('C:/Users/a/Desktop/data_science_contest/전처리데이터/dong.csv')
gas = pd.read_csv('C:/Users/a/Desktop/data_science_contest/전처리데이터/gas.csv')
household = pd.read_csv('C:/Users/a/Desktop/data_science_contest/전처리데이터/household.csv')
age = pd.read_csv('C:/Users/a/Desktop/data_science_contest/전처리데이터/age.csv')
disability = pd.read_csv('C:/Users/a/Desktop/data_science_contest/전처리데이터/disability.csv')

#%% 데이터 탐색

# 기술통계
describe = dong['가스사용비율'].describe()
    # 평균이 1에 가깝고 표준편차가 0.17로 매우 작다.

# 히스토그램
gas_ratio_hist = plt.figure(figsize = (12, 8))
plt.hist(dong['가스사용비율'])
plt.title('동별 (가정용 가스사용량 / 세대수) 히스토그램')
plt.xlabel('가스사용비율')
plt.ylabel('빈도')
plt.show()
gas_ratio_hist.savefig('gas_ratio_hist.png', dpi = 200)

# 왜도, 첨도
sp.stats.describe(dong['가스사용비율'])
    # skewness=0.8928597750044209, 왜도값이 양수로 나와 오른꼬리 분포를 가지고 있으며
    # kurtosis=5.42374279253818, 첨도가 매우 높게 나와 중앙에 많이 분포

# 박스플롯
gas_ratio_boxplot = plt.figure(figsize = (12, 12))
plt.boxplot(dong['가스사용비율'])
plt.title('가스사용비율 상자그림')
plt.show()
gas_ratio_boxplot.savefig('gas_ratio_boxplot.png', dpi = 200)

# 이상치
IQR = describe['75%'] - describe['25%'] # IQR : 3분위수 - 1분위수
criteria_low = describe['25%'] - (1.5 * IQR) # 0.7459829494127482
criteria_high = describe['75%'] + (1.5 * IQR) # 1.2129334237238805
dong_low_outlier = dong.loc[dong['가스사용비율'] < criteria_low] # 29개 데이터
dong_high_outlier = dong.loc[dong['가스사용비율'] > criteria_high] # 25개 데이터

#%% 지도 시각화

# googlemaps를 통한 위도 경도 처리
gmaps_key = '********************************'
gmaps = googlemaps.Client(key = gmaps_key)

address = []
lat = []
lng = []

for i in range(len(dong)):
    tmp_info = gmaps.geocode(dong['자치구'][i] + ' ' + dong['행정동'][i], language = 'ko')
    
    address.append(tmp_info[0]['formatted_address'])
    lat.append(tmp_info[0]['geometry']['location']['lat'])
    lng.append(tmp_info[0]['geometry']['location']['lng'])
    
    print('[' + str(i) + ']', dong['행정동'][i], '-->', tmp_info[0]['formatted_address'])

dong['lat'] = lat
dong['lng'] = lng

# folium을 이용한 시각화
gmaps.geocode('덕수궁', language = 'ko') # lat : 37.5658049, lng : 126.9751461 , 덕수궁을 지도의 중심점으로 잡았다.

# 에너지 사용량이 낮은 정도를 원의 반지름으로 표현하여 지도에 매핑
map_dong_radius = folium.Map(location = [37.5658049, 126.9751461],
                              zoom_start = 12)

for i in range(len(dong)):
    location = [dong['lat'][i], dong['lng'][i]]

    folium.CircleMarker(location = location,
                        radius = (1 - dong['가스사용비율'][i]) * 30,
                        color = '#CD3181',
                        fill_color = '#CD3181',
                        popup = dong['자치구'][i] + dong['행정동'][i]
                        ).add_to(map_dong_radius)

map_dong_radius.save('map_dong_radius.html') # 대체적으로 산이 분포하는 행정동에 가스사용량이 낮은 것을 알 수 있다.

# 가스사용량이 낮은 극단치 (가스사용량 0.7459829494127482미만, 하위 29개 데이터) 를 가지고 있는 행정동을 지도에 매핑
map_dong_top29 = folium.Map(location = [37.5658049, 126.9751461],
                             zoom_start = 12)

for i in range(29):
    location = [dong['lat'][i], dong['lng'][i]]
    
    folium.Marker(location = location,
                  icon = folium.Icon(color = 'red'),
                  popup = '[' + dong['자치구'][i] + ' ' + dong['행정동'][i] + ']' + '\n' +\
                  str(dong['가스사용비율'][i])).add_to(map_dong_top29)

map_dong_top29.save('map_dong_top29.html')  # 대체적으로 산이 분포하는 행정동에 가스사용량이 낮은 것을 알 수 있다.

#%% 상관분석
corr_matrix = dong.corr()
corr_matrix_4 = corr_matrix[abs(corr_matrix) > 0.4] # 상관계수가 0.4가 넘는 관계만 보기

plt.scatter(dong['1인세대비율'], dong['전체장애인비율'])

