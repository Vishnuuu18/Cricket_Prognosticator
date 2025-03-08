import pandas as pd
import numpy as np
df=pd.read_csv("ML/T20/t20i_info.csv")
df.head()
df.isnull().sum()
df.shape
df[df['city'].isnull()]['venue'][0].split(" ")[0]
df['city'] = df['city'].fillna(df['venue'].apply(lambda x: x.split(' ')[0]))
df.tail()
df.isnull().sum()
df['city'].value_counts()
eligible_cites = df['city'].value_counts()[df['city'].value_counts() > 600].index.tolist()
df = df[df['city'].isin(eligible_cites)]
df.shape
df
df['current_score'] = df.groupby('match_id').cumsum()['runs']
df.head()
df['over'] = df['ball'].apply(lambda x : str(x).split(".")[0])
df['ball_no'] = df['ball'].apply(lambda x : str(x).split(".")[1])
df.head()
df['ball_bowled'] = (df['over'].astype(int)*6 + df['ball_no'].astype(int))
df.tail()
df['balls_left'] = 120 - df['ball_bowled']
df.tail()
df['balls_left'] = df['balls_left'].apply(lambda x:0 if x<0 else x)
df.tail()
df.info()
df['player_dismissed'] = df['player_dismissed'].apply(lambda x:1 if x!='0' else '0')
df
df['player_dismissed'] = df['player_dismissed'].astype(int)
df['player_dismissed'] = df.groupby('match_id').cumsum()['player_dismissed']
df['wicket_left'] = 10 - df['player_dismissed']
df.tail()
df['current_run_rate'] = (df['current_score']*6) / df['ball_bowled']
df.tail()
groups = df.groupby('match_id')
# 5 over = 30 ball
match_id = df['match_id'].unique()
last_five=[]
for id in match_id:
    last_five.extend(groups.get_group(id).rolling(window = 30).sum()['runs'].values.tolist())

df['last_five'] = last_five
last_five
df.head()
final_df = df.groupby('match_id').sum()['runs'].reset_index().merge(df, on='match_id')
final_df
final_df.columns
final_df = final_df[['batting_team', 'bowling_team', 'city', 'current_score', 'balls_left', 'wicket_left',
       'current_run_rate', 'last_five', 'runs_x']]
final_df.dropna(inplace=True)
final_df
final_df.isnull().sum()
final_df.shape
final_df = final_df.sample(final_df.shape[0])
final_df.shape
X = final_df.drop(columns=['runs_x'])
y = final_df['runs_x']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error
transformer = ColumnTransformer([
    ('transformer', OneHotEncoder(sparse=False, drop='first'),['batting_team','bowling_team', 'city'])
], remainder='passthrough')
pipe = Pipeline(steps=[
    ('step1', transformer),
    ('step2', StandardScaler()),
    ('step3', XGBRegressor(n_estimators=1000, learning_rate=0.2, max_depth=12, random_state=1))
])
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
r2_score(y_test, y_pred)
mean_absolute_error(y_test, y_pred)
import pickle
pickle.dump(pipe, open('pipe.pkl', 'wb'))