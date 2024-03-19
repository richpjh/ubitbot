import pyupbit
import numpy as np
import pandas as pd

# KRW-BTC의 최근 7일간의 OHLCV 데이터를 가져옴
df = pyupbit.get_ohlcv("KRW-BTC", count=7)

# 변동폭 * k 계산, k는 0.5로 가정
df['range'] = (df['high'] - df['low']) * 0.5

# 목표 매수 가격 설정
df['target'] = df['open'] + df['range'].shift(1)

# 수익률 계산
df['ror'] = np.where(df['high'] > df['target'],  # 조건
                     df['close'] / df['target'],  # 참일 때
                     1)                           # 거짓일 때

# 누적 곱 계산(누적 수익률)
df['hpr'] = df['ror'].cumprod()

# Draw Down 계산
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# 최대 Draw Down 출력
print("MDD(%): ", df['dd'].max())

# 엑셀 파일로 저장
df.to_excel("dd.xlsx")






