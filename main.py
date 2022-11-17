from datetime import date
from os import listdir
from os import name as ordi_name
import requests
import random
import time

# Couleur
vert = ["\x1b[38;5;2m","\x1b[38;5;10m","\x1b[38;5;34m","\x1b[38;5;40m","\x1b[38;5;82m","\x1b[38;5;83m","\x1b[38;5;112m","\x1b[38;5;46m","\x1b[38;5;118m"]
bleu = ["\x1b[38;5;12m","\x1b[38;5;20m","\x1b[38;5;39m","\x1b[38;5;45m","\x1b[38;5;63m","\x1b[38;5;4m","\x1b[38;5;117m","\x1b[38;5;21m","\x1b[38;5;27m"]
rouge = ["\x1b[38;5;1m","\x1b[38;5;9m","\x1b[38;5;160m","\x1b[38;5;196m","\x1b[38;5;197m","\x1b[38;5;198m"]
reset = "\x1b[0m"

# Constante TIME
time_between_file = 1 #120 #2min
time_between_run = 1 #10800 #3h
time_between_request = 1 #5 #5s
time_between_pc_phone = 1 #64 #1min4s
time_between_proxy_test = 1 #1 #1s

max_proxy_tour = 30 #Nombre de test de proxy avant de retourner un dico

err_send = 3 #Nombre Erreur avant arreter le process de send request
number_request = 50 #Nombre requets avant arreter le process de send

def load_file(name):
    cookies={}
    headers={}
    params={}

    try:
        file = open(f"Compte/{name}","r")
        
        _locals = locals()
        exec(file.read(),globals(), _locals)
        headers = _locals["headers"]
        params = _locals["params"]
        cookies = _locals["cookies"]

        file.close()
        return True, cookies, headers, params
    except:
        print("ERREUR : Loading file",name)
        return False, None, None, None

def get_files_names():
    result = listdir("Compte")
    return result

def _send_request_with_proxy(params, cookies, headers, ip, port):
    proxies = create_proxy_dico(ip, port)
    for i in range(3): #On essaye 3fois
        try:
            response = requests.get('https://www.bing.com/search', params=params, cookies=cookies, headers=headers, proxies=proxies)
            if str(response.status_code) == "200":
                return True, response
        except:
            pass
    return False, None

def _send_request_without_proxy(params, cookies, headers):
    for i in range(3): #On essaye 3fois
        try:
            response = requests.get('https://www.bing.com/search', params=params, cookies=cookies, headers=headers)
            if str(response.status_code) == "200":
                return True, response
        except:
            pass
    return False, None

def set_word_url(params, wordlist):
    params['q'] = create_word(wordlist)
    return params

def _send_process(params, cookies, headers, proxy_dic={"IP": "PORT"}):
    #Envoie 1 requete
    for proxy_ip in proxy_dic:
        proxy_port = proxy_dic[proxy_ip]
        if _send_request_with_proxy(params, cookies, headers, proxy_ip, proxy_port)[0] == True:
            return True, "By Proxy"
    if _send_request_without_proxy(params, cookies, headers)[0] == True:
        return True, "Without Proxy"
    else:
        return False, 'ERR'



def send_daily_request(name, cookies, headers, params, wordlist, proxy_dic, registre_name):
    #set_word_url()
    nb_request = 0
    send=True
    err=0
    while send:
        params = set_word_url(params,wordlist)
        stat, info = _send_process(params,cookies,headers,proxy_dic)
        if not stat:
            print("ERR:",info)
            err+=1
        else:
            registre_add_number(name,registre_name)
            nb_request+=1
        if nb_request>=number_request or err>=err_send:
            send=False
        if int(registre_get_number(name,registre_name))>=number_request :
            send=False
    pass



def send_requests(name, cookies, headers, params, wordlist, prox_dic):
    print(f"{bleu[0]}--- Send Request",name,f"---{bleu[1]}\nprox_dic = ",prox_dic,"\n")
    try:
        for i in range(90):
            params['q'] = create_word(wordlist)
            find = False
            for ip in prox_dic:
                port = prox_dic[ip]
                proxies = create_proxy_dico(ip, port)
                try:
                    response = requests.get('https://www.bing.com/search', params=params, cookies=cookies, headers=headers, proxies=proxies)
                    print("Success by PROX",ip,port, end="\r")
                    find = True
                    break
                except:
                    print(f"\n{rouge[0]}ERROR PROXY",ip,port,bleu[1])
                    pass
            if not find: #Faire sans proxy
                response = requests.get('https://www.bing.com/search', params=params, cookies=cookies, headers=headers)
                print(f"\n{rouge[0]}Send Without PROX{bleu[1]}")
            print("\n",params['q'],response)
            time.sleep(time_between_request)
            time.sleep(int(random.randint(0,200)/100))
    except Exception as e:
        print(f"\n{rouge[0]}ERREUR : Send Request PC with Account",name, e)

    print(f"\n\n{bleu[0]}--- Header CHANGEMENT GO TO MOBILE ---{bleu[1]}\n")
    time.sleep(time_between_pc_phone)

    #Header Tel
    try:
        headers['user-agent'] = "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36"
    except:
        print(f"\n{rouge[0]}ERREUR: USER-AGENT Account File Headers dic Not Define,",name,bleu[1])
    
    try:
        for i in range(60):
            params['q'] = create_word(wordlist)
            find = False
            for ip in prox_dic:
                port = prox_dic[ip]
                proxies = create_proxy_dico(ip, port)
                try:
                    response = requests.get('https://www.bing.com/search', params=params, cookies=cookies, headers=headers, proxies=proxies)
                    print("Success by PROX",ip,port, end="\r")
                    find = True
                    break
                except:
                    print(f"\n{rouge[0]}ERROR PROXY",ip,port,bleu[1])
                    pass
            if not find: #Faire sans proxy
                response = requests.get('https://www.bing.com/search', params=params, cookies=cookies, headers=headers)
                print(f"\n{rouge[0]}Send Without PROX{bleu[1]}")
            print("\n",params['q'],response)
            time.sleep(time_between_request)
            time.sleep(int(random.randint(0,200)/100))
    except Exception as e:
        print(f"\n{rouge[0]}ERREUR: Request Mobile with Account",name,e)
    print(f"\n{bleu[0]}----------------{reset}")



