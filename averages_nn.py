import numpy as np
import pandas as pd
import scipy.io as sio

from sklearn.neural_network import MLPClassifier as mlp
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.model_selection import train_test_split



# Normalize data
scaler = StandardScaler()  
scaler.fit(X_train)  
X_train = scaler.transform(X_train)  

X_test = scaler.transform(X_test)  


clf = mlp(solver='adam', hidden_layer_sizes=(100, 100, 100), alpha=.00001)

clf.fit(X_train, y_train)                         
predictions = clf.predict(X_test)
num_correct_intentional_shootings = np.sum(predictions[y_test == 1] == 1)
num_intentional_shootings = np.sum(y_test == 1)
intentional_shooting_error_rate = 1 - num_correct_intentional_shootings / num_intentional_shootings

num_errors = np.sum(y_test != predictions)
num_instances = len(predictions)
error_rate = num_errors / num_instances

print("False negative rate: " + str(intentional_shooting_error_rate))
print("Error rate: " + str(error_rate))
