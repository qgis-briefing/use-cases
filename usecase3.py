import requests
import pandas as pd
import zipfile
import os
import processing

def download(url):
    r = requests.get(url)
    filename = local_path + url.rsplit('/', 1)[1]
    with open(filename,'wb') as output_file:
        output_file.write(r.content)

def unzip(filename):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(local_path)

local_path = 'your file path'
os.chdir(local_path)

url = 'https://www.pland.gov.hk/pland_en/info_serv/digital_planning_data/Metadata/OZP_PLAN_SHP.json'
r = requests.get(url)
df = pd.DataFrame(r.json())
df['filename'] = df['SHP_LINK'].apply(lambda x: x.rsplit('/', 1)[1])

print("1. Start downloading:")
for index, url in enumerate(df['SHP_LINK']):
    download(url)

print("2. Start unzipping:")
for index, filename in enumerate(df['filename']):
    unzip(local_path + filename)

print("3. Start merging:")
shp_files = []
for root, dirs, files in os.walk(local_path):
    for file in files:
        if file == "ZONE.shp":
            shp_files.append(os.path.join(root, file))

parameters = {'CRS': None, 
              'LAYERS': shp_files, 
              'OUTPUT': "TEMPORARY_OUTPUT"
             }

processing.runAndLoadResults("native:mergevectorlayers", parameters)
print("Completed!")
