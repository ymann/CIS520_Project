import numpy as np
import pandas as pd
import math

from sklearn.neural_network import MLPClassifier as mlp
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.model_selection import train_test_split


np.set_printoptions(threshold=np.inf)

data = np.genfromtxt('all_gun_data.csv',delimiter=',')

no_labels_data = np.copy(data)
no_labels_data = np.delete(no_labels_data, 15, axis=1)

y = data[:,15]
y = y[1:15222]


xl = no_labels_data[1:15222,:]
xul = no_labels_data[15222:23897,:]

X_train, X_test, y_train, y_test = train_test_split(xl, y)


# Normalize data
scaler = StandardScaler()  
scaler.fit(X_train)  
X_train = scaler.transform(X_train)  

X_test = scaler.transform(X_test)  

clf = mlp(solver='adam', hidden_layer_sizes=(100, 100, 100), alpha=.00001)

clf.fit(X_train, y_train)                         
predictions = clf.predict(X_test)

num_errors = np.sum(y_test != predictions)
num_instances = len(predictions)
error_rate = num_errors / num_instances

print("Error rate: " + str(error_rate))

num_correct_ones = np.sum(predictions[y_test == 1] == 1)
num_ones = np.sum(y_test == 1)
tpr = num_correct_ones / num_ones

num_correct_zeros = np.sum(predictions[y_test == 0] == 0)
num_zeros = np.sum(y_test == 0)
tnr = num_correct_zeros / num_zeros

print("TPR: " + str(tpr))
print("TNR: " + str(tnr))
am = (tpr + tnr) / 2
gm = math.sqrt(tpr * tnr)

print("AM: " + str(am))
print("GM: " + str(gm))
