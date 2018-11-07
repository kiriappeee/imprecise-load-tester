import multiprocessing
from time import sleep
import random
import requests
from datetime import datetime
import yaml
import math
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def make_request(request_url, ssl_verify):
    """Make a request."""
    return requests.get(request_url, verify=ssl_verify)


def run_test(test_url, ssl_verify, results_arr, time_taken_arr, index):
    t1 = datetime.now()
    res = make_request(test_url, ssl_verify)
    t2 = datetime.now()
    total_time = t2 - t1
    results_arr[index] = res.status_code
    time_taken_arr[index] = float("{}.{}".format(total_time.seconds, total_time.microseconds))



def percentile(N, percent, key=lambda x:x):
    """
    Find the percentile of a list of values.

    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @parameter key - optional key function to compute value from each element of N.

    @return - the percentile of the value
    Credit due to http://code.activestate.com/recipes/511478-finding-the-percentile-of-the-values/
    """
    if not N:
        return None
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1

if __name__ == "__main__":
    f = open('tests.yaml', 'r')
    test_details = yaml.load(f.read())
    for test in test_details['tests']:
        test_name = test['name']
        if 'enabled' in test and not test['enabled']:
            print("skipping {}".format(test_name))
            continue
        w = open("{}-results.txt".format(test_name), 'w')
        test_url = test['url']
        iterations = test['iterations']
        ssl_verify = test.get('verify', True)
        print("Running {} for {}".format(test_name, test_url))
        results = multiprocessing.Array('i', iterations)
        time_taken = multiprocessing.Array('f', iterations)
        for i in range(0, iterations):
            multiprocessing.Process(target=run_test, args=(test_url, ssl_verify, results, time_taken, i)).start()
            print(i)
            sleep(random.randrange(1, 11, 1) / 10)
        while(multiprocessing.active_children()):
            print("waiting for children to finish")
            print(multiprocessing.active_children())
            sleep(1)
        print("done")
        w.write("""URL - {}

Average Time - {}
50th Percentile - {}
99th Percentile - {}
Max time - {}
Min time - {}

Times -
{}

Results -
{}""".format(test_url, 
             str(sum(time_taken) / iterations),
             percentile(sorted(time_taken[:]), 0.5),
             percentile(sorted(time_taken[:]), 0.9),
             max(time_taken),
             min(time_taken),
             "\n".join([str(t) for t in time_taken[:]]),
             "\n".join([str(r) for r in results[:]])))
        w.close()
