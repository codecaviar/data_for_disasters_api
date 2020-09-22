# Run Application
import pandas as pd
import collections

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import joblib
from sqlalchemy import create_engine

BYCO_LOGO = "https://raw.githubusercontent.com/codecaviar/digital_asset_management/master/assets/bingyune-and-company-logo-6400x3600.png"

def Header(name, app):
    title = html.H2(name, style={"margin-top": 5})
    logo = html.Img(src=BYCO_LOGO, style={"float": "right", "width": 192, "height": 108, "margin-top": 5})
    return dbc.Row([dbc.Col(title, md=9, align="center"), dbc.Col(logo, md=3)])

# Start the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server # Visit http://127.0.0.1:8050/ 156

def tokenize(text):
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w not in stopwords.words("english")]
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///' + 'data/DisasterResponse.db')
df = pd.read_sql_table('disasterdata', engine)

# load mode
model = joblib.load("models/classifier.pkl")

# Graph components, when there are no messages entered
graphs = [
    [
        dcc.Graph(id="graph-genre"),
    ],
    [
        dcc.Graph(id="graph-category"),
    ],
]

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

app.layout = dbc.Container(
    [
        Header("Data for Disasters", app),
        html.Hr(),
        dbc.Navbar(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px"), width=3),
                        dbc.Col(html.A('Made with Dash', href='https://plot.ly'), width=8),
                        dbc.Col(html.A('Github', href='https://github.com/codecaviar/data_for_disasters_api'), width=1),
                    ],
                    align='center',
                    no_gutters=True,
                ),
            ],
        ),
        dbc.Jumbotron(
            [
                html.H1("Disaster Response Pipeline", className="text-center"),
                html.P("Analyzing message data for disaster response", className="text-center"),
                dcc.Input(id='input-message', type='text', value='', placeholder='Enter a message to classify', maxLength=512, className='form-control form-control-lg col-lg-12 form-group-lg'),
                dbc.Button('Classify Message', id='button-submit', className='btn btn-lg btn-success', block=True),
            ], className = 'jumbotron'
        ),
        dbc.Row(dbc.Col(html.Div(id='results'))),
        html.Br(),
        html.H2('Overview of Training Dataset', className='text-center'),
        dbc.Row([dbc.Col(graph) for graph in graphs]),
    ],
    fluid=False,
)

@app.callback(
    [Output("results", "children"), Output('graph-genre', 'figure'), Output('graph-category', 'figure')],
    [Input("button-submit", "n_clicks")],
    [State('input-message', 'value')],
)

def update_figures(n_clicks, value):

    # use model to predict classification for query
    classification_labels = model.predict([value])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    results = list()
    results.append(html.Div(
        [
            html.H2('Results', className='text-center'),
            html.P('Message to be classified: {}'.format(value), className='text-center'),
            html.H3('Categories', className='text-center')
        ]))

    for category in list(df.columns[4:]):
        if classification_results[str(category)] == 1:
            results.append(html.Li(category.replace('_', ' ').title(), className='list-group-item list-group-item-success text-center'))
        else:
            results.append(html.Li(category.replace('_', ' ').title(), className='list-group-item list-group-item-dark text-center'))

    # extract data needed for visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    df_cat = df.drop(['id', 'message', 'original','genre'], axis=1)
    category_counts = list(df_cat.sum().values)
    category_names = list(df_cat.columns)

    # Count most common words
    wordcount = {}
    for text in df.message.sample(1000):
        for word in tokenize(text):
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1

    # Create list of most common words
    word_list = []
    word_count_list = []
    for word, count in collections.Counter(wordcount).most_common(10):
        word_list.append(word)
        word_count_list.append(count)

    genre_fig = px.bar(
        genre_counts,
        x=genre_names,
        y=genre_counts,
        title="Distribution of Message Genres",
        labels={"x": "Genre", "y": "Count"}
    )
    genre_fig.update_xaxes(showticklabels=False)

    category_fig = px.bar(
        category_counts,
        x=category_names,
        y=category_counts,
        title="Distribution of Message Categories",
        labels={"x": "Category", "y": "Count"}
    )
    category_fig.update_xaxes(showticklabels=False)

    return results, genre_fig, category_fig

if __name__ == "__main__":
    app.run_server(debug=True)
