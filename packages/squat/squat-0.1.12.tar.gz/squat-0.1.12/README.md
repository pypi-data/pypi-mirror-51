# **S**pend **Q**uality and **U**sage **A**nalysis **T**ool (**SQUAT**)

This Project is a tool to analyse Bankstatements transactions
to give a comprehensive report on the spend, earning and usage of an user.
It does the following job:

* Creates and trains a Machine learning model to classify transactions based on the narration.
* All the training and other repeatative work is already done for you.
* Once the package is installed with pip, the developer just need to pass the bankstatement dataframe
to get the report.

<br><br>

## Project Components

SQUAT contains the packages or libraries required for supporting and running the whole process.

1. spacy
2. Core ENG package for spacy
3. pandas
4. jupyter notebook

**Source**:<br>
https://bitbucket.global.standardchartered.com/users/1586202/repos/squat/browse

## About the ML model

The model is created based on most common keyword observed from the bankstatements of singapore.
This project has a large scope of improving the accuracy and adding more classifications in future
depending on the type of dataset available to us.

Everytime we update the model a new version of SQUAT is supposed to get released.

## Create and use whl file

* with and updated setup.py execute the following command to create a whl file,
    ```python setup.py bdist_wheel```

* Please make sure you have pre-installed pandas, spacy and jupyter from standard chartered artifactory in your
 virtualenv

* Also make sure once spacy is installed the eng core library is also pre-installed in the virtualenv using pip.

* Now you can pip install squat using the whl file or from standard chartered artifactory if it is hosted.

## API

* You can import the utility by typing the following,
```from squat.Classifier.ClassifierUtil import ClassifierUtil```

* Read any csv or excel using pandas and create a dataframe. Please make sure the df has the following header atleast,
date, description, debit, credit, runningbalance (irrespective of the order)

* The ```ClassifierUtil``` can be initialized using the above df.

* Once initialized please make sure to call ```obj.evaluate()``` to evaluate each transaction.

* Once evaluated you can call ```get_analysis``` method to get the comprehensive analysis or call
```show_stat``` to get the statistics.

OR

* You can import the utility by typing the following,
```from squat.Classifier.ClassifierUtil import ClassifierUtilRaw```

* Read any csv or excel using pandas and create a dataframe. Please make sure the df has the following header atleast,
date, description, debit, credit, runningbalance (irrespective of the order)

* The ```ClassifierUtilRaw``` can be initialized to get the category.

* Once initialized please make sure to call ```obj.get_cat(text)``` to evaluate the category of the text.

* For Example,
	```
	obj.get_cat('paytm transaction gurgaon')
	Out: ('Digital', 0.9632782936096191)
	```