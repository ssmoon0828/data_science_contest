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
raw_family = pd.read_excel('C:/Users/ssmoo/Desktop/공공데이터/데이터/2018_동별_세대수.xls',
                           na_values = ['-'])

# 동별 연령대 데이터
raw_age = pd.read_excel('C:/Users/ssmoo/Desktop/공공데이터/데이터/2018_동별_연령대별인구수.xls',
                        na_values = ['-'])

# 동별 인구밀도 데이터
raw_pop = pd.read_excel('C:/Users/ssmoo/Desktop/data_science_contest/원래데이터/2018_동별_인구밀도.xls',
                        na_values = ['-'])

# 동별 인구이동 데이터
raw_popmove = pd.read_excel('C:/Users/ssmoo/Desktop/data_science_contest/원래데이터/2018_동별_인구이동.xls',
                            skiprows = [0, 1],
                            na_values = ['-'])

# 동별 독거노인수 데이터
raw_oldsolo = pd.read_excel('C:/Users/ssmoo/Desktop/data_science_contest/원래데이터/2018_동별_독거노인.xls',
                            skiprows = [0],
                            na_values = ['-'])

# 동별 장애인수(장애유형별) 데이터
raw_disability = pd.read_excel('C:/Users/ssmoo/Desktop/data_science_contest/원래데이터/2018_동별_장애인수_장애유형별.xls',
                               skiprows = [0, 1],
                               na_values = ['-'])

# 동별 혼인 이혼 데이터
raw_marrydivorce = pd.read_excel('C:/Users/ssmoo/Desktop/data_science_contest/원래데이터/2018_동별_혼인이혼.xls',
                                 na_values = ['-'])

# 동별 가스 사용 데이터
raw_gas = pd.read_excel('C:/Users/ssmoo/Desktop/공공데이터/데이터/2018_동별_도시가스사용량.xls',
                        skiprows = [0, 1],
                        na_values = ['-'])

# 동별 화재발생수(장소별) 데이터
raw_fire = pd.read_excel('file:///C:/Users/ssmoo/Desktop/data_science_contest/원래데이터/2018_동별_화재발생_장소별.xls',
                         na_values = ['-'],
                         skiprows = [0])
#%% 데이터 전처리

#%%동별 세대수 데이터 전처리
family = raw_family.copy()
family = family.fillna(0)

# 필요없는 데이터 제거
family = family.loc[(family['자치구'] != '합계') &\
                          (family['행정동'] != '합계') &\
                          (family['행정동'] != '소계')]

# 분리되어 있는 기간들을 평균으로 통일
family = family.groupby(['자치구', '행정동']).mean()

# n인세대별 비율 추출
for i in range(9):
    family[str(i + 1) + '인세대비율'] = family.iloc[:, i + 2] / family['전체세대수']

family['10세대이상비율'] = family['10인세대 이상'] / family['전체세대수']

# 필요한 변수 추출
family = family.iloc[:, [1, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]]

# 인덱스 -> 변수 변환
family = family.reset_index()

# csv파일로 저장
family.to_csv('family.csv', index = False)

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

#%% 동별 인구밀도 데이터 전처리
pop = raw_pop.copy()

# 변수이름 수정
pop = pop.rename(columns = {'동' : '행정동'})

# 필요없는 데이터 제거
pop = pop.loc[(pop['자치구'] != '합계') &\
              (pop['행정동'] != '합계') &\
              (pop['행정동'] != '소계')]

# 필요한 변수 추출
pop = pop[['자치구', '행정동', '인구밀도']]

# 자치구 행정동 가나다순 배열
pop = pop.sort_values(['자치구', '행정동'])

# csv 파일로 저장
pop.to_csv('pop.csv', index = False)

#%% 동별 인구이동 데이터 전처리
popmove = raw_popmove.copy()

# 변수이름 수정
popmove = popmove.rename(columns = {'동' : '행정동',
                                    popmove.columns[3] : '전입수',
                                    popmove.columns[4] : '전출수'})

# 필요없는 데이터 제거 
popmove = popmove.loc[(popmove['자치구'] != '합계') &\
                      (popmove['행정동'] != '합계') &\
                      (popmove['행정동'] != '소계')]

# 필요한 변수 생성
popmove = pd.merge(popmove, age, on = ['자치구', '행정동'])
popmove['전입비율'] = popmove['전입수'] / popmove['전체인구수']
popmove['전출비율'] = popmove['전출수'] / popmove['전체인구수']

# 필요한 변수 추출
popmove = popmove[['자치구', '행정동', '전입수', '전출수', '전입비율', '전출비율']]

