# Flight Delay Prediction 


[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/yemaney/flight_delay_prediction/main/flight_delay.py)
![](gif.gif)

---
# Motivation

The world has become globalized, and one consequence of this fact is the increasing amount of travel, both (inter) and (intra) nationaly. This is a trend that doesn't seem to being slowed anytime soon, save for the occurence of a pandmeic of course. 

In fact, air travel has almost doubled between 2004 and 2019. With approximately 38.9 million flight performed by the global airline industry. 
- https://www.statista.com/statistics/564769/airline-industry-number-of-flights/

Knowing this, the motivation is clear. Air travel is here to stay. Being able to accurately predict flight delays can empower these airlines to improve their schedules, find delay patterns, deploy preventative measures, and send out warnings earlier. Which has the potential to save them a lot of money, but also improves the customer’s overall experience. 

---

# Included in this Project
- Explanatory Analysis Notebook
- Modeling Notebook
- Dashboard

# Part 1
### Explanatory Data Analysis
- Perform in-depth analysis of the data to identify patterns, trends, and connections
- Use pandas, numpy, and matplotlib to explore and visualize the data addressing specifically:
    - Categorical and Numerical data-types, missing values
    - Time series analysis
    - Correlations
    - Distributions

# Part 2
### Deployment of a Dashboard for Data Analysis
- can be run on remote streamlit server [link]()
- can also be deployed locally

```
git clone https://github.com/yemaney/flight_delay_prediction.git
python -m venv venv
source  venv/Scripts/activate
pip install -r requirments.txt
streamlit run streamlit_app.py
```
### Modeling
- Use inferences from `Part 1` to:
    - develop choose relevant features for modeling
    - to `feature engineer` new relevant features for modeling
- Use `scikit-learn` API to develop models
    - models attempted are:
        - logistic regression
        - Naive Bayes
        - Support Vector Machines
        - RandomForrestClassifier
        - XGBoost
- Evaluate models
    - Measure results 
        - with metrics:
            - accuracy
            - recall
            - precision
            - f1-score
        - With `Recall` being the metric of attention

    - Cross validate and plot performance for each model 
    - Grid-Search to hyperparameter tune the algorithms

- Deal with the class imbalance in the data using Synthetic Minority Oversampling Technique (SMOTE)
---