def registre_get_number(name, registre_name):
    #Renvoie le nombre de request associé à un nom
    """
    Registre = 10-12-2022:COMPTE;RECHERCHE:COMPTE;RECHER
    """
    file = open(registre_name,"r")
    c = file.read().split('\n')
    file.close()
    line = c[-1]
    cut = line.split(":")
    if str(cut[0]) == str(date.today()):
        del cut[0] #Supprime la date
        for compte in cut:
            name_compte, stat = compte.split(";")
            if name_compte == name:
                return stat
    return 0
        
    

def registre_add_number(name,registre_name):
    try:
        file = open(registre_name,"r")
        c = file.read().split("\n")
        file.close()
    except:
        file = open(registre_name,"w")
        file.close()
        c=[':']
    line = c[-1]
    cut = line.split(":")
    if str(cut[0]) == str(date.today()):
        compte_ls = cut[1:]
    else:
        print("Today not found")
        c.append(f"{str(date.today())}")
        compte_ls = []
    
    find = False
    t=0
    for compte in compte_ls:
        l = compte.split(";")
        if l[0] == name:
            l[1] = str(int(l[1]) + 1)
            find = True
            compte_ls[t] = ";".join(l)
        t += 1
    if not find:
        compte_ls.append(f"{name};1")
    result_ls = [str(date.today())]
    for i in compte_ls:
        result_ls.append(i)
    result = ":".join(result_ls)
    c[-1] = result
    
    file = open(registre_name,"w")
    file.write("\n".join(c))
    file.close()



            
            
"""
def registre_open():
    file = open("registre.txt","r")
    c=file.read().split("\n")[-1]
    file.close()
    return c

def registre_write(name):
    file = open("registre.txt","r")
    c = file.read().split("\n")
    file.close()
    l = c[-1].split(":")
    if l[0] != str(date.today()):
        c.append(":".join([str(date.today()),name]))
    else:
        l.append(name)
        c[-1] = ":".join(l)
    file = open("registre.txt","w")
    file.write("\n".join(c))
    file.close()

def is_already_open(name):
    #WW1sdFlYUm9ZWGc9
    try:
        print(registre_open().split(":")[0])
        if registre_open().split(":")[0] != str(date.today()):
            print("Mauvaise date")
            return False
        else:
            if name not in registre_open().split(":") :
                return False
    except:
        file = open("registre.txt","w")
        file.close()
        return False
    return True

"""
def open_dico():
    file = open("dico.txt","r")
    c = file.read().split("\n")
    file.close()
    if len(c) < 3:
        return []
    return c

def create_word_by_dico(wordlist):
    if wordlist in [[], [''], None]:
        wordlist=open_dico()
    result=[]
    for i in range(random.randint(1,6)):
        result.append(random.choice(wordlist))
    result = "+".join(result)
    return result

def create_word_by_calcul():
    r=""
    for i in range(random.randint(1,10)):
        r+=str(random.randint(1,50))
        r+=random.choice(["%2B","%2F","-","*"])
    r+=str(random.randint(1,50))
    return r

def create_word_by_definition(wordlist):
    if wordlist in [[], [''], None]:
        wordlist=open_dico()
    result = random.choice(["definition de", "def","défff","définition","déff de","dfinition de"])
    result += " "
    result += random.choice(wordlist)
    return result

def create_word_by_random_char():
    r=""
    for i in range(random.randint(1,10)):
        r+=random.choice(list("abcdefghijklmnopqrstuvwxyz"))
    return r

def create_word(wordlist):
    nb = int((((random.randint(1,250)^2)%4*(int(time.time())/random.randint(1,3)))%4)+1)
    nb = random.choice([1,2,3,4,nb])
    n=0 #Credit Only (Useless)
    if nb == 1 or n=="WW1sdFlYUm9ZWGc9" or wordlist in [[],[''],None]:
        return create_word_by_calcul()
    elif nb == 2:
        return create_word_by_definition(wordlist)
    elif nb == 3:
        return create_word_by_random_char()
    else:
        return create_word_by_dico(wordlist)


