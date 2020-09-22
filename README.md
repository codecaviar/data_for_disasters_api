<img src="https://raw.githubusercontent.com/codecaviar/digital_asset_management/master/assets/bingyune-and-company-logo-6400x3600.png" align="left" width="200" height="auto">

<br/><br/><br/><br/>

----------

# Data for Disasters: One Big Idea to Improve Response Time

**Code Caviar Story**: https://www.bingyune.com/blog/data-for-disasters-api

## Project Overview

Every year, natural disasters displace millions of people around the world from their homes. The most basic needs become scarce and dire in the event of an emergency: health, water, and shelter, among others. Since 1980, the United States alone suffered 246 weather and climate disasters that topped over $1 billion in losses according to the [National Centers for Environmental Information](https://www.ncdc.noaa.gov/billions). Using data to expertly identify, manage, and mitigate the risks of destructive hurricanes, intense droughts, raging wildfires, and other severe weather and climate events is becoming more critical in disaster response and recovery. Currently, satellite and aerial imagery are key tools used to locate and map areas affected by a disaster. However, with the increasing popularity and integration of social media platforms into everyday life, more people are also turning to social media as a channel to call for aid, stay up to with the safety of members in their communities, and share other relevant information in the event of a disaster. Future disaster response techniques will continue to incorporate real-time social media and other disaster related messages to provide prompt and strategic assistance.

**The goal of this project is to build a simple application that can analyze incoming disaster messages and classify them into specific categories.** The project makes use of the "Multilingual Disaster Response Messages" dataset from [Appen](https://appen.com/datasets/combined-disaster-response-data/) : "The dataset contains 30,000 messages drawn from events including an earthquake in Haiti in 2010, an earthquake in Chile in 2010, floods in Pakistan in 2010, super-storm Sandy in the U.S.A. in 2012, and news articles spanning a large number of years and 100s of different disasters." The messages in the dataset have been sorted into 36 categories, such as Water, Hospitals, and Aid-Related, to help emergency personnel coordinate their aid efforts.

## Getting Started

Cloning the git repository and installing the provided packages will help you get a copy of the project up and running on your local machine. The analysis for this project was performed using Jupyter Notebook (.ipynb) and the packages were managed using the Anaconda platform.

```
git clone https://github.com/codecaviar/data_for_disasters_api.git
conda env create -f environment.yml
```

### Instructions:
1. Run the following commands in the project's root directory to set up a database and the model
    - To run ETL pipeline that cleans data and stores in database

        `python3 data/data_wrangling.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`

    - To run ML pipeline that trains classifier and saves

        `python3 models/data_modeling.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the project's root directory to run the web app: `python3 src/app.py`

#### ETL Pipeline (Extract, Transform, Load)

The data_wrangling.py file is a data cleaning pipeline that:

* Loads the messages and categories datasets (.csv files)
* Merges the two datasets
* Cleans the data
* Stores it in a SQLite database (.db file)

#### ML Pipeline (Machine Learning)

The data_modeling.py file is a machine learning pipeline that:

* Loads data from the SQLite database
* Splits the dataset into training and test sets
* Builds a text processing and machine learning pipeline (NLTK)
* Trains and tunes a model using GridSearchCV
* Outputs results on the test set
* Exports the final model as a pickle file

### Disaster Response App

<img src="assets/fig4-disaster-response-pipeline.png>
<img src="assets/fig6-classify-message-results.png>
<img src="assets/fig7_2-overview-training-category-data.png>

## Authors

- **BingYune Chen** - [LinkedIn](https://www.linkedin.com/in/bingyune-chen/)
- **BingYune & Co** - [GitHub](https://github.com/codecaviar)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

[Udacity](https://blog.udacity.com/2016/07/nanodegree-101.html) has a mission to train the world’s workforce in the careers of the future. The organization partners with leading technology companies to learn how technology is transforming industries, and teaches the critical tech skills that companies are looking for in their workforce. With Udacity's powerful and flexible digital education platform, even the busiest learners can prepare themselves to take on the most in-demand tech roles.

[General Assembly](https://generalassemb.ly/education/data-science-immersive/san-francisco) is a global education company on a mission to empower individuals and companies through dynamic training programs, exclusive thought leader events, and high-impact networking opportunities. The curricula focus on the in-demand skills every company today needs: coding, data, design, digital marketing, and product management. General Assembly also works with companies, from startups to more than 40 of the Fortune 100, to provide innovative tech training, onboarding, and hiring strategies to solve talent gaps.

The project referenced the following:
* https://theindex.generalassemb.ly/harnessing-the-power-of-data-for-disaster-relief-73950a64531d
* https://katba-caroline.com/disaster-response-message-classification-pipelines-nltk-flask/
* https://hbr.org/2006/11/disaster-relief-inc

----------
The Code Caviar is a digital magazine about data science and analytics that dives deep into key topics, so you can experience the thrill of solving at scale.
