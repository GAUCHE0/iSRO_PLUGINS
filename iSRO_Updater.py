from phBot import *
import QtBind
import urllib.request
import re
import os
import shutil

pName = 'iSRO_Updater'
pVersion = '1.0.0'
pUrl = 'https://raw.githubusercontent.com/GAUCHE0/iSRO_PLUGINS/main/iSRO_Updater.py'

# ______________________________ YÜKLEMELER ______________________________ #

gui = QtBind.init(__name__,pName)
lblPlugins = QtBind.createLabel(gui,"BİLGİSAYARDA BULUNAN PLUGİNLER:",21,11)
lvwPlugins = QtBind.createList(gui,21,30,700,200)
lstPluginsData = []
btnCheck = QtBind.createButton(gui,'btnCheck_clicked',"  GÜNCELLEMELERİ KONTROL ET  ",350,8)
btnUpdate = QtBind.createButton(gui,'btnUpdate_clicked',"  SEÇİLİ PLUGİNİ GÜNCELLE  ",550,8)

# ______________________________ METHODLAR ______________________________ #

def GetPluginsFolder():
	return str(os.path.dirname(os.path.realpath(__file__)))
def btnCheck_clicked():
	QtBind.clear(gui,lvwPlugins)
	pyFolder = GetPluginsFolder()
	files = os.listdir(pyFolder)
	global lstPluginsData
	for filename in files:
		if filename.endswith(".py"):
			pyFile = pyFolder+"\\"+filename
			with open(pyFile,"r",errors='ignore') as f:
				pyCode = str(f.read())
				if re.search("\npVersion = [0-9a-zA-Z.'\"]*",pyCode):
					pyVersion = re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
					pyName = filename[:-3]
					if re.search("\npName = ([0-9a-zA-Z'\"]*)",pyCode):
						pyName = re.search("\npName = ([0-9a-zA-Z'\"]*)",pyCode).group(0)[10:-1]
					pyUrl = pyCode.find("\npUrl = ")
					pyInfo = filename+" ("+pyName+" v"+pyVersion+") - "

					pData = {}
					pData['canUpdate'] = False
					if pyUrl != -1:
						pyUrl = pyCode[pyUrl+9:].split('\n')[0][:-1]
						pyNewVersion = getVersion(pyUrl)
						if pyNewVersion and compareVersion(pyVersion,pyNewVersion):
							pData['canUpdate'] = True
							pData['url'] = pyUrl
							pData['filename'] = filename
							pData['pName'] = pyName
							pyInfo += "GÜNCELLEME BULUNDU. (v"+pyNewVersion+")"
						else:
							pyInfo += "GÜNCELLENDİ."
					else:
						pyInfo += "GÜNCELLENEMİYOR, URL BULUNAMADI."
					QtBind.append(gui,lvwPlugins,pyInfo)
					lstPluginsData.append(pData)
def getVersion(url):
	try:
		req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
		with urllib.request.urlopen(req) as w:
			pyCode = str(w.read().decode("utf-8"))
			if re.search("\npVersion = [0-9.'\"]*",pyCode):
				return re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
	except:
		pass
	return None

def compareVersion(a, b):
	a = tuple(map(int, (a.split("."))))
	b = tuple(map(int, (b.split("."))))
	return a < b

def btnUpdate_clicked():
	indexSelected = QtBind.currentIndex(gui,lvwPlugins)
	if indexSelected >= 0:
		pyData = lstPluginsData[indexSelected]
		if "canUpdate" in pyData and pyData['canUpdate']:
			pyUrl = pyData['url']
			try:
				req = urllib.request.Request(pyUrl, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
				with urllib.request.urlopen(req) as w:
					pyCode = str(w.read().decode("utf-8"))
					pyVersion = re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
					pyFolder = GetPluginsFolder()+'\\'
					shutil.copyfile(pyFolder+pyData['filename'],pyFolder+pyData['pName']+".py.bkp")
					os.remove(pyFolder+pyData['filename'])
					with open(pyFolder+pyData['pName']+".py","w+") as f:
						f.write(pyCode)
					QtBind.removeAt(gui,lvwPlugins,indexSelected)
					QtBind.append(gui,lvwPlugins,pyData['pName']+".py ("+pyData['pName']+" v"+pyVersion+") - Updated recently")
					log('Plugin: "'+pyData['pName']+'" PLUGİNGÜNCELLENDİ')
			except:
				log("Plugin: GÜNCELLEME ALINIRKEN HATA OLUŞTU. DAHA SONRA TEKRAR DENEYİNİZ.")

log('Plugin: '+pName+' v'+pVersion+' BAŞARIYLA YÜKLENDİ')
