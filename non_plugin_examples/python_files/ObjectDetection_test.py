
# coding: utf-8

# In[2]:

# ON YOUR MACHINE CMD: pip install azure-cognitiveservices-vision-customvision

from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models


# In[21]:

project_id = "<PROJECT ID>"
prediction_key = "<PREDICTION KEY>"
iteration_id = "<ITERATION ID>"

predictor = prediction_endpoint.PredictionEndpoint(prediction_key)

# Open the sample image and get back the prediction results.
with open("<FILE NAME>.jpg", mode="rb") as test_data:
    results = predictor.predict_image(project_id, test_data, iteration_id)
    tags = list()
    
    for prediction in results.predictions:
        if prediction.probability > 0.2:
            tags.append(prediction.tag_name)
            
    if len(tags) == 0:
        tags.append("nothing found")

print(tags)
print(type(tags))

