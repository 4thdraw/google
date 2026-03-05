# %%

from google.oauth2.service_account import Credentials
import gspread #Google Sheets 전용 라이브러리
import pandas as pd
import matplotlib.pyplot as plt




# 한글 폰트  기본설정접근 수정 (예: 맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
# 한글폰트가 기본인 경우 - 부호가 깨지는 경우가 있음. 이를 방지하기 위해 아래 설정 추가
# 유니코드에서 마이너스 기호가 깨지는 문제 해결
# 네모모양으로 표시되는 경우는 폰트가 해당 문자를 지원하지 않아서 발생하는 문제입니다.
plt.rcParams['axes.unicode_minus'] = False

# 1. 인증 범위 설정
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# 2. 서비스 계정 인증

#google.oauth2.service_account.Credentials
# 🔑 주요 메서드
# 메서드	설명
# from_service_account_file()	JSON 파일로부터 인증 객체 생성
# from_service_account_info()	dict 형태 JSON 정보로 생성
# with_scopes()	접근 범위(scope) 추가
# with_subject()	사용자 위임(도메인 위임) 설정
# refresh(request)	액세스 토큰 갱신
# before_request(request, method, url, headers)	API 요청 전에 토큰 자동 처리

client = gspread.authorize(creds)

# 1️⃣ creds 안에는
# → 서비스계정 키 + 토큰 생성 정보 있음

# 2️⃣ gspread.authorize(creds)가
# 토큰 생성
# API 요청 준비
# 인증 헤더 생성

# 3️⃣ 그 결과로
# 👉 Client 객체 생성

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

# %%
worksheet = spreadsheet.sheet1


# 4. 데이터 가져오기
# 셀 실행순간에만 데이터를 가져와서 저장
# 구글시트에서 수정한 다음 이 부분을 다시 실행하면 최신 데이터로 업데이트됨
data = worksheet.get_all_records()
df = pd.DataFrame(data)
print(df.shape)
# %%
print(df.head())

# %%
# 데이터로 정보 가치 확인하기
# 이 컬럼들은 정보량이 0입니다.
# Index = 데이터의 위치를 식별하는 "이름표" 컬럼저장 객체 , index는 고유한 행의 값
df.nunique()

# %%
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
