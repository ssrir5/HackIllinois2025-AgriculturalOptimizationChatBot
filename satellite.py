import requests
from requests.structures import CaseInsensitiveDict
import json
import time
import os
import dotenv

EOS_API_KEY = os.getenv("EOS_API")

class EOSDataFetcher:
      def __init__(self, coordinates):
         self.coordinates = coordinates
         self.api_key = EOS_API_KEY          
      def fetch_method(self):
         coordinates = [[-88.53641996249753,40.25214774890757],[-88.52732763016792,40.25204948880202],[-88.52752074921699,40.248774070314056],[-88.53640851596099,40.24887233517511]]
         coordinates.append(coordinates[0])
         api_key = self.api_key

         url = f"https://api-connect.eos.com/api/gdw/api?api_key={api_key}"
         headers = CaseInsensitiveDict()
         headers["Content-Type"] = "application/json"
         data = {
            "type": "mt_stats",
            "params": {
               "bm_type": ["NDVI", "NDMI", "EVI"],
               "date_start": "2024-09-01",
               "date_end": "2025-03-02",
               "geometry": {
                     "coordinates": [coordinates],
                     "type": "Polygon"
               },
               "reference": "ref_20200924-00-20",
               "sensors": ["sentinel2"]
            }
         }
         json_data = json.dumps(data)
         resp = requests.post(url, headers=headers, data=json_data)
         task_id = json.loads(resp.text)["task_id"]


         time.sleep(5)

         url = f"https://api-connect.eos.com/api/gdw/api/{task_id}?api_key={api_key}"
         resp = requests.get(url)
         parsed_data = json.loads(resp.text)

         ndvi_stats = []
         ndmi_stats = []
         evi_stats = []

         for result in parsed_data["result"]:
            ndvi_stats.append(result["indexes"]["NDVI"])
            ndmi_stats.append(result["indexes"]["NDMI"])
            evi_stats.append(result["indexes"]["EVI"])
         data_description = "The following data contains statistics for each tile of my land for NDVI, NDMI, and EVI. These statistics include various metrics such as the first quartile (q1), third quartile (q3), maximum (max), minimum (min), 10th percentile (p10), 90th percentile (p90), standard deviation (std), median, average, and variance. This information is crucial for understanding the vegetation health, moisture levels, and overall condition of the land."

         return  data_description + " " + str({'NDVI': ndvi_stats, 'NDMI': ndmi_stats, 'EVI':evi_stats  })
if __name__ == "__main__":
   fetcher = EOSDataFetcher()
   result_dict = fetcher.fetch_method()
   print(result_dict)
   # print(ndmi_stats)
   # print(evi_stats)


# class EOSDataFetcher:
#     def __init__(self):
#         self.api_key = EOS_API_KEY
#         self.base_url = "https://api-connect.eos.com/api/gdw/api"
#         self.headers = CaseInsensitiveDict()
#         self.headers["Content-Type"] = "application/json"

#     def fetch_data(
#         self, coordinates, bm_types, date_start, date_end, reference, sensors
#     ):
#         coordinates.append(coordinates[0])  # Close the polygon
#         data = {
#             "type": "mt_stats",
#             "params": {
#                 "bm_type": bm_types,
#                 "date_start": date_start,
#                 "date_end": date_end,
#                 "geometry": {"coordinates": [coordinates], "type": "Polygon"},
#                 "reference": reference,
#                 "sensors": sensors,
#             },
#         }
#         json_data = json.dumps(data)
#         resp = requests.post(
#             f"{self.base_url}?api_key={self.api_key}",
#             headers=self.headers,
#             data=json_data,
#         )
#         task_id = json.loads(resp.text)["task_id"]

#         # Wait for the task to complete
#         time.sleep(120)

#         # Fetch the results
#         resp = requests.get(f"{self.base_url}/{task_id}?api_key={self.api_key}")
#         parsed_data = json.loads(resp.text)
#         print(f'parsed_data: {parsed_data}')
#         return parsed_data

#     def fetch_and_explain_data(self, coordinates):
#         bm_types = ["NDVI", "NDMI", "EVI"]
#         date_start = "2024-09-01"
#         date_end = "2025-03-02"
#         reference = "ref_20200924-00-20"
#         sensors = ["sentinel2"]

#         data = self.fetch_data(
#             coordinates, bm_types, date_start, date_end, reference, sensors
#         )
#       #   print('*')
#       #   print(data)
#         # Explanatory string
#         explanatory_string = (
#             "The following data contains statistics for each tile of my land for NDVI, NDMI, and EVI. "
#             "These statistics include various metrics such as the first quartile (q1), third quartile (q3), "
#             "maximum (max), minimum (min), 10th percentile (p10), 90th percentile (p90), standard deviation (std), "
#             "median, average, and variance. This information is crucial for understanding the vegetation health, "
#             "moisture levels, and overall condition of the land.\n\n"
#         )

#         # Combine the explanatory string with the fetched data
#         combined_string = explanatory_string + str(data)

#         return combined_string


# # Example usage
# if __name__ == "__main__":
#     api_key = "apk.55914a899f76dab152d9b7ce70e20de65e0ef85107aecb3e38805f5156b35de9"
#     coordinates = [
#         [-88.53641996249753, 40.25214774890757],
#         [-88.52732763016792, 40.25204948880202],
#         [-88.52752074921699, 40.248774070314056],
#         [-88.53640851596099, 40.24887233517511],
#     ]

#     fetcher = EOSDataFetcher()
#     result = fetcher.fetch_and_explain_data(coordinates)
#     print(result)