# 자치구 행정동 가나다순 배열
popmove = popmove.sort_values(['자치구', '행정동'])

# csv 파일로 저장
popmove.to_csv('popmove.csv', index = False)

#%% 동별 독거노인수 데이터 전처리
oldsolo = raw_oldsolo.copy()

# 변수 이름 변경
oldsolo = oldsolo.rename(columns = {'동' : '행정동',
                                    '계' : '전체독거노인수',
                                    '계.1' : '국민기초생활보장수급권자수',
                                    '계.2' : '저소득노인수',
                                    '계.3' : '일반독거노인수'})
# 필요없는 데이터 제거
oldsolo = oldsolo.loc[(oldsolo['자치구'] != '합계') &\
                      (oldsolo['행정동'] != '합계') &\
                      (oldsolo['행정동'] != '소계')]

# 필요한 변수 생성
oldsolo = oldsolo[['자치구', '행정동', '전체독거노인수', '국민기초생활보장수급권자수',
                   '저소득노인수', '일반독거노인수']]
oldsolo = pd.merge(oldsolo, age, on = ['자치구', '행정동'])
for i in range(4):
    oldsolo[oldsolo.columns[i + 2][:-1] + '비율'] = oldsolo.iloc[:, i + 2] / oldsolo['전체인구수']

# 필요한 변수 추출
oldsolo = oldsolo[['자치구', '행정동', '전체독거노인비율', '국민기초생활보장수급권자비율',
                   '저소득노인비율', '일반독거노인비율']]

# 자치구 행정동 가나다순 배열
oldsolo = oldsolo.sort_values(['자치구', '행정동'])

# csv파일로 저장
oldsolo.to_csv('oldsolo.csv', index = False)

#%% 동별 장애인수 데이터 전처리
disability = raw_disability.copy()
disability = disability.fillna(0)
# 변수 이름 변경
disability = disability.rename(columns = {'동' : '행정동',
                                          '계' : '전체장애인수',
                                          '계.1' : '지체장애인수',
                                          '계.2' : '뇌병변장애인수',
                                          '계.3' : '시각장애인수',
                                          '계.4' : '청각장애인수',
                                          '계.5' : '언어장애인수',
                                          '계.6' : '지적장애인수',
                                          '계.7' : '자폐성장애인수',
                                          '계.8' : '정신장애인수',
                                          '계.9' : '신장장애인수',
                                          '계.10' : '심장장애인수',
                                          '계.11' : '호흡기장애인수',
                                          '계.12' : '간장애인수',
                                          '계.13' : '안면장애인수',
                                          '계.14' : '장루요루장애인수',
                                          '계.15' : '뇌전증장애인수'})

# 필요없는 행 제거
disability = disability.loc[(disability['자치구'] != '합계') &\
                            (disability['행정동'] != '합계') &\
                            (disability['행정동'] != '소계') &\
                            (disability['행정동'] != '기타')]

# 필요한 변수 추출
disability = disability[['자치구', '행정동', '전체장애인수', '지체장애인수',
                         '뇌병변장애인수', '시각장애인수', '청각장애인수',
                         '언어장애인수', '지적장애인수', '자폐성장애인수',
                         '정신장애인수', '신장장애인수', '심장장애인수',
                         '호흡기장애인수', '간장애인수', '안면장애인수',
                         '장루요루장애인수', '뇌전증장애인수']]

# 비율 변수 생성
disability = pd.merge(disability, age, on = ['자치구', '행정동'])

for i in range(16):
    disability[disability.columns[i + 2][: -1] + '비율'] = disability.iloc[:, i + 2] / disability['전체인구수']

# 필요한 변수 추출
disability = disability[['자치구', '행정동', '전체장애인비율', '지체장애인비율',
                         '뇌병변장애인비율', '시각장애인비율', '청각장애인비율',
                         '언어장애인비율', '지적장애인비율', '자폐성장애인비율',
                         '정신장애인비율', '신장장애인비율', '심장장애인비율',
                         '호흡기장애인비율', '간장애인비율', '안면장애인비율',
                         '장루요루장애인비율', '뇌전증장애인비율']]

# 자치구 행정동 가나다순 배열
disability = disability.sort_values(['자치구', '행정동'])

# csv파일로 저장
disability.to_csv('disability.csv', index = False)

#%% 동별 혼인 이혼
marrydivorce = raw_marrydivorce.copy()

# 변수 이름 수정
marrydivorce = marrydivorce.rename(columns = {'동' : '행정동'})

# 필요없는 데이터 제거
marrydivorce = marrydivorce.loc[(marrydivorce['자치구'] != '합계') &\
                            (marrydivorce['행정동'] != '합계') &\
                            (marrydivorce['행정동'] != '소계')]

