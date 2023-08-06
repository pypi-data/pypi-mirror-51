# GapLearn

GapLearn bridges gaps between other machine learning and deep learning tools. All models can be passed to the functions below regardless of the framework they were built upon (scikit-learn, tensorflow, xgboost, or even good ole numpy). 

My first package objective is to bring transparency to the often black-boxy model training process by making by making robust post-mortem analysis of the hyperparameter and feature selection processes possible. The functions below also further automate some processes while still giving the user full control of the results.

Many features are on their way. Unit tests and full documentation will be added shortly.

The source code is available on [GitHub](https://www.github.com/awhedon/gaplearn)

## Installation

```bash
pip install gaplearn
```

See the latest version on [PyPI](https://pypi.org/project/gaplearn/)

## Submodules

### cv

The `cv` submodule will have these classes (sfs has been released):

#### SFS
**Description:**
- This is a sequential feature selector that enables you to perform backwards elimination with any model (not just a linear regression).
- At each step, the feature that has the lowest permutation importance is selected for removal. The permutation importance is measured as the decrease in accuracy by default, but the user can pass any custom scoring function.

**Improvements on their way:**
- Add forward selection and all subsets testing
- Add more built-in scoring functions to for assessing feature permutation importance
- Create custom permutation scoring method to remove `eli5` as a dependency

##### Methods
**backwards_elimination(X, y, model, params = {}, fit_function = None, predict_function = None, score_function = None, score_name = 'score', cols = [], verbose = 0)**
- Run the backwards elimination
- **Params:**
	- X: (DataFrame or matrix) with independent variables
	- y: (iterable) dependent corresponding variable values
	- params: (dict) parameter set for model
	- model: a model architecture to be trained and evaluated
	- fit_function: (function) the function that will be used to train the model; the function must accept the parameters `model`, `X`, and `y`; if this value is not set, `backwards_elimination` will attempt to use your model's `fit` method
	- predict_function: (function) the function that will be used to make predictions with the model; the function must accept the parameters `model`, and `X`; if this value is not set, `backwards_elimination` will attempt to use your model's `predict` method
	- score_function: (function) the function that will be used to score the model and determine the feature permutation importance; the function must accept the parameters `y` and `preds`; if this value is not set, the accuracy will be used
	- score_name: (str) name of the score calculated by the `score_function`; 'score' by default
	- cols: (list) the names of the columns in the matrix or DataFrame
	- verbose: (0, 1, or 2) determines the amount of printing

**get_summary_be()**
- Get a summary of the results by step; this can be used to more robustly and holistically determine which feature set is ideal for your problem

**get_results_be()**
- Get the results for each observation within each step; this can be used to more robustly and holistically determine which feature set is ideal for your problem

**get_features_be()**
- Get all the features used in the sequential feature selection

**get_set_by_score_be(min_score = None, num_steps = 'all')**
- Get the n feature sets (n is determined by `num_steps`) that achieve a score greather than or equal to `min_score`
- **Params:**
 	- min_score: (float or int) the minumum score a feature set must achieve to be returned
 	- num_steps: (str or int) the number of feature sets to return; 'all' is the only valid str option

**get_set_by_features_be(num_features, max_features = None)**
- Get the all feature sets that have `num_features` features; if `max_features` is set, feature sets with between `num_features` and `max_features` features will be returned
- **Params:**
 	- num_features: (int) the number of features the returned feature set should have; functions as a minimum if `max_features` is set
 	- max_features: (int) the maximum number of features the returned feature sets should have


**Example 1:**
```python
#### Perform a backwards elimination with sci-kit learn's random forest model ####

import pandas as pd
from gaplearn.cv import SFS

X = pd.read_csv('X_classification.csv')
y = pd.read_csv('y_classification.csv')

fs = SFS()

print('The backwards elimination has been run: {}'.format(fs.be_complete)) # prints False

from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier()

# Run the backwards elimination
fs.backwards_elimination(X, y, model = rfc, params = {'n_jobs': -1})

# Get the step-by-step summary
summary = fs.get_summary_be() # Alternatively, `summary = fs.summary_be`

# Get the predictions and true values for each observation
results = fs.get_results_be() # Alternatively, `results = fs.results_be

# Get the features used in the analysis
features = fs.features_be # Alternatives, `sorted(list(results['feature to remove']))

# Identify which feature set can achieve at least 85% accuracy with the smallest number of features
at_least_85 = fs.get_set_by_score_be(min_score = .85, num_steps = 1)

# Identify the best model with only 4 features
features_4 = fs.get_set_by_features_be(num_features = 4)
```

**Example 2:**
```python
#### Perform a more complex backwards elimination with sci-kit learn's naive bayes model ####

import pandas as pd
from gaplearn.cv import SFS

from sklearn.linear_model import SGDRegressor

model_sgd = SGDRegressor(loss = 'modified_huber', penalty = 'elasticnet')

X = pd.read_csv('X_regression.csv')
y = pd.read_csv('y_regression.csv')

fs = SFS()

# Define a score_function
def mse(y, preds):
	score = sum([(preds[i] - y[i]) ** 2 for i in range(y.shape[0])]) / y.shape[0]
	return score

# Define a predict_function
def arbitrary_prediction(model, X):
	preds = model.predict(X) + 1 # arbitrarily deciding to add 1 to the prediction (realistically, this would be a wrapper for model that don't have a `fit` method)
	return preds

# Define a predict_function
def predict_w_proba(model, X):
	preds = [1 if x[1] > 0.6 else 0 for x in model.predict_proba(X)]
	return preds

# Run the backwards elimination
fs.backwards_elimination(X, y, model = model_sgd, predict_function = predict_w_proba, score_function = mse)

# Get the step-by-step summary
summary = fs.get_summary_be() # Alternatively, `summary = fs.summary_be`

# Get the predictions and true values for each observation
results = fs.get_results_be() # Alternatively, `results = fs.results_be`

# Get the features used in the analysis
features = fs.features_be # Alternatively, `sorted(list(results['feature to remove']))`

# Identify which two feature sets can achieve at least 85% accuracy with the smallest number of features
at_least_85 = fs.get_set_by_score_be(min_score = .85, num_steps = 2)

# Identify the best models with 3-5 features
features_3_5 = fs.get_set_by_features_be(num_features = 3, max_features = 5)
```

#### SearchCluster
**Description:**
- This is a hyperparameter grid/random search for clustering algorithms
- Unlike other grid/random search algorithms, this one enables you to get the observation-by-observation results from each parameter set so that you can do deep post-mortem analysis of the grid/random search.

**Documentation:**
Coming soon. See the documentation for details, in the meantime: https://github.com/awhedon/gaplearn
##### Methods
**search_cluster(model, params, X, cols = None, fit_function = None, label_function = None, centroid_function = None, score_function = None, metric_name = 'score', random = None, centroid = False, verbose = 0)**
- Run the grid/random hyperparameter search
- **Params:**
	- model: a model architecture to be trained and evaluated
	- params: (dict) the hypterparameter grid (ex.: {'C': [0.1, 0.5, 0.9], ...})
	- X: (DataFrame or matrix) features to be used for clustering
	- cols: (list) the names of the columns in the matrix or DataFrame
	- fit_function: (function) the function that will be used to train the model; the function must accept the parameters `model`, `params`, and `X`; if this value is not set, `search_cluster` will attempt to use your model's `fit` method
	- label_function: (function) the function that will use the trained model to attach labels to the unseen data; the function must accept the parameter `model`; if this value is not set, `search_cluster` will attempt to extract your model's `labels_` attribute value
	- centroid_function: (function) the function that will extract the cluster centroids from the trained model; the function must accept the parameter `model`; if this value is not set, `search_cluster` will attempt to extract your model's `cluster_centers_` attribute value
	- score_function: (function) the function that will score the results from the trained model; the function must accept the parameters `X` and `labels`; if this value is not set, `search_cluster` will calculate the silhouette score
	- metric_name: (str) the name of the evaluation metric; 'score' is the default
	- random: (int or float) if int, the maximum number of parameter sets to use; if float, the percentage of parameter sets to use (.7 means that 70% of the available parameter sets will be used for testing); default is None, which means that all parameter sets will be used
	- centroid: (bool) if the model is centroid-based, you can set this to True and define a `centroid_function` (or leave it as None if the model has a `cluster_centers_` attribute) so that the cluster centers will be extracted
	- verbose: (0 or 1) determines the amount of printing

**get_best_model(return_scores = False)**

**get_best_models(n = 1, return_scores= False)**

**get_best_params()**

**get_labels()**

**get_param_results()**


**Example 1:**
```python
from gaplearn.cv import SearchCluster
import pandas as pd

from sklearn import KMeans

sc = SearchCluster()

X = pd.read_csv('X_clustering.csv')

params = {'': , '': [], '': []}

# Run the hyperparameter grid search
sc.search_cluster(model = KMeans, params = params, X = X, centroid = True)

# Get the best model
best_model = sc.get_best_model() # Alternatively, `best_model = sc.best_model`

# Get the five best models and their performance
best_models_5, best_models_5_scores = sc.get_best_models(n = 5, return_scores = True)

# Get the model params that performed best
best_params = sc.get_best_params() # Alternatively, `best_params = sc.best_params`

# Get a summary of the results for each parameter set
param_results = sc.get_param_results() # Alternatively, `param_results = sc.param_results`

# Get the labels for each observation for each parameter set's k-fold validation to robustly analyze the differences in performance
labels = sc.get_labels() # Alternatively, `labels = sc.labels_df`
```

**Example 2:**
```python
from gaplearn.cv import SearchCluster
import pandas as pd
import random

from my_module import ModelClass

sc = SearchCluster()

X = pd.read_csv('X_clustering.csv')

params = {'param1': ['value1', 'value2', 'value3'], 'param2': ['value1', 'value2', 'value3'], 'param3': ['value1', 'value2', 'value3']}

def fit_function(model, params, X):
	model(**params).fit_my_model(X)
	return model

def score_function(X, labels):
	score = random.random()
	return score

# Run the hyperparameter random search, testing 50% of the parameter sets
sc.search_cluster(model = KMeans, params = params, X = X, fit_function = fit_function, score_function = score_function, random = 0.5)

# Get the best model and results
best_model, best_model_scores = sc.get_best_model(return_scores = True)

# Get the five best models and their performance
best_models_5, best_models_5_scores = sc.get_best_models(n = 5, return_scores = True)

# Get the model params that performed best
best_params = sc.get_best_params() # Alternatively, `best_params = sc.best_params`

# Get a summary of the results for each parameter set
param_results = sc.get_param_results() # Alternatively, `param_results = sc.param_results`

# Get the labels for each observation for each parameter set's k-fold validation to robustly analyze the differences in performance
labels = sc.get_labels() # Alternatively, `labels = sc.labels_df`
```

#### Search (in development)
**Description:**
- This is a hyperparameter grid/random search for both regression algorithms and classification algorithms
- Unlike other grid/random search algorithms, this one enables you to get the observation-by-observation results from each parameter set so that you can do deep post-mortem analysis of the grid/random search.

### data_eng

The `data_eng` submodule will have these classes:

#### DistributedSQL (in development)
**Description:**
- This enables users to chunk multi-parameter sql queries and process them on multiple threads.