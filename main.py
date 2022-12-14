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
        print('! ?????????????????????')
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
        print('! ?????????????????????')
        return False

    skillTestResult = skillTestMsg ['result']

    skillTestFid = skillTestResult ['fid']
    skillTestWordId = skillTestResult ['workId']

    if(skillTestFid == '' or skillTestWordId == ''):
        print('! ?????????????????????')
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

    data = '{"workId":' + str(skillTestWordId) + ',"fid":' + str(skillTestFid) + ',"testinfo":"???????????????","testanswer":"0|0|0","testMark":100,"testResult":1,"courseId":"' + str(courseId) + '","grade":' + str(grade) + ',"cityCode":' + str(cityCode) + ',"schoolId":' + str(schoolId) + ',"classroom":' + str(classroom) + '}'

    requestData = requests.post(testSignUrl, data=data.encode('utf-8'), cookies=cookies, headers=headers, proxies=proxies)

    try:
        requestMsg = json.loads(requestData.text)
    except:
        print('! ?????????????????????')
        return False

    isSkillTestSuccess = requestMsg ['success']

    if(isSkillTestSuccess):
        return True
    else:
        return False

def doHomework(courseId, UserID, ServerSide, cityCode, schoolId, classroom, grade, gradeId):
    print('+ ??????????????????????????? (??????)...')
    
    if(watchVideo(courseId, UserID, ServerSide, gradeId)):
        print('+ ?????????????????? (??????)')
        return True
    else:
        print('+ ?????????????????? (??????)')
        return False

    print('+ ??????????????????????????? (??????)...')

    if(doSkillTest(courseId, UserID, ServerSide, cityCode, schoolId, classroom, grade)):
        print('+ ?????????????????? (??????)')
        return True
    else:
        print('+ ?????????????????? (??????)')
        return False

def doSpecialSign(specialId, UserID, ServerSide):

    # TO-DO ?????? API ??????
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
            print('! ????????????')
            return False

        isSignSeccuss = specialSignMsg ['result']
        signMsg = specialSignMsg ['msg']

        if(isSignSeccuss):
            print('+ ???????????? ' + str(currentWork) + ' ????????????' + signMsg)
        else:
            print('! ??????????????? ' + str(currentWork) + ' ????????????' + signMsg)

def getspecialId(url):
    parentUrl = getParentDir(url)
    jsUrl = parentUrl + "/js/common.js"

    requestData = requests.get(jsUrl, proxies=proxies)
    requestText = requestData.text

    releaseData = getSubStr(requestText, "release:{", "}")

    return getSubStr(releaseData, "specialId: ", ",")

def doSpecial(url, UserID, ServerSide):
    print('+ ??????????????????????????????...')

    specialId = getspecialId(url)

    print("* ?????? ID: " + specialId)

    if(specialId == '' or specialId == '0'):
        print("! ??????????????????????????????")
        return
    
    doSpecialSign(specialId, UserID, ServerSide)

def doWorkUtil(username, password):
    accountLogin = loginAccount(username, password)

    print('\n- ????????????: ' + username)
    print('- ????????????...\n')

    try:
        accountMsg = json.loads(accountLogin)
    except:
        print('! ?????????????????????????????????')
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
        print('! ????????????????????????????????????????????????')
        exit()

    if(grade == '' or cityId == '' or schoolId == '' or classroomId == ''):
        print('! ????????????????????????????????????????????????')
        exit()

    homeworkList = getHomeworkList(UserId, webUrl)

    try:
        workListData = json.loads(homeworkList)
    except:
        print('! ?????????????????????????????????')
        exit()

    print('- ????????????????????????...')

    numOfWork = len(workListData)

    print('= ???????????? ' + str(numOfWork) + ' ?????????\n')

    for currentWork in range(numOfWork):
        print('> ??????????????? ' + str(currentWork + 1) + '/' + str(numOfWork) + ' ????????? ===================')
        currentWorkData = workListData [currentWork]

        currentWorkTitle = currentWorkData ['title']
        currentWorkUrl = currentWorkData ['url']
        workStatus = currentWorkData ['workStatus']
        currentWorkType = currentWorkData ['sort']

        print('= ??????????????????: ' + currentWorkTitle)
        print('= ??????????????????: ' + currentWorkUrl)
        
        if(currentWorkType == 'Skill'):
            print('= ??????????????????: ' + '????????????')
        elif(currentWorkType == 'Special'):
            print('= ??????????????????: ' + '????????????')
        else:
            print('= ??????????????????: ' + '??????')

        if(workStatus == 'Finished'):
            print('= ????????????????????????: ' + '?????????')
        elif(workStatus == 'UnFinish'):
            print('= ????????????????????????: ' + '?????????')
            if(currentWorkType == 'Skill'):
                courseId = getCourseId(currentWorkUrl)
                gradeId = getSubStr(currentWorkUrl, 'gid=', '&')
                print('= ??????????????????: ' + courseId)
                doHomework(courseId, UserId, webUrl, cityId, schoolId, classroomId, grade, gradeId)
            elif(currentWorkType == 'Special'):
                specialUrl = str(currentWorkUrl).replace('index', 'jiating')
                doSpecial(specialUrl, UserId, webUrl)
            else:
                print('! ????????????')
        else:
            print('= ????????????????????????: ' + '??????')
        print('< ??????????????? ' + str(currentWork + 1) + '/' + str(numOfWork) + ' ????????? ===================\n')

if __name__ == '__main__':
    currentPath = os.getcwd()
    pathArg = os.sep

    configFilePath = currentPath + pathArg + 'account.txt'
    configFile = open(configFilePath, 'r', encoding = 'UTF-8')
    configFileContent = configFile.read()

    configArray = configFileContent.split('\n')
    numOfAccount = len(configArray)

    failWork = 0

    print('\n- ??? ' + str(numOfAccount) + ' ?????????')

    for currentAccount in range(numOfAccount):
        splitAccount = configArray [currentAccount].split(',')

        username = splitAccount [0]
        password = splitAccount [1]

        doWorkUtil(username, password)