# 필요한 변수 추출
marrydivorce = marrydivorce[['자치구', '행정동', '혼인', '이혼']]

# 자치구 행정동 가나다순 배열
marrydivorce = marrydivorce.sort_values(['자치구', '행정동'])

# csv파일로 저장
marrydivorce.to_csv('marrydivorce.csv', index = False)
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
gas = pd.merge(gas, family, on = ['자치구', '행정동'])
gas['가스사용비율'] = gas['가스사용량'] / gas['전체세대수']

# 필요한 변수 추출
gas = gas[['자치구', '행정동', '가스사용량', '가스사용비율']]

# 자치구 행정동 가나다 순 배열
gas = gas.sort_values(['자치구', '행정동'])

# csv파일로 저장
gas.to_csv('gas.csv', index = False)

#%% 동별 화재발생수 데이터 전처리(수가 아닌 비율처리를 하기 애매하다.)
fire = raw_fire.copy()
fire = fire.fillna(0)

# 변수 이름 수정
fire = fire.rename(columns = {'동' : '행정동',
                              '합계' : '화재발생수'})

# 필요없는 데이터 제거
fire = fire.loc[(fire['자치구'] != '합계') &\
                (fire['행정동'] != '합계') &\
                (fire['행정동'] != '소계')]

# 필요한 변수 추출
fire = fire[['자치구', '행정동', '화재발생수']]

# 자치구 행정동 가나다순 배열
#%% 데이터 통합

# 행정동 데이터가 모두 같은지 확인
set(family['행정동']) == set(age['행정동']) # 424 True
set(age['행정동']) == set(pop['행정동']) # 424 True
set(pop['행정동']) == set(popmove['행정동']) # 424 True
set(popmove['행정동']) == set(oldsolo['행정동']) # 424 True
set(oldsolo['행정동']) == set(disability['행정동']) # 424 Ture
set(disability['행정동']) == set(marrydivorce['행정동']) # 424 True
set(marrydivorce['행정동']) == set(gas['행정동']) # 424 - 423 False
set(marrydivorce['행정동']) - set(gas['행정동']) # gas에는 염리동 데이터가 없다
set(marrydivorce['행정동']) == set(fire['행정동']) # 424 - 422 False
set(marrydivorce['행정동']) - set(fire['행정동']) # fire에는 돈암2동, 둔촌1동 데이터가 없다.

# merge
dong = pd.merge(family, age, on = ['자치구', '행정동'])
dong = pd.merge(dong, pop, on = ['자치구', '행정동'])
dong = pd.merge(dong, popmove, on = ['자치구', '행정동'])
dong = pd.merge(dong, oldsolo, on = ['자치구', '행정동'])
dong = pd.merge(dong, disability, on = ['자치구', '행정동'])
dong = pd.merge(dong, marrydivorce, on = ['자치구', '행정동'])
dong = pd.merge(dong, gas, on = ['자치구', '행정동'], how = 'left')
dong = pd.merge(dong, fire, on = ['자치구', '행정동'], how = 'left')

# 염리동, 돈암2동, 둔촌1동 결측값데이터는 평균으로 처리
dong.loc[dong['행정동'] == '염리동', '가스사용량'] = np.mean(dong['가스사용량'])
dong.loc[dong['행정동'] == '염리동', '가스사용비율'] = np.mean(dong['가스사용비율'])
dong.loc[dong['행정동'] == '돈암2동', '화재발생수'] = np.mean(dong['화재발생수'])
dong.loc[dong['행정동'] == '둔촌1동', '화재발생수'] = np.mean(dong['화재발생수'])

# 위도 경도 변수 추가
gmaps_key = '**********************************'
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

# dong 데이터  csv 파일로 저장
dong.to_csv('dong.csv', index = False)
#%% 데이터 분석
dong = pd.read_csv('C:/Users/ssmoo/Desktop/data_science_contest/전처리데이터/dong.csv')

#%% 상관분석
dong_corr = dong.corr()
dong_corr.to_csv('dong_corr.csv')

# 상관계수가 0.4 이상인것만 확인
dong_corr04 = dong_corr[abs(dong_corr) > 0.4]
dong_corr05 = dong_corr[abs(dong_corr) > 0.5]
dong_corr06 = dong_corr[abs(dong_corr) > 0.6]
dong_corr07 = dong_corr[abs(dong_corr) > 0.7]

plt.scatter(dong['전체장애인비율'], dong['전체독거노인비율'])
plt.hist(dong['전체독거노인비율'])
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

