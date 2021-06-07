"""
This file contains a dataclass object that reads files from google earth engine 
and then returns them as tif files
"""
# My jupyter path on my mac is different to pip, the easy answer is to append the path to where my packages are inported
import sys
sys.path.append("/Users/calummeikle/Documents/ClimateModelling/SatelliteImagery/env/lib/python3.9/site-packages/")
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import ee
from pathlib import Path

def authentication():
    # Trigger the authentication flow.
    ee.Authenticate()

    # Initialize the library.
    ee.Initialize()

class DataDownload():
    
    def __init__(self, geojson, dataset, start_date, end_date, band=None):
        authentication()

        coords = geojson['features'][0]['geometry']['coordinates']
        self.aoi = ee.Geometry.Polygon(coords)

        self.dataset = dataset
        self.start_date = start_date
        self.end_date = end_date
        self.band = band

        self.data_folder = Path("../satellite_data/")
        self.filename = f'{self.dataset}_{self.start_date}_{self.end_date}_{self.band}'

    def image_selection(self):
        self.img = ee.Image((ee.ImageCollection(self.dataset)
            .filterBounds(self.aoi)
            .filterDate(self.start_date, self.end_date)
            .first()
            .clip(self.aoi)))
        self.img = self.img.select(self.band)

    def export_to_tiff(self):
        """
        Useful for when processing with rasterio
        """

        # Get a particular image
        self.image_selection()

        mytask = ee.batch.Export.table.toDrive(
            image=self.img,
            folder='data_earth_engine',
            fileNamePrefix=self.filename,
            fileFormat='GeoTIFF'
            )

        ee.batch.data.startProcessing(mytask.id, mytask.config)

    def link_to_download(self):
        link = self.img.getDownloadURL({
            'scale': 30,
            'fileFormat': 'GeoTIFF',
            })
        return link

# if __name__ == "__main__":
#     # A geojson for the Tokyo area taken from geojson.io
#     geoJSON = {
#     "type": "FeatureCollection",
#     "features": [
#         {
#         "type": "Feature",
#         "properties": {},
#         "geometry": {
#             "type": "Polygon",
#             "coordinates": [
#             [
#                 [
#                 139.2572021484375,
#                 35.420391545750746
#                 ],
#                 [
#                 140.18554687499997,
#                 35.420391545750746
#                 ],
#                 [
#                 140.18554687499997,
#                 35.98245135784044
#                 ],
#                 [
#                 139.2572021484375,
#                 35.98245135784044
#                 ],
#                 [
#                 139.2572021484375,
#                 35.420391545750746
#                 ]
#             ]
#             ]
#         }
#         }
#     ]
#     }
#     START_DATE = '2020-08-01'
#     END_DATE = '2020-09-01'
#     c = DataDownload(geoJSON, 'COPERNICUS/S2_SR', START_DATE, END_DATE)
#     c.export_to_tiff("blah blah")
    