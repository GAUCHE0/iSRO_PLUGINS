from phBot import *
import QtBind
from threading import Timer
from datetime import datetime
from datetime import timedelta
import struct
import random
import json
import os
import subprocess

pName = 'iAcademy'
pVersion = '1.0.0'
pUrl = ''

SEQUENCE_DEFAULT_NUMBER = 30000
NOTIFICATION_SOUND_PATH = 'c:\\Windows\\Media\\chimes.wav'

isCreatingCharacter = False
isDeletingCharacter = False
CreatingNickname = ""
isRestarted = False

gui = QtBind.init(__name__,pName)
QtBind.createList(gui,60,5,265,115)
cbxEnabled = QtBind.createCheckBox(gui,'cbxDoNothing','AKTİF ET',70,15)

_x = 350
_y = 10
QtBind.createList(gui,_x+200,_y+140,135,100)
lblProfileName = QtBind.createLabel(gui,"### CONFIG ADI ###",_x+210,_y+150)
tbxProfileName = QtBind.createLineEdit(gui,"",_x+213,_y+170,110,19)
btnSaveConfig = QtBind.createButton(gui,'btnSaveConfig_clicked',"   KAYDET   ",_x+240,_y+195)
btnLoadConfig = QtBind.createButton(gui,'btnLoadConfig_clicked',"    YÜKLE    ",_x+240,_y+215)

_x = 70
_y = 40
cbxSelectChar = QtBind.createCheckBox(gui,'cbxDoNothing','SEÇ ( DÜŞÜKSE 40LVLDEN )',_x,_y-1)
cbxSelectCharOnAcademy = QtBind.createCheckBox(gui,'cbxDoNothing','SEÇ ( 40-50LVL ARASINDA VE AKADEMİDEYSE )',_x,_y+19)
cbxCreateChar = QtBind.createCheckBox(gui,'cbxDoNothing','OLUŞTUR ( SEÇİM YAPILAMADIYSA )',_x,_y+39)
cbxDeleteChar = QtBind.createCheckBox(gui,'cbxDoNothing','SİL ( 40-50LVL ARASINDA )',_x,_y+59)

_x = 500
_y = 40
QtBind.createList(gui,_x+5,_y-10,205,80)
lblNickname = QtBind.createLabel(gui," NICK PREFIX :",_x+15,_y)
tbxNickname = QtBind.createLineEdit(gui,"",_x+94,_y-3,102,19)
_y+=20
lblSequence = QtBind.createLabel(gui,"MAX NICK NO :",_x+15,_y)
tbxSequence = QtBind.createLineEdit(gui,"",_x+95,_y-3,101,19)
_y+=20
lblRace = QtBind.createLabel(gui,"                IRK :",_x+15,_y)
cmbxRace = QtBind.createCombobox(gui,_x+95,_y-3,101,19)
QtBind.append(gui,cmbxRace,"CH")
QtBind.append(gui,cmbxRace,"EU")

_y = 140
_x = 70
QtBind.createList(gui,60,130,410,135)
lblFullCharacters = QtBind.createLabel(gui,"ARKA PLANDA ÇALIŞACAK COMMANDLINE AKSİYONLARI :",_x,_y)
_y+=20
lblCMD = QtBind.createLabel(gui,"SİSTEM KOMUTUNU YÜRÜT (CMD) :",_x+10,_y)
tbxCMD = QtBind.createLineEdit(gui,"",255,_y-3,205,19)
_y+=20
cbxExit = QtBind.createCheckBox(gui,'cbxDoNothing','BOTU KAPAT',_x+9,_y)
_y+=20
cbxNotification_Full = QtBind.createCheckBox(gui,'cbxDoNothing','PHBOT NOTLARINI GÖRÜNTÜLE',_x+9,_y)
_y+=20
cbxSound_Full = QtBind.createCheckBox(gui,'cbxDoNothing','SES ÇAL.  DOSYA YOLU : ',_x+9,_y)
tbxSound_Full = QtBind.createLineEdit(gui,'',225,_y-1,235,19)
_y+=20
cbxLog_Full = QtBind.createCheckBox(gui,'cbxDoNothing','LOG KAYITLARINI TUT',_x+9,_y)

