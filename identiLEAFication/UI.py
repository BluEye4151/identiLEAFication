import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import re
import ClientController
import Struct
import numpy

class UserInterface(tk.Frame):
    def __init__(self, master):
        super(UserInterface, self).__init__(master)
        # must ----------------------------------------------------------------
        self.clientController = ClientController.ClientController() # including NN and DB init
        
        # variables and info --------------------------------------------------
        self.searchIcon = ImageTk.PhotoImage(Image.open('./icons/search.png').resize((19,19)))
        self.cameraIcon = ImageTk.PhotoImage(Image.open('./icons/camera.png').resize((200,200)))
        self.currentImage = Image.open('./icons/waiting.png')
        self.displayIcon = ImageTk.PhotoImage(self.currentImage.resize((300,300)))
        self.loadingIcon = ImageTk.PhotoImage(Image.open('./icons/loading.png'))
        self.errorIcon = ImageTk.PhotoImage(Image.open('./icons/error.png'))
        self.filepath = ''
        self.currentPage = 'main'
        self.imgIsLoaded = False
        self.displayName = ''
        self.displayInfo = ''
        self.varClass = tk.StringVar()
        self.varFamily = tk.StringVar()
        self.varSpecies = tk.StringVar()
        self.varIllname = tk.StringVar()
        self.queriedIcon = ImageTk.PhotoImage(Image.open('./icons/waiting.png').resize((150,150)))
        self.dictionaryC2E, self.dictionaryE2C = Struct.loadDictionary()
        self.authorizationClick = 0
        self.chooseMode = tk.StringVar()
        self.modeChoice = ''
        
        # widgets -------------------------------------------------------------
        self.null=tk.Label(self, width=1)
        # 搜索功能——输入框.....主界面
        self.searchEntry=tk.Entry(self, width=38)   
        # 搜索功能——开始搜索...主界面
        self.searchButton=tk.Button(self, height=20, width=20, image=self.searchIcon,
                                    command=lambda:self.search())  
        # 进入识图——界面按钮...主界面
        self.cameraButton=tk.Button(self, height=200, width=200, image=self.cameraIcon,
                                    command=lambda:self.MainToPhotoPage())    
        # 识叶标签——示意.......主界面
        self.welcomeLabel=tk.Label(self, text='识叶', font=('楷体',15))   
        # 查询功能——界面切换...主界面
        self.inquireButton=tk.Button(self, text='查询', font=('楷体',15),
                                     command=lambda:self.MainToInquirePage())   
        # 说明功能——弹出提示框.主界面、照片界面、信息界面、查询界面
        self.instructButton=tk.Button(self, text='说明', font=('楷体',15),
                                      command=lambda:self.tips())  
        # 帮助弹窗——消息框.....主界面、照片界面、信息界面、查询界面
        self.instructBox=tk.messagebox       
        # 选择图片——按钮.......照片界面
        self.selectButton=tk.Button(self, text='选择图片', font=('楷体',15),
                                    command=lambda:self.selectImage())    
        # 展示图片——标签.......照片界面、信息界面
        self.pictureLabel=tk.Label(self, height=300, width=300, image=self.displayIcon)  
        # 返回主页——按钮.......照片界面、信息界面、查询界面
        self.backButton=tk.Button(self, text='返回', font=('楷体',15))  
        # 识别图片——按钮.......照片界面
        self.recogButton=tk.Button(self, text='识别图片', font=('楷体',15),
                                   command=lambda:self.PhotoToInfoPage())   
        # 病害名称——文字.......信息界面
        self.illnameText=tk.Text(self, width=16, height=5, font=('等线', 11), wrap='word')   
        # 详细信息——文字.......信息界面
        self.infomationText=tk.Text(self, width=45, height=20,
                                    yscrollcommand=tk.Scrollbar(self).set)
        # 继续识别——切换页面...信息界面
        self.continueButton=tk.Button(self, text='继续识别', font=('楷体',15),
                                      command=lambda:self.InfoToPhotoPage())  
        # 筛选某纲——下拉框.....查询界面
        self.classBox=ttk.Combobox(self, textvariable=self.varClass, width=17, font=12,
                                   value=self.E2Clookup(('Monocotyledons','Dicotyledoneae')))
        self.classBox.bind("<<ComboboxSelected>>",self.updateFamily)
        self.classTip=tk.Label(self, text='纲', font=('等线',12))
        # 筛选某科——下拉框.....查询界面 
        self.familyBox=ttk.Combobox(self, textvariable=self.varFamily, width=17, font=12) 
        self.familyBox.bind("<<ComboboxSelected>>",self.updateSpecies)
        self.familyTip=tk.Label(self, text='科', font=('等线',12))
        # 筛选某种——下拉框.....查询界面
        self.speciesBox=ttk.Combobox(self, textvariable=self.varSpecies, width=17, font=12) 
        self.speciesBox.bind("<<ComboboxSelected>>",self.updateIllname)
        self.speciesTip=tk.Label(self, text='种', font=('等线',12))
        # 筛选病害——下拉框.....查询界面
        self.illnameBox=ttk.Combobox(self, textvariable=self.varIllname, width=17, font=12)
        self.illnameTip=tk.Label(self, text='病害情况', font=12)
        # 提交查询——按钮.......查询界面
        self.admitButton=tk.Button(self, text='查询', font=('楷体',15),
                                   command=lambda:self.updateInfo())  
        # 查询结果——标签.......查询界面
        self.queriedIconLabel=tk.Label(self, width=150, height=150, image=self.queriedIcon)
        # 查询结果——文字.......查询界面
        self.queriedInfoText=tk.Text(self, width=27, height=15)
        # 选择模式——下拉框.......管理员界面
        self.chooseModeTip=tk.Label(self, text='选择模式', font=('等线',12))
        self.chooseModeBox=ttk.Combobox(self, textvariable=self.chooseMode, 
                                        width=25, font=12,
                                        value=('插入图片','删除记录','更新记录','MySQL语句'))
        self.chooseModeBox.bind("<<ComboboxSelected>>",self.updateAdminPage)
        # 修改细节——下拉框.......管理员界面
        self.targetTableBox=ttk.Combobox(self, width=25, font=12)
        self.targetTableBox.bind("<<ComboboxSelected>>",self.updateRecordInfo)
        self.targetTableTip=tk.Label(self, text='目标表格', font=('等线',12))
        self.targetTupleBox=ttk.Combobox(self, width=25, font=12)
        self.targetTupleBox.bind("<<ComboboxSelected>>",self.updateAttributeInfo)
        self.targetTupleTip=tk.Label(self, text='目标记录', font=('等线',12))
        self.targetAttributeBox=ttk.Combobox(self, width=25, font=12)
        self.targetAttributeBox.bind("<<ComboboxSelected>>",self.originalValue)
        self.targetAttributeTip=tk.Label(self, text='目标字段', font=('等线',12))
        self.newInfomationText=tk.Text(self, width=38, height=20)
        self.newInfomationTip=tk.Label(self, text='更新记录', font=('等线',12))
        self.executeQueryButton=tk.Button(self, text='执行', font=('楷体',15),
                                          command=lambda:self.executeAdminQuery())
        self.chosenPictureLabel=tk.Label(self, height=150, width=150,
                             image=ImageTk.PhotoImage(Image.open('./icons/waiting.png')))
        self.updateTupleText=tk.Text(self, width=45, height=20)
        
        # initialize methods --------------------------------------------------
        self.createMainPage()
        self.grid()
        self.clientController = ClientController.ClientController()
        
        # pre-load variables --------------------------------------------------
        