def _get_proxy_list():
    # Renvoie une dico {IP:PORT}
    #https://free-proxy-list.net
    try:
        response = requests.get("https://free-proxy-list.net")
        content = response.content.decode()
        
        tbody = content.split("<tbody>")[1].split("</tbody>")[0]
        result = {}
        
        for tr in tbody.split("<tr>")[1:]:
            """
            TR = 
            <td>156.239.50.234</td><td>3128</td><td>US</td><td class='hm'>United States</td><td>transparent</td><td class='hm'>no</td><td class='hx'>no</td><td class='hm'>1 hour 26 mins ago</td></tr>
            """
            try:
                td = tr.split("<td>")[1:]
                #print(tr)
                https_supported = tr.split("<td class='hx'>")[1]
                #print(https_supported[:2])
                if str(https_supported)[:2] != "no" :
                   
                    ip = td[0].split("</td>")[0]
                    port = td[1].split("</td>")[0]
                    result[f"{ip}"]=str(port)
            except:
                pass
        return result
    except:
        return {}

def test_proxy(ip, port):
    # Renvoie si le proxy marche avec BING
    proxies = create_proxy_dico(ip, port)
    try:
        response = requests.get(f"https://www.bing.com/search?q={create_word_by_random_char()}", proxies=proxies, timeout=5)
        if get_public_ip(ip, port) == None:
            return False
        return True
    except:
        return False

def get_public_ip(ip, port):
    # Renvoie l'IP publique
    try:
        proxies = create_proxy_dico(ip, port)
        return (requests.get("https://ident.me", proxies=proxies, timeout=5)).content.decode()
    except:
        return None

def proxy(min_size):
    # Renvoie un dico de proxy utilisable
    prox = _get_proxy_list()
    avaible = {}
    tour=0
    for ip in prox:
        #Test de faire une requête
        port = prox[ip]
        print(f"{tour}. TEST : " + ip + ":" + port)
        if test_proxy(ip,port):
            print("---> IP is UP and your PUBLIC IP is",get_public_ip(ip,port))
            avaible[ip]=port
        
        if len(avaible)>min_size:
            return avaible
        if len(avaible)>int(min_size/2) or tour>max_proxy_tour:
            return avaible
        tour+=1
        time.sleep(time_between_proxy_test)
    return {}

def create_proxy_dico(ip, port):
    # Creer l'argument proxies pour request
    if ordi_name == "nt":
        proxies = {
            'http': f"{ip}:{port}",
            'https': f"{ip}:{port}",
        }
    else: #LINUX
        proxies = {
            'http': f"http://{ip}:{port}",
            'https': f"https://{ip}:{port}",
        }
    return proxies


def _start():
    #Constante
    wordlist = open_dico()
    print("Version PC",ordi_name)
    while True:
        print(f"{bleu[0]}--- Get Proxy ---{bleu[1]}")
        
        min_size=len(get_files_names())+1
        prox_dic = proxy(min_size)
        
        print("PROX_DIC:",prox_dic,f"\n{bleu[0]}-------------{reset}\n")
        for name in get_files_names():
            print(f"\n{vert[0]}--- File",name,f"---{vert[1]}")
                
            print("Load FILE info :")
            result, cookies, headers, params = load_file(name)
            print("Success Loading :",result,f"\n{vert[0]}-------------{reset}\n")
            if result:
                if random.randint(1,5) == 4:
                    print("Random Chose without Proxy")
                    send_daily_request(name, cookies, headers, params, wordlist,{},"registre_pc.txt")
                    time.sleep(time_between_pc_phone)
                    #Header Tel
                    try:
                        headers['user-agent'] = "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36"
                    except:
                        print(f"\n{rouge[0]}ERREUR: USER-AGENT Account File Headers dic Not Define,",name,bleu[1])
                    send_daily_request(name, cookies, headers, params, wordlist,{},"registre_phone.txt")
                    #send_requests(name, cookies, headers, params, wordlist, {})
                else:
                    print("Random Chose WITH PROXY")
                    send_daily_request(name, cookies, headers, params, wordlist,prox_dic,"registre_pc.txt")
                    time.sleep(time_between_pc_phone)
                    #Header Tel
                    try:
                        headers['user-agent'] = "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36"
                    except:
                        print(f"\n{rouge[0]}ERREUR: USER-AGENT Account File Headers dic Not Define,",name,bleu[1])
                    send_daily_request(name, cookies, headers, params, wordlist,prox_dic,"registre_phone.txt")
                    #send_requests(name, cookies, headers, params, wordlist, prox_dic)
            else:
                print("Erreur Loading FILE INFO\n-------------\n")
            
            time.sleep(time_between_file)
        time.sleep(time_between_run) #3Heures
        
        if wordlist in [[], [''], None]:
            wordlist = open_dico()



if __name__ == "__main__":
    print("Micosoft Reward Cracker\nBy BiMathAx 11-2022")
    _start()
    


