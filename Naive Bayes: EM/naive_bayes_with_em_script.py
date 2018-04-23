import naive_bayes_em as nb
import numpy as np

x = nb.SemiNB()

data = np.genfromtxt('all_gun_data.csv',delimiter=',')

no_labels_data = np.copy(data)
no_labels_data = np.delete(no_labels_data, 15, axis=1)

y = data[:,15]
y = y[1:15222]

yc = np.tile(y, (2,1))
y2 = 1-yc[1]
y = np.transpose(np.vstack((y2, y)))

xl = np.transpose(no_labels_data[1:15222,:])
xul = np.transpose(no_labels_data[15222:23897,:])
x.train_semi(xl, y, xul)