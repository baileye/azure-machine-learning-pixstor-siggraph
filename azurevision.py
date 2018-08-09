import logging
import requests

from arcapix.search.metadata.plugins.base import Plugin, PluginStatus
from arcapix.search.metadata.helpers import Metadata
from arcapix.search.metadata.utils import load_image

logger = logging.getLogger(__name__)

# FOR TESTING ONLY!
logger.setLevel(logging.INFO)

class AzureComputerVisionPlugin(Plugin):

    def namespace(self):
        return 'image'
        
    def handles(self, ext=None, mimetype=None):
        #logger.info('azure computer vision')
        return mimetype and mimetype.startswith('image/')
        
    def schema(self):
        return [{
            "name": "computervision",
            "prompt": "Tags from Microsoft Cognitive Services Computer Vision API",
            "value": {
                "datatype": "[String]"
                }
            }]
    
    def _extract(self, filename):
        values = azure_computervision(filename)
        
        return {'computervision': values}
        
    def process(self, id_, file_, fileinfo=None):
        try:
            data = self._extract(file_)
            
            if Metadata(id_, self).update(data):
                return PluginStatus.SUCCESS
            
            return PluginStatus.ERRORED
        
        except:
            logger.exception("Error while processing %r (%s)", file_, id_)
            return PluginStatus.FATAL


def azure_computervision(filename):
    """
    Get a Microsoft Cognitive Services Computer Vision tags from the API.
    This is a generic computer vision API that can be called on images and URLs
    """

    # Change this to your subscription key
    subscription_key = "<INSERT SUBSCRIPTION KEY HERE>"
    assert subscription_key

    # Change this to your API endpoint - it will change based on the region you select
    vision_base_url = "https://northeurope.api.cognitive.microsoft.com/vision/v2.0/"

    analyze_url = vision_base_url + "analyze"
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/octet-stream'}
    params     = {'visualFeatures': 'Categories,Description,Color'}

    with open(filename, mode="rb") as image_data:
        response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
        
        response.raise_for_status()
        analysis = response.json()
        
        image_tags = analysis["description"]["tags"]
        
        tags = list()
        count = 0

        for prediction in image_tags:
            if count < 5:
                tags.append(prediction)
                count += 1
        
        return tags
