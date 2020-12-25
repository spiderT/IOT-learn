
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models
import base64
import io
import sys

SECRET_ID = "你的Secret ID"
SECRET_KEY = "你的Secret Key"

try:
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "asr.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    clientProfile.signMethod = "TC3-HMAC-SHA256"
    client = asr_client.AsrClient(cred, "ap-beijing", clientProfile)
    # 读取文件以及 base64
    with open('./geektime-00.wav', "rb") as f:
        if sys.version_info[0] == 2:
            content = base64.b64encode(f.read())
        else:
            content = base64.b64encode(f.read()).decode('utf-8')
        f.close()
    # 发送请求
    req = models.SentenceRecognitionRequest()
    params = {"ProjectId": 0, "SubServiceType": 2,
              "SourceType": 1, "UsrAudioKey": "sessionid-geektime"}
    req._deserialize(params)
    req.DataLen = len(content)
    req.Data = content
    req.EngSerViceType = "16k_zh"
    req.VoiceFormat = "wav"
    resp = client.SentenceRecognition(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)
