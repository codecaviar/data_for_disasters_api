# Train machine learning classifier
import sys
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import numpy as np
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
import pickle

def load_data(database_filepath):
    '''
    Loads sqlite database and return X (training) and y (target) arrays
    and associated y category names

    Args:
        database_filepath (str): database filename

    Returns:
        X (pandas.Series): dataset
        y (pandas.DataFrame): dataframe containing the categories
        category_names (list): list containing the categories name
    '''
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql_table('disasterdata', engine)

    X = df['message'].values
    y = df.drop(['id', 'message', 'original','genre'], axis=1).values

    category_names = df.drop(['id', 'message', 'original','genre'], axis=1)

    return X, y, category_names


def tokenize(text):
    '''
    Defines tokenizer for the sklearn CountVectorizer feature
    extraction model which converts a collection of text documents
    to a matrix of token (word) counts

    Args:
        text (str): input text

    Returns:
        clean_tokens (list): tokens obtained from the input text
    '''

    # Normalize and lower case text
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())

    # tokenize text
    tokens = word_tokenize(text)

    # Remove stop words
    tokens = [w for w in tokens if w not in stopwords.words("english")]

    # initiate lemmatizer
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        # lemmatize and remove leading/trailing white space
        clean_tok = lemmatizer.lemmatize(tok).strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model(grid_search_cv = False):
    '''
    Build the model

    Args:
        grid_search_cv (bool): if True after building the pipeline it will be performed an exhaustive search over specified parameter values ti find the best ones

    Returns:
        pipeline (pipeline.Pipeline): model
    '''
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer = tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(
            RandomForestClassifier(n_estimators=200, n_jobs=-1)))])

    #pipeline.get_params()

    if grid_search_cv == True:
        print('Searching for best parameters...')
        parameters = {'vect__ngram_range': ((1, 1), (1, 2))
            , 'vect__max_df': (0.5, 0.75, 1.0)
            , 'tfidf__use_idf': (True, False)
            , 'clf__estimator__n_estimators': [50, 100, 200]
            , 'clf__estimator__min_samples_split': [2, 3, 4]
        }

        pipeline = GridSearchCV(pipeline, param_grid = parameters)

    return pipeline


def evaluate_model(model, X_test, y_test, category_names):
    '''
    Evaluates the performance of the pipeline model for each target
    category using the sklearn classification_report function. Also prints the average precision, recall and f1 score for all categories.

    Args:
        model (pipeline.Pipeline): model to evaluate
        X_test (pandas.Series): dataset
        y_test (pandas.DataFrame): dataframe containing the categories
        category_names (str): categories name
    '''
    # Lists for storing the precision, recall and f1 scores
    prec_values, recall_values, f1_values = [], [], []

    # Run prediction using the fitted model
    y_pred = model.predict(X_test)

    # Insure prediction and test arrays are the same size
    assert y_pred.shape == y_test.shape,"Prediction and test arrays not same size!"

    for i in range(0, y_pred.shape[1]):
        print('-'*40)
        print('CATEGORY = {}'.format(category_names.columns[i]))
        print('-'*40)
        cls_rpt = classification_report(y_test[:,i][np.newaxis].T,
                                        y_pred[:,i][np.newaxis].T)
        print(len(cls_rpt.split()))
        print(cls_rpt.split())
        # Track metrics for all columns
        if len(cls_rpt.split()) > 24:
            prec_values.append(float(cls_rpt.split()[19]))
            recall_values.append(float(cls_rpt.split()[20]))
            f1_values.append(float(cls_rpt.split()[21]))

        print('For all columns ---------')
        print('Average precision: {:.2f}'.format(np.array(prec_values).mean()))
        print('Average recall: {:.2f}'.format(np.array(recall_values).mean()))
        print('Average f1 values: {:.2f}'.format(np.array(f1_values).mean()))
    return


def save_model(model, model_filepath):
    '''
    Save in a pickle file the model

    Args:
        model (pipeline.Pipeline): model to be saved
        model_filepath (str): destination pickle filename
    '''
    pickle.dump(model, open(model_filepath, 'wb'))
    return


def main():
    '''
    Parse the command line arguments
    '''
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=42)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database as the first argument and the filepath of the pickle file to save the model to as the second argument. \n\nExample: python train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
