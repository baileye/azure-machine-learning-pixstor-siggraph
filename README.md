# Azure Cognitive Services with PixStor

This repository will cover how to set up a plugin for [PixStor](https://www.pixitmedia.com/pixstor/) that uses [Microsoft Cognitive Services](https://azure.microsoft.com/en-gb/services/cognitive-services/) to add information about your image archive. The code and contents here are intended as a sample and proof-of-concept only.

# Repo contents

- [azurevision.py](azurevision.py)
   - Plugin that uses the Azure [Computer Vision API](https://azure.microsoft.com/en-gb/services/cognitive-services/computer-vision/) to generate a set of tags for the image. This is a generic service and will work on a wide-array of images but it is not designed for specific classification models or problems. This plugin and API is a great first start to using Machine Learning to add information about your image archive.
- [azureclassification.py](azureclassification.py)
  - Plugin that uses the Azure [Custom Vision Service](https://azure.microsoft.com/en-gb/services/cognitive-services/custom-vision-service/). This plugin has a trained model that classifies each image based on the custom trained model. This service is designed to help you answer a specific question about your images, for example "is this a photo of a a wood texture?", or "is this wood grain or chipboard?"
- [azureobjectdetection.py](azureobjectdetection.py)
   - [Object Detection](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/python-tutorial-od)


# Instructions

The instructions are split into using the standard Azure Vision API, the Custom Vision service for classification, and the Custom Vision service for object detection. You will need an Azure account to make use of Microsoft Cognitive Services.

## Azure Vision API

- Set up the vision API in your subscription. You can [start a trial and see your API keys here](https://azure.microsoft.com/en-us/try/cognitive-services/my-apis/). If you have previously set up a trial, you will have to create a vision key in the [Azure Portal](https://portal.azure.com/). Click on ' Create a resource' and search for 'Computer Vision'. Follow the steps in the portal to set up the Computer Vision service.
- Edit the [azurevision.py](azurevision.py) file and change the 'azure_api_key' variable to be your key. Change the variable 'azure_endpoint' to your API endpoint
    - To find your key and API endpoint in the portal click on the resource group you used when creating your Computer Vision service. Then click on the Computer Vision service. If the 'Quick Start' tab hasn't opened click on the sidebar to show it. That page will have your API key and the API endpoint you need.
- Copy the [azurevision.py](azurevision.py)

## Azure Custom Vision Service

In V2 we are able to build a classification model that is built on images you can submit that are specific to your problem.

**One example is:** given a set of images of films (Paddington 2, Wonderwoman, Star Wars: Last jedi ...) can the model predict the correct film given a new image.


## Deployment Steps:
### Create Project
- Visit [https://www.customvision.ai/](https://www.customvision.ai/) and sign in with your Azure credentials

![Custom Vision Sign in Website](images/customvision.JPG "Custom Vision Sign in Website")

- Create a new project

![Create new project](images/newproject.JPG "Create new project")

- Set up the question/problem by entering project details:
  - **Name** of project
  - **Description** of what the project does
  - **Domains:** These are pre-trained models that your model will be built off. This is a [form of transfer learning](https://en.wikipedia.org/wiki/Transfer_learning). Choose your base model and build on top. If non of the specific base models suit, choose general.
  - **Resource Group:** In the drop down you should see the previously created Azure Resource group when you created the Azure Storage account and Azure Function
  - Finally click **Create Project**
![New Project Details](images/newprojectdetails.JPG "New Project Details")

- On the new project dashboard, choose **Add Images**
![project dashboard](images/newprojectdashboard.JPG "Project Dashboard")
- Upload a set of images that you have as a set - these are called a class. So for example all images of the Paddington 2 film
![Add Images](images/addimages.JPG "Add Images")
- Add a 'tag' or 'category' to these images
![Tag Images](images/addclass.JPG "Tag Images")
- Upload those files
![Complete Upload](images/completeupload.JPG "Complete Upload")
- Now you have added one class for your classification problem, now add more in the same way ...
![Add Another Class](images/addanotherclass.JPG "Add Another Class")
- Once you ahve added all training images and classes, its ready to train the specific model. Choose the **Train** button in the top menu bar
![Train Model](images/train.JPG "Train Model")
- View the first training results. For only a few images this is good and we will see this improve overtime
![First Training Results](images/firsttrainresults.JPG "First Training Results")

### Test the API
- Lets now test the trained API with a new image. Choose Quick test and upload an image to your API via the UI
![Quick Test](images/quicktest.JPG "Quick Test")
![Test Image Results](images/testimageresults.JPG "Test Image Results")

### Retrain the API
- Now you have tested an image you can feed this information back into the model so the model is always improving and updating. In the **Predictions** tab you will now see the images you submitted to your model
![Predictions Tab](images/predictions.JPG "Predicitions Tab")
- Select an image and confirm the correct tag for the image
![Confirm Prediction](images/confirmprediction.JPG "Confirm Prediction")
- Now see that image appear in your training images tab
![Added to Training Images](images/convertedtotraining.JPG "Added to Training Images")
- Choose the train button again and see iteration 2 improve the performance of your model
![Retrain Results](images/retrain.JPG "Retrain Results")




## Background

[PixStor](https://www.pixitmedia.com/pixstor/) is a high performance, highly scalable, enterprise-class storage solution specifically designed for Media & Entertainment workflows. PixStor combines flash, disk, tape and cloud storage with affordable, high performance Ethernet into a unified system that’s higher performing, limitless in scale and lower cost than traditional legacy solutions. Data moves seamlessly through many tiers of storage – from fast flash to cost-effective, high capacity object storage, all the way out to the cloud – depending on how frequently it needs to be accessed. This allows media organizations to accelerate high resolution workflows and store valuable assets more safely and economically.

[Microsoft Cognitive Services](https://azure.microsoft.com/en-gb/services/cognitive-services/) are a set of APIs, SDKs and services available to developers to make their applications more intelligent, engaging and discoverable. Microsoft Cognitive Services expands on Microsoft’s evolving portfolio of machine learning APIs and enables developers to easily add intelligent features – such as emotion and video detection; facial, speech and vision recognition; and speech and language understanding – into their applications. Our vision is for more personal computing experiences and enhanced productivity aided by systems that increasingly can see, hear, speak, understand and even begin to reason.


