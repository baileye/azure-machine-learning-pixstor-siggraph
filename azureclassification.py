import logging

from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models

from arcapix.search.metadata.plugins.base import Plugin, PluginStatus
from arcapix.search.metadata.helpers import Metadata
from arcapix.search.metadata.utils import load_image

logger = logging.getLogger(__name__)

class AzureClassificationPlugin(Plugin):

    def namespace(self):
        return 'image'
        
    def handles(self, ext=None, mimetype=None):
        return mimetype and mimetype.startswith('image/')
        
    def schema(self):
        return [{
            "name": "azureclassification",
            "prompt": "Tags from Azure Classification API",
            "value": {
                "datatype": "[String]"
                }
            }]
    
    def _extract(self, filename):
        values = azure_classification(filename)
        
        return {'azureclassification': values}
        
    def process(self, id_, file_, fileinfo=None):
        try:
            data = self._extract(file_)
            
            if Metadata(id_, self).update(data):
                return PluginStatus.SUCCESS
            
            return PluginStatus.ERRORED
        
        except:
            logger.exception("Error while processing %r (%s)", file_, id_)
            return PluginStatus.FATAL


def azure_classification(filename):
    """Get an azure classification from the Azure Custom Vision API for an image.
    
    """

    # Azure API Call
    project_id = "<PROJECT ID>"
    prediction_key = "<PREDICTION KEY>"
    iteration_id = "<MODEL ITERATION ID>"

    predictor = prediction_endpoint.PredictionEndpoint(prediction_key)
    with open(filename, mode="rb") as image_data:
        results = predictor.predict_image(project_id, image_data, iteration_id)
        tags = list()
        for prediction in results.predictions:
            if prediction.probability > 0.1:
                tags.append(prediction.tag_name)
        return tags