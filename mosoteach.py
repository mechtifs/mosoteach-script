import requests
from bs4 import BeautifulSoup


# Fill in your class course ID and login token here
clazz = 'class_couse_id'
token = 'login_token'

# Main function
headers = {
    'Host': 'www.mosoteach.cn',
    'Cookie': 'login_token='+token,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://www.mosoteach.cn/web/index.php?c=interaction&m=index&clazz_course_id='+clazz,
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'Te': 'trailers',
    'Connection': 'close',
}
r = requests.get(
    'https://www.mosoteach.cn/web/index.php?c=res&m=index&clazz_course_id='+clazz, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
headers['Referer'] = 'https://www.mosoteach.cn/web/index.php?c=res&m=index&clazz_course_id='+clazz
headers.update({
    'Origin': 'https://www.mosoteach.cn',
    'X-Requested-With': 'XMLHttpRequest',
})
for res in soup.select('.res-row-open-enable'):
    if res.select('span')[9].attrs['style'] == 'color:#8fc31f':
        continue
    dur = str(round(float((res.select('span')[5].contents[0].split()[0]))*60))
    data = {
        'clazz_course_id': clazz,
        'res_id': res.attrs['data-value'],
        'watch_to': dur,
        'duration': dur,
        'current_watch_to': dur,
    }
    print(data)
    r = requests.post(
        'https://www.mosoteach.cn/web/index.php?c=res&m=save_watch_to', headers=headers, data=data)
