import pandas as pd

d = {
'current': [[-1.8795300221255817, '2018-09-14T13:36:00Z']],
'voltage': [[12.0, '2018-09-14T13:36:00Z']]
}

fields = ['current', 'voltage']

df = pd.DataFrame()
for field in fields:
    df_aux = pd.DataFrame(d[field], columns = [field, 'time'])  # check above definition of d
    df_aux.set_index('time', inplace = True)
    df[field] = df_aux[field]

df.index = pd.to_datetime(df.index, errors='coerce')   #convert it to datetime

print(df.head())