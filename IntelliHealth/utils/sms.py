import json

from tencentcloud.common import credential
from tencentcloud.sms.v20210111 import sms_client, models
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from django.conf import settings


cred = credential.Credential(settings.SMS_SECRET_ID, settings.SMS_SECRET_KEY)
client = sms_client.SmsClient(cred, "ap-beijing")
req = models.SendSmsRequest()
req.SmsSdkAppId = settings.SMS_APPID
req.SignName = settings.SMS_SIGN_NAME


def sms_sender(phone_number, mode, params):
    try:
        req.PhoneNumberSet = [f"+86{phone_number}", ]
        req.TemplateId = settings.SMS_MODE[mode - 1]
        req.TemplateParamSet = params
        resp = client.SendSms(req)
        print(resp.SendStatusSet[0].Code)
        return resp.SendStatusSet[0].Code == 'Ok'
    except TencentCloudSDKException as err:
        print(err)
        return False
