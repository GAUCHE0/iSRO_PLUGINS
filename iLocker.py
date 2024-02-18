from phBot import *
import phBotChat
import struct
import time
import QtBind
import json
import os

pName = 'iLocker'
pVersion = '1.0.0'
pUrl = 'https://raw.githubusercontent.com/GAUCHE0/iSRO_PLUGINS/main/iLocker.py'

gui = QtBind.init(__name__,pName)

_x = 10
_y = 0
ButtonArea1 = QtBind.createList(gui, _x + 215, _y + 50, _x + 290, _y + 120)
lblptmaster = QtBind.createLabel(gui, "PT MASTER :", _x + 235, _y + 70)
tbxptmaster = QtBind.createLineEdit(gui, "", _x + 345, _y + 70, 150, 18)
lblakamaster = QtBind.createLabel(gui, "AKADEMI MASTER :", _x + 235, _y + 90)
tbxakamaster = QtBind.createLineEdit(gui, "", _x + 345, _y + 90, 150, 18)
lblsoru = QtBind.createLabel(gui, "SORU :", _x + 235, _y + 110)
tbxsoru = QtBind.createLineEdit(gui, "", _x + 345, _y + 110, 150, 18)
lblcevap = QtBind.createLabel(gui, "CEVAP :", _x + 235, _y + 130)
tbxcevap = QtBind.createLineEdit(gui, "", _x + 345, _y + 130, 150, 18)
# SAVE / LOAD BUTON
ButtonArea2 = QtBind.createList(gui, _x + 215, _y + 200, _x + 290, _y + 80)
btnKaydet = QtBind.createButton(gui, 'btnKaydet_clicked', "    KAYDET    ", _x + 395, _y + 230)
btnYukle = QtBind.createButton(gui, 'btnYukle_clicked', "     YUKLE     ", _x + 395, _y + 250)
lblProfil = QtBind.createLabel(gui, "CONFIG PROFIL ISMI :", _x + 250, _y + 212)
tbxProfil = QtBind.createLineEdit(gui, "", _x + 370, _y + 209, 110, 19)

btnhakkinda = QtBind.createButton(gui,'btnhakkinda_clicked',"         HAKKINDA         ",610,290)
lblinfo = QtBind.createLabel(gui, "iLocker : ", _x, _y+20)
def btnhakkinda_clicked():
	log('\n\niLocker : \n    # BU PLUGIN AKADEMI VE PARTI LISTELERINDEN OTOMATIK GIRIS YAPARKEN\nISTENMEYEN KISILERIN GIRMESINI ENGELLEMEK ICIN TASARLANMISTIR.\n    # BIR NEVI SIFRELEME SISTEMI OLUP, MASTER CHARIN BELIRLENEN SORUYU\nSORMASININ ARDINDAN GIRIS YAPAN CHARIN DOGRU CEVABI VERMESIYLE CALISIR.\n    # KURULUM :\n - PARTI MASTER: PARTY MASTERI OLACAK CHARIN ADI.\n - AKADEMI MASTER: AKADEMI MASTERI OLACAK CHARIN ADI.\n - SORU: CHAT EKRANINDA SORDURMAK ISTEDIGIN SORU.\n - CEVAP: SORULAN SORUYA VERILMESINI ISTEDIGIN YANIT.\n(SIFRE NITELIGINDE OLUP BASKA BIR KISI ILE PAYLASMAYIN.)')


# User settings
MATCH_PARTY_MASTER = tbxptmaster
MATCH_ACADEMY_MASTER = tbxakamaster
MATCH_REPLY_DELAY_MAX = 10
QUESTION_PASSWORD = tbxcevap
QUESTION_MESSAGE = tbxsoru
# ______________________________ Initializing ______________________________ #

# Globals
questionPartyTime = None
questionPartyCharName = ""
questionPartyRID = 0
questionPartyJID = 0
questionAcademyTime = None
questionAcademyCharName = ""
questionAcademyRID = 0
questionAcademyJID = 0

def getPath():
    return get_config_dir() + pName + "\\"


def getConfig(name):
    if not name:
        name = pName;
    return getPath() + name + ".json"

def loadDefaultConfig():
    # DATAYI TEMİZLE
    QtBind.setText(gui, tbxptmaster, "")
    QtBind.setText(gui, tbxakamaster, "")
    QtBind.setText(gui, tbxsoru, "")
    QtBind.setText(gui, tbxcevap, "")

def loadConfigs(fileName=""):
    loadDefaultConfig()
    if os.path.exists(getConfig(fileName)):
        data = {}
        with open(getConfig(fileName), "r") as f:
            data = json.load(f)
        QtBind.setText(gui, tbxProfil, fileName)
        if "PTMASTER" in data:
            QtBind.setText(gui, tbxptmaster, data["PTMASTER"])
        if "AKAMASTER" in data:
            QtBind.setText(gui, tbxakamaster, data["AKAMASTER"])
        if "SORU" in data:
            QtBind.setText(gui, tbxsoru, data["SORU"])
        if "CEVAP" in data:
            QtBind.setText(gui, tbxcevap, data["CEVAP"])
        return True
    return False

