import concurrent.futures
import time, requests
from collections import defaultdict
from urllib.parse import urlsplit, parse_qs, urlunsplit


errors = []
start = time.time()
urls = ["http://www.google.com", "http://www.apple.com", "http://www.microsoft.com", "http://www.amazon.com",
        "http://www.facebook.com"]
results = defaultdict(dict)


# Retrieve a single page and report the url and contents
def load_url(url, timeout):
    parsed_url = list(urlsplit(url))

    if not parsed_url[1]:
        errors.append(url)
        return "error"

    for scheme in ["http", "https"]:
        parsed_url[0] = scheme
        parsed_url[2] = ""
        parsed_url[3] = ""

        req = requests.get(urlunsplit(parsed_url))
        results[parsed_url[1]][parsed_url[0]] = req.status_code
    return "{} Done".format(parsed_url)


# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in urls}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('"%s" fetched in %ss' % (url, (time.time() - start)))
            # print "Elapsed Time: %ss" % (time.time() - start)


print(results)