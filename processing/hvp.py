import pandas as pd
df = [x for x in range(1,12)]  
x = [x for x in range(1,12)]   
i  = 0

df = pd.read_csv(r"./time_occur.csv",index_col=0)
df = df[df['2011']==0]

def pred(num):  
    res = []  
    t = 2011
    for i in range(0,11):
        y1 = [0]
        t = t + 1
        for m in range(t,2022):
            # print(sum(df["%d" %m][:num]))
            y1.append(sum(df["%d" %m][:num]))
        y1 = [x/num for x in y1]
        res.append(y1)
    return res

data = []
# m = 0
for i,j,k in zip(pred(10)[0][:], pred(20)[0][:],pred(50)[0][:]):
    data.append([i,j,k])
    # m = m + 1
df = pd.DataFrame(data, index=[i for i in range(0,11)])
df.columns = ["top10", "top20", "top50"]
df.to_csv("hvp2011.csv")