btnhakkinda = QtBind.createButton(gui,'btnhakkinda_clicked',"         HAKKINDA         ",610,290)
def btnhakkinda_clicked():
	log('\n\niAcademy:\n * GAUCHE TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.\n\n    # BU PLUGIN ILE;\n - CHAR OLUSTURMA (ISTEDIGINIZ IRKTA, NICKLE VE SIRAYLA),\n - CHAR SILME (40-100 LVL ARASI),\n - AKADEMIDE OLAN CHARLARI SILMEDEN TEKRAR OYUNA GIRME (40-50 LVL ARASI)\nISLEVLERINI YAPTIRABILIRSINIZ.\n    # ID ICERISINDE CHAR ALANI KALMADIGINDA;\n - BOTU KAPATMA,\n - PHBOT BILDIRIMLERINDE GOSTERME,\n - DOSYA YOLUNU BELIRTTIGINIZ SESI CALMA (.waw UZANTILI),\n - LOG DOSYASI OLUSTURMA\nOZELLIKLERI BULUNMAKTADIR. ')

def getPath():
	return get_config_dir()+pName+"\\"

def getConfig(name):
	if not name:
		name = pName;
	return getPath()+name+".json"

def loadDefaultConfig():
	# Clear data
	QtBind.setText(gui,tbxProfileName,"")
	QtBind.setChecked(gui,cbxEnabled,False)

	QtBind.setChecked(gui,cbxSelectChar,True)
	QtBind.setChecked(gui,cbxCreateChar,True)
	QtBind.setChecked(gui,cbxDeleteChar,True)
	QtBind.setChecked(gui,cbxSelectCharOnAcademy,False)

	QtBind.setText(gui,tbxNickname,"")
	QtBind.setText(gui,tbxSequence,str(SEQUENCE_DEFAULT_NUMBER))
	QtBind.setText(gui,cmbxRace,"CH")

	QtBind.setText(gui,tbxCMD,"")
	QtBind.setChecked(gui,cbxNotification_Full,False)
	QtBind.setChecked(gui,cbxSound_Full,False)
	QtBind.setText(gui,tbxSound_Full,NOTIFICATION_SOUND_PATH)
	QtBind.setChecked(gui,cbxLog_Full,False)

	QtBind.setChecked(gui,cbxExit,False)

def loadConfigs(fileName=""):
	loadDefaultConfig()
	if os.path.exists(getConfig(fileName)):
		data = {}
		with open(getConfig(fileName),"r") as f:
			data = json.load(f)

		QtBind.setText(gui,tbxProfileName,fileName)

		if "Etkin" in data and data['Etkin']:
			QtBind.setChecked(gui,cbxEnabled,True)

		if "Charsec" in data and not data['Charsec']:
			QtBind.setChecked(gui,cbxSelectChar,False)
		if "charolustur" in data and not data['charolustur']:
			QtBind.setChecked(gui,cbxCreateChar,False)
		if "charsil" in data and not data['charsil']:
			QtBind.setChecked(gui,cbxDeleteChar,False)
		if "akademidekicharısec" in data and data['akademidekicharısec']:
			QtBind.setChecked(gui,cbxSelectCharOnAcademy,True)

		if "nick" in data:
			QtBind.setText(gui,tbxNickname,data["nick"])
		if "aralik" in data and data["aralik"]:
			QtBind.setText(gui,tbxSequence,data["Sequence"])
		if "irk" in data:
			QtBind.setText(gui,cmbxRace,data["irk"])

		if "CMD" in data:
			QtBind.setText(gui,tbxCMD,data["CMD"])
		if "bildirim" in data and data['bildirim']:
			QtBind.setChecked(gui,cbxNotification_Full,True)
		if "ses" in data and data['ses']:
			QtBind.setChecked(gui,cbxNotification_Full,True)
		if "sesyolu" in data and data["sesyolu"]:
			QtBind.setText(gui,tbxSound_Full,data["sesyolu"])
		if "log" in data and data['log']:
			QtBind.setChecked(gui,cbxLog_Full,True)

		if "cikis" in data and data['cikis']:
			QtBind.setChecked(gui,cbxExit,True)
		
		return True
	return False
def saveConfigs(fileName=""):
	data = {}
	data["Etkin"] = QtBind.isChecked(gui,cbxEnabled)

	data["Charsec"] = QtBind.isChecked(gui,cbxSelectChar)
	data["charolustur"] = QtBind.isChecked(gui,cbxCreateChar)
	data["charsil"] = QtBind.isChecked(gui,cbxDeleteChar)
	data["akademidekicharısec"] = QtBind.isChecked(gui,cbxSelectCharOnAcademy)

	data["nick"] = QtBind.text(gui,tbxNickname)
	sequence = QtBind.text(gui,tbxSequence)
	if sequence.isnumeric():
		data["aralik"] = sequence
	else:
		data["aralik"] = str(SEQUENCE_DEFAULT_NUMBER)
		QtBind.setText(gui,tbxSequence,data["aralik"])
	data["irk"] = QtBind.text(gui,cmbxRace)

	data["CMD"] = QtBind.text(gui,tbxCMD)
	data["bildirim"] = QtBind.isChecked(gui,cbxNotification_Full)
	data["ses"] = QtBind.isChecked(gui,cbxSound_Full)
	data["sesyolu"] = QtBind.text(gui,tbxSound_Full)
	data["log"] = QtBind.isChecked(gui,cbxLog_Full)
	data["cikis"] = QtBind.isChecked(gui,cbxExit)
	with open(getConfig(fileName),"w") as f:
		f.write(json.dumps(data,indent=4,sort_keys=True))

