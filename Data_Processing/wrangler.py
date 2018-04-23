
# coding: utf-8

# In[21]:


import pandas as pd
import json
import csv
import os
import re


# In[35]:


f = open("all_avg_gun_data_svm_minus_labels.csv", "w+")


# In[37]:


with open("avgs_gun_data.csv", "r") as inp:
    for line in inp:
        data = line.split(',')
        count = 1;
        for i in data:
            if(not(count == 16)):
                f.write(str(count) + ":" + str(i) + " ")
            count = count + 1;
    


# In[ ]:


data_df = pd.DataFrame.from_csv('Articles-with-extracted-info.tsv', sep='\t')


# In[ ]:


f = open("all_gun_data_svm_minus_labels.csv", "w+")
l = open("labels.csv", "w+")


# In[ ]:


shots_fired_dict = {'' : -1}
type_of_gun_dict = {'' : -1}
city_dict = {'':-1}
for i, row in data_df.iterrows():
    feat_num = 1
    data_json = json.loads(row['Json'])
    # Handle circumstances
    shots_fired = data_json['circumstances']['number-of-shots-fired']['value']
    if(not(shots_fired in shots_fired_dict)):
        shots_fired_dict[shots_fired] = len(shots_fired_dict) - 1
    if(not(shots_fired == '')):
        f.write(str(feat_num) + ":" + str(shots_fired_dict[shots_fired]))
    feat_num = feat_num + 1

    gun_type = data_json['circumstances']['type-of-gun']['value']
    if(not(gun_type in type_of_gun_dict)):
        type_of_gun_dict[gun_type] = len(type_of_gun_dict) - 1
    if(not(gun_type == '')):
        f.write(" " + str(feat_num) + ":" + str(type_of_gun_dict[gun_type]))
    feat_num = feat_num + 1

    # Handle date-and-time
    city = data_json['date-and-time']['city']['value']
    if(not(city in city_dict)):
        city_dict[city] = len(city_dict) - 1
    if(not(city == '')):
        f.write(" " + str(feat_num) + ":" + str(city_dict[city]))
    feat_num = feat_num + 1

    # Handle radios 1-3
    for j in range(1,4):
        for key in data_json['radio' + str(j)]:
            if(not(feat_num == 16)):
                if(data_json['radio' + str(j)][key] == 'Yes'):
                    f.write(" " + str(feat_num) + ":1")
                elif (data_json['radio' + str(j)][key] == 'No'):
                    f.write(" " + str(feat_num) + ":0")
            feat_num = feat_num + 1

    # Handle shooters
    num_male = 0
    num_female = 0
    cum_age = 0
    shooter_json = data_json['shooter-section']
    for shooter in shooter_json:
        age_list = re.findall(r'^\D*(\d+)', shooter['age']['value'])
        if(age_list):
            cum_age = cum_age + int(age_list[0])
        if(shooter['gender'] == 'Male'):
            num_male = num_male + 1
        if(shooter['gender'] == 'Female'):
            num_female = num_female + 1
    if (cum_age == 0):
        age = -1
    else:
        age = cum_age / len(shooter_json)

    f.write(" " + str(feat_num) + ":" + str(num_male))
    feat_num = feat_num + 1
    f.write(" " + str(feat_num) + ":" + str(num_female))
    feat_num = feat_num + 1
    if(not(age == -1)):
        f.write(" " + str(feat_num) + ":" + str(age))
    feat_num = feat_num + 1



    # Handle victims
    male_vics = 0
    female_vics = 0
    cumv_age = 0
    num_killed = 0
    num_hosp = 0
    num_inj = 0
    victim_json = data_json['victim-section']
    for victim in victim_json:
        age_list = re.findall(r'^\D*(\d+)', shooter['age']['value'])
        if(age_list):
            cumv_age = cumv_age + int(age_list[0])
        if(victim['gender'] == 'Male'):
            male_vics = male_vics + 1
        if(victim['gender'] == 'Female'):
            female_vics = female_vics + 1
        was_list = victim['victim-was']
        if('killed' in was_list):
            num_killed = num_killed + 1
        elif('hospitalized' in was_list):
            num_hosp = num_hosp + 1
        elif('injured' in was_list):
            num_inj = num_inj + 1

    if (cumv_age == 0):
        v_age = -1
    else:
        v_age = cumv_age / len(victim_json)
    f.write(" " + str(feat_num) + ":" + str(male_vics))
    feat_num = feat_num + 1
    f.write(" " + str(feat_num) + ":" + str(female_vics))
    feat_num = feat_num + 1
    if(not(v_age == -1)):
        f.write(" " + str(feat_num) + ":" + str(v_age))
    feat_num = feat_num + 1
    f.write(" " + str(feat_num) + ":" + str(num_killed))
    feat_num = feat_num + 1
    f.write(" " + str(feat_num) + ":" + str(num_hosp))
    feat_num = feat_num + 1
    f.write(" " + str(feat_num) + ":" + str(num_inj))
    feat_num = feat_num + 1


    f.write('\n')


