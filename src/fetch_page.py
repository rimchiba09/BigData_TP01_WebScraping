import requests

URL = "https://en.wikiquote.org/wiki/Albert_Einstein"


HEADERS = {
    "User-Agent": "TP01-Scraper/1.0 (Univ Eloued student project; rim-chiba@univ-eloued.dz)"
}

response = requests.get(URL, headers=HEADERS, timeout=15)

print("Status code:", response.status_code) 
print("Length:", len(response.text))
print(response.text[:3000])                   