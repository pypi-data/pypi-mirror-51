# llp

Literary Language Processing (LLP): corpora, models, and tools for the digital humanities.

## Quickstart

1) Install:

```
pip install llp                       # install with pip in terminal
```

2) Download an existing corpus...

```
llp status                            # show which corpora/data are available
llp download ECCO_TCP                 # download a corpus
```

...or import your own:

```
llp import                            # use the "import" command \
  -path_txt mycorpus/txts             # a folder of txt files  (use -path_xml for xml) \
  -path_metadata mycorpus/meta.xls    # a metadata csv/tsv/xls about those txt files \
  -col_fn filename                    # filename in the metadata corresponding to the .txt filename
```

...or start a new one:

```
llp create                            # then follow the interactive prompt
```

3) Then you can load the corpus in Python:

```python
import llp                            # import llp as a python module
corpus = llp.load('ECCO_TCP')         # load the corpus by name or ID
```

...and play with convenient Corpus objects...

```python
df = corpus.metadata                  # get corpus metadata as a pandas dataframe
smpl=df.query('1740 < year < 1780')   # do a quick query on the metadata

texts = corpus.texts()                # get a convenient Text object for each text
texts_smpl = corpus.texts(smpl.id)    # get Text objects for a specific list of IDs
```

...and Text objects:

```python
for text in texts_smpl:               # loop over Text objects
    text_meta = text.meta             # get text metadata as dictionary
    author = text.author              # get common metadata as attributes    

    txt = text.txt                    # get plain text as string
    xml = text.xml                    # get xml as string

    tokens = text.tokens              # get list of words (incl punct)
    words  = text.words               # get list of words (excl punct)
    counts = text.word_counts         # get word counts as dictionary (from JSON if saved)
    ocracc = text.ocr_accuracy        # get estimate of ocr accuracy
    
    spacy_obj = text.spacy            # get a spacy text object
    nltk_obj = text.nltk              # get an nltk text object
    blob_obj = text.blob              # get a textblob object
```

## Corpus magic

Each corpus object can generate data about itself:

```python
corpus.save_metadata()                # save metadata from xml files (if possible)
corpus.save_plain_text()              # save plain text from xml (if possible)
corpus.save_mfw()                     # save list of all words in corpus and their total  count
corpus.save_freqs()                   # save counts as JSON files
corpus.save_dtm()                     # save a document-term matrix with top N words
```

You can also run these commands in the terminal:

```
llp install my_corpus                 # this is equivalent to python above
llp install my_corpus -parallel 4     # but can access parallel processing with MPI/Slingshot
llp install my_corpus dtm             # run a specific step
```

Generating this kind of data allows for easier access to things like:

```python
mfw = corpus.mfw(n=10000)             # get the 10K most frequent words
dtm = corpus.freqs(words=mfw)         # get a document-term matrix as a pandas dataframe
```

You can also build word2vec models:

```python
w2v_model = corpus.word2vec()         # get an llp word2vec model object
w2v_model.model()                     # run the modeling process
w2v_model.save()                      # save the model somewhere
gensim_model = w2v_model.gensim       # get the original gensim object
```

