# In[ ]:


for i, row in data_df.iterrows():
    data_json = json.loads(row['Json'])
    if(data_json['radio' + str(j)][key] == 'Yes'):
        l.write("1\n")
    elif (data_json['radio' + str(j)][key] == 'No'):
        l.write("-1\n")
    else:
        l.write("0\n")


# In[ ]:


f = open("all_gun_data.csv", "w+")


# In[ ]:


shots_fired_dict = {'' : -1}
type_of_gun_dict = {'' : -1}
city_dict = {'':-1}

for i, row in data_df.iterrows():
    data_json = json.loads(row['Json'])
    # Handle circumstances
    shots_fired = data_json['circumstances']['number-of-shots-fired']['value']
    if(not(shots_fired in shots_fired_dict)):
        shots_fired_dict[shots_fired] = len(shots_fired_dict) - 1
    f.write(str(shots_fired_dict[shots_fired]) + ', ')
    
    gun_type = data_json['circumstances']['type-of-gun']['value']
    if(not(gun_type in type_of_gun_dict)):
        type_of_gun_dict[gun_type] = len(type_of_gun_dict) - 1
    f.write(str(type_of_gun_dict[gun_type]) + ', ')
    
    # Handle date-and-time
    city = data_json['date-and-time']['city']['value']
    if(not(city in city_dict)):
        city_dict[city] = len(city_dict) - 1
    f.write(str(city_dict[city]) + ', ')
    
    # Handle radios 1-3
    for j in range(1,4):
        for key in data_json['radio' + str(j)]:
            if(data_json['radio' + str(j)][key] == 'Yes'):
                f.write('1, ')
            elif (data_json['radio' + str(j)][key] == 'No'):
                f.write('0, ')
            else:
                f.write('-1, ')
    
    # Handle shooters
    num_male = 0
    num_female = 0
    cum_age = 0
    shooter_json = data_json['shooter-section']
    for shooter in shooter_json:
        age_list = re.findall(r'^\D*(\d+)', shooter['age']['value'])
        if(age_list):
            cum_age = cum_age + int(age_list[0])
        if(shooter['gender'] == 'Male'):
            num_male = num_male + 1
        if(shooter['gender'] == 'Female'):
            num_female = num_female + 1
    if (cum_age == 0):
        age = -1
    else:
        age = cum_age / len(shooter_json)
        
    f.write(str(num_male) + ", " + str(num_female) + ", " + str(age) + ", ")
    
    
    
    # Handle victims
    male_vics = 0
    female_vics = 0
    cumv_age = 0
    num_killed = 0
    num_hosp = 0
    num_inj = 0
    victim_json = data_json['victim-section']
    for victim in victim_json:
        age_list = re.findall(r'^\D*(\d+)', shooter['age']['value'])
        if(age_list):
            cumv_age = cumv_age + int(age_list[0])
        if(victim['gender'] == 'Male'):
            male_vics = male_vics + 1
        if(victim['gender'] == 'Female'):
            female_vics = female_vics + 1
        was_list = victim['victim-was']
        if('killed' in was_list):
            num_killed = num_killed + 1
        elif('hospitalized' in was_list):
            num_hosp = num_hosp + 1
        elif('injured' in was_list):
            num_inj = num_inj + 1
            
    if (cumv_age == 0):
        v_age = -1
    else:
        v_age = cumv_age / len(victim_json)
        
    f.write(str(male_vics) + ", " + str(female_vics) + ", " + str(v_age) + ", " + 
           str(num_killed) + ", " + str(num_hosp) + ", " + str(num_inj))
            
    
    f.write('\n')


# In[ ]:


f.close();


# In[ ]:


s = open("shots_fired_dict.txt", "w+")
for key in shots_fired_dict:
    s.write(key +"\t" + str(shots_fired_dict[key]) + '\n')
s.close();


# In[ ]:


t = open("type_of_gun_dict.txt", "w+")
for key in type_of_gun_dict:
    t.write(key +"\t" + str(type_of_gun_dict[key]) + '\n')
t.close();


# In[ ]:


c = open("city_dict.txt", "w+")
for key in city_dict:
    c.write(key +"\t" + str(city_dict[key]) + '\n')
c.close();


# In[ ]:


json.loads(data_df['Json'][12])

