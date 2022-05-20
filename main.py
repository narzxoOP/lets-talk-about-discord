import os, httpx, json, threading, itertools, time

lock = threading.Lock()
config = json.load(open('./config.json'))
proxies = itertools.cycle(open('./proxies.txt', 'r+').read().splitlines())
tokens = itertools.cycle(open('./tokens.txt', 'r+').read().splitlines())


class Console:
    @staticmethod
    def printf(content: str):
        lock.acquire()
        print(f'{content}')
        lock.release()

class CaptchaSolver:
    @staticmethod
    def get_captcha_key(static_proxy: str, proxy: str) -> str:
        task_payload = {
            'clientKey': config['captcha_key'],
            'task': {
                'userAgent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.1012 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36',
                'websiteKey': 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34',
                'websiteURL': 'https://discord.com',
                'type': 'HCaptchaTaskProxyless', #'HCaptchaTask',

                #'proxyPassword': static_proxy.split('@')[0].split(':')[1],
                #'proxyAddress': static_proxy.split('@')[1].split(':')[0],
                #'proxyLogin': static_proxy.split('@')[0].split(':')[0],
                #'proxyPort': static_proxy.split('@')[1].split(':')[1],
                #'proxyType': 'http',
            }
        }
        key = None

        with httpx.Client(headers={'content-type': 'application/json', 'accept': 'application/json'}, timeout=30) as client: # ,proxie=static_proxy
            try:
                task_id = client.post(f'https://api.{config["captcha_api"]}/createTask', json=task_payload).json()['taskId']
                print(task_id)
                get_task_payload = {
                    'clientKey': config['captcha_key'],
                    'taskId': task_id
                }

                while key is None:
                    try:
                        response = client.post(f'https://api.{config["captcha_api"]}/getTaskResult',
                                               json=get_task_payload,
                                               timeout=30).json()
                        print(response)
                        if 'ERROR_PROXY_CONNECT_REFUSED' in str(response):
                            return 'ERROR'

                        if 'ERROR' in str(response):
                            return 'ERROR'

                        if response['status'] == 'ready':
                            key = response['solution']['gRecaptchaResponse']
                        else:
                            time.sleep(3)
                    except Exception as e:
                        if 'ERROR_PROXY_CONNECT_REFUSED' in str(e):
                            key = 'ERROR'
                        else:
                            pass
                
                print(key)
                return key

            except Exception as e:
                if 'ERROR_PROXY_CONNECT_REFUSED' in str(e):
                    return 'ERROR'
                else:
                    print(e)
                    pass

class Verifier(threading.Thread):
    def __init__(self, token: str):
        threading.Thread.__init__(self)
        self.token = token
        self.headers = {
            'accept': '*/*',
            'Connection': 'keep-alive',
            'accept-encoding': 'application/json',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'X-Debug-Options': 'bugReporterEnabled',
            'cache-control': 'no-cache',
            'sec-ch-ua': "'Chromium';v='92', ' Not A;Brand';v='99', 'Google Chrome';v='92'",
            'sec-fetch-site': 'same-origin',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImZyLUZSIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk4LjAuNDc1OC44MiBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiOTguMC40NzU4LjgyIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjExNDQwNywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
            'x-discord-locale': 'fr',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            'te': 'trailers',
            'authorization': token,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }

    def run(self):
        try:
            prox = 'http://'+next(proxies).split('\n')[0]
            with httpx.Client(headers=self.headers, proxies=prox, timeout=30) as client:
                experiments = client.get('https://discordapp.com/api/v9/experiments')
                __sdcfduid = experiments.cookies.get('__sdcfduid')
                __dcfduid = experiments.cookies.get('__dcfduid')

                client.headers['cookie'] = f'__dcfduid={__dcfduid}; __sdcfduid={__sdcfduid}; locale=fr'

                cookies = httpx.Cookies()
                cookies.set('__sdcfduid', __sdcfduid, domain='discord.com')
                cookies.set('__dcfduid', __dcfduid, domain='discord.com')
                cookies.set('locale', 'fr', domain='discord.com')
                client.cookies = cookies

                client.headers['authorization'] = self.token
                verification_link = "https://click.discord.com/ls/click?upn=qDOo8cnwIoKzt0aLL1cBeFE1RlVCKJFF5zAq8ml-2BFh1dq-2FeX22E9yMPFmLMSO5CYc4bFqmQm6jLyvRoSDmBb6h2NDw9Q8pmBdR9pLsj2Vw7FmSDod17vNFe-2Fa-2BBrTOt-2FaG7E-2BHaaA-2ByHhmisjMwOvIAnJ9Wv9euXjhhhb1Eihd5i4f-2B2gg1VfTHyZP0B-2FGMZK8LHgm98Knd6T-2F8fBNQnJtqUyqmbaYiW4CXg7zyEUug-3D2gst_ABoG7LHbwgewcRUF-2BDalnIrzVKs7mb0ibgDT9a0HaNem0Xx-2BPvnp3MIi3FBWKSn4PmYkqPEKQWaFux9NmJdhx-2FYEmuj-2F-2BNnwshixkJXK6sQUJ47kmIztZbkyj7PmDP97QlxtgtdBkfG01LaQPc8paAF-2F39BMvlkLMhdRPkl0lQ0TwfQLRUGHrzvmTKAOW0vrliEyVGNgy4U8AG6uZKakEVMTy2g07-2BFnXGdJWDnRgIQ-2FWrn-2BzY-2BUzzI-2Bhzlj30dLKUa6gtt1T-2Bl1J8rfFq-2Bs4w-3D-3D"

                # the kid say to put the link hard code ^^^^^

                verification_token = str(client.get(verification_link, follow_redirects=True).url).split('https://discord.com/verify#token=')[1]
                print(verification_token)

                need_captcha = False
                while True:
                    resp = client.post('https://ptb.discord.com/api/v9/auth/verify', json={'captcha_key': None if need_captcha == False else CaptchaSolver.get_captcha_key(prox, prox), 'token': verification_token}).json()

                    try:
                        if 'captcha' in str(resp):
                            need_captcha = True
                            print(f'[-] Need captcha')
                        elif 'token' in str(resp):
                            token = resp['token']
                            Console.printf(f'[+] Verified {token}')
                            with open('./verified.txt', 'a+') as f:
                                f.write(f'{token}\n')
                        else:
                            print(resp)
                    except:
                        pass
        except Exception as e:
            print(e)

if __name__ == '__main__':
    for tokens in open('./tokens.txt', 'r+').read().splitlines():
        while threading.active_count() >= config['threads']:
            time.sleep(1)

        Verifier(tokens.split('\n')[0]).start()