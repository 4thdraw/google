# %%

from google.oauth2.service_account import Credentials
import gspread #Google Sheets 전용 라이브러리
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


# 1. 인증 범위 설정
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "./key/logical-contact-489206-a2-594ef50d3ae3.json",
    scopes=scope
)


client = gspread.authorize(creds)




print(type(client))


# %%
# 3. 시트 열기
spreadsheet = client.open("python_google_sheet_api")
print(f"""
      파일 제목: {spreadsheet.title}, 
      시트 수: {len(spreadsheet.worksheets())}, 
      파일 고유 ID: {spreadsheet.id}, 
      URL: {spreadsheet.url}
""")
# 무사히 가져왔는지 확인


worksheet = spreadsheet.sheet1



data = worksheet.get_all_records()
df = pd.DataFrame(data)
print(df.shape)

print(df.head())

# %%

df.nunique()


# 값이 동일한 컬럼확인하기
meaningless_cols = df.columns[df.nunique() == 1]
print(meaningless_cols)


df = df.drop(columns=meaningless_cols) # 의미 없는 컬럼 제거
print(df.head())


# %%
# 5. 시각화 예시 (예: 남/여 인원수 막대그래프)

plt.figure()  
# 새로운 그래프(figure)를 생성한다.
# 하나의 캔버스를 만든다고 생각하면 된다.
# 여러 그래프를 그릴 때 이전 그래프와 겹치는 것을 방지한다.

plt.bar(df["성별"], df["인원(명)"])
# 막대그래프(bar chart)를 그린다.
# x축 : df["성별"] → 성별 컬럼 값 (예: 남, 여)
# y축 : df["인원(명)"] → 각 성별에 해당하는 인원수
# 즉 성별별 인원수를 막대그래프로 표현

plt.xlabel("성별")
# x축의 이름(label)을 "성별"로 설정

plt.ylabel("인원(명)")
# y축의 이름(label)을 "인원(명)"으로 설정

plt.title("서울시 요양보호사 성별 인원수")
# 그래프의 제목(title)을 설정

# 막대 위에 숫자 표시
# for i, v in enumerate(df["인원(명)"]):
#     plt.text(i, v, str(v), ha="center", va="bottom")

plt.show()
# 지금까지 설정한 그래프를 화면에 출력
# matplotlib에서는 show()를 호출해야 그래프가 표시됨


# %%

# 시각화 성능화를 위한 집계 후 시각화
# groupby()로 성별별 인원수 합계 계산 / 같은 값끼리 묶어서 합계 계산

df_sum = df.groupby("성별")["인원(명)"].sum()
print(df_sum)
# df_sum은 성별별 인원수 합계가 담긴 시리즈 객체 ( 데이터 프레임으로 변환할 필요 없음 )
# %%
plt.figure()
colors = ["skyblue", "salmon"]
plt.bar(df_sum.index, df_sum.values, color=colors)
plt.xlabel("성별")
plt.ylabel("인원(명)")
plt.title("서울시 요양보호사 성별 인원수")

plt.show()

# %%
#df_sum = df.groupby("교육기관명")["인원(명)"].sum()
df_sum = df.groupby("교육기관명")["인원(명)"].sum().sort_values(ascending=False).head(20)
# 교육기관명별 인원수 합계를 계산한 후, 내림차순으로 정렬하여 상위 20개만 추출
print(df_sum)
plt.figure(figsize=(10, 6)) # 그래프의 크기를 가로 10인치, 세로 6인치로 설정
plt.bar(df_sum.index, df_sum.values, color="lightgreen")   
plt.xlabel("교육기관명")
plt.ylabel("인원(명)")
plt.title("서울시 요양보호사 교육기관별 인원수")
plt.xticks(rotation=45, ha="right")  # x축 레이블을 45도 회전하여 겹치지 않도록 설정
plt.tight_layout()  # 그래프 요소들이 겹치지 않도록 레이아웃 조정
plt.show() 

# %%
import string
df_sum = df.groupby("교육기관명")["인원(명)"].sum().sort_values(ascending=False).head(20)
# A,B,C... 코드 생성
codes = list(string.ascii_uppercase[:len(df_sum)])
print(codes)
# 기관명 → 코드 매핑
mapping = dict(zip(codes, df_sum.index))
# zip()은 여러 iterable(리스트, 튜플 등)을 같은 위치끼리 묶어서 하나의 쌍(pair)으로 만들어 주는 함수입니다.


print(mapping)


plt.figure(figsize=(10,6))
plt.bar(codes, df_sum.values, color="lightgreen")

plt.xlabel("교육기관 코드")
plt.ylabel("인원(명)")
plt.title("서울시 요양보호사 교육기관별 인원수 (Top 20)")

plt.tight_layout()
plt.show()

# 코드표 출력
for k,v in mapping.items():
    print(f"{k} : {v}")

# %%
plt.figure(figsize=(10,6))

plt.bar(codes, df_sum.values, color="lightgreen")

plt.xlabel("교육기관 코드")
plt.ylabel("인원(명)")
plt.title("서울시 요양보호사 교육기관별 인원수")

# legend 텍스트 만들기
legend_text = [f"{k} : {v}" for k,v in mapping.items()]
# ython의 리스트 컴프리헨션(list comprehension) 이라는 문법
# 다른 언어에서는 보통 여러 줄로 작성하는 것을 한 줄로 간결하게 표현

# legend_text = []

# for k, v in mapping.items():
#     legend_text.append(f"{k} : {v}")
# ['A : 종로...', 'B : 강남...', 'C : 송파...']

print(legend_text)


plt.legend(legend_text, title="교육기관 코드", bbox_to_anchor=(1.05,1), loc="upper left")

plt.tight_layout()
plt.show()

