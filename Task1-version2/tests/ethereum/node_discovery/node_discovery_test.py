import requests
from bs4 import BeautifulSoup

# Making a GET request
r = requests.get('https://etherscan.io/nodetracker/nodes')
print("Http Response Code:", r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
print("HTML content ", soup)

s = soup.find('div', class_='entry-content')
content = s.find_all('p')

print(content)