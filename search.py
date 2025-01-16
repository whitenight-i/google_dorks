import requests
from bs4 import BeautifulSoup
import argparse
import time

# List of search queries
SEARCH_QUERIES = [
    "intitle:\"index of\" \"site:{}\"",
    "filetype:log inurl:log site:{}",
    "filetype:sql inurl:sql site:{}",
    "filetype:env inurl:.env site:{}",
    "inurl:/phpinfo.php site:{}",
    "inurl:/admin site:{}",
    "inurl:/backup site:{}",
    "inurl:wp- site:{}",
    "filetype:config inurl:config site:{}",
    "filetype:ini inurl:wp-config.php site:{}",
    "filetype:json inurl:credentials site:{}",
    "intext:\"password\" filetype:log site:{}",
    "intext:\"username\" filetype:log site:{}",
    "filetype:sql \"password\" site:{}",
    "filetype:sql inurl:db site:{}",
    "filetype:sql inurl:dump site:{}",
    "filetype:bak inurl:db site:{}",
    "inurl:\".git\" site:{}",
    "inurl:\"/.git/config\" site:{}",
    "intitle:\"index of\" \".git\" site:{}",
    "intext:\"email\" site:{}",
    "inurl:\"contact\" intext:\"@{}\" -www.{}",
    "filetype:xls inurl:\"email\" site:{}",
    "intitle:\"Apache2 Ubuntu Default Page: It works\" site:{}",
    "intitle:\"Index of /\" \"Apache Server\" site:{}",
    "intitle:\"Welcome to nginx\" site:{}",
    "filetype:env \"DB_PASSWORD\" site:{}",
    "intext:\"api_key\" filetype:env site:{}",
    "intext:\"AWS_ACCESS_KEY_ID\" filetype:env site:{}",
    "filetype:bak inurl:backup site:{}",
    "filetype:zip inurl:backup site:{}",
    "filetype:tgz inurl:backup site:{}"
]

# Function to perform search using Google
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to perform search for query: {query} - HTTP {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error during request for query: {query} - {e}")
        return None

# Function to parse search results page
def parse_results(page_content):
    results = []
    soup = BeautifulSoup(page_content, 'html.parser')
    links = soup.find_all('a', href=True)
    
    for link in links:
        href = link['href']
        if 'url?q=' in href:
            url = href.split('url?q=')[1].split('&')[0]
            results.append(url)
    
    return results

# Function to check file status and size
def check_file(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            size = response.headers.get('Content-Length', 'Unknown size')
            print(f"[200 OK] {url} - Size: {size} bytes")
        else:
            print(f"[ERROR {response.status_code}] {url}")
    except requests.RequestException as e:
        print(f"[FAILED] {url} - {e}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Google Dorking Tool")
    parser.add_argument("-s", "--site", help="Target site to search", required=False)
    parser.add_argument("-l", "--list", help="File containing a list of target sites", required=False)
    args = parser.parse_args()

    if not args.site and not args.list:
        print("Error: You must provide a site (-s) or a list of sites (-l).")
        return

    sites = []
    if args.site:
        sites.append(args.site)
    if args.list:
        try:
            with open(args.list, "r") as file:
                sites.extend(line.strip() for line in file if line.strip())
        except FileNotFoundError:
            print(f"Error: File {args.list} not found.")
            return

    for site in sites:
        print(f"\n[SEARCHING SITE] {site}")
        for query_template in SEARCH_QUERIES:
            query = query_template.format(site)
            print(f"\n[SEARCHING QUERY] {query}")
            page_content = search_google(query)
            if page_content:
                results = parse_results(page_content)
                for result in results:
                    check_file(result)
            time.sleep(1)  # Delay to prevent overloading requests

if __name__ == "__main__":
    main()
