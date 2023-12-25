from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json

AccessKey_ID = 'LTAI5t9asHV1ydNb12XtzV2W'
AccessKey_Secret = '6ntiLaldnEufILbtR1CfMu3YeG0MFt'


def send_sms(mobile_phone, code):
    """
        阿里云短信服务公用接口
        :param action: 指明短信相关的哪些接口
        :param query_param_dict: 短信相关接口的参数（字典形式）
        :return:
    """
    query_param_dict = {
        # 签名
        'SignName': 'harden',
        # 模板编号
        'TemplateCode': 'SMS_464345728',
        # 发给谁
        'PhoneNumbers': mobile_phone,
        # 发送验证码内容
        'TemplateParam ': {"code": code}
    }
    client = AcsClient(AccessKey_ID, AccessKey_Secret, 'default')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    # 以上部分是公用的不变
    request.set_action_name('SendSms')
    # set_action_name 这个是选择你调用的接口的名称，如：SendSms，SendBatchSms等
    request.add_query_param('RegionId', "default")
    # 这个参数也是固定的

    # request.add_query_param('PhoneNumbers', mobile_phone)  # 发给谁
    # request.add_query_param('SignName', "harden")  # 签名
    # request.add_query_param('TemplateCode', "SMS_464345728")  # 模板编号
    # template = {
    #     'code': code,
    # }
    # request.add_query_param('TemplateParam', f"{template}")  # 发送验证码内容
    for k, v in query_param_dict.items():
        if type(v) == "enum":
            return
        request.add_query_param(k, v)
    response = client.do_action_with_exception(request)
    return json.loads(str(response, encoding='utf-8'))


if __name__ == '__main__':
    phone = '15616435916'
    code = '1234'
    send_sms(phone, code)
    # {"Message":"触发分钟级流控Permits:1","RequestId":"CDDD2912-5BD5-5296-8785-9950F3CF9B6D","Code":"isv.BUSINESS_LIMIT_CONTROL"}
