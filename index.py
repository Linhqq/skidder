import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Định nghĩa các API và các URL tương ứng
api_endpoints = {
    "https://paste-drop.com": "https://et.goatbypassers.xyz/api/adlinks/bypass?url=",
    "https://pastebin.com": "https://et.goatbypassers.xyz/api/adlinks/bypass?url=",
    "https://mobile.codex.lol/?token=": "https://et.goatbypassers.xyz/api/adlinks/bypass?url=",
    "https://rekonise.com": "https://et.goatbypassers.xyz/api/adlinks/bypass?url=",
    "https://sub2Unlock.com": "https://et.goatbypassers.xyz/api/adlinks/bypass?url=",
    "https://sub2Unlock.io": "https://et.goatbypassers.xyz/api/adlinks/bypass?url=",
    "https://sub2Unlock.net": "https://et.goatbypassers.xyz/api/adlinks/bypass?url=",
    "https://www.mediafire.com/": "https://et.goatbypassers.xyz/api/adlinks/bypass?url=",
    "https://gateway.platoboost.com/a/8?id=": "http://45.90.13.151:6041/?url=",
    "https://gateway.platoboost.com/a/2569?id=": "http://45.90.13.151:6041/?url=",
    "https://flux.li/android/external/start.php?HWID=": "https://kakansnks-f168r6ieh-my-team-7fa79d02.vercel.app/api/fluxus?link=",
    "https://banana-hub.xyz": "http://45.90.13.151:6132/api/bypass?link=",
    "https://linkvertise.com": "http://45.90.13.151:6132/api/bypass?link=",
    "https://direct-link.net": "http://45.90.13.151:6132/api/bypass?link=",  # Thêm endpoint cho direct-link
    "https://link-center.net": "http://45.90.13.151:6132/api/bypass?link="   # Thêm endpoint cho link-center
}

def select_api(link):
    for url, api in api_endpoints.items():
        if link.startswith(url):
            return api
    return None

def bypass_link(link):
    api = select_api(link)
    if api is None:
        return {"key": "Unsupported URL"}

    if api in [
        "http://45.90.13.151:6132/api/bypass?link=",
    ]:
        full_url = f"{api}{link}&api_key=goatbypassersontop"
    else:
        full_url = f"{api}{link}"
    
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return {"key": "Request failed", "message": str(e)}
    except requests.exceptions.JSONDecodeError:
        return {"key": "Invalid JSON response"}

    # Điều chỉnh định dạng JSON cho các API cụ thể
    if api == "https://et.goatbypassers.xyz/api/adlinks/bypass?url=":
        if 'bypassed' in data:
            data = {"key": data['bypassed']}
    elif api == "https://kakansnks-f168r6ieh-my-team-7fa79d02.vercel.app/api/fluxus?link=":
        if 'execution_time' in data:
            data = {"key": data.get('key'), "time": data['execution_time']}
    elif api == "http://45.90.13.151:6132/api/bypass?link=":  # Xử lý cho bananahub và linkvertise
        if 'key' in data:
            data = {"key": data['key']}
    
    return data

@app.route('/bypass', methods=['GET'])
def bypass():
    link = request.args.get('url')
    if not link:
        return jsonify({"key": "No URL provided"}), 400

    result = bypass_link(link)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
