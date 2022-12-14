# Reconstruct-mat2vec

### Code for "Predicting the future applications of any material through learning from past literature", yet to be published.
#### Yu Wu, Teng Liu, Haiyang Song, Yinghe Zhao*, Jinxing Gu, Kailang Liu, Huiqiao Li, Jinlan Wang* and Tianyou Zhai*

The code consists of four parts.

#### Data collection and processing

The code for data collection and processing is in *./get_data*,
Literature collection can be achieved by running
```shell
python search_abstract.py
```
The processing of the collected literature can be achieved by running
```shell
python run_processt.py
```

Finally, run
```shell
python merge.py
```
The output file *2011.txt* is the established corpus based on the literature from 2011 and earlier (the year 1921 is the start point). Notably, the selection of the start and end points is arbitrary; herein, the years 1921 and 2011 are only used as an example.

#### Generation of word embeddings by Word2vec skip-gram

The code for generating the word embeddings of existing materials is in *./word2vec*

Using *2011.txt* as input, the word embeddings of existing materials can be generated by running
```shell
python ./train_dm.py --corpus 2011.txt --model_name 2011sg-200-30-8-15-0.01-N --epochs 30 --size 200 --window 8 --negative  15 --min_count 1 --learning_rate 0.01 --subsample 0.0001 -sg
```

and *./word2vec/make_hxs.ipynb*

The output file *w2v2011.txt* records existing materials and their word embeddings

#### Generation of reconstructed word embeddings

Change the format of the file *w2v2011.txt* by running
```shell
python make_dataset.py --vectors w2v2011.txt --output w2v2011.pkl --w2v-format   
```

The file *2022_2012.txt* records materials that have never been mentioned in the literature from 2011 and earlier but appear in the literature published between 2012 and 2022. Therefore, the materials in the file *2022_2012.txt* belong to new materials for w2v2011.pkl. *2022_2012.txt* was built by the following two steps. First, we established a corpus based on the literature published between 2012 and 2022 using the code in the first part. Second, we extracted materials that are in the above corpus but do not exist in the corpus *2011.txt*. The extraction of materials from the corpus was implemented in pymatgen.

The code for the generation of reconstructed word embeddings is in *./MIMICK*

Copy *w2v2011.pkl* and *2022_2012.txt* to *./MIMICK* and then run
```shell
python model.py ???dataset w2v2011.pkl --vocab 2022_2012.txt --output RWE2022_2012.txt --num-epochs 50 --learning-rate 0.001 --all-from-mimick --num-lstm-layers 2
```
A text file (*RWE2022_2012.txt*) containing new materials and their word embeddings can be obtained.

### Historical validation of predictions
The code for historical validation of predictions is in *./processing*

For a target application (e.g., ???thermoelectric???), materials that have been reported to serve the application and those unreported materials can be separated by running
```shell
python occur.py
```
The following files are required to run the above code:
- *hxs_2011.csv*: A file containing the desired materials for performing HVP
- *#year#.txt*: To calculate the HVP results for the materials in the above file by a particular year, a corpus needs to be established based on the literature before the particular year. For convenience, the corpus is divided into a series of text files according to the year.

After running the above code, a file named ???occur.csv??? can be obtained. The file is the basis for HVP.

Next, run
```shell
python time_predict.py
```
Three files are required to run the above code:
- *occur.csv*:See above
- *hxs_2011.csv*: See above
- *word_embedding.txt*: A file that includes the word embeddings of materials in *hxs_2011.csv* and the target application.

Using the output file generated in the above step as input, the results of HVP can be obtained by running
```shell
python hvp.py
```
