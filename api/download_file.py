import requests
from requests.auth import HTTPBasicAuth
import sys
import time

def downloadFile(url, directory) :
    """Downloads the file given in url displaying a nice progress bar during the
    process.
    """
    # Define local filename from url last part
    localFilename = url.split('/')[-1]

    # Download file into local file
    with open(directory + '/' + localFilename + '.zip', 'wb') as f:

        # Start counting process time
        start = time.process_time()
        
        # Get response object ready for stream
        r = requests.get(url,
                        auth=HTTPBasicAuth('kokyuhoapi', 'simple123'),
                        stream=True)

        # Get total length in bits, init downloaded counter
        total_length = r.headers.get('content-length')
        dl = 0

        # Check file is not empty
        if total_length is None: # no content length header
            f.write(r.content)

        # Download file in chunks and keep updating stdout with a progress bar
        else:
            i = 0
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)
                done = int(50 * dl / int(total_length))
                if i%100 == 0:
                    sys.stdout.write("\r[%s%s] Downloading %s of %s MB; %s Mbps" % (
                                    '=' * done, ' ' * (50-done), 
                                    str(round(dl/1024/1024,2)),
                                    str(round(int(total_length)/1024/1024, 2)), 
                                    round((dl//(time.process_time() - start))/1024/1024, 2)))
                    print('')
                i += 1
    return (time.process_time() - start)

def main() :
    """Sets the url and directory and runs the downloadFile function, passing these values.
    """
    # Define url and target directory
    url = "https://scihub.copernicus.eu/dhus/odata/v1/Products('bc88e6f3-7934-407a-82ab-2bbb26ec2cfe')/$value"
    directory = "."

    # Call function
    time_elapsed = downloadFile(url, directory)

    print("Download complete...")
    print("Time Elapsed:", time_elapsed)

if __name__ == "__main__" :
    main()
