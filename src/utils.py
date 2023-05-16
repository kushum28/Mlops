from datetime import datetime
import pandas as pd # version 1.1.3
import matplotlib.pyplot as plt


plt.style.use('ggplot')
# In[]
def parser(s):
    try: 
        to_return = datetime.strptime(str(s), '%m/%d/%Y %H:%M:%S')
    except:
        to_return = datetime.strptime(str(s), '%Y-%m-%d %H:%M:%S')
    return to_return

# In[]
def reset_index(dataframe):
    """ Reset the dataframe index """
    dataframe = dataframe.reset_index(
        inplace=False).drop(['index'], axis='columns')
    return dataframe