def saveConfigs(fileName=""):
    data = {}
    data["PTMASTER"] = QtBind.text(gui, tbxptmaster)
    data["AKAMASTER"] = QtBind.text(gui, tbxakamaster)
    data["SORU"] = QtBind.text(gui, tbxsoru)
    data["CEVAP"] = QtBind.text(gui, tbxcevap)
    with open(getConfig(fileName), "w") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))

def btnKaydet_clicked():
    strConfigName = QtBind.text(gui, tbxProfil)
    saveConfigs(strConfigName)
    if strConfigName:
        log('Plugin: [' + strConfigName + '] PROFILI KAYIT EDILDI.')
    else:
        log("Plugin: KAYIT EDILDI..")


def btnYukle_clicked():
    strConfigName = QtBind.text(gui, tbxProfil)
    if loadConfigs(strConfigName):
        if strConfigName:
            log("Plugin: [" + strConfigName + "] PROFILI YUKLENDI.")
        else:
            log("Plugin: YUKLENDI..")
    elif strConfigName:
        log("Plugin: [" + strConfigName + "] PROFILI BULUNAMADI.")

def Inject_PartyMatchJoinResponse(requestID,joinID,response):
    p = struct.pack('I', requestID)
    p += struct.pack('I', joinID)
    p += struct.pack('B',1 if response else 0)
    inject_joymax(0x306E,p,False)

def Inject_AcademyMatchJoinResponse(requestID,joinID,response):
    p = struct.pack('I', requestID)
    p += struct.pack('I', joinID)
    p += struct.pack('B',1 if response else 0)
    inject_joymax(0x347F,p,False)

def handle_joymax(opcode,data):
    if opcode == 0x706D and QUESTION_PASSWORD:
        try:
            global questionPartyTime,questionPartyRID,questionPartyJID,questionPartyCharName

            questionPartyTime = time.time()

            index=0
            questionPartyRID = struct.unpack_from('<I',data,index)[0]
            index+=4
            questionPartyJID = struct.unpack_from('<I',data,index)[0]
            index+=22

            charLength = struct.unpack_from('<H',data,index)[0]
            index+=2
            questionPartyCharName = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')

            phBotChat.Private(questionPartyCharName,QUESTION_MESSAGE)

        except:
            log("Plugin: Ayrıstırma hatasi. Sifre Sunucuda kullanilamiyor !")
            log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(get_locale())+"]")
    elif opcode == 0x747E and QUESTION_PASSWORD:
        try:
            global questionAcademyTime,questionAcademyRID,questionAcademyJID,questionAcademyCharName

            questionAcademyTime = time.time()

            index=0
            questionAcademyRID = struct.unpack_from('<I',data,index)[0]
            index+=4
            questionAcademyJID = struct.unpack_from('<I',data,index)[0]
            index+=18

            charLength = struct.unpack_from('<H',data,index)[0]
            index+=2
            questionAcademyCharName = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')

            phBotChat.Private(questionAcademyCharName,QUESTION_MESSAGE)

        except:
            log("Plugin: Ayrıstırma hatasi. Sifre Sunucuda kullanilamiyor !")
            log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(get_locale())+"]")
    return True

def handle_chat(t,charName,message):
    if t != 2:
        return
    if not QUESTION_PASSWORD:
        return

    if message == QUESTION_MESSAGE:
        if MATCH_PARTY_MASTER == charName or MATCH_ACADEMY_MASTER == charName:
            phBotChat.Private(charName,QUESTION_PASSWORD)
        else:
            phBotChat.Private(charName,"Üzgünüm Master Değilsin. :)")
        return

    if charName == questionPartyCharName:
        now = time.time()
        if now - questionPartyTime < MATCH_REPLY_DELAY_MAX:
            if message == QUESTION_PASSWORD:
                log("Plugin: "+charName+" Şifre ile PT'ye girdi.")
                Inject_PartyMatchJoinResponse(questionPartyRID,questionPartyJID,True)
            else:
                log("Plugin: "+charName+" Yanlış şifre. PT Daveti iptal edildi.")
                Inject_PartyMatchJoinResponse(questionPartyRID,questionPartyJID,False)
            return

    if charName == questionAcademyCharName:
        now = time.time()
        if now - questionAcademyTime < MATCH_REPLY_DELAY_MAX:
            if message == QUESTION_PASSWORD:
                log("Plugin: "+charName+" Şifre ile AKADEMİ'ye girdi.")
                Inject_AcademyMatchJoinResponse(questionAcademyRID,questionAcademyJID,True)
            else:
                log("Plugin: "+charName+" Yanlış şifre. AKADEMİ Daveti iptal edildi.")
                Inject_AcademyMatchJoinResponse(questionAcademyRID,questionAcademyJID,False)
            return

if os.path.exists(getPath()):
    useDefaultConfig = True
    if loadConfigs(pName):
        log("Plugin: "+pName+" KAYIT YÜKLENDİ..")
        useDefaultConfig = False
    else:
        log("Plugin: "+pName+" KAYIT BULUNAMADI..")
        if useDefaultConfig:
            loadConfigs()
else:
    loadDefaultConfig()
    os.makedirs(getPath())
    log('Plugin: "' + pName + '" CONFIG KLASORU OLUSTURULDU..')


log('Plugin: ' + pName + ' v' + pVersion + ' BASARIYLA YUKLENDI')
