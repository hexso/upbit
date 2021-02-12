import requests
import json

def GetToken():
    url = "https://kauth.kakao.com/oauth/token"

    data = {
        "grant_type": "authorization_code",
        "client_id": "",
        "redirect_uri": "https://localhost.com",
        "code": ""

    }
    response = requests.post(url, data=data)

    tokens = response.json()

    print(tokens)

def GetAccessToken():
    '''
    {'access_token': 'VMe------------------------------------------------',

    'expires_in': 21599,

    'token_type': 'bearer'}
    :return:
    '''
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": "<REST_API 앱키를 입력하세요>",
        "refresh_token": "<refresh token을 입력하세요>"
    }
    response = requests.post(url, data=data)

    print(response.json())

class Kakao:

    def __init__(self):
        print()
        self.token = ''

    def sendMsg(self, msg):
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {
            "Authorization": "Bearer " + self.token
        }
        data = {
            "template_object" : json.dumps({ "object_type" : "text",
                                             "text" : msg,
                                             "link" : {
                                                            "web_url" : "www.naver.com"
                                                        }
            })
        }
        response = requests.post(url, headers=headers, data=data)
        print(response.status_code)
        if response.json().get('result_code') == 0:
            print('메시지를 성공적으로 보냈습니다.')
        else:
            print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

if __name__ == '__main__':
    kakao = Kakao()
    kakao.sendMsg('hello')