# legend() 함수는 그래프에 범례(legend)를 추가하는 함수입니다.
# legend_text는 범례에 표시할 텍스트 리스트입니다.

# %%
plt.figure(figsize=(10,6))

plt.bar(codes, df_sum.values, color="lightgreen")

plt.xlabel("교육기관 코드")
plt.ylabel("인원(명)")
plt.title("서울시 요양보호사 교육기관별 인원수")

# legend 텍스트 만들기
legend_text = [f"{k} : {v}" for k,v in mapping.items()]

from matplotlib.patches import Patch
#Patch는 matplotlib에서 채워진 도형(shape) 을 의미
handles = [
    Patch(color="lightgreen", label=f"{k} : {v}")
    for k,v in mapping.items()
]
#그래프에 범례(legend)를 표시하면서 위치와 제목을 설정하는 코드
#Patch(label="A : 종로교육원")
plt.legend(handles=handles,
           title="교육기관 코드",
           bbox_to_anchor=(1.05,1), # (0,0)   = 왼쪽 아래  (1,1)   = 오른쪽 위
           loc="upper left")

# | loc 값            | 의미               | legend 기준점 위치  |
# | ---------------- | ---------------- | -------------- |
# | `"best"`         | 자동으로 가장 좋은 위치 선택 | 데이터 안 가리는 위치   |
# | `"upper right"`  | 오른쪽 위            | legend의 오른쪽 위  |
# | `"upper left"`   | 왼쪽 위             | legend의 왼쪽 위   |
# | `"lower left"`   | 왼쪽 아래            | legend의 왼쪽 아래  |
# | `"lower right"`  | 오른쪽 아래           | legend의 오른쪽 아래 |
# | `"right"`        | 오른쪽 중앙           | legend의 오른쪽 중앙 |
# | `"center left"`  | 왼쪽 중앙            | legend의 왼쪽 중앙  |
# | `"center right"` | 오른쪽 중앙           | legend의 오른쪽 중앙 |
# | `"lower center"` | 아래 중앙            | legend의 아래 중앙  |
# | `"upper center"` | 위 중앙             | legend의 위 중앙   |
# | `"center"`       | 중앙               | legend의 중심     |

plt.tight_layout() # 여백(margin)을 자동 계산하여 그래프 요소들이 겹치지 않도록 조정하는 함수
plt.show()

# %%
import numpy as np
colors = plt.cm.tab20(np.linspace(0,1,len(df_sum)))
plt.figure(figsize=(10,6))

plt.bar(codes, df_sum.values, color=colors)

plt.xlabel("교육기관 코드")
plt.ylabel("인원(명)")
plt.title("서울시 요양보호사 교육기관별 인원수")
# 코드표 문자열
text = "\n".join([f"{k} : {v}" for k,v in mapping.items()])

plt.text(
    1.02, 0.5,
    text,
    transform=plt.gca().transAxes,
    fontsize=8,
    verticalalignment='center'
)

plt.tight_layout()
plt.show()

# %%
df_filtered = df[df["교육기관명"].str.contains("영업중", na=False)]


df_sum = df_filtered.groupby("교육기관명")["인원(명)"].sum().sort_values(ascending=False).head(20)

print(df_sum)

codes = list(string.ascii_uppercase[:len(df_sum)])
print(codes)
# 기관명 → 코드 매핑
mapping = dict(zip(codes, df_sum.index))
print(mapping)

# %%


# | 코드                    | 의미                 |
# | --------------------- | ------------------ |
# | `str.contains("영업중")` | 문자열 안에 "영업중" 포함 여부 |
# | `na=False`            | NaN 값 에러 방지        |
# | `df[...]`             | 조건에 맞는 행만 선택       |

plt.figure(figsize=(10,6))

plt.bar(codes, df_sum.values, color=colors)

plt.xlabel("교육기관 코드")
plt.ylabel("인원(명)")
plt.title("서울시 요양보호사 교육기관별 인원수")
# 코드표 문자열
text = "\n".join([f"{k} : {v}" for k,v in mapping.items()])

plt.text(
    1.02, 0.5,
    text,
    transform=plt.gca().transAxes,
    fontsize=8,
    verticalalignment='center'
)

plt.tight_layout()
plt.show()

# %%
df_sum = df.groupby("자치구명")["인원(명)"].sum()

# 항상 인원수 기준 정렬
df_sum = df_sum.sort_values(ascending=False)

# 30개 초과하면 상위 30개만
if len(df_sum) > 30:
    df_sum = df_sum.head(30)
    print(f"자치구가 {len(df_sum)}개 이상이라 상위 30개만 표시")

plt.figure(figsize=(10,6))
plt.bar(df_sum.index, df_sum.values, color="skyblue")

plt.xlabel("자치구")
plt.ylabel("인원(명)")
plt.title("서울시 자치구별 요양보호사 인원")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# Pandas DataFrame과 직접 연동하여 시각화 Seaborn 라이브러리 활용
# “컬럼이 많은 데이터”에 특히 강함

print(df.head())

import seaborn as sns
df_sum = (
    df.groupby("자치구명")["인원(명)"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(10,6))

sns.barplot(data=df_sum, x="자치구명", y="인원(명)")

plt.xticks(rotation=45)
plt.title("서울시 자치구별 요양보호사 인원")

plt.show()
# %%
# 자치구 + 성별 기준 인원 합계
df_gender = (
    df.groupby(["자치구명", "성별"])["인원(명)"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12,6))

sns.barplot(
    data=df_gender,
    x="자치구명",
    y="인원(명)",
    hue="성별"
)
# hue = 색상 기준 그룹

plt.xticks(rotation=45)
plt.title("자치구별 요양보호사 성별 인원 비교")

plt.tight_layout()
plt.show()
# %%
