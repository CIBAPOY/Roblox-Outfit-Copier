import requests
import json
import os

os.system('cls')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

cookie = None

print(f"{bcolors.WARNING}   ____        _    __ _ _    _____            _           ")
print("  / __ \      | |  / _(_) |  / ____|          (_)          ")
print(" | |  | |_   _| |_| |_ _| |_| |     ___  _ __  _  ___ _ __ ")
print(" | |  | | | | | __|  _| | __| |    / _ \| '_ \| |/ _ \ '__|")
print(" | |__| | |_| | |_| | | | |_| |___| (_) | |_) | |  __/ |   ")
print("  \____/ \__,_|\__|_| |_|\__|\_____\___/| .__/|_|\___|_|   ")
print("                                        | |                ")
print(f"                                        |_|                {bcolors.ENDC}")

print("\n")

for x in range(1):
	print("\n")

try:
	dir = os.path.dirname(os.path.abspath(__file__))
	cook = os.path.join(dir, "cookie.txt")

	f = open(cook, "r")
	cookie = f.read()
	f.close()
except:
	exit("Failed to find cookie.txt")


testing = requests.post('https://auth.roblox.com/v2/logout', cookies = {'.ROBLOSECURITY':cookie})
token = None

try:
	token = testing.headers['x-csrf-token']
except:
	pass

header = {
	'.ROBLOSECURITY': cookie,
	'x-csrf-token': token,
	'content-type': 'application/json'
}



player = None

try:
	player = requests.get('https://www.roblox.com/mobileapi/userinfo', headers=header, cookies = {'.ROBLOSECURITY':cookie}).json()
	print((f"Current Login: {bcolors.OKGREEN}{player['UserName']}({player['UserID']}){bcolors.ENDC}"))
except:
	exit(f"{bcolors.FAIL}Invalid Cookie{bcolors.ENDC}")




if not token:
	exit(f"{bcolors.FAIL}Invalid Cookie{bcolors.ENDC}")

copycat = input("Player Username: ")

data = '{ "usernames": [ "' + copycat + '" ], "excludeBannedUsers": true }'

r = requests.post('https://users.roblox.com/v1/usernames/users', data=data, headers={'content-type': 'text/json'}).json()
try:
	copycat = str(r['data'][0]['id'])
except:
	exit(f"Failed to find specified user: {copycat}")

username = str(r['data'][0]['name'])
print(f'Fetching info about {bcolors.OKGREEN}{username}({copycat}){bcolors.ENDC}')


r = requests.get(f"https://avatar.roblox.com/v1/users/{copycat}/currently-wearing")
doorg = r.json()["assetIds"]

r = requests.get(f"https://avatar.roblox.com/v1/users/{copycat}/avatar")
fagtardtism = r.json()["bodyColors"]






userid = player['UserID']
robuxAmnt = requests.get(f'https://economy.roblox.com/v1/users/{userid}/currency', headers=header, cookies = {'.ROBLOSECURITY':cookie}).json()['robux']
print(f'{bcolors.HEADER}You have {robuxAmnt} Robux{bcolors.ENDC}')
requests.post('https://avatar.roblox.com/v1/avatar/set-player-avatar-type', headers=header, data = '{"playerAvatarType": " ' + r.json()['playerAvatarType'] +'"}', cookies={'.ROBLOSECURITY':cookie})


requests.post('https://avatar.roblox.com/v1/avatar/set-scales', headers=header, data=json.dumps(r.json()['scales']), cookies={'.ROBLOSECURITY':cookie}).json()




r = requests.post("https://avatar.roblox.com/v1/avatar/set-wearing-assets", headers=header, data=json.dumps({}), cookies = {'.ROBLOSECURITY':cookie})

r = requests.post("https://avatar.roblox.com/v1/avatar/set-body-colors", headers=header, data=json.dumps(fagtardtism), cookies = {'.ROBLOSECURITY':cookie})

purchaseItemCount = 0
robuxSpent = 0

assetNames = {}

