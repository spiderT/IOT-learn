
import json
import base64

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tts.v20190823 import tts_client, models

SECRET_ID = "你的Secret ID"
SECRET_KEY = "你的Secret Key"

try:
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "tts.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = tts_client.TtsClient(cred, "ap-beijing", clientProfile)

    req = models.TextToVoiceRequest()
    params = {
        "Text": "我已经把灯关了",
        "SessionId": "sessionid-geektime",
        "ModelType": 1,
        "ProjectId": 0,
        "VoiceType": 1002
    }
    req.from_json_string(json.dumps(params))

    resp = client.TextToVoice(req)
    print(resp.to_json_string())

    if resp.Audio is not None:
        audio = resp.Audio
        data = base64.b64decode(audio)
        wav_file = open("temp.wav", "wb")
        wav_file.write(data)
        wav_file.close()

except TencentCloudSDKException as err:
    print(err)
