from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JobSerializer
from .models import Job
from multiprocessing import Process, Manager
import api.main as main
import os

# Views
@api_view(['GET'])
def apiOverview(request):
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
	jobs = Job.objects.all().order_by('-id')
	serializer = JobSerializer(jobs, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def JobDetail(request, pk):
	job = Job.objects.get(id=pk)
	serializer = JobSerializer(job, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def JobCreate(request):
	serializer = JobSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def JobUpdate(request, pk):
	job = Job.objects.get(id=pk)
	serializer = JobSerializer(instance=job, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def JobDelete(request, pk):
	job = Job.objects.get(id=pk)
	job.delete()

	return Response('Item succsesfully delete!')

@api_view(['GET'])
def JobRun(request, pk):

	print("Starting job...")

	# Get job
	job = Job.objects.get(id=pk)

	# Get user input (or API)
	res_list = job.res_list.split(',')
	r_list = job.r_list.split(',')
	g_list = job.g_list.split(',')
	b_list = job.b_list.split(',')
    
    # Define image path
	imagePath = './S2B_MSIL2A_20210605T110619_N0300_R137_T29TQH_20210605T143100.SAFE/GRANULE/L2A_T29TQH_A022185_20210605T111526/IMG_DATA/'

    # Check if Output folder exists, else create it
	if not os.path.exists('./Output'):
		os.makedirs('Output')

	# Start parallel processes
	processes = []
	manager = Manager()
	return_dict = manager.dict()
	for i in range(len(res_list)):
		p = Process(target=main.renderImage, args=[i, res_list, r_list, g_list, b_list, imagePath, return_dict])
		p.start()
		processes.append(p)
	
	# Wait for them to finish
	for p in processes:
		p.join()

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
