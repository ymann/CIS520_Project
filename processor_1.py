
# coding: utf-8

# In[ ]:


import pandas as pd
import json
import csv


# In[ ]:


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

data_df = pd.DataFrame.from_csv('~/Downloads/Articles-with-extracted-info.tsv', sep='\t')


# In[ ]:


df = pd.DataFrame()
list_of_keys = []


# In[ ]:


def flattener(x):
    return flatten_json(json.loads(x))

def strip_keys(x):
    return list(x.values())


# In[ ]:


df_json = pd.DataFrame(data_df['Json'])
df_json = df_json.reset_index()
df_json = df_json.Json
df_json = df_json.apply(flattener, 1)


# In[ ]:


list_of_keys = list(df_json.iloc[0].keys())


# In[ ]:


df_json = df_json.apply(strip_keys, 1)


# In[ ]:


df_json.apply(pd.Series)
print(df_json.head(1))
# df_json[40]


# In[ ]:


# df_json.to_csv('data.csv', index=False)

