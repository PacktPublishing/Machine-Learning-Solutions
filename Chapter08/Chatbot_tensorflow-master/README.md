# Tensorflow Chatbot

This is code for building chatbot using tensorflow.

Overview
============
In this code, we implement Tensorflows [Sequence to Sequence](https://www.tensorflow.org/versions/r0.12/tutorials/seq2seq/index.html) model to train a
chatbot on the [Cornell Movie Dialogue dataset](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html). After training for a few hours, the bot is able to hold a fun conversation.


Dependencies
============

* numpy
* scipy 
* six
* It is must to install tensorflow 0.12.1version. Find installation instruction form [here](https://www.tensorflow.org/versions/r0.12/get_started/os_setup.html)

Use [pip](https://pypi.python.org/pypi/pip) to install any missing dependencies

#### Important note
You must run this code on python 2.7 version and tensorflow 0.12.1 version. 

Usage
===========

To train the bot, edit the `seq2seq.ini` file so that mode is set to train like so

`mode = train`

then run the code like so

``python execute.py``

To test the bot during or after training, edit the `seq2seq.ini` file so that mode is set to test like so

`mode = test`

then run the code like so

``python execute.py``

I have also upload the pretrained model which you can download and test the model.

For training I have used GPU Gforce 1060 6-GB. It take 1 hour in order to generate the sentences.

Credits
===========
Credit for the majority of code here goes to [suriyadeepan](https://github.com/suriyadeepan). I've merely created a wrapper to get people started. 
