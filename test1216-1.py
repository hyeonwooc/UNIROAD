import streamlit as st 
# 오늘의 날짜
from datetime import datetime, timedelta
import time
import os
os.chdir('C:/Users/User/빅프로젝트')

from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np

# 레시피 기본+재료+과정 데이터프레임 병합하기

file_name = "기본재료과정"  # 기본 + 재료 + 과정 csv 저장할 파일 이름

ingredient = pd.read_csv('레시피 재료명 최최종.csv', encoding='cp949')
basic = pd.read_csv('레시피 기본정보.csv', encoding='cp949')
process = pd.read_csv('레시피 과정정보.csv', encoding='cp949')

process.sort_values(by=['레시피 코드', '요리설명순서'], ascending=True)

ing1 = ingredient[['레시피 코드', '재료명', '재료용량']]
ing1['재료명 + 용량'] = ing1['재료명'] + ' ' + ing1['재료용량']

# basic['재료모음'] = np.nan

unique_code = ing1['레시피 코드'].unique()

temp_temp_list = []
temp_temp_list2 = []

for i in unique_code :
    temp= ''
    temp2 = ''
    
    temp_list = ing1[ing1['레시피 코드'] == i]
    for j in temp_list['재료명'] :
        temp += j
        temp += ', '
    temp_temp_list.append(temp[:-2])
    
    for k in temp_list['재료명 + 용량']:
        temp2 += str(k)
        temp2 += ', '
    temp_temp_list2.append(temp2[:-2])
    
new_temp = pd.DataFrame(unique_code)
new_temp['met'] = temp_temp_list
new_temp['met+vol'] = temp_temp_list2

##############
# 컬럼명 변경
new_temp.rename(columns={0 : 'recipe_code'}, inplace=True)
###
# 컬럼명 변경
basic.rename(columns={'레시피 코드' : 'recipe_code'}, inplace=True)
merge_b_i = pd.merge(basic, new_temp ,on ='recipe_code', how = 'inner')
#merge_b_i.to_csv('수정재료.csv', encoding='cp949')

temp = []
for i in range(0, process.shape[0]):
    
    row = process.loc[i] # 현재 행 위치
    idx = process.index[i] # 햔재 인덱스?
    
#     print(row['요리설명순서'])
    temp.append(str(row['요리설명순서']) + '. ' + str(row['요리설명']+'\n'))

process['과정'] = temp
proc = process.copy()
proc['new과정팁'] = proc['과정팁']+proc['Unnamed: 5']+ proc['Unnamed: 6']+proc['Unnamed: 7']+proc['Unnamed: 8']+proc['Unnamed: 9']+proc['Unnamed: 10']+proc['Unnamed: 11']+proc['Unnamed: 12']+proc['Unnamed: 13']+proc['Unnamed: 14']+proc['Unnamed: 15']+proc['Unnamed: 16']+proc['Unnamed: 17']
del_cols = ['Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17']
proc.drop(del_cols, axis=1, inplace=True)


# 과정정보 합쳐보기
# basic['process'] = np.nan
unique_code = proc['레시피 코드'].unique()

temp_temp_list = []

for i in unique_code :
    temp= ''
    temp_list = proc[ proc['레시피 코드'] == i ]
    for j in temp_list['과정'] :
        temp += j
        temp += ' '
    temp_temp_list.append(temp[:-2])
    
new_temp = pd.DataFrame(unique_code)
new_temp['proc'] = temp_temp_list

#  컬럼명 변경
new_temp.rename(columns={0 : 'recipe_code'}, inplace=True)
merge_b_i_p = pd.merge(merge_b_i, new_temp ,on ='recipe_code', how = 'inner')
merge_b_i_p.to_csv(f'{file_name}.csv', encoding='cp949', index = None)

# df = pd.read_csv(f'{file_name}.csv', encoding='cp949')
df = merge_b_i_p.copy()


# 마켓걸리 상품 데이터
price_kurly= pd.read_csv('kr_price - 시트1 - 복사본.csv', encoding = 'cp949')
price_kurly1 = price_kurly.copy()


today = datetime.today()
user1 = pd.read_csv('user1.csv', encoding = 'cp949')

