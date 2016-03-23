#Fresno County

Dataset:

http://www.co.fresno.ca.us/DepartmentPage.aspx?id=52122

Assessor's Office, Mapping Department

559-600-3585

##Usage
1.  Download shapefile from link above.
2.  Unzip file.
3.  Navigate to the unzipped directory in the terminal.
4.  Run (replacing [name] with the name of your downloaded Shapefile): $ `ogr2ogr -f GeoJSON -t_srs crs:84 [name].geojson [name].shp`
5.  Move the resulting geojson file to the Fresno directory and run the geojson-convert.py script (inside the virtual environment.)
6.  When satisfied with the output of the json file, run the geojson-import.py script.
7.  Check the Montage schema to ensure the data imported successfully.
