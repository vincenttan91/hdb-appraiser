def token_call(email, password):
    import http.client
    import mimetypes
    import json

    conn = http.client.HTTPSConnection("developers.onemap.sg")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append('--' + boundary)
    dataList.append('Content-Disposition: form-data; name=email;')

    dataList.append('Content-Type: {}'.format('multipart/form-data'))
    dataList.append('')

    dataList.append(email)
    dataList.append('--' + boundary)
    dataList.append('Content-Disposition: form-data; name=password;')

    dataList.append('Content-Type: {}'.format('multipart/form-data'))
    dataList.append('')

    dataList.append(password)
    dataList.append('--' + boundary + '--')
    dataList.append('')
    body = '\r\n'.join(dataList)
    payload = body
    headers = {
        'Cookie': 'Domain=developers.onemap.sg; onemap2=CgAACl54OdmSjAStCDygAg==',
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/privateapi/auth/post/getToken", payload, headers)
    res = conn.getresponse().read()
    token = json.loads(res)

    with open('./token.json', 'w', encoding='utf-8') as f:
        json.dump(token, f, ensure_ascii=False, indent=4)

    return token['access_token']

def get_token(email, password):
    import json
    import time

    try:
        with open('./token.json', 'r', encoding='utf-8') as f:
            token = json.load(f)

            if int(token['expiry_timestamp']) - time.time() > 0:
                return token['access_token']

            else:
                return token_call(email, password)

    except FileNotFoundError:
        return token_call(email, password)