######################################### 내가 가진 상품 ##################################################################
got_items = []
got_ing = []
alarm_list = []
show_list = []
for i in range(user1.shape[0]):
    for idx, row in price_kurly1.iterrows() :
        if user1['상품이름'][i] == row['상품이름'] :
  
            
            got_ing.append( row['재료이름'] )
            purchase_day = datetime.strptime(user1['구매날짜'][i], "%Y-%m-%d").date()
            got_items.append(i)
            
            if row['공산//냉장/냉동'] == '공산' :
                
                user1['유통기한'][i] = purchase_day + timedelta(days=row['일(유통)'])
                day = purchase_day + timedelta(days=row['일(유통)'])
                if (day - (today.date())).days <= 3  :
                    alarm_list.append(row['재료이름'])
                    show_list,append(row['상품이름'])
            elif row['공산//냉장/냉동'] == '냉장' :
                
                user1['유통기한'][i] = purchase_day + timedelta(5)
                day = purchase_day + timedelta(5)
                if (day - (today.date())).days <= 3 :
                    alarm_list.append(row['재료이름'])
                    show_list.append(row['상품이름'])
            else :
                user1['유통기한'][i] = purchase_day + timedelta(5)
                day = purchase_day + timedelta(5)
                if (day - (today.date())).days <= 3 :
                    alarm_list.append(row['재료이름'])
                    show_list.append(row['상품이름'])
################################################################  구매목록 
st.markdown ("## 구매목록")
st.dataframe(user1)
################################################################  구매목록

st.markdown("## 임박상품")
for i in range(len(show_list)):
    for idx, row in user1.iterrows():
        if show_list[i] == row['상품이름']:
           # deltaday = datetime.strftime((row['유통기한'] -today.date()), "%d")
            byday = (row['유통기한'] -today.date()).days
            dday = datetime.strftime(row['유통기한'] , "%Y-%m-%d")
            st.metric(label=row['상품이름'], value= dday, delta= f'{byday}일 남았습니다.')
            st.write("Kurly's")
        
df['no_arr'] = np.nan
df['cnt'] = np.nan
df['no_cnt'] = np.nan

# df sort 만드는 구문
for i in range(0, df.shape[0]):
    cnt = 0 # 한 행마다 cnt 0으로 초기화
    no_cnt = 0
    row = df.loc[i] # 한 행마다 row에 가져옴
    no_arr = [] # 없는 재료 리스트, 매 행마다 초기화
    no_str = ""
    arr = row['met'].split(', ') # 한 요리의 재료를 리스트로 만들었습니다.
    
    for j in arr:
        if j in alarm_list : # 내가 가진, 유통기한 임박 재료가 지금 요리에 있을 때
            cnt += 1 
        else : # 내가 가진 재료가 지금 요리에 없을 때
            no_str += j
            no_str += ', '
            no_cnt += 1
            
    no_str = no_str[:-2]
    df.loc[i,'no_arr'] = no_str
    df.loc[i,'cnt'] = cnt
    df.loc[i,'no_cnt'] = no_cnt
df_sort = df.sort_values(by=['cnt', 'no_cnt'], ascending=[False, True])[:5]
df_sort.reset_index(drop=True, inplace=True)
df_sort.to_csv('df_sort.csv', encoding = 'cp949')
df_sort = pd.read_csv('df_sort.csv', encoding = 'cp949')

# 필요한 재료 마켓컬리 검색결과 , 버전 5
# 빈 리스트 생성
no_arr = []

for i in range(0, df_sort.shape[0]):
    row = df_sort.loc[i]
#     print(row['레시피 이름'])
    no_arr.append( list(row['no_arr'].split(', ')) )
    
k_arr = []
for i in range(len(no_arr)):
    k_arr.append([])

# no_arr 만드는 구무
for i in range(len(no_arr)):
#     print(no_arr[i])
    for j in no_arr[i]:
        TF = False
#         print(j)
        for idx, row  in price_kurly1.iterrows():
            # 유통기한 데이터 - 
        
        
            if j == row['재료이름']:
                k_arr[i].append(row['상품이름']+ ' ' +str(int(row['중량(g)/용량(ml)'])) + row['단위'] +str(' {0:,}'.format((int(row['가격']))))+'원')
                TF = True
                continue
        if TF == False:
            for idx, row in price_kurly1.iterrows():
            
                if ((j in row['재료이름']) or (row['재료이름'] in j)):
                    if j != '물':
                        k_arr[i].append(row['상품이름']+ ' ' +str(int(row['중량(g)/용량(ml)']))+row['단위'] +str(' {0:,}'.format((int(row['가격']))))+'원')
                    

### 레세피 순위, 사진, 레시피 설명, 레시피 필요 재료 검색결과
tab1, tab2, tab3, tab4, tab5 = st.tabs(['1순위','2순위','3순위','4순위','5순위'])

