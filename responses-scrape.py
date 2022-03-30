#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
urllib3.disable_warnings()
import numpy as np
import datetime as dt     
date = dt.date.today


# In[2]:


master=pd.read_csv(f'data/foil_records_20180101_2022-03-27.csv')
linkData=master.copy()

data2022=linkData[linkData.date_submitted.str.contains("2022-")].reset_index(drop=True)
links2022=data2022.foil_link
ids2022=data2022.foil_id


# In[3]:


# url_base="https://a860-openrecords.nyc.gov/request/api/v1.0/responses?start=0&request_id="
# ids2022=["FOIL-2022-057-04259", "FOIL-2021-054-00084"]
# url_end='&with_template=true'
# URL=f'{url_base}{ids2022}{url_end}'


# In[6]:


# for ids in ids2022:
#     print(f'{url_base}{ids}{url_end}')

print(ids2022[2642])


# In[4]:


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome\
    /99.0.4844.83 Safari/537.36'
}


# In[ ]:


url_base="https://a860-openrecords.nyc.gov/request/api/v1.0/responses?start=0&request_id="
url_end='&with_template=true'

count=0
for eachId in ids2022[3642:]:
    count=count+1
    print(count,":", eachId)
    responses_list=[]
    response=requests.get(f'{url_base}{eachId}{url_end}', headers=headers, verify=False)
    response_text=response.json()['responses'] 
    response_count = response.json()['total']    

    if response_count != 0:
        for ele in response_text:
            responses_dict={}
            responses_dict['foil_id']=eachId

            doc=BeautifulSoup(ele['template'])

            for ele1 in doc.find_all('div', class_='row response-row'):
                responses_dict['r_number']="R"+ ele1.find(class_="col-md-1 response-row-num").text.strip()
                responses_dict['r_title']=ele1.find('strong').text.strip()
                responses_dict['r_date']=ele1.find("span", class_="flask-moment").text.strip()
            for script in doc.find_all("script"):
                responses_dict['r_body']= script.text.strip()
            for popup in doc.find_all('div', class_="modal fade"):
                responses_dict['popup_id']=popup.find('div', class_="response-id").text.strip()
                responses_dict['popup_title']=popup.find(class_="modal-title").text.strip()
                responses_dict['popup_body']=popup.find(class_="modal-body").text.strip()
                
            responses_list.append(responses_dict)
            
    else:
        
        no_responses_dict={}
        no_responses_dict['foil_id']=eachId

        no_responses_dict['r_number']="R0"
        no_responses_dict['r_title']="No responses"
        no_responses_dict['r_date']=np.nan
        no_responses_dict['r_body']= np.nan
        no_responses_dict['popup_id']=np.nan
        no_responses_dict['popup_title']=np.nan
        no_responses_dict['popup_body']=np.nan

        responses_list.append(no_responses_dict)

    df=pd.DataFrame(responses_list)
    df.to_csv(f'response-files/response-{eachId}.csv', index=False)


# In[18]:


ids2022[3642:]


# In[ ]:




