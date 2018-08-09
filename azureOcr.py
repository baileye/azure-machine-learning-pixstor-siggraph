import logging
import requests

from arcapix.search.metadata.plugins.base import Plugin, PluginStatus
from arcapix.search.metadata.helpers import Metadata
from arcapix.search.metadata.utils import load_image

logger = logging.getLogger(__name__)

class AzureOcrPlugin(Plugin):

    def namespace(self):
        return 'image'
        
    def handles(self, ext=None, mimetype=None):
        return mimetype and mimetype.startswith('image/')
        
    def schema(self):
        return [{
            "name": "ocr",
            "prompt": "OCR from Microsoft Cognitive Services Computer Vision API",
            "value": {
                "datatype": "[String]"
                }
            }]
    
    def _extract(self, filename):
        values = azure_ocr(filename)
        
        return {'ocr': values}
        
    def process(self, id_, file_, fileinfo=None):
        try:
            data = self._extract(file_)
            
            if Metadata(id_, self).update(data):
                return PluginStatus.SUCCESS
            
            return PluginStatus.ERRORED
        
        except:
            logger.exception("Error while processing %r (%s)", file_, id_)
            return PluginStatus.FATAL


def azure_ocr(filename):
    """
    Get a Microsoft Cognitive Services Computer Vision OCR from the API.
    This is a generic computer vision API that can be called on images and URLs
    """

    # Change this to your subscription key
    subscription_key = "df5d088dd5214fae8deb20c7c7fbbcfa"
    assert subscription_key

    # Change this to your API endpoint - it will change based on the region you select
    vision_base_url = "https://northeurope.api.cognitive.microsoft.com/vision/v2.0/"

    analyze_url = vision_base_url + "ocr"
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/octet-stream'}
    params     = {'language': 'en', 'detectOrientation': 'true'}

    with open(filename, mode="rb") as image_data:
        response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
        
        response.raise_for_status()
        analysis = response.json()
        
        lines = list()
        count = 0

        for line in analysis['regions'][0]['lines']:
            for word in line['words']:
                lines.append(word['text'])
        return lines
