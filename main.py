# -*- coding: utf-8 -*-

import requests
import uuid
import json
import os

# Proxy
proxies={
    'http':'http://127.0.0.1:7890/',
    'https':'http://127.0.0.1:7890/'
}


def getUUID():
    return uuid.uuid1()

def getParentDir(path=None, offset=-1):
    result = path if path else __file__
    for i in range(abs(offset)):
        result = os.path.dirname(result)
    return result

def getCourseId(url):
    cutUrl = url.split('li=')
    return cutUrl[1]

def getSubStr(s, start_str, stop_str):
    start_pos = s.find(start_str)
    if start_pos == -1:
        return None
    start_pos += len(start_str)
    stop_pos = s.find(stop_str, start_pos)
    if stop_pos == -1:
        return None
    return s[start_pos:stop_pos]

def loginAccount(username, password):
    url = 'https://appapi.xueanquan.com/usercenter/api/v1/account/PostLogin'

    data = '{"EquipmentId":"' + str(getUUID()) + '","Password":"' + password + '","Username":"' + username + '"}'

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'safetreeapp/1.8.7',
        'Content-Type': 'application/json'
    }

    requestData = requests.post(url, data=data, headers=headers, proxies=proxies)

    if(requestData.status_code == 200):
        return requestData.text
    else:
        return '-1'

def getHomeworkList(UserID, ServerSide):
    url = 'https://applet.xueanquan.com/pt/zhejiang/safeapph5/api/v1/homework/homeworklist'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'safetreeapp/1.8.7',
    }

    cookies = {
        'UserID': UserID,
        'EquipmentId': str(getUUID()),
        'ServerSide': ServerSide
    }

    requestData = requests.get(url, cookies=cookies, headers=headers, proxies=proxies)

    if(requestData.status_code == 200):
        return requestData.text
    else:
        return '-1'

def watchVideo(courseId, UserID, ServerSide, gradeId):
    videoSignUrl = 'https://yyapi.xueanquan.com/zhejiang/api/v1/StudentHomeWork/VideoPlayRecordSave?courseId=' + courseId + '&gradeId=' + gradeId

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'safetreeapp/1.8.7',
    }

    cookies = {
        'UserID': UserID,
        'EquipmentId': str(getUUID()),
        'ServerSide': ServerSide
    }

    videoSignData = requests.post(videoSignUrl, cookies=cookies, headers=headers, proxies=proxies)

    try:
        videoSignMsg = json.loads(videoSignData.text)
    except:
        print('! 模块二执行失败')
        return False

    isVideoSignSuccess = videoSignMsg ['success']

    if(isVideoSignSuccess):
        return True
    else:
        return False

def doSkillTest(courseId, UserID, ServerSide, cityCode, schoolId, classroom, grade):
    testUrl = 'https://yyapi.xueanquan.com/zhejiang/api/v1/StudentHomeWork/GetSkillTestPaper?courseId=' + courseId

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'safetreeapp/1.8.7',
    }

    cookies = {
        'UserID': UserID,
        'EquipmentId': str(getUUID()),
        'ServerSide': ServerSide
    }

    skillTestData = requests.get(testUrl, cookies=cookies, headers=headers, proxies=proxies)

    try:
        skillTestMsg = json.loads(skillTestData.text)
    except:
        print('! 模块二执行失败')
        return False

    skillTestResult = skillTestMsg ['result']

    skillTestFid = skillTestResult ['fid']
    skillTestWordId = skillTestResult ['workId']

    if(skillTestFid == '' or skillTestWordId == ''):
        print('! 模块二执行失败')
        return False

    testSignUrl = 'https://yyapi.xueanquan.com/zhejiang/api/v1/StudentHomeWork/HomeWorkSign'

    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'safetreeapp/1.8.7',
    }

    cookies = {
        'UserID': UserID,
        'EquipmentId': str(getUUID()),
        'ServerSide': ServerSide
    }

    data = '{"workId":' + str(skillTestWordId) + ',"fid":' + str(skillTestFid) + ',"testinfo":"已掌握技能","testanswer":"0|0|0","testMark":100,"testResult":1,"courseId":"' + str(courseId) + '","grade":' + str(grade) + ',"cityCode":' + str(cityCode) + ',"schoolId":' + str(schoolId) + ',"classroom":' + str(classroom) + '}'

    requestData = requests.post(testSignUrl, data=data.encode('utf-8'), cookies=cookies, headers=headers, proxies=proxies)

    try:
        requestMsg = json.loads(requestData.text)
    except:
        print('! 模块二执行失败')
        return False

    isSkillTestSuccess = requestMsg ['success']

    if(isSkillTestSuccess):
        return True
    else:
        return False

def doHomework(courseId, UserID, ServerSide, cityCode, schoolId, classroom, grade, gradeId):
    print('+ 正在自动完成模块一 (视频)...')
    
    if(watchVideo(courseId, UserID, ServerSide, gradeId)):
        print('+ 已完成模块一 (视频)')
        return True
    else:
        print('+ 未完成模块一 (视频)')
        return False

    print('+ 正在自动完成模块二 (答题)...')

    if(doSkillTest(courseId, UserID, ServerSide, cityCode, schoolId, classroom, grade)):
        print('+ 已完成模块二 (答题)')
        return True
    else:
        print('+ 未完成模块二 (答题)')
        return False

