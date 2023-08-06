# ddplt

Useful utility functions for evaluation of ML.

**Motivation:**
The main motivation behind this package is to create a single place where the utility functions for ML projects are located. These functions represent the best I was able to scrape from various tutorials or offical documentation on the web.


## Confusion matrix

This function prints and plots the confusion matrix.

The code:

```python
import numpy as np
from ddplt import plot_confusion_matrix

y_test = np.array([0, 0, 1, 1, 2, 0])
y_pred = np.array([0, 1, 1, 2, 2, 0])
class_names = np.array(['hip', 'hop', 'pop'])
ax, cm = plot_confusion_matrix(y_test, y_pred, class_names)
```

will create a plot like:
![conf_matrix](img/cm_hip_hop_pop.png)


## Learning curve

Create plot showing performance evaluation for different sizes of training data. The method should accept: 
- existing `Axes`
- performance measure (e.g. accuracy, MSE, precision, recall, etc.)
- ...


## ROC curve

Plot showing Receiver Operating Characteristics of a predictor.


## Correlation heatmap

Grid where each square has a color denoting strength of a correlation between predictors. You can choose between Pearson and Spearman correlation coefficient, the result is shown inside the square. 

