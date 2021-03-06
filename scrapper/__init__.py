import os
import urllib.error
import urllib.request

from bs4 import BeautifulSoup

class Scrapper:
    _empty_file_sizes = [0, 4275]
    _url = 'https://prnt.sc'
    _path = './images'

    def __init__(self, path):
        if path is not None:
            self._path = path

    def generate_random_url(self, slug):
        return { 'url': f'{self._url}/{slug}.png', 'name': f'{slug}.png' }

    def scrape(self, img):
        try:
            filename = f'''{self._path}/{img['name']}'''

            fake_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:43.0) Gecko/20100101 Firefox/43.0 '
            headers = {
                'user-agent': fake_agent,
            }

            request = urllib.request.Request(
                img['url'],
                headers = headers,
            )

            response = urllib.request.urlopen(request)
            html = response.read()
            soup = BeautifulSoup(str(html), 'html.parser')
            image = soup.find(id = 'screenshot-image')

            if image is not None:
                src = image.get('src')
                opener = urllib.request.URLopener()
                opener.addheader('User-Agent', fake_agent)
                opener.retrieve(src, filename)
            else:
                return 404

            file_size = os.path.getsize(filename)

            if file_size in self._empty_file_sizes:
                print(f'''[-] Invalid image url {img['url']}''')
                os.remove(filename)
                return 404
            else:
                print(f'''[+] Valid image url {img['url']}''')
        except urllib.error.HTTPError as e:
            print(f'''[-] {e} - {img['url']}''')
            return e.code
        except (urllib.error.ContentTooShortError, ValueError):
            return 400

        return 200
