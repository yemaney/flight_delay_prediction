# Flight Delay Prediction

<img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1053&q=80">


---
# Motivation

The world has become globalized, and one consequence of this fact is the increasing amount of travel, both (inter) and (intra) nationaly. This is a trend that doesn't seem to being slowed anytime soon, save for the occurence of a pandmeic of course. 

In fact, air travel has almost doubled between 2004 and 2019. With approximately 38.9 million flight performed by the global airline industry. 
- https://www.statista.com/statistics/564769/airline-industry-number-of-flights/

Knowing this, the motivation is clear. Air travel is here to stay. Being able to accurately predict flight delays can empower these airlines to improve their schedules, find delay patterns, deploy preventative measures, and send out warnings earlier. Which would not only has the potential to save them a lot of money, but also improves the customers overall experience. 

---

# Included in this Project
- Explanatory Analysis Notebook
- Modeling Notebook
- common
    - custom scripts used in EDA Notebook
# Part 1
### Explanatory Data Analysis
- Perform in-depth analysis of the data to identify patterns, trends, and connections
- Use pandas, numpy, and matplotlib to explore and visualize the data addressing specifically:
    - Categorical and Numerical data-types, missing values
    - Time series analysis
    - Correlations
    - Distributions
# Part 2
### Modeling
- Use inferences from `Part 1` to:
    - develop choose relevant features for modeling
    - to `feature engineer` new relevant features for modeling
- Use `scikit-learn` api to develop models
    - models attempted are:
        - logistic regression
        - RandomForrestClassifier
        - XGBoost
- Evaluate models
    - Crossvalidate results 
        - with metrics:
            - accuracy
            - recall
    - GridSearch:
        - Hyper-parameter tuning for best model
---