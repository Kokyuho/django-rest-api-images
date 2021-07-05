import requests
from requests.auth import HTTPBasicAuth
import sys
import time

def downloadFile(url, directory) :
    localFilename = url.split('/')[-1]
    with open(directory + '/' + localFilename + '.zip', 'wb') as f:
        start = time.process_time()
        r = requests.get(url,
                        auth=HTTPBasicAuth('kokyuhoapi', 'simple123'),
                        stream=True)
        total_length = r.headers.get('content-length')
        dl = 0
        if total_length is None: # no content length header
            f.write(r.content)
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
    if len(sys.argv) > 1 :
        url = sys.argv[1]
    else :
        url = "https://scihub.copernicus.eu/dhus/odata/v1/Products('bc88e6f3-7934-407a-82ab-2bbb26ec2cfe')/$value"
    directory = "."

    time_elapsed = downloadFile(url, directory)
    print("Download complete...")
    print("Time Elapsed:", time_elapsed)

if __name__ == "__main__" :
    main()