with tab1:
    st.caption('1순위')
    i=0
    row = df_sort.loc[i]
    name = row['레시피 이름']
    no_met = row['no_arr']
    cnt = row['cnt']
    re = row['proc']    
    for idx, row in basic.iterrows():
        if row['레시피 이름'] == name:
            url = row['대표이미지 URL']
    st.image(url)
    st.write(f'{i+1}순위는 [{name}] ({int(cnt)})이고 \n필요한 재료는 "{no_met}" 입니다.')  
    explain = df_sort['간략(요약) 소개'].values[i]
    need_ing = no_arr[i]
    if st.button(name + '의 레시피', key='re_1'):
        st.write(f'{re}입니다.') 
    if st.button('재료 검색결과', key='search_1'):
        st.write(f'{explain}\n\n↓↓↓\n\n마켓컬리 검색결과\n\n ↓↓↓\n\n')
        for k in range(len(k_arr[i])):
            st.write(k_arr[i][k])
   
with tab2:
    i=1
    row = df_sort.loc[i]
    name = row['레시피 이름']
    no_met = row['no_arr']
    cnt = row['cnt']
    re = row['proc']    
    for idx, row in basic.iterrows():
        if row['레시피 이름'] == name:
            url = row['대표이미지 URL']
    st.image(url)
    st.write(f'{i+1}순위는 [{name}] ({int(cnt)})이고 \n필요한 재료는 "{no_met}" 입니다.')
    explain = df_sort['간략(요약) 소개'].values[i]
    need_ing = no_arr[i]
    
    if st.button(name + '의 레시피', key='re_2'):
        st.write(f'{re}입니다.')
    if st.button('재료 검색결과', key= 'search_2'):
        st.write(f'{explain}\n\n↓↓↓\n\n마켓컬리 검색결과\n\n ↓↓↓\n\n')
        for k in range(len(k_arr[i])):
            st.write(k_arr[i][k])
            
with tab3:
    i=2
    row = df_sort.loc[i]
    name = row['레시피 이름']
    no_met = row['no_arr']
    cnt = row['cnt']
    re = row['proc']    
    for idx, row in basic.iterrows():
        if row['레시피 이름'] == name:
            url = row['대표이미지 URL']
    st.image(url)
    st.write(f'{i+1}순위는 [{name}] ({int(cnt)})이고 \n필요한 재료는 "{no_met}" 입니다.')
    explain = df_sort['간략(요약) 소개'].values[i]
    need_ing = no_arr[i]
    
    if st.button(name + '의 레시피', key='re_3'):
        st.write(f'{re}입니다.')
    if st.button('재료 검색결과', key = 'search_3'):
        st.write(f'{explain}\n\n↓↓↓\n\n마켓컬리 검색결과\n\n ↓↓↓\n\n')
        for k in range(len(k_arr[i])):
            st.write(k_arr[i][k])
            
with tab4:
    i=3
    row = df_sort.loc[i]
    name = row['레시피 이름']
    no_met = row['no_arr']
    cnt = row['cnt']
    re = row['proc']    
    for idx, row in basic.iterrows():
        if row['레시피 이름'] == name:
            url = row['대표이미지 URL']
    st.image(url)
    st.write(f'{i+1}순위는 [{name}] ({int(cnt)})이고 \n필요한 재료는 "{no_met}" 입니다.')
    explain = df_sort['간략(요약) 소개'].values[i]
    need_ing = no_arr[i]
    if st.button(name + '의 레시피', key=' re_4'):
        st.write(f'{re}입니다.')
    if st.button('재료 검색결과', key='search_4'):
        st.write(f'{explain}\n\n↓↓↓\n\n마켓컬리 검색결과\n\n ↓↓↓\n\n')
        for k in range(len(k_arr[i])):
            st.write(k_arr[i][k])

with tab5:
    i=4
    row = df_sort.loc[i]
    name = row['레시피 이름']
    no_met = row['no_arr']
    cnt = row['cnt']
    re = row['proc']
    for idx, row in basic.iterrows():
        if row['레시피 이름'] == name:
            url = row['대표이미지 URL']
    st.image(url)
    st.write(f'{i+1}순위는 [{name}] ({int(cnt)})이고 \n필요한 재료는 "{no_met}" 입니다.')
    explain = df_sort['간략(요약) 소개'].values[i]
    need_ing = no_arr[i]
    if st.button(name + '의 레시피' ,key='re_5'):
        st.write(f'{re}입니다.')
    if st.button('재료 검색결과', key = 'search_5'):
        st.write(f'{explain}\n\n↓↓↓\n\n마켓컬리 검색결과\n\n ↓↓↓\n\n')
        for k in range(len(k_arr[i])):
            st.write(k_arr[i][k])
