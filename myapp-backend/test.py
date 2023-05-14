import json

fr=open("./data/cc-cc408-hya==elasticsearch_cluster_health_active_shards==cluster.csv","r",encoding='utf-8')
ls=[]
for line in fr:
    line=line.replace("\n","")
    ls.append(line.split(","))
fr.close()

for i in range(1,len(ls)):
    ls[i]=dict(zip(ls[0],ls[i]))
b = json.dumps(ls[1:], sort_keys=True,indent=4,ensure_ascii=False)

b1=json.loads(b)

date=[]
value=[]
for index in b1:
    date.append(index['date'])
    value.append(int(index['value']))
print(date)
print(value)



