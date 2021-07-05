from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JobSerializer
from .models import Job
from multiprocessing import Process, Manager
import api.main as main
import os
import api.download_file
import time
import zipfile


#### API VIEWS ####

@api_view(['GET'])
def apiOverview(request):
	"""Gives a list overview of the possible API commands to use.
	"""
	api_urls = {
		'Job List':'/job-list/',
		'Detail View':'/job-detail/<str:pk>/',
		'Create Job':'/job-create/', # Lists must be coma separated with no spaces
		'Update Job':'/job-update/<str:pk>/',
		'Delete Job':'/job-delete/<str:pk>/',
		'Run Job': '/job-run/<str:pk>/', # Returns primary key of job
		}
	return Response(api_urls)

@api_view(['GET'])
def jobList(request):
	"""Shows a list of available jobs to process
	"""
	jobs = Job.objects.all().order_by('-id')
	serializer = JobSerializer(jobs, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def JobDetail(request, pk):
	"""Gives details of a particular batch job ID.
	"""
	job = Job.objects.get(id=pk)
	serializer = JobSerializer(job, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def JobCreate(request):
	"""Creates a new batch job for satellite imagery renderings. This must be followed
	by a json object that includes at least the 4 lists (res_list, r_list, g_list and
	b_list) with appropiate values.
	Example JSON for a new batch job:
	{
		"res_list": "20,20,60",
		"r_list": "B04,B12,B06",
		"g_list": "B03,B11,B04",
		"b_list": "B02,B03,B02"
	}
	"""
	serializer = JobSerializer(data=request.data)

	# Check data consistency
	# Get user input (or API)
	res_list = request.data['res_list'].split(',')
	r_list = request.data['r_list'].split(',')
	g_list = request.data['g_list'].split(',')
	b_list = request.data['b_list'].split(',')

	# Check lists consistency
	# Check spacial resolutions
	for res in res_list:
		if res not in ('10','20','60'):
			raise ValueError('Some spacial resolution value given is not valid.')
	# Check length of lists consistency
	if len(res_list) != len(r_list) or \
	   len(res_list) != len(g_list) or \
	   len(res_list) != len(b_list):
	   	raise ValueError('List lengths must be equal.')
	# Check bands given depending on resolution
	for list in [r_list, g_list, b_list]:
		for i in range(len(list)):
			if res_list[i] == '10':
				if list[i] not in ('B02', 'B03', 'B04', 'B08'):
					raise ValueError('Some band value given is not valid.')
			elif res_list[i] == '20':
				if list[i] not in ('B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B8A', 'B11', 'B12'):
					raise ValueError('Some band value given is not valid.')
			if res_list[i] == '60':
				if list[i] not in ('B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B8A', 'B09', 'B11', 'B12'):
					raise ValueError('Some band value given is not valid.')

	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['POST'])
def JobUpdate(request, pk):
	"""Updates a given batch job ID. A json object similar to the one in JobCreate must
	be given.
	"""
	job = Job.objects.get(id=pk)
	serializer = JobSerializer(instance=job, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def JobDelete(request, pk):
	"""Deletes a given batch job.
	"""
	job = Job.objects.get(id=pk)
	job.delete()

	return Response('Item succsesfully delete!')

@api_view(['GET'])
def JobRun(request, pk):
	"""Runs a satellite imagery rendering batch job given by its ID. If imagery folder
	is not available, it will attempt to download and extract it first. This will
	take quite some time, as the files are large. Then it will render the selected images
	given by the lists utilizing multiprocessing.
	"""
	print("Starting job...")

	# Get job
	job = Job.objects.get(id=pk)

	# Get lists
	res_list = job.res_list.split(',')
	r_list = job.r_list.split(',')
	g_list = job.g_list.split(',')
	b_list = job.b_list.split(',')
    
	# Check if satellite imagery folder exists, else download it
	if not os.path.exists('./S2B_MSIL2A_20210605T110619_N0300_R137_T29TQH_20210605T143100.SAFE'):
		print("Satellite imagery file not found, attempting download now...")
		time.sleep(5)
		api.download_file.main()
		filename = './$value.zip'
		if os.path.exists(filename):
			with zipfile.ZipFile(filename, 'r') as zip_ref:
				zip_ref.extractall('.')

	# Check one more time for good measure
	if not os.path.exists('./S2B_MSIL2A_20210605T110619_N0300_R137_T29TQH_20210605T143100.SAFE'):
		raise FileExistsError('Satellite imagery files not available.')

    # Define image path
	imagePath = './S2B_MSIL2A_20210605T110619_N0300_R137_T29TQH_20210605T143100.SAFE/GRANULE/L2A_T29TQH_A022185_20210605T111526/IMG_DATA/'

    # Check if Output folder exists, else create it
	if not os.path.exists('./Output'):
		os.makedirs('Output')

	# Start parallel rendering processes
	processes = []
	manager = Manager()
	return_dict = manager.dict() # This manager.dict() will hold the output values (paths)
	for i in range(len(res_list)):

		# Create a new process and start it
		p = Process(target=main.renderImage, args=[i, res_list, r_list, g_list, b_list, imagePath, return_dict])
		p.start()
		processes.append(p)
	
	# Wait for them to finish
	for p in processes:
		p.join()

	# Print paths
	print(return_dict.values())

	# Change status to Done
	job.status = "Done"

	# Add output locations, coma separated
	output = ''
	for value in return_dict.values():
		output += value + ','
	job.output = output
	job.save()

	serializer = JobSerializer(job, many=False)
	return Response(serializer.data)