#==========================page changeing methods==============================
    def MainToPhotoPage(self):
        self.quitMainPage()
        self.currentPage = 'photo'        
        self.createPhotoPage()
        
    def PhotoToMainPage(self):
        self.quitPhotoPage()
        self.currentPage = 'main'
        self.createMainPage()
        
    def PhotoToInfoPage(self):
        self.quitPhotoPage()
        self.currentPage = 'info'
        self.createInfoPage()
        self.predict()

    def InfoToMainPage(self):
        self.quitInfoPage()
        self.currentPage = 'main'
        self.createMainPage()
        
    def InfoToPhotoPage(self):
        self.quitInfoPage()
        self.currentPage = 'photo'
        self.createPhotoPage()
        
    def MainToInquirePage(self):
        self.quitMainPage()
        self.currentPage = 'inquire'
        self.createInquirePage()
        
    def InquireToMainPage(self):
        self.quitInquirePage()
        self.currentPage = 'main'
        self.createMainPage()
      
    def InquireToAdminPage(self):
        self.quitInquirePage()
        self.currentPage = 'admin'
        self.createAdminPage()
        
    def AdminToInquirePage(self):
        self.clearAdminPage('all')
        self.currentPage = 'inquire'
        self.createInquirePage()
        
#================================create pages==================================
    def createMainPage(self):
        self.searchEntry.grid(row=0, column=0, padx=20, pady=20, columnspan=10) 
        self.searchButton.grid(row=0, column=11, columnspan=3)
        self.welcomeLabel.grid(row=1, column=7)
        self.cameraButton.grid(row=2, column=7, pady=50)  
        self.inquireButton.grid(row=3, column=4, columnspan=5, sticky='W')
        self.instructButton.grid(row=3, column=5, columnspan=6, sticky='E')     
        
    def quitMainPage(self):
        self.searchEntry.grid_forget()
        self.searchButton.grid_forget()
        self.cameraButton.grid_forget()
        self.welcomeLabel.grid_forget()
        self.null.grid_forget()
        self.inquireButton.grid_forget()
        self.instructButton.grid_forget()
    
    def createPhotoPage(self):
        self.imgIsLoaded = False
        self.displayIcon = ImageTk.PhotoImage(Image.open('./icons/waiting.png').resize((300,300)))
        self.pictureLabel.config(image=self.displayIcon)
        self.backButton.config(command=lambda:self.PhotoToMainPage())
        self.pictureLabel.config(height=300, width=300)
        self.backButton.config(text='返回')
        self.selectButton.grid(row=0, column=5, pady=14)
        self.null.grid(row=1)
        self.pictureLabel.grid(row=2, column=2, padx=12, columnspan=9)
        self.backButton.grid(row=3, column=0, columnspan=3, padx=12, pady=30, sticky='E')
        self.recogButton.grid(row=3,column=5)
        self.instructButton.grid(row=3, column=8, columnspan=3, sticky='W')
        
    def quitPhotoPage(self):
        self.selectButton.grid_forget()
        self.null.grid_forget()
        self.pictureLabel.grid_forget()
        self.backButton.grid_forget()
        self.recogButton.grid_forget()
        self.instructButton.grid_forget()     
    
    def createInfoPage(self):
        self.backButton.config(command=lambda:self.InfoToMainPage())
        self.pictureLabel.config(height=150, width=150)
        self.backButton.config(text='主菜单')
        self.pictureLabel.grid(row=0, column=0, padx=20, pady=5, rowspan=3, columnspan=8)
        self.illnameText.grid(row=1, column=8)
        self.infomationText.grid(row=3, columnspan=10, padx=18)
        self.continueButton.grid(row=4, column=0)
        self.backButton.grid(row=4, column=7)
        self.instructButton.grid(row=4, column=8, columnspan=3, sticky='E')
    
    def quitInfoPage(self):
        self.backButton.grid_forget()
        self.pictureLabel.grid_forget()
        self.illnameText.grid_forget()
        self.infomationText.grid_forget()
        self.continueButton.grid_forget()
        self.instructButton.grid_forget()
    
    def createInquirePage(self):
        # set page to default settings
        self.queriedIcon = ImageTk.PhotoImage(Image.open('./icons/waiting.png').resize((150,150)))
        self.queriedIconLabel.config(image=self.queriedIcon)
        self.queriedInfoText.delete(0.0, tk.END)
        self.familyBox.set('')
        self.classBox.set('')
        self.speciesBox.set('')
        self.illnameBox.set('')
        self.backButton.config(command=lambda:self.InquireToMainPage())
        # create widgets
        self.classTip.grid(row=0, column=0, pady=10)
        self.classBox.grid(row=0, column=1, columnspan=3, sticky='W')
        self.familyTip.grid(row=1, column=0, pady=10)
        self.familyBox.grid(row=1, column=1, columnspan=3, sticky='W')
        self.speciesTip.grid(row=2, column=0, pady=10)
        self.speciesBox.grid(row=2, column=1, columnspan=3, sticky='W')
        self.illnameTip.grid(row=3, column=0, pady=10)
        self.illnameBox.grid(row=3, column=1, columnspan=3, sticky='W')
        self.queriedIconLabel.grid(row=4, column=0, pady=10)
        self.queriedInfoText.grid(row=4, column=1)
        self.backButton.grid(row=5, column=0, pady=20)
        self.admitButton.grid(row=5, column=1, sticky='W')
        self.instructButton.grid(row=5, column=1, sticky='E')
        
    def quitInquirePage(self):
        self.backButton.grid_forget()
        self.classTip.grid_forget()
        self.classBox.grid_forget()
        self.familyTip.grid_forget()
        self.familyBox.grid_forget()
        self.speciesTip.grid_forget()
        self.speciesBox.grid_forget()
        self.illnameTip.grid_forget()
        self.illnameBox.grid_forget()
        self.admitButton.grid_forget()
        self.instructButton.grid_forget()
        self.queriedIconLabel.grid_forget()
        self.queriedInfoText.grid_forget()
    
    def createAdminPage(self):
        self.chooseModeBox.set('')
        self.backButton.config(command=lambda:self.AdminToInquirePage())
        self.targetTableBox.config(value=(self.clientController.
                                          inquire('show tables from plantvillage',
                                                  mode='relation')))     
        self.backButton.grid(row=0, column=0, pady=10)
        self.executeQueryButton.grid(row=0, column=2)
        self.instructButton.grid(row=0, column=4)
        self.chooseModeTip.grid(row=1, column=0, pady=10)
        self.chooseModeBox.grid(row=1, column=1, columnspan=4, sticky='W')
    
