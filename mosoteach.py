import requests
from bs4 import BeautifulSoup


# Fill in your accounts here
accounts = [{'account': '111', 'password': 'aaa'},
            {'account': '222', 'password': 'bbb'},
            {'account': '333', 'password': 'ccc'}, ]

# Main function
for account in accounts:
    print('Account:', account['account'])

    # Log in
    headers = {
        'Host': 'coreapi-proxy.mosoteach.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Cache-Control': 'max-age=0',
        'Te': 'trailers',
        'Connection': 'close',
    }
    r = requests.post(
        'https://coreapi-proxy.mosoteach.cn/index.php/passports/account-login', headers=headers, json=account)
    headers['Host'] = 'www.mosoteach.cn'
    try:
        headers.update({
            'Cookie': 'login_token='+r.json()['token'],
            'Sec-Fetch-User': '?1',
        })
    except KeyError:
        quit('Wrong account or password!')
    print('Login token: '+r.json()['token'])

    # Get class course ID
    r = requests.post(
        'https://www.mosoteach.cn/web/index.php?c=clazzcourse&m=my_joined', headers=headers)
    headers.pop('Content-Type')
    headers['Sec-Fetch-Dest'] = 'document'
    headers['Sec-Fetch-Mode'] = 'navigate'
    headers['Sec-Fetch-Site'] = 'same-origin'
    for clazz in r.json()['data']:
        print('Class ID: '+clazz['id'])

        # Get video ID
        r = requests.get(
            'https://www.mosoteach.cn/web/index.php?c=res&m=index&clazz_course_id='+clazz['id'], headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        headers['Referer'] = 'https://www.mosoteach.cn/web/index.php?c=res&m=index&clazz_course_id='+clazz['id']
        headers.update({
            'Origin': 'https://www.mosoteach.cn',
            'X-Requested-With': 'XMLHttpRequest',
        })
        for res in soup.findAll('div', {'data-mime': 'video'}):
            if res.select('span')[9].attrs['style'] == 'color:#8fc31f':
                continue
            dur = str(
                round(float((res.select('span')[5].contents[0].split()[0]))*60))
            print('Video ID: '+res.attrs['data-value']+', duration: '+dur+'s')
            data = {
                'clazz_course_id': clazz['id'],
                'res_id': res.attrs['data-value'],
                'watch_to': dur,
                'duration': dur,
                'current_watch_to': dur,
            }

            # Save watch time
            r = requests.post(
                'https://www.mosoteach.cn/web/index.php?c=res&m=save_watch_to', headers=headers, data=data)
