from pybliometrics.scopus import ScopusSearch
from datetime import datetime
import re
from pybliometrics.scopus import AbstractRetrieval
import multiprocessing
import argparse

# 消除证书验证的错误
# from requests_toolbelt import SSLAdapter
# import requests
# adapter = SSLAdapter('TLSv1')
# s1 = requests.Session()
# s1.mount('https://', adapter)



def download_abstract(year):
    start = datetime.now().replace(microsecond=0)

    s = ScopusSearch('SUBJAREA(MATE) AND SRCTYPE(j) AND LANGUAGE(English) AND PUBYEAR = %d' %year, \
            refreash=False, subscriber=True, download=True, verbose=True)

    result = s.results
    size = len(result)
    f1 = open('./abs/abs%d.txt' %year,'w',encoding='utf-8')
    f2 = open('./doi/doi%d.txt' %year,'w',encoding='utf-8')
    count = 0
    for item in result:
        doi = item.doi
        tit = item.title
        abs = item.description
        if tit is not None:
            f1.write(tit)
            f1.write(". ")
        if abs is not None:
            f1.write(abs + '\n')
        if doi is not None:
            f2.write(doi+'\n')
        count = count + 1
    end = datetime.now().replace(microsecond=0)
    print(end-start)
    print(size)
    print(count)
    if size != count:
        print("ERROR, NOT SUCCESS")
    else:
        print("Congratulations!!")
# download_abstract(1980)
if __name__ == "__main__":
    pool = multiprocessing.Pool(50)
    for i in range(2021,2023):
        pool.apply_async(func=download_abstract, args=(i,))
    pool.close()
    pool.join()
    print("end!")

