#!/usr/bin/env python
# coding: utf-8

# In[73]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# In[74]:


database = pd.read_csv('database.csv')
mexico = pd.read_csv('database_prediction.csv')


# In[75]:


last_column = database[database.columns[-1]]
mexico_last_column = mexico[mexico.columns[-1]]


# In[76]:


differences = abs(last_column - mexico_last_column[0])
paises_parecidos = differences.sort_values()[0:7]


# In[77]:


database = database.T
mexico = mexico.T


# In[78]:


database_paises_parecidos = database[paises_parecidos.index]


# In[79]:


paises_to_plot = pd.concat([mexico,database_paises_parecidos],axis=1)


# In[80]:


paises_to_plot.plot(title='Comparativa de México con otros países')
plt.xlabel('Día')
plt.ylabel('Casos Confirmados')
plt.grid(True,linestyle='--')
plt.xticks(range(0,100,10),range(0,100,10))
plt.savefig('Figure',dpi=600)
#plt.show()

