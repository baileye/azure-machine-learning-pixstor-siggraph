
# coding: utf-8

# In[15]:

import requests

subscription_key = "<SUBSCRIPTION KEY>"
assert subscription_key

vision_base_url = "https://<DATA CENTER REGION>.api.cognitive.microsoft.com/vision/v2.0/"

analyze_url = vision_base_url + "analyze"
headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/octet-stream'}
params     = {'visualFeatures': 'Categories,Description,Color'}

with open("<FILE NAME>.jpg", mode="rb") as image_data:
    response = requests.post(
    analyze_url, headers=headers, params=params, data=image_data)
        
    response.raise_for_status()
    analysis = response.json()
    print(analysis)
        
    image_tags = analysis["description"]["tags"]
    print(image_tags)
    
    
    tags = list()
    count = 0
    for prediction in image_tags:
        if count < 5:
            tags.append(prediction)
            count += 1

    print(tags)
    print(type(tags))
        

