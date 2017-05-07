import json

path = '/Users/hiroshiteraoka/GW/5_4/pycamp-20170503/teraoka_hiroshi/Data/usagov_bitly_data2013-05-17-1368832207'

records = [json.loads(line) for line in open(path)]

print('User-Agent:', records[0]['a'])


####Pandasとは
#
# DataFrame テーブル
# Series 縦１列の事
import pandas as pd
from pandas import DataFrame


df = DataFrame(data=records)
tz = df['tz']
print(tz)