def btnSaveConfig_clicked():
	strConfigName = QtBind.text(gui,tbxProfileName)
	saveConfigs(strConfigName)
	if strConfigName:
		log('Plugin: PROFIL ['+strConfigName+'] KAYDEDİLDİ.')
	else:
		log("Plugin: PROFIL KAYDEDİLDİ.")

def btnLoadConfig_clicked():
	strConfigName = QtBind.text(gui,tbxProfileName)
	if loadConfigs(strConfigName):
		if strConfigName:
			log("Plugin: PROFIL ["+strConfigName+"] YÜKLENDİ.")
		else:
			log("Plugin: PROFIL YÜKLENDİ.")
	elif strConfigName:
		log("Plugin: PROFIL ["+strConfigName+"] BULUNAMADI.")

def CreateCharacter():
	race = QtBind.text(gui,cmbxRace)
	if race != 'EU':
		race = 'CH'

		model = get_monster_string('CHAR_CH_MAN_ADVENTURER')
		chest = get_item_string('ITEM_CH_M_HEAVY_01_BA_A_DEF')
		legs = get_item_string('ITEM_CH_M_HEAVY_01_LA_A_DEF')
		shoes = get_item_string('ITEM_CH_M_HEAVY_01_FA_A_DEF')
		weapon = get_item_string('ITEM_CH_SWORD_01_A_DEF')
	else:
		race = 'EU'

		model = get_monster_string('CHAR_EU_MAN_NOBLE')
		chest = get_item_string('ITEM_EU_M_HEAVY_01_BA_A_DEF')
		legs = get_item_string('ITEM_EU_M_HEAVY_01_LA_A_DEF')
		shoes = get_item_string('ITEM_EU_M_HEAVY_01_FA_A_DEF')
		weapon = get_item_string('ITEM_EU_SWORD_01_A_DEF')

	if not model or not chest or not legs or not shoes or not weapon:
		log('Plugin: HATA, ITEM KODU BU SUNUCUDA DEGISTIRILMIS.')
		return

	global isCreatingCharacter
	isCreatingCharacter = True
	log('Plugin: CHAR SEÇİLİYOR. ['+CreatingNickname+'] ('+race+')')
	p = b'\x01'
	p += struct.pack('<H', len(CreatingNickname))
	p += CreatingNickname.encode('ascii')
	p += struct.pack('<I', model['model'])
	p += struct.pack('<B', 0)
	p += struct.pack('<I', chest['model'])
	p += struct.pack('<I', legs['model'])
	p += struct.pack('<I', shoes['model'])
	p += struct.pack('<I', weapon['model'])
	inject_joymax(0x7007,p, False)

	Timer(2.5,Inject_RequestCharacterList).start()

def Inject_RequestCharacterList():
	inject_joymax(0x7007,b'\x02',False)
def Inject_DeleteCharacter(charName):
	p = b'\x03'
	p += struct.pack('<H', len(charName))
	p += charName.encode('ascii')
	inject_joymax(0x7007,p, False)
def Inject_CheckName(charName):
	p = b'\x04'
	p += struct.pack('<H', len(charName))
	p += charName.encode('ascii')
	inject_joymax(0x7007,p, False)
def GetRandomNick():
	# Adding names with max. 12 letters
	names = ["Aegon","Aerys","Aemon","Aeron","Alliser","Areo","Bran","Bronn","Benjen","Brynden","Beric","Balon","Bowen","Craster","Davos","Daario","Doran","Darrik","Dyron","Eddard","Edric","Euron","Edmure","Gendry","Gilly","Gregor","GreyWorm","Hoster","Jon","Jaime","Jorah","Joffrey","Jeor","Jaqen","Jojen","Janos","Kevan","Khal","Lancel","Loras","Maekar","Mace","Mance","Nestor","Oberyn","Petyr","Podrick","Quentyn","Robert","Robb","Ramsay","Roose","Rickon","Rickard","Rhaegar","Renly","Rodrik","Randyll","Samwell","Sandor","Stannis","Stefon","Tywin","Tyrion","Theon","Tormund","Trystane","Tommen","Val","Varys","Viserys","Victarion","Vimar","Walder","Wyman","Yoren","Yohn","Zane"]
	name = names[random.randint(0,len(names)-1)]
	# Fill with discord style
	if len(name) < 12:
		maxWidth = 12-len(name)
		if maxWidth > 4 :
			maxWidth = 4
		numbers = pow(10,maxWidth)-1
		name = str(name)+(str(random.randint(0,numbers))).zfill(maxWidth)
	return name
