# Chatbot using Keras
Here we are building a chatbot and this chatbot can have resoning capability.

## Dataset Information
Here we are using bAbI dataset which is buit by Facebook AI Research. 

## Dependencies

* Python 2.7
* TensorFlow 1.4.1: Refer this [link](https://www.tensorflow.org/install/)
* keras:            Refer this [link](https://keras.io/#installation)
* functools:        It's python standard library.
* tarfile:          It's python standard library.
* re :              It's python standard library.
* h5py:             `$ sudo pip install h5py`


## Usage 
* The dataset used here is babi-tasks-v1-2. Link of the dataset is [here](https://research.fb.com/downloads/babi/), its a relatively small dataset but a great dataset nonetheless

* In `main.py` file there are following parameters which can be change in following manner to train and test the model

* We are using the concepts of memory network and it is LSTM based models performed better than GRU based models for this task. 


### For Training
```bash
Step 1: Open main.py

Step 2: For training, set the parameters as given below.
train_model = 1         #(1 means training mode and 0 means no training mode) 
train_epochs = 100
load_model = 0          #( 1 means load the trained model and 0 means doesn't load trained model)
batch_size = 32
lstm_size = 64
test_qualitative = 0    #(1 means test trained on randomly generated story and 0 means do not perform test on ramdomly generated story)
user_questions = 0      #(1 means test trained on randomly generated story and 0 means do not perform test on ramdomly generated story)

Step 3: Run main.py
```

### For Testing
Here we can perform two types of testing.
* Testing for randomly generated story
* Testing for used given story

#### Testing for randomly generated story
```bash
Step 1: Open main.py

Setp 2: For testing ramdomly generated story, set the parameters as given below.

train_model = 0
train_epochs = 100
load_model = 1
batch_size = 32
lstm_size = 64
test_qualitative = 1
user_questions = 0

Step 3: Run main.py
```
#### Testing for used given story

```bash
Step 1: Open main.py

Setp 2: For testing user given story, set the parameters as given below.

train_model = 0
train_epochs = 100
load_model = 1
batch_size = 32
lstm_size = 64
test_qualitative = 0
user_questions = 1

Step 3: Run main.py
```

 

## Credit
Credit for the majority of code here goes to [Batchu Vishal](https://github.com/erilyth). I've merely created a wrapper to get people started. 
