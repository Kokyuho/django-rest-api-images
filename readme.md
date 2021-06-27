# Satellite imagery parallel processing Django REST Framework API

Satellite imagery from the ESA Copernicus Sentinel 2 MSI instrument can be freely downloaded and used. Once we download an image product, corresponding with a certain world area and date taken, we will find in its containing folder the data corresponding to several spectral bands, each coming from different sensors able to perceive a certain wavelength and spacial resolution.

Each spectral band can be seen as a grey-scale image. A true color image can therefore be obtained combining the red, green and blue bands (RGB). However, many other combinations using e.g. infrared or ultraviolet bands can be used to obtain an image with certain interesting properties, such as cloud penetration or vegetation or water body detection. 

This example Django REST API program lets the client sent a batch job to the server and then run it, choosing the spacial resolution and the three bands to be combined to obtain the rendered images. The program will make use of parallel processing capabilities to process all the jobs and store the images in an output folder. A list with the filenames of the images will be returned.

Install requirements:
1) Clone the repository.
2) Download and extract the following satellite image product in the same folder (large file, +900Mb): https://scihub.copernicus.eu/dhus/odata/v1/Products('bc88e6f3-7934-407a-82ab-2bbb26ec2cfe')/$value
3) Install dependencies (pip install -r requirements.txt)

Usage:
```
python manage.py runserver
```

Using the REST API:
1) Navigate to '/api/' to see a list of the available API commands.
2) Create a task with '/job-create/', e.g. giving:
```
{
    "res_list": "20,20,60",
    "r_list": "B04,B12,B06",
    "g_list": "B03,B11,B04",
    "b_list": "B02,B03,B02"
}
```
3) Run the job with '/job-run/pk' where pk = primary key of the job. The server will start rendering the image combinations given in the lists (i=0, i=1,...) and will return the JSON object with status Done and Output the list of the output images locations.

