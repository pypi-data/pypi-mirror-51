Fast Sentence Embeddings (fse)
==================================

Fast Sentence Embeddings is a Python library that serves as an addition to Gensim. This library is intended to compute *sentence vectors* for large collections of sentences or documents. 


Features
------------

Find the corresponding blog post(s) here: https://medium.com/@oliverbor/fse-2b1ffa791cf9 (will be updated soon)

**fse** implements three algorithms for sentence embeddings. You can choose
between *unweighted sentence averages*,  *smooth inverse frequency averages*, and *unsupervised smooth inverse frequency averages*. 

Key features of **fse** are: 

**[X]** Supports Average, SIF, and uSIF Embeddings

**[X]** Full support for Gensims Word2Vec and all other compatible classes

**[X]** Full support for Gensims FastText with out-of-vocabulary words

**[X]** Induction of word frequencies for pre-trained embeddings

**[X]** Incredibly fast Cython core routines 

**[X]** Dedicated input file formats for easy usage (including disk streaming)

**[X]** Ram-to-disk training for large corpora

**[X]** Disk-to-disk training for even larger corpora

**[X]** Many fail-safe checks for easy usage

**[X]** Simple interface for developing your own models

**[X]** Extensive documentation of all functions

**[X]** 98% unittest coverage

Usage
-------------

Within the folder nootebooks you can find the following guides:

**Tutorial.ipynb** offers a detailed walk-through of some of the most important functions fse has to offer.

**STS-Benchmarks.ipynb** contains an example of how to use the library with pre-trained models to
replicate the STS Benchmark results [4] reported in the papers.


In order to use the **fse** model, you first need some pre-trained gensim 
word embedding model, which is then used by **fse** to compute the sentence embeddings.

After computing sentence embeddings, you can use them in supervised or
unsupervised NLP applications, as they serve as a formidable baseline.

The models presented are based on
- Deep-averaging embeddings [1]
- Smooth inverse frequency embeddings [2]
- Unsupervised smooth inverse frequency embeddings [3]

Credits to Radim Řehůřek and all contributors for the **awesome** library
and code that Gensim provides. A whole lot of the code found in this lib is based on Gensim.

In order to use **fse** you must first estimate a Gensim model which containes a
gensim.models.keyedvectors.BaseKeyedVectors class, for example 
*Word2Vec* or *Fasttext*. Then you can proceed to compute sentence embeddings
for a corpus.

	from gensim.models import FastText
	sentences = [["cat", "say", "meow"], ["dog", "say", "woof"]]
	ft = FastText(sentences, min_count=1, size=10)

	from fse.models import Average
	from fse import IndexedSentence
	model = Average(ft)
	model.train([IndexedSentence(s, i) for i, s in enumerate(sentences)])

	model.sv.similarity(0,1)

The current version does offer multi-core support out of the box. However, for most
applications a single core will most likely suffice.

To install **fse** on Colab, check out: https://colab.research.google.com/drive/1qq9GBgEosG7YSRn7r6e02T9snJb04OEi 

Results
------------

Model | [STS Benchmark](http://ixa2.si.ehu.es/stswiki/index.php/STSbenchmark#Results)
:---: | :---:
`CBOW-Paranmt` | **79.85**
`uSIF-Paranmt` | 79.02
`SIF-Paranmt` | 76.75
`SIF-Paragram` | 73.86
`uSIF-Paragram` | 73.64
`SIF-FT` | 73.38
`SIF-Glove` | 71.95
`SIF-W2V` | 71.12
`uSIF-FT` | 69.4
`uSIF-Glove` | 67.16
`uSIF-W2V` | 66.99
`CBOW-W2V` | 61.54
`CBOW-Paragram` | 50.38
`CBOW-FT` | 48.49
`CBOW-Glove` | 40.41


Installation
------------

This software depends on [NumPy, Scipy, Scikit-learn, Gensim, and Wordfreq]. 
You must have them installed prior to installing fse.

As with gensim, it is also recommended you install a fast BLAS library
before installing fse.

The simple way to install **fse** is:

    pip install --upgrade fse

In case you want to build from the source, just run:

    python setup.py install

If building the Cython extension fails (you will be notified), try:

    pip install git+https://github.com/oborchers/Fast_Sentence_Embeddings


Literature
-------------

1. Iyyer M, Manjunatha V, Boyd-Graber J, Daumé III H (2015) Deep Unordered 
Composition Rivals Syntactic Methods for Text Classification. Proc. 53rd Annu. 
Meet. Assoc. Comput. Linguist. 7th Int. Jt. Conf. Nat. Lang. Process., 1681–1691.

2. Arora S, Liang Y, Ma T (2017) A Simple but Tough-to-Beat Baseline for Sentence
Embeddings. Int. Conf. Learn. Represent. (Toulon, France), 1–16.

3. Ethayarajh K (2018) Unsupervised Random Walk Sentence Embeddings: A Strong but Simple Baseline.
Proceedings of the 3rd Workshop on Representation Learning for NLP. (Toulon, France), 91–100.

4. Eneko Agirre, Daniel Cer, Mona Diab, Iñigo Lopez-Gazpio, Lucia Specia. Semeval-2017 Task 1: Semantic Textual Similarity Multilingual and Crosslingual Focused Evaluation. Proceedings of SemEval 2017.


Copyright
-------------

Author: Oliver Borchers <borchers@bwl.uni-mannheim.de>

Copyright (C) 2019 Oliver Borchers