def GetSequence():	
	sequence = QtBind.text(gui,tbxSequence)
	if sequence.isnumeric():
		sequence = int(sequence)
	else:
		sequence = SEQUENCE_DEFAULT_NUMBER

	QtBind.setText(gui,tbxSequence,str(sequence+1))
	saveConfigs(QtBind.text(gui,tbxProfileName))
	
	return sequence
def GetNickSequence(nickname):
	seq = str(GetSequence())
	nick = nickname+seq
	nickLength = len(nick)
	if nickLength > 12: # MAX CHAR NICK KARAKTER SAYISI
		nickLength -= 12
		nick = nickname[:-nickLength]+seq
	return nick

def createNickname():
	global CreatingNickname
	customName = QtBind.text(gui,tbxNickname) 
	if customName:
		CreatingNickname = GetNickSequence(customName)
	else:
		CreatingNickname = GetRandomNick()
	log("Plugin: NICK KONTROL EDILIYOR.. ["+CreatingNickname+"]")
	Inject_CheckName(CreatingNickname)
def KillBot():
	log("Plugin: BOT KAPATILIYOR..")
	# Suicide :(
	os.kill(os.getpid(),9)

def RestartBotWithCommandLine():
	global isRestarted
	if isRestarted:
		return
	isRestarted = True
	cmd = ' '.join(get_command_line_args())
	subprocess.Popen(cmd)
	log("Plugin: BOT 5 SANİYE İÇİNDE KAPATILIYOR..")
	Timer(5.0,KillBot).start()

