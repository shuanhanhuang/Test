from django.shortcuts import render
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import auth
from testapp.form import HomeForm,SignedForm,MeetingInnerForm,MeetingForm,ContactForm,ContractForm,ContractInnerForm,ChangeForm
from testapp.models import Home,Signed,MeetingInner,Meeting,Contact,Contract,ContractInner,Change

Acount = 0
# Bcount = 0
# Create your views here.
def HomePost(request):
    global Acount
    if request.method == "POST":  #如果是以POST方式才處理
        homeform = HomeForm(request.POST)  #建立forms物件
        if homeform.is_valid():
            Acount= Acount+1        
            cType = homeform.cleaned_data['cType']
            cDepartment =homeform.cleaned_data['cDepartment']
            cDate = datetime.now()
            if(Acount//100 == 0):
                if((Acount%100)//10 ==0):
                    count = "00"
                else:
                    count = "0"
            else:
                count =""
            if(homeform.cleaned_data['cType'] == "簽呈"):
                cNumber = "A"+str(cDate.year)+str(cDate.month)+str(cDate.day)+count+str(Acount)
            elif(homeform.cleaned_data['cType'] == "會議記錄"):
                cNumber = "D"+str(cDate.year)+str(cDate.month)+str(cDate.day)+count+str(Acount)
            elif(homeform.cleaned_data['cType'] == "內部連絡單"):
                cNumber = "E"+str(cDate.year)+str(cDate.month)+str(cDate.day)+count+str(Acount)
            elif(homeform.cleaned_data['cType'] == "工程發包議價記錄單"):
                cNumber = "C"+str(cDate.year)+str(cDate.month)+str(cDate.day)+count+str(Acount)
            elif(homeform.cleaned_data['cType'] == "設計變更通知單"):
                cNumber = "B"+str(cDate.year)+str(cDate.month)+str(cDate.day)+count+str(Acount)
            cAuther = homeform.cleaned_data['cAuther']
            cEndDate =  datetime.now() #取得表單輸入資料
            cProgress =  homeform.cleaned_data['cProgress']
            unit = Home.objects.create(cType=cType,cNumber=cNumber,cAuther=cAuther, cDate=cDate, cDepartment=cDepartment, cEndDate=cEndDate, cProgress=cProgress)
            home = unit.save()  #寫入資料庫
            message = '已儲存...'
            if cType == "簽呈":
                 return redirect('/signPost/'+str(cNumber)+'/')
            elif cType == '會議記錄':
                return redirect('/meetingPost/'+str(cNumber)+'/')
            elif cType == '內部連絡單':
                return redirect('/contactPost/'+str(cNumber)+'/')
            elif cType == '工程發包議價記錄單':
                return redirect('/contractPost/'+str(cNumber)+'/')
            elif cType == '設計變更通知單':
                return redirect('/changePost/'+str(cNumber)+'/')
            return redirect('/homeIndex/')
        else:
            message = '驗證碼錯誤！'
    else:
        message = '姓名、主旨必須輸入！'
    homeform = HomeForm()
    return render(request, "HomePost.html", locals())
def homeIndex(request):
    all = Home.objects.all().order_by("id")
    allHomeCount = len(all)
    return render(request, "homeIndex.html",locals())

def homeEdit(request,id=None,mode=None):
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Home.objects.get(id=id)  #取得要修改的資料記  
        strdate=str(unit.cDate)
        strdate2=strdate.replace("年","-")
        strdate2=strdate.replace("月","-")
        strdate2=strdate.replace("日","-")
        unit.cDate = strdate2

        strdate1=str(unit.cEndDate)
        strdate3=strdate1.replace("年","-")
        strdate3=strdate1.replace("月","-")
        strdate3=strdate1.replace("日","-")
        unit.cEndDate = strdate3
        return render(request, "homeEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = Home.objects.get(id=id)  #取得要修改的資料記錄
        unit.cAuther = request.POST['cAuther']
        unit.cDepartment=request.POST['cDepartment']
        unit.cEndDate = request.POST['cEndDate']
        unit.cProgress=request.POST['cProgress']
        unit.save()  #寫入資料庫
        message = '已修改...'
        return redirect('/homeIndex/')
    
def homeDelete(request,id=None):
	if id!=None:
		if request.method == "POST":  #如果是以POST方式才處理
			id=request.POST['cId'] #取得表單輸入的編號
		try:
			unit = Home.objects.get(id=id)
			unit.delete()
			return redirect('/homeIndex/')
		except:
			message = "讀取錯誤!"
	return render(request, "homeDelete.html", locals())

def Detail(request,cNumber=None):
    index = Home.objects.get(cNumber = cNumber)
    if index.cType == "簽呈":
        sign_detail = Signed.objects.get(cNumber=cNumber)
        return redirect('/signEdit/'+str(cNumber)+'/'+str(sign_detail.id)+'/load')
    elif index.cType == "會議記錄":
        meeting_detail = Meeting.objects.get(cNumber=cNumber)
        return redirect('/meetingEdit/'+str(cNumber)+'/'+str(meeting_detail.id)+'/load')
    elif index.cType == '內部連絡單':
        contact_detail = Contact.objects.get(cNumber=cNumber)
        return redirect('/contactEdit/'+str(cNumber)+'/'+str(contact_detail.id)+'/load')
    elif index.cType == '工程發包議價記錄單':
        contract_detail = Contract.objects.get(cNumber=cNumber)
        return redirect('/contractEdit/'+str(cNumber)+'/'+str(contract_detail.id)+'/load')
    else:
        change_detail = Change.objects.get(cNumber=cNumber)
        return redirect('/changeEdit/'+str(cNumber)+'/'+str(change_detail.id)+'/load')


#簽呈
def signPost(request,cNumber=None):
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Signed.objects.filter(home=home).order_by("id")
    if request.method == 'POST':
        signedform = SignedForm(request.POST)
        if signedform.is_valid():
            cNumber =  home.cNumber
            cJob_title = signedform.cleaned_data['cJob_title']
            cSubject =  signedform.cleaned_data['cSubject']
            cDiscription =  signedform.cleaned_data['cDiscription']
            # Save the signature data with the associated document
            signunit = Signed.objects.create(home=home, cNumber=cNumber,cJob_title= cJob_title, cSubject=cSubject, cDiscription=cDiscription)
            signunit.save()
            return redirect('/signIndex/'+str(home.cNumber)+'/')
        else:
             message="驗證錯誤"
    else:
         message='主旨為必填項目'
    signedform = SignedForm()
    return render(request, "signPost.html", locals())

def signIndex(request,cNumber=None):
    home = Home.objects.get(cNumber=cNumber)
    sign = Signed.objects.get(cNumber=cNumber)
    return render(request, "signIndex.html",locals())

def signallIndex(request):
    signall = Signed.objects.all().order_by("id")
    signallCount = len(signall)
    return render(request, "signall_Index.html",locals())

def signEdit(request,id=None,mode=None,cNumber=None):
    index = Home.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Signed.objects.get(id = id)  #取得要修改的資料記
        return render(request, "SignEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = Signed.objects.get(id = id)  #取得要修改的資料記錄
        unit.cJob_title = request.POST['cJob_title']
        unit.cSubject=request.POST['cSubject']
        unit.cDiscription=request.POST['cDiscription']
        unit.save()  #寫入資料庫
        message = '已修改...'
        return redirect('/signIndex/'+str(index.cNumber)+'/')


#會議記錄 
def meetingPost(request,cNumber=None):
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Meeting.objects.filter(home=home).order_by("id")
    if request.method == 'POST':
        meetingform = MeetingForm(request.POST)
        if meetingform.is_valid():
            cNumber =  home.cNumber
            cMeetingType = meetingform.cleaned_data['cMeetingType']
            cRecoder = meetingform.cleaned_data['cRecoder']
            cLocation = meetingform.cleaned_data['cLocation']
            cTime = meetingform.cleaned_data['cTime']
            cLeader = meetingform.cleaned_data['cLeader']
            cTopic =  meetingform.cleaned_data['cTopic']
            cAttendees1 =  meetingform.cleaned_data['cAttendees1']
            cAttendees2 =  meetingform.cleaned_data['cAttendees2']
            cViceGeneral_Sign =  meetingform.cleaned_data['cViceGeneral_Sign']
            cManger_Sign =  meetingform.cleaned_data['cManger_Sign']
            # Save the signature data with the associated document
            unit = Meeting.objects.create(home=home,cNumber=cNumber, cRecoder=cRecoder, cMeetingType=cMeetingType, cLocation=cLocation, cTime=cTime, cLeader=cLeader, cTopic=cTopic, cAttendees1=cAttendees1, cAttendees2=cAttendees2, cManger_Sign=cManger_Sign, cViceGeneral_Sign=cViceGeneral_Sign)
            unit.save()  #寫入資料庫
            return redirect('/meetingIndex/'+str(home.cNumber)+'/')
        else:
             message="驗證錯誤"
    else:
         message='會議型態、地點、時間、主席、紀錄、主題必須輸入或勾選！'
    meetingform = MeetingForm()
    return render(request, "meetingPost.html", locals())

def meetingEdit(request,id=None,mode=None,cNumber=None):
    index = Home.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Meeting.objects.get(id = id)  #取得要修改的資料記
        return render(request, "meetingEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = Meeting.objects.get(id = id)  #取得要修改的資料記錄
        unit.cRecoder=request.POST['cRecoder']
        unit.cMeetingType = request.POST['cMeetingType']
        unit.cLocation=request.POST['cLocation']
        unit.cTopic=request.POST['cTopic']
        unit.cTime=request.POST['cTime']
        unit.cAttendees1=request.POST['cAttendees1']
        unit.cAttendees2=request.POST['cAttendees2']
        unit.cManger_Sign = request.POST['cManger_Sign']
        unit.cLeader = request.POST['cLeader']
        unit.cViceGeneral_Sign = request.POST['cViceGeneral_Sign']
        unit.save()  #寫入資料庫
        message = '已修改...'
        return redirect('/meetingIndex/'+str(index.cNumber)+'/')
    
def meetingIndex(request,cNumber=None):
    home = Home.objects.get(cNumber=cNumber)
    meeting = Meeting.objects.get(cNumber=cNumber)
    return render(request, "meetingIndex.html",locals())

def meetingallIndex(request):
    meetingall = Meeting.objects.all().order_by("id")
    meetingallCount = len(meetingall)
    return render(request, "meetingall_Index.html",locals())


#會議記錄-會議內容
def meetinginnerPost(request,cNumber=None):
    innermeeting = Meeting.objects.get(cNumber = cNumber)
    unitinner = MeetingInner.objects.filter(innermeeting=innermeeting).order_by("id")
    if request.method == "POST":  #如果是以POST方式才處理
        meetinginnerform = MeetingInnerForm(request.POST)  #建立forms物件
        if meetinginnerform.is_valid():
            cContent = meetinginnerform.cleaned_data['cContent']
            cDoPerson = meetinginnerform.cleaned_data['cDoPerson']
            cExpectDate = meetinginnerform.cleaned_data['cExpectDate']
            cOther = meetinginnerform.cleaned_data['cOther']
            innerunit = MeetingInner.objects.create(innermeeting=innermeeting,cContent=cContent, cDoPerson=cDoPerson, cExpectDate=cExpectDate, cOther=cOther)
            innerunit.save()
            return redirect('/meetinginnerIndex/'+str(innermeeting.cNumber)+'/')
        else:
             message="驗證錯誤"
    else:
         message='無一定要新增的選項'
    meetinginnerform = MeetingInnerForm()
    return render(request, "meetinginnerPost.html", locals())

def meetinginnerEdit(request,id=None,mode=None,cNumber=None):
    index = Meeting.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = MeetingInner.objects.get(id=id)  #取得要修改的資料記
        return render(request, "meetinginnerEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = MeetingInner.objects.get(id=id)  #取得要修改的資料記錄
        unit.cContent = request.POST['cContent']
        unit.cDoPerson=request.POST['cDoPerson']
        unit.cExpectDate=request.POST['cExpectDate']
        unit.cOther=request.POST['cOther']
        unit.save()  #寫入資料庫
        message = '已修改...'
        return redirect('/meetinginnerIndex/'+str(index.cNumber)+'/')

def meetinginnerIndex(request,cNumber=None):
    id = Meeting.objects.get(cNumber = cNumber)
    unitinner = MeetingInner.objects.filter(innermeeting=id).order_by("id")
    allinnerMeetingCount = len(unitinner)
    return render(request, "meetinginnerIndex.html",locals())

def meetinginnerDelete(request,id=None,cNumber=None):
    index = Meeting.objects.get(cNumber = cNumber)
    if id!=None:
        if request.method == "POST":  #如果是以POST方式才處理
            id=request.POST['cId'] #取得表單輸入的編號
        try:
            unit = MeetingInner.objects.get(id=id)
            unit.delete()
            return redirect('/meetinginnerIndex/'+str(index.cNumber)+'/')
        except:
            message = "讀取錯誤!"
    return render(request, "meetinginnerDelete.html", locals())


# 內部連絡單
def contactPost(request,cNumber=None):
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Contact.objects.filter(home=home).order_by("id")
    if request.method == 'POST':
        contactform = ContactForm(request.POST)
        if contactform.is_valid():
            cNumber =  home.cNumber
            cAutherManager = contactform.cleaned_data['cAutherManager']
            cDecisionDep = contactform.cleaned_data['cDecisionDep']
            cImplementDep = contactform.cleaned_data['cImplementDep']
            cOption = contactform.cleaned_data['cOption']
            cSubject =  contactform.cleaned_data['cSubject']
            cDiscription =  contactform.cleaned_data['cDiscription']
            unit = Contact.objects.create(home=home, cNumber=cNumber, cAutherManager=cAutherManager, cDecisionDep=cDecisionDep, cSubject=cSubject, cImplementDep=cImplementDep, cDiscription=cDiscription, cOption=cOption)
            unit.save()  #寫入資料庫
            return redirect('/contactIndex/'+str(home.cNumber)+'/')
        else:
             message="執行單位未選填"
    else:
         message='主旨、執行單位必須輸入或勾選!'
    contactform = ContactForm()
    return render(request, "contactPost.html", locals())

def contactIndex(request,cNumber=None):
    home = Home.objects.get(cNumber=cNumber)
    contact = Contact.objects.get(cNumber=cNumber)
    return render(request, "contactIndex.html",locals())

def contactallIndex(request):
    contactall = Contact.objects.all().order_by("id")
    contactallCount = len(contactall)
    return render(request, "contactall_Index.html",locals())

def contactEdit(request,id=None,mode=None,cNumber=None):
    index = Home.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Contact.objects.get(id = id)  #取得要修改的資料記
        return render(request, "contactEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = Contact.objects.get(id = id)  #取得要修改的資料記錄
        unit.cDecisionDep=request.POST['cDecisionDep']
        unit.cImplementDep=request.POST['cImplementDep']
        unit.cSubject=request.POST['cSubject']
        unit.cDiscription=request.POST['cDiscription']
        unit.cAutherManager = request.POST['cAutherManager']
        unit.cOption = request.POST['cOption']
        unit.save()  #寫入資料庫
        message = '已修改...'
        return redirect('/contactIndex/'+str(index.cNumber)+'/')
    
#工程發包議價記錄單
def contractPost(request,cNumber=None):
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Contract.objects.filter(home=home).order_by("id")
    if request.method == 'POST':
        contractform = ContractForm(request.POST)
        if contractform.is_valid():
            cNumber =  home.cNumber
            cClient = contractform.cleaned_data['cClient']
            cLocation = contractform.cleaned_data['cLocation']
            cContent = contractform.cleaned_data['cContent']
            cPayMode = contractform.cleaned_data['cPayMode']
            cBudget =  contractform.cleaned_data['cBudget']
            cOther =  contractform.cleaned_data['cOther']
            cConfirm =  contractform.cleaned_data['cConfirm']
            cGeneral_Sign =  contractform.cleaned_data['cGeneral_Sign']
            cViceGeneral_Sign =  contractform.cleaned_data['cViceGeneral_Sign']
            cManager_Sign =  contractform.cleaned_data['cManager_Sign']
            cDepartmentManager_Sign =  contractform.cleaned_data['cDepartmentManager_Sign']
            cUndertaker = contractform.cleaned_data['cUndertaker']
            unit = Contract.objects.create(home=home, cNumber=cNumber, cClient=cClient, cLocation=cLocation, cContent=cContent, cPayMode=cPayMode, cOther=cOther, cBudget=cBudget, cConfirm=cConfirm, cGeneral_Sign=cGeneral_Sign,
                                          cViceGeneral_Sign=cViceGeneral_Sign,cManager_Sign=cManager_Sign,cDepartmentManager_Sign=cDepartmentManager_Sign, cUndertaker=cUndertaker)
            unit.save()  #寫入資料庫
            return redirect('/contractIndex/'+str(home.cNumber)+'/')
        else:
             message="驗證錯誤"
    else:
         message='客戶名稱、工作地點、工程預算必須輸入或勾選!'
    contractform = ContractForm()
    return render(request, "contractPost.html", locals())

def contractIndex(request,cNumber=None):
    home = Home.objects.get(cNumber=cNumber)
    contract = Contract.objects.get(cNumber=cNumber)
    return render(request, "contractIndex.html",locals())

def contractallIndex(request):
    contractall = Contract.objects.all().order_by("id")
    contractallCount = len(contractall)
    return render(request, "contractall_Index.html",locals())

def contractEdit(request,id=None,mode=None,cNumber=None):
    index = Home.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Contract.objects.get(id = id)  #取得要修改的資料記
        return render(request, "contractEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = Contract.objects.get(id = id)  #取得要修改的資料記錄
        unit.cClient=request.POST['cClient']
        unit.cLocation=request.POST['cLocation']
        unit.cContent=request.POST['cContent']
        unit.cPayMode=request.POST['cPayMode']
        unit.cBudget = request.POST['cBudget']
        unit.cOther = request.POST['cOther']
        unit.cConfirm=request.POST['cConfirm']
        unit.cGeneral_Sign=request.POST['cGeneral_Sign']
        unit.cViceGeneral_Sign=request.POST['cViceGeneral_Sign']
        unit.cManager_Sign = request.POST['cManager_Sign']
        unit.cDepartmentManager_Sign = request.POST['cDepartmentManager_Sign']
        unit.cUndertaker = request.POST['cUndertaker']
        unit.save()  #寫入資料庫
        message = '已修改...'
        return redirect('/contractIndex/'+str(index.cNumber)+'/')
    
#工程發包議價記錄單-議價記錄
def contractinnerPost(request,cNumber=None):
    innercontract = Contract.objects.get(cNumber = cNumber)
    unitinner = ContractInner.objects.filter(innercontract=innercontract).order_by("id")
    if request.method == "POST":  #如果是以POST方式才處理
        contractinnerform = ContractInnerForm(request.POST)  #建立forms物件
        if contractinnerform.is_valid():
            cContractor = contractinnerform.cleaned_data['cContractor']
            cQuotation = contractinnerform.cleaned_data['cQuotation']
            cBargain1 = contractinnerform.cleaned_data['cBargain1']
            cBargain2 = contractinnerform.cleaned_data['cBargain2']
            cRemark = contractinnerform.cleaned_data['cRemark']
            innerunit = ContractInner.objects.create(innercontract=innercontract,cContractor=cContractor, cQuotation=cQuotation, cBargain1=cBargain1, cBargain2=cBargain2, cRemark=cRemark)
            innerunit.save()
            return redirect('/contractinnerIndex/'+str(innercontract.cNumber)+'/')
        else:
             message="驗證錯誤"
    else:
         message='無一定要新增的選項'
    contractinnerform = ContractInnerForm()
    return render(request, "contractinnerPost.html", locals())

def contractinnerEdit(request,id=None,mode=None,cNumber=None):
    index = Contract.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = ContractInner.objects.get(id=id)  #取得要修改的資料記
        return render(request, "contractinnerEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = ContractInner.objects.get(id=id)  #取得要修改的資料記錄
        unit.cContractor = request.POST['cContractor']
        unit.cQuotation=request.POST['cQuotation']
        unit.cBargain1=request.POST['cBargain1']
        unit.cBargain2=request.POST['cBargain2']
        unit.cRemark=request.POST['cRemark']
        unit.save()  #寫入資料庫
        message = '已修改...'
        return redirect('/contractinnerIndex/'+str(index.cNumber)+'/')

def contractinnerIndex(request,cNumber=None):
    id = Contract.objects.get(cNumber = cNumber)
    unitinner = ContractInner.objects.filter(innercontract=id).order_by("id")
    allinnerContractCount = len(unitinner)
    return render(request, "contractinnerIndex.html",locals())

def contractinnerDelete(request,id=None,cNumber=None):
    index = Contract.objects.get(cNumber = cNumber)
    if id!=None:
        if request.method == "POST":  #如果是以POST方式才處理
            id=request.POST['cId'] #取得表單輸入的編號
        try:
            unit = ContractInner.objects.get(id=id)
            unit.delete()
            return redirect('/contractinnerIndex/'+str(index.cNumber)+'/')
        except:
            message = "讀取錯誤!"
    return render(request, "contractinnerDelete.html", locals())

#設計變更通知單
def changePost(request,cNumber=None):
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Change.objects.filter(home=home).order_by("id")
    if request.method == 'POST':
        changeform = ChangeForm(request.POST)
        if changeform.is_valid():
            cNumber =  home.cNumber
            cProjectName = changeform.cleaned_data['cProjectName']
            cChangeitem = changeform.cleaned_data['cChangeitem']
            cChangereason = changeform.cleaned_data['cChangereason']
            cAffectitem = changeform.cleaned_data['cAffectitem']
            cRisk =  changeform.cleaned_data['cRisk']
            cKeypoint =  changeform.cleaned_data['cKeypoint']
            cOption_FS =  changeform.cleaned_data['cOption_FS']
            cOption_Design =  changeform.cleaned_data['cOption_Design']
            cOption_Quality =  changeform.cleaned_data['cOption_Quality']
            cOption_Purchase =  changeform.cleaned_data['cOption_Purchase']
            cCC =  changeform.cleaned_data['cCC']
            cEarn = changeform.cleaned_data['cEarn']
            cTech_bulletin = changeform.cleaned_data['cTech_bulletin']
            cApproved =  changeform.cleaned_data['cKeypoint']
            cReview =  changeform.cleaned_data['cReview']
            cUndertaker =  changeform.cleaned_data['cUndertaker']
            cFs_Sign =  changeform.cleaned_data['cFs_Sign']
            cDesign_Sign =  changeform.cleaned_data['cDesign_Sign']
            cQuality_Sign =  changeform.cleaned_data['cQuality_Sign']
            cPurchase_Sign = changeform.cleaned_data['cPurchase_Sign']
            unit = Change.objects.create(home=home, cNumber=cNumber, cProjectName=cProjectName, cChangeitem=cChangeitem, cChangereason=cChangereason, cAffectitem=cAffectitem,
                                          cRisk=cRisk,cKeypoint=cKeypoint, cOption_FS=cOption_FS,cOption_Design=cOption_Design,
                                          cOption_Quality=cOption_Quality,cOption_Purchase=cOption_Purchase,cCC=cCC,cEarn=cEarn,
                                          cTech_bulletin=cTech_bulletin,cApproved=cApproved,cReview=cReview,cUndertaker=cUndertaker,
                                          cFs_Sign=cFs_Sign,cDesign_Sign=cDesign_Sign,cQuality_Sign=cQuality_Sign,cPurchase_Sign=cPurchase_Sign)
            unit.save()  #寫入資料庫
            return redirect('/changeIndex/'+str(home.cNumber)+'/')
        else:
             message="副本未選填"
    else:
         message='專案名稱和副本必須輸入或勾選'
    changeform = ChangeForm()
    return render(request, "changePost.html", locals())

def changeIndex(request,cNumber=None):
    home = Home.objects.get(cNumber=cNumber)
    change = Change.objects.get(cNumber=cNumber)
    return render(request, "changeIndex.html",locals())

def changeallIndex(request):
    changeall = Change.objects.all().order_by("id")
    changeallCount = len(changeall)
    return render(request, "changeall_Index.html",locals())

def changeEdit(request,id=None,mode=None,cNumber=None):
    index = Home.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Change.objects.get(id = id)  #取得要修改的資料記
        return render(request, "changeEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = Change.objects.get(id = id)  #取得要修改的資料記錄
        unit.cProjectName=request.POST['cProjectName']
        unit.cChangeitem=request.POST['cChangeitem']
        unit.cChangereason=request.POST['cChangereason']
        unit.cHowChange=request.POST['cHowChange']
        unit.cAffectitem = request.POST['cAffectitem']
        unit.cRisk = request.POST['cRisk']
        unit.cEarn = request.POST['cEarn']
        unit.cKeypoint=request.POST['cKeypoint']
        unit.cOption_FS=request.POST['cOption_FS']
        unit.cOption_Design=request.POST['cOption_Design']
        unit.cOption_Quality=request.POST['cOption_Quality']
        unit.cOption_Purchase = request.POST['cOption_Purchase']
        unit.cCC = request.POST['cCC']
        unit.cTech_bulletin=request.POST['cTech_bulletin']
        unit.cApproved=request.POST['cApproved']
        unit.cReview=request.POST['cReview']
        unit.cUndertaker = request.POST['cUndertaker']
        unit.cFs_Sign = request.POST['cFs_Sign']
        unit.cDesign_Sign = request.POST['cDesign_Sign']
        unit.cQuality_Sign = request.POST['cQuality_Sign']
        unit.cPurchase_Sign = request.POST['cPurchase_Sign']
        unit.save()  #寫入資料庫
        message = '已修改...'
        return redirect('/changeIndex/'+str(index.cNumber)+'/')
    
def login(request):
	if request.method == 'POST':
		name = request.POST['user']
		password = request.POST['password']
		user = auth.authenticate(username=name, password=password)
		if user is not None:
			if user.is_active:
				auth.login(request,user)
				return redirect('/homeIndex/')
				message = '登入成功！'
			else:
				message = '帳號尚未啟用！'
		else:
			message = '登入失敗！'
	return render(request, "login.html", locals())

def logout(request):
	auth.logout(request)
	return redirect('/HomePage/')

def HomePage(request):
	if request.user.is_authenticated:
		name=request.user.username
	return render(request, "HomePage.html", locals())