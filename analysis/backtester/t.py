import time; from common import *
t=time.time(); eq,tr=run(); print(time.time()-t); print(summ(eq,tr)); print(eq.index[0], eq.index[-1])
print(PX.loc[START:].notna().sum(axis=1).iloc[[0,-1]])
last=PX.apply(lambda s:s.last_valid_index()); print((last<PX.index[-1]-pd.Timedelta(days=10)).sum(),"names end early")
