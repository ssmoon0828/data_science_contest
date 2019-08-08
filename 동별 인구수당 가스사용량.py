#%% 모듈 장착

# 기본모듈
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family = 'Gulim')

# 통계 모듈
import scipy as sp

# 지도시각화 모듈
import googlemaps
import folium
#%% 데이터 불러오기
gas = pd.read_excel('C:/Users/a/Desktop/공공데이터/데이터/2018_동별_도시가스사용량.xls',
                    skiprows = [0, 1],
                    na_values = ['-'])


household = pd.read_excel('C:/Users/a/Desktop/공공데이터/데이터/2018_동별_세대수.xls',
                          na_values = ['-'])


#%% 데이터 전처리

# 합계, 소계 데이터 지우기
gas = gas.loc[(gas['동'] != '합계') & (gas['동'] != '소계')]
household = household.loc[(household['자치구'] != '합계') &\
                          (household['행정동'] != '합계') &\
                          (household['행정동'] != '소계')]

# household, gas데이터셋에 기간변수가 필요 없다
# 또한 gas 데이터에서 가정용 가스가 아닌 합계, 일반용, 업무용, 산업용, 열병합, 수송용 변수를 지워준다.
del gas['기간'], household['기간']
del gas['합계'], gas['일반용'], gas['업무용'], gas['산업용'], gas['열병합'], gas['수송용']

# gas 데이터의 동 변수이름을 행정동으로 바꾸어 household 변수이름과 통일시켜준다.
# 
gas = gas.rename(columns = {'동' : '행정동',
                            '소계' : '가정용가스사용량',
                            '취사용' : '가정용-취사용가스사용량',
                            '취사/난방 겸용' : '가정용-취사/난방_겸용가스사용량'})

len(gas['행정동'].unique()) # 422 / 423
len(household['행정동'].unique()) # 423 / 5088
    # household 데이터셋이 월별로 분리되어있기 때문에 데이터가 훨씬많다.


 # 염리동 : gas 데이터셋에 염리동 데이터가 없다. 염리동 데이터를 지워준다.
set(household['행정동']) - set(gas['행정동'])
household = household.loc[household['행정동'] != '염리동']

# 자치구 행정동 별로 groupby 를 해준다.
household = household.groupby(['자치구', '행정동']).mean()

# gas 데이터의 자치구, 행정동 변수를 index로 넣는다.
gas = gas.set_index(['자치구', '행정동'])

# 두 데이터를 합친다
gas_household = pd.merge(household, gas, left_index = True, right_index = True)

# index를 열로 변환
gas_household.reset_index(inplace = True)
gas_household = gas_household.sort_values(['자치구', '행정동'])

# 상관관계
corr = gas_household.corr()
     # 가정용에서는 세대수가 높은 상관관계(0.926686)를 보이는 반면
     # 취사용에서는 0.24로 매우 낮은 상관관계, 취사/난방에서는 약 0.7로 어중간한 상관관계를 보였다.

# 가스사용량 / 세대수 변수 추가
gas_household['가스사용비율'] = gas_household['가정용가스사용량'] / gas_household['전체세대수']

# sorting
gas_household_sort = gas_household.sort_values('가스사용비율')
gas_household_sort.index = range(423)

## 필요한 변수만 추출
gas_household_sort = gas_household_sort[['자치구', '행정동', '전체세대수', '가정용가스사용량', '가스사용비율']]

#%% 데이터 탐색

# 히스토그램
gas_household_hist = plt.figure(figsize = (12, 8))
plt.hist(gas_household_sort['가스사용비율'])
plt.title('동별 가스사용비율 히스토그램')
plt.xlabel('가정용 가스사용량 / 세대수')
plt.show()
gas_household_hist.savefig('gas_household_hist.png', dpi = 200)

# 기술통계
describe = gas_household_sort['가스사용비율'].describe()

# 박스플롯
gas_household_boxplot = plt.figure(figsize = (12, 12))
plt.boxplot(gas_household_sort['가스사용비율'])
plt.show()
gas_household_boxplot.savefig('gast_household_boxplot.png', dpi = 200)

# 이상치
IQR = describe['75%'] - describe['25%'] # IQR : 3분위수 - 1분위수
criteria = describe['25%'] - (1.5 * IQR) # 0.7459829494127482
low_outlier = gas_household_sort.loc[gas_household_sort['가스사용비율'] < criteria]

#%% 지도시각화

# googlemaps를 통한 위도 경도 처리
gmaps_key = 'AIzaSyCjtmeThkkpApWjJAXwlc9BRzFes7J9zoA'
gmaps = googlemaps.Client(key = gmaps_key)

gas_household_sort['지도코드'] = gas_household_sort['자치구'] + ' ' + gas_household_sort['행정동']

address = []
lat = []
lng = []

for i in range(len(gas_household_sort)):
    tmp_info = gmaps.geocode(gas_household_sort['지도코드'][i], language = 'ko')
    
    address.append(tmp_info[0]['formatted_address'])
    lat.append(tmp_info[0]['geometry']['location']['lat'])
    lng.append(tmp_info[0]['geometry']['location']['lng'])
    
    print('[' + str(i) + ']', gas_household_sort['지도코드'][i], '-->', tmp_info[0]['formatted_address'])

gas_household_sort['주소'] = address
gas_household_sort['lat'] = lat
gas_household_sort['lng'] = lng

gas_household_sort.to_csv('gas_household_sort.csv')

# folium을 이용한 시각화
gmaps.geocode('덕수궁', language = 'ko') # lat : 37.5658049, lng : 126.9751461 , 덕수궁을 지도의 중심점으로 잡았다.

# 에너지 사용량이 낮은 정도를 원의 반지름으로 표현하여 지도에 매핑
map_seoul_radius = folium.Map(location = [37.5658049, 126.9751461],
                              zoom_start = 12)

for i in range(len(gas_household_sort)):
    location = [gas_household_sort['lat'][i], gas_household_sort['lng'][i]]

    folium.CircleMarker(location = location,
                        radius = (1 - gas_household_sort['가스사용비율'][i]) * 30,
                        color = '#CD3181',
                        fill_color = '#CD3181',
                        popup = gas_household_sort['지도코드'][i]
                        ).add_to(map_seoul_radius)

map_seoul_radius.save('map_seoul_radius.html') # 대체적으로 산이 분포하는 행정동에 가스사용량이 낮은 것을 알 수 있다.

# 가스사용량이 낮은 극단치 (가스사용량 0.7459829494127482미만, 하위 28개 데이터) 를 가지고 있는 행정동을 지도에 매핑
map_seoul_top28 = folium.Map(location = [37.5658049, 126.9751461],
                             zoom_start = 12)

for i in range(28):
    location = [gas_household_sort['lat'][i], gas_household_sort['lng'][i]]
    
    folium.Marker(location = location,
                  icon = folium.Icon(color = 'red'),
                  popup = '[' + gas_household_sort['지도코드'][i] + ']' + '\n' +\
                  str(gas_household_sort['가스사용비율'][i])).add_to(map_seoul_top28)

map_seoul_top28.save('map_seoul_top28.html')  # 대체적으로 산이 분포하는 행정동에 가스사용량이 낮은 것을 알 수 있다.

#%% 통계적 해석