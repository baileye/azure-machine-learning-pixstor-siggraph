import logging

from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models

from arcapix.search.metadata.plugins.base import Plugin, PluginStatus
from arcapix.search.metadata.helpers import Metadata
from arcapix.search.metadata.utils import load_image

logger = logging.getLogger(__name__)

# FOR TESTING ONLY!
logger.setLevel(logging.INFO)

class AzureObjectDetectionPlugin(Plugin):

    def namespace(self):
        return 'image'
        
    def handles(self, ext=None, mimetype=None):
        #logger.info('objectdetection')
        return mimetype and mimetype.startswith('image/')
        
    def schema(self):
        return [{
            "name": "objectdetection",
            "prompt": "Tags from Cognitive Services Object Detection trained model API",
            "value": {
                "datatype": "[String]"
                }
            }]
    
    def _extract(self, filename):
        values = azure_objectdetection(filename)
        
        return {'objectdetection': values}
        
    def process(self, id_, file_, fileinfo=None):
        try:
            data = self._extract(file_)
            
            if Metadata(id_, self).update(data):
                return PluginStatus.SUCCESS
            
            return PluginStatus.ERRORED
        
        except:
            logger.exception("Error while processing %r (%s)", file_, id_)
            return PluginStatus.FATAL


def azure_objectdetection(filename):
    """
    Get an azure object detection result from the Azure Custom Vision API for an image.
    
    """
    # Change these to your custom vision keys
    project_id = "PROJECT ID"
    prediction_key = "PREDICTION KEY"
    iteration_id = "MODEL ITERATION ID"

    predictor = prediction_endpoint.PredictionEndpoint(prediction_key)

    # Open the sample image and get back the prediction results.
    with open(filename, mode="rb") as image_data:
        results = predictor.predict_image(project_id, image_data, iteration_id)
        tags = list()
        for prediction in results.predictions:
            if prediction.probability > 0.2:
                tags.append(prediction.tag_name)
        if len(tags) == 0:
            tags.append("nothing found")
        
        return tags