def doSpecialSign(specialId, UserID, ServerSide):

    # TO-DO 通用 API 替换
    # /Topic/topic/main/api/v1/
    url = 'https://huodongapi.xueanquan.com/p/zhejiang/Topic/topic/platformapi/api/v1/records/sign'

    for currentWork in range(1, 3):

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'safetreeapp/1.8.7',
        }

        cookies = {
            'UserID': UserID,
            'EquipmentId': str(getUUID()),
            'ServerSide': ServerSide
        }

        data = '{"specialId":' + specialId + ',"step":' + str(currentWork) + '}'

        requestData = requests.post(url, data=data, headers=headers, cookies=cookies, proxies=proxies)

        try:
            specialSignMsg = json.loads(requestData.text)
        except:
            print('! 执行失败')
            return False

        isSignSeccuss = specialSignMsg ['result']
        signMsg = specialSignMsg ['msg']

        if(isSignSeccuss):
            print('+ 已完成第 ' + str(currentWork) + ' 个模块，' + signMsg)
        else:
            print('! 不能完成第 ' + str(currentWork) + ' 个模块，' + signMsg)

def getspecialId(url):
    parentUrl = getParentDir(url)
    jsUrl = parentUrl + "/js/common.js"

    requestData = requests.get(jsUrl, proxies=proxies)
    requestText = requestData.text

    releaseData = getSubStr(requestText, "release:{", "}")

    return getSubStr(releaseData, "specialId: ", ",")

def doSpecial(url, UserID, ServerSide):
    print('+ 正在自动完成专题活动...')

    specialId = getspecialId(url)

    print("* 活动 ID: " + specialId)

    if(specialId == '' or specialId == '0'):
        print("! 执行失败，活动不存在")
        return
    
    doSpecialSign(specialId, UserID, ServerSide)

def doWorkUtil(username, password):
    accountLogin = loginAccount(username, password)

    print('\n- 当前账号: ' + username)
    print('- 正在登录...\n')

    try:
        accountMsg = json.loads(accountLogin)
    except:
        print('! 登录失败，返回信息有误')
        exit()
    
    accountData = accountMsg ['data']

    try:
        webUrl = accountData ['webUrl']
        UserId = accountData ['accessCookie']
        grade = accountData ['grade']
        cityId = accountData ['cityId']
        schoolId = accountData ['schoolId']
        classroomId = accountData ['classroomId']
    except:
        print('! 登录失败，请检查账号信息是否有误')
        exit()

    if(grade == '' or cityId == '' or schoolId == '' or classroomId == ''):
        print('! 登录失败，请检查账号信息是否有误')
        exit()

    homeworkList = getHomeworkList(UserId, webUrl)

    try:
        workListData = json.loads(homeworkList)
    except:
        print('! 登录失败，返回信息有误')
        exit()

    print('- 正在解析任务列表...')

    numOfWork = len(workListData)

    print('= 获取到了 ' + str(numOfWork) + ' 个任务\n')

    for currentWork in range(numOfWork):
        print('> 正在解析第 ' + str(currentWork + 1) + '/' + str(numOfWork) + ' 个任务 ===================')
        currentWorkData = workListData [currentWork]

        currentWorkTitle = currentWorkData ['title']
        currentWorkUrl = currentWorkData ['url']
        workStatus = currentWorkData ['workStatus']
        currentWorkType = currentWorkData ['sort']

        print('= 当前课程标题: ' + currentWorkTitle)
        print('= 当前课程链接: ' + currentWorkUrl)
        
        if(currentWorkType == 'Skill'):
            print('= 当前课程类型: ' + '普通课程')
        elif(currentWorkType == 'Special'):
            print('= 当前课程类型: ' + '专题活动')
        else:
            print('= 当前课程类型: ' + '未知')

        if(workStatus == 'Finished'):
            print('= 当前课程完成情况: ' + '已完成')
        elif(workStatus == 'UnFinish'):
            print('= 当前课程完成情况: ' + '未完成')
            if(currentWorkType == 'Skill'):
                courseId = getCourseId(currentWorkUrl)
                gradeId = getSubStr(currentWorkUrl, 'gid=', '&')
                print('= 当前课程编号: ' + courseId)
                doHomework(courseId, UserId, webUrl, cityId, schoolId, classroomId, grade, gradeId)
            elif(currentWorkType == 'Special'):
                specialUrl = str(currentWorkUrl).replace('index', 'jiating')
                doSpecial(specialUrl, UserId, webUrl)
            else:
                print('! 未知错误')
        else:
            print('= 当前课程完成情况: ' + '未知')
        print('< 完成解析第 ' + str(currentWork + 1) + '/' + str(numOfWork) + ' 个任务 ===================\n')

if __name__ == '__main__':
    currentPath = os.getcwd()
    pathArg = os.sep

    configFilePath = currentPath + pathArg + 'account.txt'
    configFile = open(configFilePath, 'r', encoding = 'UTF-8')
    configFileContent = configFile.read()

    configArray = configFileContent.split('\n')
    numOfAccount = len(configArray)

    failWork = 0

    print('\n- 共 ' + str(numOfAccount) + ' 个账号')

    for currentAccount in range(numOfAccount):
        splitAccount = configArray [currentAccount].split(',')

        username = splitAccount [0]
        password = splitAccount [1]

        doWorkUtil(username, password)