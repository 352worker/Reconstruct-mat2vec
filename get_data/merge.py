from tqdm import tqdm
for year in range(2001,2022):
    f0 = open("./final/%d.txt" %year, 'w', encoding="utf-8")
    for i in tqdm(range(1921, year+1)):
        f = open("./text-v0/%dpara.txt" %i, 'r', encoding="utf-8")
        for line in f:
            f0.write(line)