#============================application methods===============================
    def selectImage(self):
        if self.currentPage=='photo':
            try:
                self.filepath = filedialog.askopenfilename()
                self.currentImage = Image.open(self.filepath)
                self.displayIcon = ImageTk.PhotoImage(self.currentImage.resize((300,300)))
                self.pictureLabel.configure(image = self.displayIcon)
                self.update()
                self.imgIsLoaded = True
            except:
                self.imgIsLoaded = False
        elif self.currentPage=='admin':
            try:
                self.filepath = filedialog.askopenfilename()
                self.currentImage = Image.open(self.filepath)
                self.displayIcon = ImageTk.PhotoImage(self.currentImage.resize((150,150)))
                self.chosenPictureLabel.config(image = self.displayIcon)
                self.update()
            except:
                return
        
    def updateNameAndInfo(self, name, info):
        self.illnameText.delete(0.0, tk.END)
        self.illnameText.insert(tk.INSERT,name)
        self.infomationText.delete(0.0, tk.END)
        self.infomationText.insert(tk.INSERT,info)
        self.update()
        
    def predict(self):
        if (self.imgIsLoaded == False):
            self.updateNameAndInfo('啊哦 出错啦！','请选择图片后再进行识别！')
            return -1
        else:
            result = self.clientController.queryNN(self.currentImage) # ill name
            #----------extract species name from answer from NN-----------
            speciesName = re.search(r'[a-zA-Z]+', result).group()
            # --- query DB ---
            query = 'select * from ' + speciesName + ' where illness = "' + result + '"'
            #----------extract infomation from answer from DB----------
            result = self.clientController.inquire(query, mode='info')
            illnessName, illnessDetail, illnessSuggestion = self.modifyTextFromDB(result)
            self.updateNameAndInfo('物种:\n'+speciesName+'\n'+'病况:\n'+illnessName, 
                                   illnessDetail+'\n\n应对措施:\n'+illnessSuggestion)
            
    def modifyTextFromDB(self, textlist):
        # deal with illness name
        illnessName = re.sub(r'(_+)', ' ', textlist[0][0])
        illnessName = re.sub(r'([a-zA-Z]+\s)', '', illnessName, 1)
        #replace underlines with space
        illnessDetail = '  ' + textlist[0][2]
        # deal with illness suggestion
        illnessSuggestion = textlist[0][3]
        return illnessName, illnessDetail, illnessSuggestion
            
    def tips(self):
        if(self.currentPage=='main'):
            content = ("在上方输入框中输入关键字，点击搜索按钮，将提示完整内容\n\n"+
            "点击相机按钮进入识图页面\n\n"+
            "点击查询按钮进入纲——科——种——病害查询页面")
        elif(self.currentPage=='photo'):
            content = ("点击选择图片按钮打开资源管理器，选择待识别图片\n"+
                       "打开的图片会在屏幕中央处显示\n\n"+
                       "点击识别图片按钮即上传所选图片并识别\n"+
                       "这个过程可能需要等待几秒钟\n\n"+
                       "点击返回按钮回到主界面")
        elif(self.currentPage=='info'):
            content = ("右上文字框为物种名及病害名\n\n"+
                       "中央文字框为病害细节及推荐的应对措施\n\n"+
                       "点击继续识别回到图片选择界面\n\n"+
                       "点击主菜单按钮返回主界面")
        elif(self.currentPage=='inquire'):
            content = ("可通过下拉菜单选择对应的纲（等）\n"+
                       "也可以通过输入来选择查询对象\n"+
                       "点击查询按钮将根据用户选择返回信息\n"+
                       "左下图片为对应病害的一张示意图\n"+
                       "右下文字框内部分为病害的细节及应对方法\n"+
                       "点击返回按钮回到主界面")
        elif(self.currentPage=='admin'):
            content = ("数据库维护人员可在此界面进行数据库操作")
        title='帮助'    
        self.instructBox.showinfo(title, content)
        
    def updateFamily(self, *args):  # update next menu after selection in this combobox
        if(self.currentPage!='inquire'):
            return
        table = self.C2Elookup([self.classBox.get()])[0]
        query = 'select * from ' + str(table)
        answer = self.clientController.inquire(query, mode='relation')
        result = []
        for tuples in answer:
            result.append(tuples[0])
        result = self.E2Clookup(result)
        self.familyBox.config(value=result)
        self.familyBox.set('')
        self.speciesBox.set('')
        self.illnameBox.set('')
        self.update()
        
    def updateSpecies(self, *args):
        if(self.currentPage!='inquire'):
            return
        table = self.C2Elookup([self.familyBox.get()])[0]
        query = 'select * from ' + str(table)
        answer = self.clientController.inquire(query, mode='relation')
        result = []
        for tuples in answer:
            result.append(tuples[0])
        result = self.E2Clookup(result)
        self.speciesBox.config(value=result)
        self.speciesBox.set('')
        self.illnameBox.set('')
        self.update()
    
    def updateIllname(self, *args):
        if(self.currentPage!='inquire'):
            return
        table = self.C2Elookup([self.speciesBox.get()])[0]
        query = 'select * from ' + str(table)
        answer = self.clientController.inquire(query, mode='relation')
        result = []
        for tuples in answer:
            result.append(tuples[0])
        result = self.E2Clookup(result)
        self.illnameBox.config(value=result)
        self.illnameBox.set('')
        self.update()
    
    def updateInfo(self, *args):
        if(self.illnameBox.get() not in self.dictionaryC2E):
            if(self.illnameBox.get()=='20011231'):
                self.authorizationClick += 1 # 开发者模式
                if(self.authorizationClick>4):
                    self.InquireToAdminPage()
            self.queriedIconLabel.config(image=self.errorIcon)
            self.queriedInfoText.delete(0.0, tk.END)
            self.queriedInfoText.insert(tk.INSERT,'请正确输入要查询的内容')
            self.update()
            return
        if(self.currentPage!='inquire'):
            return
        self.queriedIconLabel.configure(image=self.loadingIcon)
        self.update()
        # step1: get relative infomation
        table = self.C2Elookup([self.speciesBox.get()])[0]
        ill = self.C2Elookup([self.illnameBox.get()])[0]
        query = 'select * from ' + str(table) + ' where illness = "' + ill + '"'
        answer = self.clientController.inquire(query, mode='info')
        illnessName, illnessDetail, illnessSuggestion = self.modifyTextFromDB(answer)
        self.queriedInfoText.delete(0.0, tk.END)
        self.queriedInfoText.insert(tk.INSERT,'病况:\n'+illnessDetail+'\n\n对策:\n'+illnessSuggestion)
        self.update()
        # step2: get a picture as an example
        query = 'select * from (SELECT * FROM ' + str(ill) + ' LIMIT 10) temptable ORDER BY RAND() limit 1'
        answer = self.clientController.inquire(query, mode='image') # pic is in answer[2]
        answer[0][2].save('./cache/img.png')
        self.queriedIcon = ImageTk.PhotoImage(Image.open('./cache/img.png').resize((150,150)))
        self.queriedIconLabel.configure(image=self.queriedIcon)
        self.update()
        
    def E2Clookup(self, tuples):
        result = []
        for item in tuples:
            result.append(self.dictionaryE2C[item])
        return tuple(result)
    
    def C2Elookup(self, tuples):
        result = []
        for item in tuples:
            result.append(self.dictionaryC2E[item])
        return tuple(result)
    
    def updateAdminPage(self, *args):
        self.targetTableBox.set('')
        self.targetTupleBox.set('')
        self.targetAttributeBox.set('')
        self.update()
        self.modeChoice = self.chooseModeBox.get()
        self.clearAdminPage('half')
        if self.modeChoice=='插入图片':
            self.targetTableTip.grid(row=2, column=0, pady=10)
            self.targetTableBox.grid(row=2, column=1, columnspan=4, sticky='W')
            self.selectButton.grid(row=3, column=0, columnspan=3)
            self.chosenPictureLabel.grid(row=3, column=3, columnspan=2, sticky='W')
        elif self.modeChoice=='删除记录':
            self.targetTableTip.grid(row=2, column=0, pady=10)
            self.targetTableBox.grid(row=2, column=1, columnspan=4, sticky='W')
            self.targetTupleTip.grid(row=3, column=0, pady=10)
            self.targetTupleBox.grid(row=3, column=1, columnspan=4, sticky='W')
        elif self.modeChoice=='更新记录':
            self.targetTableTip.grid(row=2, column=0, pady=10)
            self.targetTableBox.grid(row=2, column=1, columnspan=4, sticky='W')
            self.targetTupleTip.grid(row=3, column=0, pady=10)
            self.targetTupleBox.grid(row=3, column=1, columnspan=4, sticky='W')
            self.targetAttributeTip.grid(row=4, column=0, pady=10)
            self.targetAttributeBox.grid(row=4, column=1, columnspan=4, sticky='W')
            self.updateTupleText.grid(row=5, column=0, columnspan=5)
        elif self.modeChoice=='MySQL语句':
            self.updateTupleText.grid(row=2, column=0, columnspan=5)
        else:
            self.instructBox.showerror('Bad choice...', '请正确选择模式')
        
    def clearAdminPage(self, mode):
        if mode=='half':
            self.targetTableTip.grid_forget()
            self.targetTableBox.grid_forget()
            self.targetTupleTip.grid_forget()
            self.targetTupleBox.grid_forget()
            self.newInfomationTip.grid_forget()
            self.newInfomationText.grid_forget()
            self.selectButton.grid_forget()
            self.chosenPictureLabel.grid_forget()
            self.updateTupleText.grid_forget()
            self.targetAttributeTip.grid_forget()
            self.targetAttributeBox.grid_forget()
        elif mode=='all':
            self.clearAdminPage('half')
            self.backButton.grid_forget()
            self.chooseModeTip.grid_forget()
            self.chooseModeBox.grid_forget()
            self.executeQueryButton.grid_forget()
            self.instructButton.grid_forget()
            
    def executeAdminQuery(self):
        if self.modeChoice=='插入图片':
            try:
                ID=(self.filepath.split('/')[len(self.filepath.split('/'))-1]#name without postfix
                    [0:len(self.filepath.split('/')[len(self.filepath.split('/'))-1])-4])
                category = str(self.targetTableBox.get())
                img = Image.open(self.filepath).resize((256,256))
                pic = numpy.array(img).reshape(256*256*3)
                stringpic = ''
                for i in range(len(pic)):
                    stringpic+=(str(pic[i])+',')
                stringpic = stringpic[:len(stringpic)-1]
                sql = "insert into " + str(self.targetTableBox.get()) + " values(%s,%s,%s)"
                ret = self.clientController.cursor.execute(sql,(ID,category,numpy.array(stringpic)))
                self.clientController.conn.commit()
                if(ret!=0):
                    self.instructBox.showinfo('插入命令执行结果', '图片插入成功！')
                else:
                    self.instructBox.showinfo('插入命令执行结果', '图片插入失败...')
            except:
                self.instructBox.showinfo('插入命令执行结果', '图片插入失败...')
        if self.modeChoice=='删除记录':
            try:
                targetTable = self.targetTableBox.get()
                deleteTarget = self.targetTupleBox.get()
                attr = self.clientController.inquire('SHOW FULL FIELDS FROM '+str(targetTable),
                                                     mode='relation')
                query=('delete from '+targetTable+' where '+str(attr[0][0])+
                       ' = "'+ str(deleteTarget)) + '"'
                print(query)
                ret = self.clientController.cursor.execute(query)
                self.clientController.conn.commit()
                if(ret!=0):
                    self.instructBox.showinfo('删除命令执行结果', '记录删除成功！')
                else:
                    self.instructBox.showinfo('删除命令执行结果', '记录删除失败...')
            except:
                self.instructBox.showinfo('删除命令执行结果', '记录删除失败...')
        if self.modeChoice=='更新记录':
            try:
                targetTable = self.targetTableBox.get()
                attr = self.clientController.inquire('SHOW FULL FIELDS FROM '+str(targetTable),
                                                     mode='relation')
                query=('update ' + targetTable +
                       ' set ' + self.targetAttributeBox.get() + '="' + 
                       str(self.updateTupleText.get(0.0, tk.END)) + '"' +
                       ' where ' + str(attr[0][0]) +
                       ' = "' + self.targetTupleBox.get() + '"')
                ret = self.clientController.cursor.execute(query)
                self.clientController.conn.commit()
                if(ret!=0):
                    self.instructBox.showinfo('更新命令执行结果', '记录更新成功！')
                else:
                    self.instructBox.showinfo('删除命令执行结果', '记录更新失败...')
            except:
                self.instructBox.showinfo('删除命令执行结果', '记录更新失败...')
        if self.modeChoice=='MySQL语句':
            try:
                query = self.updateTupleText.get(0.0, tk.END)
                ret = self.clientController.cursor.execute(query)
                self.clientController.conn.commit()
                if(ret!=0):
                    self.instructBox.showinfo('MySQL命令执行结果', '命令执行成功！')
                else:
                    self.instructBox.showinfo('MySQL命令执行结果', '命令执行成功...')
            except:
                self.instructBox.showinfo('MySQL命令执行结果', '命令执行成功...')
        
    def updateRecordInfo(self, *args):
        self.targetTupleBox.set('')
        self.targetAttributeBox.set('')
        self.update()
        targetTable = self.targetTableBox.get()
        attr = self.clientController.inquire('SHOW FULL FIELDS FROM '+str(targetTable),
                                             mode='relation')
        query = 'select ' + str(attr[0][0]) + ' from ' + str(targetTable)
        primaryKeyValues = self.clientController.inquire(query, mode='relation')
        self.targetTupleBox.config(value=tuple(primaryKeyValues))
        self.update()
        
    def updateAttributeInfo(self, *args):
        self.targetAttributeBox.set('')
        self.update()
        targetTable = self.targetTableBox.get()
        attr = self.clientController.inquire('SHOW FULL FIELDS FROM '+str(targetTable),
                                             mode='relation')
        result = []
        for item in attr:
            result.append(str(item[0]))    # stores all attr name
        if(result[2]=='image'):  # delete image in case the programme dies
            result = result[0:2]
        self.targetAttributeBox.config(value=tuple(result))
        self.update()
        
    def originalValue(self, *args):
        attr = self.clientController.inquire('SHOW FULL FIELDS FROM '+self.targetTableBox.get(),
                                             mode='relation')
        query = ('select ' + self.targetAttributeBox.get() + 
                 ' from ' + self.targetTableBox.get() + 
                 ' where ' + str(attr[0][0]) + 
                                 '="' + self.targetTupleBox.get() + '"')
        result = self.clientController.inquire(query, mode='table')
        self.updateTupleText.delete(0.0, tk.END)
        self.updateTupleText.insert(tk.INSERT,result)
        
    def search(self):
        userInput = str(self.searchEntry.get()).lower()
        if(userInput==''):
            return
        state = []
        for item in self.dictionaryC2E:
            if userInput in item.lower():
                state.append(str(item))
        for item in self.dictionaryE2C:
            if userInput in item.lower():
                newfound = self.dictionaryE2C[item]
                if newfound not in state:
                    state.append(newfound)
        self.instructBox.showinfo('查找结果', state)

#------------------------------------------------------------------------------      
root = tk.Tk()
root.title('识叶')
app = UserInterface(root)
root.geometry('360x500')
root.mainloop()