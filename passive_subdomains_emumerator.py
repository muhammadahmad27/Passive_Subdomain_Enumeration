import requests
import re
import threading

def crt_sh_search(domain, start, subdomains):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    print(f"Sending request to URL: {url} - Page {start}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data from crt.sh: {response.status_code}")
        return
    data = response.json()
    for entry in data[start:start + 100]:  # Process a batch of 100 entries
        if 'name_value' in entry:
            names = entry['name_value'].split('\n')
            for name in names:
                if name.endswith('.' + domain):
                    subdomains.add(name)

def main(domain):
    subdomains = set()
    threads = []
    num_threads = 5  # Number of threads

    for i in range(num_threads):
        start = i * 100
        thread = threading.Thread(target=crt_sh_search, args=(domain, start, subdomains))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if subdomains:
        print("Found subdomains:")
        for subdomain in sorted(subdomains):
            print(subdomain)
    else:
        print("No subdomains found.")

if __name__ == "__main__":
    root_domain = input("Enter the root domain (e.g., example.com): ")
    if root_domain.startswith("http://") or root_domain.startswith("https://"):
        root_domain = root_domain.split("//")[1]
    if root_domain.endswith("/"):
        root_domain = root_domain[:-1]
    main(root_domain)
