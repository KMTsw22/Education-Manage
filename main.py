import json
import sys
import time

from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from PyQt5.QtWidgets import *
from PyQt5.Qt import QFont, QSize
from PyQt5 import uic, Qt, QtCore
from Ui import Ui_Dialog

# form_class = uic.loadUiType("MainUi.ui")[0]
class MyWindow(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.StuList = []
        self.CheckBoxList = []
        self.StudentCount = 0
        self.InitUi()
    def InitUi(self):
        self.setupUi(self)
        self.Upload.clicked.connect(self.UploadInfor)
        self.UpdateBtn.clicked.connect(self.Update)
        self.Delete.clicked.connect(self.DeleteStudent)
        self.SendBtn.clicked.connect(self.Send)
        self.TotalInComeBtn.clicked.connect(self.FinalInCome)
        self.AccountBtn.clicked.connect(self.Account)
        self.AllBtn.stateChanged.connect(self.AllCheck)
        self.SetTable()
    def AllCheck(self):
        if self.AllBtn.isChecked():
            for i in range(len(self.StuList)):
                self.CheckBoxList[i].setChecked(True)
        else:
            for i in range(len(self.StuList)):
                self.CheckBoxList[i].setChecked(False)

    def checked(self):
        checkedList = []
        for i in range(self.StudentCount):
            if self.CheckBoxList[i].isChecked():
                checkedList.append(i)
        return checkedList
    def SetTable(self):
        self.StudentInfor.setRowCount(0)  # 모든 행 삭제
        self.StudentInfor.setColumnCount(0)  # 모든 열 삭제

        self.CheckBoxList = []
        # for i in range(len(self.CheckBoxList)):
        #     self.CheckBoxList[i].check(False)
        self.StuList = self.UploadEveryone()
        self.StudentCount = len(self.StuList)
        self.StudentInfor.setRowCount(len(self.StuList))
        self.StudentInfor.setColumnCount(7)
        self.StudentInfor.setHorizontalHeaderLabels(["선택", "이름", "나이", "학원비","교재비", "총", "전화번호"])
        for i in range(self.StudentCount):
            Check = QCheckBox()
            self.CheckBoxList.append(Check)
        for i in range(self.StudentCount):
            cellWidget = QWidget()
            layoutCB = QHBoxLayout(cellWidget)
            layoutCB.addWidget(self.CheckBoxList[i])
            layoutCB.setAlignment(QtCore.Qt.AlignCenter)
            layoutCB.setContentsMargins(0, 0, 0, 0)
            cellWidget.setLayout(layoutCB)
            self.StudentInfor.setCellWidget(i, 0, cellWidget)
            self.StudentInfor.setItem(i,1,QTableWidgetItem(self.StuList[i][0]))
            self.StudentInfor.setItem(i,2,QTableWidgetItem(self.StuList[i][1]))
            self.StudentInfor.setItem(i,3,QTableWidgetItem(self.StuList[i][2]))
            self.StudentInfor.setItem(i,4,QTableWidgetItem(self.StuList[i][3]))
            self.StudentInfor.setItem(i,5,QTableWidgetItem(self.StuList[i][4]))
            self.StudentInfor.setItem(i,6,QTableWidgetItem(self.StuList[i][5]))
        self.StudentInfor.setColumnWidth(0,2)

        self.Index.setMaximum(len(self.StuList)+1)
    def Update(self):
        UpdateData = { 'StudentInfor': []}

        for i in range(len(self.StuList)):
            name = self.StudentInfor.item(i, 1).text()
            age = self.StudentInfor.item(i, 2).text()
            cost = self.StudentInfor.item(i, 3).text()
            BookCost = self.StudentInfor.item(i, 4).text()
            TotalCost = self.StudentInfor.item(i, 5).text()
            telephone = self.StudentInfor.item(i, 6).text()
            UpdateData['StudentInfor'].append({'이름': name, '나이':age,'학원비':cost, '교재비':BookCost, '총': TotalCost, '전화번호':telephone})
        with open("ui.json", "w") as f:
            json.dump(UpdateData, f, indent=4)

    def getInfor(self):

        name = self.Name.text()
        cost = self.Cost.text()
        age = self.Age.text()
        telephone = self.TelePhone.text()
        BookCost = self.BookCost.text()
        if name==""or cost=="" or age == "" or telephone =="" or BookCost == "":
            return [1]
        TotalCost = (int(cost) + int(BookCost)) * 10000
        a = 1
        return [name, age, str(int(cost) * 10000), str(int(BookCost) * 10000), str(TotalCost),telephone]

    def UploadInfor(self):
        index = self.Index.value() - 1

        Student = self.getInfor()
        if len(Student) == 1:
            return

        infor = {
            "이름" : Student[0],
            "나이" : Student[1],
            "학원비" : str(Student[2]),
            "교재비" : str(Student[3]),
            "총" : str(Student[4]),
            "전화번호": Student[5]
        }
        with open('ui.json', 'r+') as file:
            file_content = json.load(file)
            UpdateData = {
                'StudentInfor': []
            }
            i = 0
            if index == -1:
                index = 0
            visited =  False
            for value in file_content["StudentInfor"]:
                if i == index:
                    UpdateData['StudentInfor'].append(infor)
                UpdateData['StudentInfor'].append(value)
                i += 1
            file_content["StudentInfor"].insert(index, infor)
            file.seek(0)
            json.dump(file_content, file, indent=4)
        self.UploadEveryone()
        self.SetTable()
    def UploadEveryone(self):
        self.StuList = []
        with open("ui.json", "r") as f:
            data = json.load(f)
        student_info = data['StudentInfor']
        for student in student_info:
            name = student['이름']
            age = student['나이']
            cost = student['학원비']
            BookCost = student['교재비']
            telephone = student['전화번호']
            TotalCost = int(BookCost) + int(cost)
            self.StuList.append([name, age, cost, BookCost, str(TotalCost), telephone])
        return self.StuList

    def DeleteStudent(self):
        with open("ui.json", "r") as f:
            data = json.load(f)
        checkedList = self.checked()
        UpdateData = {'StudentInfor':[]}
        for i in range(self.StudentCount):
            if i not in checkedList:
                UpdateData['StudentInfor'].append(data['StudentInfor'][i])

        with open('ui.json', 'w') as file:
            json.dump(UpdateData, file, indent=4)
        self.UploadEveryone()
        self.SetTable()
        print(self.CheckBoxList)
    def Account(self):
        from selenium.webdriver.common.by import By
        from selenium import webdriver
        driver = webdriver.Chrome()
        url = 'https://console.coolsms.co.kr/oauth2/login'
        driver.get('https://console.coolsms.co.kr/dashboard')
        id = "mintae1134@gmail.com"
        pwd = "kmt2003~"
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(id)
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(pwd)
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/div/div/main/div[2]/div/div/div/div/div/div/div/div/div[4]/div/div[2]/div/span/button/span[1]').click()
        Money = driver.find_element(By.XPATH,
                                    '/html/body/div[5]/div[4]/div/div/div/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[1]/div/div[1]/div/div[1]/p').text
        self.AccountText.setText(Money)
        driver.quit()
    def Send(self):
        CheckedBoxList = self.checked()
        studentList = []
        for i in range(len(self.StuList)):
            if i in CheckedBoxList:
                studentList.append(self.StuList[i])
        self.sendmessage(studentList)
        print(self.StuList)
    def FinalInCome(self):
        with open('ui.json', 'r') as json_file:
            json_data = json_file.read()
        # JSON을 파이썬 사전으로 변환
        dictionary = json.loads(json_data)
        # 파이썬 사전을 다시 JSON으로 변환
        json_data = json.dumps(dictionary,indent= 4, ensure_ascii=False)
        Month = self.MonthSelect.text()
        # 텍스트 파일로 저장
        with open(f'{Month}.txt', 'w') as text_file:
            text_file.write(json_data)

    def sendmessage(self, StudentList):
        api_key = ''
        api_secret = ''

        for i in range(len(StudentList)):
            name = StudentList[i][0]
            edu = StudentList[i][2]
            book = StudentList[i][3]
            total = StudentList[i][4]
            telephone = StudentList[i][5]
            params = dict()
            params['type'] = 'lms'  # Message type ( sms, lms, mms, ata )
            params['to'] = telephone  # Recipients Number '01000000000,01000000001'
            params['from'] = ''  # Sender number
            params['text'] = ''# # Message
            cool = Message(api_key, api_secret)
            # print(cool)
            try:
                response = cool.send(params)
                # print(response)
                # print("Success Count : %s" % response['success_count'])
                # print("Error Count : %s" % response['error_count'])
                # print("Group ID : %s" % response['group_id'])
                # print()
                self.SuccessMessage.setText(self.SuccessMessage.toPlainText() + name +" 학생 메시지 보내기 성공!\n")
                if "error_list" in response:
                    # print("Error List : %s" % response['error_list'])
                    pass
            except CoolsmsException as e:
                # print("Error Code : %s" % e.code)
                # print("Error Message : %s" % e.msg)
                pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