def handle_joymax(opcode,data):
	if opcode == 0xB007 and QtBind.isChecked(gui,cbxEnabled):
		locale = get_locale()
		try:
			global isCreatingCharacter, isDeletingCharacter
			index = 0
			action = data[index]
			index+=1
			success = data[index]
			index+=1
			if action == 1:
				if isCreatingCharacter:
					isCreatingCharacter = False
					if success == 1:
						log("Plugin: CHAR BAŞARIYLA OLUŞTURULDU.")
					else:
						log("Plugin: CHAR OLUŞTURULAMADI !")
			elif action == 3:
				if isDeletingCharacter:
					isDeletingCharacter = False
					if success == 1:
						log("Plugin: CHAR BAŞARIYLA SİLİNDİ.")
					else:
						log("Plugin: CHAR SİLİNEMEDİ !")
			elif action == 4:
				if isCreatingCharacter:
					if success == 1:
						log("Plugin: NICK KULLANILABİLİR..")
						CreateCharacter()
					else:
						log("Plugin: NICK KULLANIMDA !")
						Timer(1.0,createNickname).start()
			elif action == 2:
				if success == 1:
					charList = []
					nChars = data[index]
					index+=1
					log("Plugin: iAcademy CHAR LİSTESİ: "+ ("BOŞ" if not nChars else ""))
					for i in range(nChars):
						character = {}
						character['model_id'] = struct.unpack_from('<I',data,index)[0]
						index+=4
						charLength = struct.unpack_from('<H',data,index)[0]
						index+=2
						character['name'] = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')
						index+= charLength

						if locale == 18 or locale == 54 or locale == 56:
							index+=2+struct.unpack_from('<H',data,index)[0]
						
						index+=1
						character['level'] = data[index]
						index+=1
						index+=8
						index+=2
						index+=2
						index+=2

						if locale == 18 or locale == 54 or locale == 56:
							index+=4

						index+=4
						index+=4

						if locale == 18 or locale == 54 or locale == 56:
							index+=2

						character['is_deleting'] = data[index]
						index+=1 #

						if locale == 18 or locale == 54 or locale == 56:
							index+=4

						if character['is_deleting']:
							minutesLeft = struct.unpack_from('<I',data,index)[0]
							character['deleted_at'] = datetime.now() + timedelta(minutes=minutesLeft)
							index+=4
						
						index+=1
						if data[index]:
							index+=1
							strLength = struct.unpack_from('<H', data, index)[0]
							index+=(2 + strLength)
						else:
							index+=1

						character['academy_type'] = data[index]
						index+=1
						forCount = data[index]
						index+=1
						for j in range(forCount):
							index+=4
							index+=1
						forCount = data[index]
						index+=1
						for j in range(forCount):
							index+=4
							index+=1

						charList.append(character)
						log(str(i+1)+") "+character['name']+" (Lv."+str(character['level'])+")"+(" [* "+character['deleted_at'].strftime('%H:%M %d/%m/%Y')+"]" if character['is_deleting'] else ""))

					if locale == 18 or locale == 54 or locale == 56:
						index+=1
					try:
						if i == (nChars-1):
							data[index]
							log("Plugin: PAKET AYRIŞTIRMA HATASI..!")
					except:
						try:
							data[index-1]
						except:
							log("Plugin: PAKET AYRIŞTIRMA HATASI..!")

					try:
						# call event
						OnCharacterList(charList)
					except Exception as innerEx:
						log("Plugin: "+str(innerEx))
		except Exception as ex:
			log("Plugin: HATA ! ["+str(ex)+"] - "+pName+" BU SUNUCUDA KULLANILAMAZ !")
			log("Data [" + ("BOŞ" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(locale)+"]")
	return True

def OnCharacterList(CharList):
	for character in CharList:
		if not character['is_deleting']:
			charName = character['name']
			charLevel = character['level']
			charAcademyType = character['academy_type']

			# 40 50 LVL ARASI AKADEMİDE OLMA KOŞULU
			if charLevel >= 40 and charLevel <= 50 and charAcademyType != 0:
				if QtBind.isChecked(gui,cbxSelectCharOnAcademy):
					log("Plugin: CHAR SEÇİLİYOR.. ["+charName+"] (CHAR AKADEMİDE..)")
					select_character(charName)
					return

			# 40 50 LVL ARASI CHARLARI SİLME
			if charLevel >= 40 and charLevel <= 50:
				if QtBind.isChecked(gui,cbxDeleteChar):
					global isDeletingCharacter
					isDeletingCharacter = True
					log("Plugin: CHAR SİLİNİYOR. ["+charName+"] (40-50LVL ARASI)")
					Inject_DeleteCharacter(charName)
					Timer(3.0,Inject_RequestCharacterList).start()
					return

			# 40 LVL DAN DÜŞÜK CHARLARI SEÇME
			if charLevel < 40:
				if QtBind.isChecked(gui,cbxSelectChar):
					log("Plugin: CHAR SEÇİLİYOR.. ["+charName+"] (40LVL'DAN DÜŞÜK..)")
					select_character(charName)
					return

	# CHAR KAPASİTESİ DOLU OLARAK GÖSTERME LİMİTİ
	if len(CharList) < 4:
		if QtBind.isChecked(gui,cbxCreateChar):
			global isCreatingCharacter
			isCreatingCharacter = True
			Timer(3.0,createNickname).start()
	else:
		errMessage = "Plugin: ID İÇERİSİNDE YETERLİ CHAR KAPASİTESİ YOK !"
		log(errMessage)

		cmd = QtBind.text(gui,tbxCMD)
		if cmd:
			log("Plugin: KOMUT UYGULANIYOR.. ["+cmd+"]")
			subprocess.Popen(cmd)

		if QtBind.isChecked(gui,cbxNotification_Full):
			show_notification(pName+' v'+pVersion,errMessage)

		if QtBind.isChecked(gui,cbxSound_Full):
			try:
				path = QtBind.text(gui,tbxSound_Full)
				play_wav(path if path else NOTIFICATION_SOUND_PATH)
			except:
				pass

		if QtBind.isChecked(gui,cbxLog_Full):
			from datetime import datetime
			logText = datetime.now().strftime('%m/%d/%Y - %H:%M:%S')+': '+errMessage
			profileName = QtBind.text(gui,tbxProfileName)
			logText += '\nPROFIL KULLANIMDA: '+ (profileName if profileName else 'None')
			with open(getPath()+'_log.txt','a') as f:
				f.write(logText)

		if QtBind.isChecked(gui,cbxExit):
			log("Plugin: BOT 5 SANİYE İÇERİSİNDE KAPATILIYOR..")
			Timer(5.0,KillBot).start()

log('Plugin: '+pName+' v'+pVersion+' BAŞARIYLA YÜKLENDİ.')

if os.path.exists(getPath()):
	useDefaultConfig = True
	if useDefaultConfig:
		loadConfigs()
else:
	loadDefaultConfig()
	os.makedirs(getPath())
	log('Plugin: "'+pName+'" folder has been created')
