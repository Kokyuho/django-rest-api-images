# Satellite imagery parallel processing Django REST Framework API

Satellite imagery from the ESA Copernicus Sentinel 2 MSI instrument can be freely downloaded and used. Once we download an image product, corresponding with a certain world area and date taken, we will find in its containing folder the data corresponding to several spectral bands, each coming from different sensors able to perceive a certain wavelength and spacial resolution.

Each spectral band can be seen as a grey-scale image. A true color image can therefore be obtained combining the red, green and blue bands (RGB). However, many other combinations using e.g. infrared or ultraviolet bands can be used to obtain an image with certain interesting properties, such as cloud penetration or vegetation or water body detection. 

This example Django REST API program lets the client programatically send a batch rendering job to the server and then run it, choosing the spacial resolution and the three bands to be combined to obtain the rendered images. The program will make use of parallel processing capabilities to process all the rendering jobs and store the images in an output folder. A list with the filenames of the images rendered will be returned that later another application could use to access the output files.

UPDATE: Docker containarization is now possible. A Dockerfile has been added.

UPDATE2: Satellite imagery folder will now automatically download if it is not available. This is a large file (900+ MB) so please be patient the first time you run the program.

**Install requirements**:
1) Clone the repository.
2) Install dependencies (pip install -r requirements.txt) or, alternatively, run docker build.
```
docker build -t django-rest-api-images .
```

**Usage**:
```
python manage.py runserver
```

**Usage with Docker**:
```
docker run --name=django-rest-api-images -e PYTHONUNBUFFERED=1 -p 8000:8000 django-rest-api-images
```

**Using the REST API**:
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
(This creates e.g. a batch job of 3 renderings, with 20, 20 and 60m spacial resolution and corresponding rgb combinations).
Note: Lists must be comma separated values chosen from the following lists:
```
if res == '10':
    accepted_list = ('B02', 'B03', 'B04', 'B08') 
elif res == '20':
    accepted_list = ('B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B8A', 'B11', 'B12')
elif res == '60':
    accepted_list = ('B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B8A', 'B09', 'B11', 'B12')
```

3) Run the job with '/job-run/pk' where pk = primary key of the job. The server will start rendering the image combinations given in the lists (i=0, i=1,...) and will return the JSON object with status Done and Output the list of the output images locations.

Final Note: There is also a simpler command line python version of this program: https://github.com/Kokyuho/parallel-processing-images.git. There, input parameters are given directly from command line.