print("\n")
print("****************")
print(f'{bcolors.WARNING}Attempting Purchases{bcolors.ENDC}')
print("****************")
print("\n")
for x in doorg:
	
	bundleInfo = requests.get(f'https://catalog.roblox.com/v1/assets/{x}/bundles?sortOrder=Asc&limit=10').json()
	bundleId = 0
	r = requests.get(f"https://api.roblox.com/Marketplace/ProductInfo?assetId={x}").json()
	isBundle = False
	if len(bundleInfo['data']) > 0:
		bundleId = bundleInfo['data'][0]['id']
		isBundle = True
	data = {
		'expectedCurrency': 1,
		'expectedPrice': r["PriceInRobux"],
		'expectedSellerId': r["Creator"]["Id"]
	} 

	assetNames[r['AssetId']] = r['Name']
	owned = requests.get(f"http://api.roblox.com/Ownership/HasAsset?userId={player['UserID']}&assetId={r['AssetId']}").json()
	if r['PriceInRobux'] == None:
		r['PriceInRobux'] = 0

	if not owned and r['PriceInRobux'] <= robuxAmnt and not isBundle and not r['IsLimited'] and r['PriceInRobux'] <= robuxAmnt and r['IsForSale'] or not owned and not isBundle and not r['IsLimited'] and r['IsPublicDomain']:
		print(f'{bcolors.HEADER}You have {robuxAmnt} Robux{bcolors.ENDC}')
		
		if r['PriceInRobux'] != 0:
			afterPurchase = robuxAmnt - r['PriceInRobux']
			print(f'{bcolors.HEADER}You will have {afterPurchase} Robux after purchasing{bcolors.ENDC}')

		if r['PriceInRobux'] == 0 or input(f"{bcolors.OKCYAN}Do you want to purchase {r['Name']} for R${r['PriceInRobux']}?{bcolors.ENDC} ({bcolors.OKGREEN}Y{bcolors.ENDC}/{bcolors.FAIL}N{bcolors.ENDC})").lower() == 'y':
			if r['PriceInRobux'] != 0:
				
				robuxSpent = (robuxSpent + r['PriceInRobux'])
				robuxAmnt = robuxAmnt - r['PriceInRobux']
			name = r['Name']
			priceinbobux = r['PriceInRobux']
			print(f'{bcolors.OKGREEN}Purchased {name} for R${priceinbobux}{bcolors.ENDC}')
				
			purchaseItemCount = purchaseItemCount + 1
			r = requests.post(f"https://economy.roblox.com/v1/purchases/products/{r['ProductId']}", headers=header, data=json.dumps(data), cookies = {'.ROBLOSECURITY':cookie})
		else:
			print(f"{bcolors.FAIL}Skipped purchase{bcolors.ENDC}")
	elif r['PriceInRobux'] > robuxAmnt:
		print(f"{bcolors.WARNING}Skipped purchase of '{r['Name']}' because you do not have enough Robux.{bcolors.ENDC}")
	elif owned:
		print(f"{bcolors.WARNING}Skipped purchase of '{r['Name']}' because it was already owned.{bcolors.ENDC}")
	elif r['IsLimited'] == True:
		print(f"{bcolors.WARNING}Skipped purchase of '{r['Name']}' because it is a limited.{bcolors.ENDC}")
	elif isBundle:
		print(f"{bcolors.WARNING}Skipped purchase of '{r['Name']}' because it is a bundle, you can purchase the bundle here{bcolors.ENDC} {bcolors.HEADER}https://www.roblox.com/bundles/{bundleId}{bcolors.ENDC}")
	elif r['IsForSale'] == False:
		print(f"{bcolors.WARNING}Skipped purchase of '{r['Name']}' because it is not for sale.{bcolors.ENDC}")
	print()
print("\n")
print("****************")
print(f'{bcolors.WARNING}Attempting Equips{bcolors.ENDC}')
print("****************")
print("\n")

for x in doorg:
	
	r = requests.post(f"https://avatar.roblox.com/v1/avatar/assets/{x}/wear", headers=header, cookies = {'.ROBLOSECURITY':cookie})
	try:
		if r.json()['success']:
			print(f'{bcolors.OKGREEN}Equipped "{assetNames[x]}"{bcolors.ENDC}')
	except:
		errormsg = r.json()['errors'][0]['message']
		print(f'{bcolors.FAIL}Failed to equip "{assetNames[x]}" (REASON: {str(errormsg).upper()}){bcolors.ENDC}')
		
for x in range(3):
	print("\n")
print("****************")
print(f"{bcolors.OKGREEN}Completed Avatar Copy Of {username}({copycat}){bcolors.ENDC}")
print(f'{bcolors.WARNING}Purchased {purchaseItemCount} item(s){bcolors.ENDC}')
print(f"{bcolors.WARNING}Spent R${robuxSpent}{bcolors.ENDC}")
if input(f"Do you want to save this as an outfit? ({bcolors.OKGREEN}Y{bcolors.ENDC}/{bcolors.FAIL}N{bcolors.ENDC})").lower() == 'y':
	r = requests.get(f"https://avatar.roblox.com/v1/users/{copycat}/avatar").json()
	r['assetIds'] = []
	r['scale'] = r['scales']
	for x in r['assets']:
		r['assetIds'].append(x['id'])

	r.pop('assets', None)
	r.pop('scales',None)
	r.pop('emotes',None)
	r.pop('defaultShirtApplied',None)
	r.pop('defaultPantsApplied',None)
	
	r['name'] = (f"{username} Copy")
	output = requests.post('https://avatar.roblox.com/v1/outfits/create',data = json.dumps(r),headers=header,cookies={'.ROBLOSECURITY':cookie}).json()
	try:
		if output['success']:
			print(f"{bcolors.OKGREEN}Created new outfit: {username} Copy{bcolors.ENDC}")
	except:
		error = output['errors'][0]['message']
		print(f"{bcolors.FAIL}Failed to create new outfit: {error.upper()}{bcolors.ENDC}")
