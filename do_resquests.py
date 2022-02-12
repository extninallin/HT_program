from numpy import append
from pandas import read_csv
import asyncio
import aiohttp
import time

url = 'https://internal-api.mercadolibre.com/sites/{}/users/{}/handling_time?logistic_type={}'
# list_seller = read_csv("MLA__SSHP-359043_sellers_XD.csv")
# lista = list_seller['Sellers'].values.tolist()
# list_seller = []
lista = []
results = []
sellers =[]
payloads=[]
# start = time.time()

################  BACKUP  #####################
def get_tasks(session, site, logistic_type, lista):
    tasks = []
    for seller in lista:
        tasks.append(asyncio.create_task(session.get(
            url.format(site, seller, logistic_type), ssl=False)))
    return tasks

async def get_backup_async(site, logistic_type, lista):
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, site, logistic_type, lista)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.json())
    countList = len(lista)
    with open(f"sellers_{site}_{logistic_type}_{countList}_BAK.txt", 'w') as outfile:
        count = 0
        for item in lista:
            outfile.write(f"{item};{results[count]}\n".replace(
                "'", '"').replace("None", "null"))
            count += 1

def get_backup(site, logistic_type, csv_file):

    list_seller = read_csv(csv_file,header=None)
    # lista = list_seller.values.tolist()
    lista = list_seller.iloc[:,0].tolist()
    start = time.time()

    try:
        asyncio.run(get_backup_async(site, logistic_type, lista))
        end = time.time()
        total_time = end - start
        print("It took {} seconds to make {} API calls".format(
            total_time, len(lista)))

    except Exception as e:
        print(f"NOK - Algo salio mal: {e}")
########################################################################

###################### ROLLBACK ##################################
async def post_rollback(site, logistic_type, sellers, body):
    async with aiohttp.ClientSession() as session:
        for seller in sellers:
            for payload in body:
                responses = await asyncio.create_task(session.post(url.format(site, seller, logistic_type), ssl=False, data=payload))

def format_txt(txt_file):
    with open(txt_file, "r") as input_file:
        content = input_file.readlines()
        for line in content:
            tokens = line.split(";")
            sellers.append(tokens[0])
            payloads.append(tokens[1])

def post_backup(site, logistic_type, txt_file):
    
    format_txt(txt_file)
    try:
        asyncio.run(post_rollback(site, logistic_type, sellers, payloads))
    except Exception as e:
        print(f"NOK - Algo salio mal: {e}")
########################################################################