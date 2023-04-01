# 데이터 저장할 리스트
cu_store_data =[]
has_cu_store_name = []
has_cu_store_addr = []

# 제공하는 서비스
cu_offer_service = {0 : '24h', 1 : 'post', 2 : 'bakery', 3 :'chicken', 4 : 'coffee', 5 : 'lotto', 6 :'toto' , 7 : 'atm', 8 : 'print', 9 : 'POSmoney', 10 : 'battery'}

# url 목록
url = 'https://cu.bgfretail.com/store/list.do?category=store'
cu_gu_api = 'https://cu.bgfretail.com/store/GugunList.do'
cu_dong_api = 'https://cu.bgfretail.com/store/DongList.do'
cu_store_api = 'https://cu.bgfretail.com/store/list_Ajax.do'

r = requests.get(url)
bs = BS(r.text)
sido_list = []

# 요청 페이로드

cu_gu_payload = {'pageIndex':'1','listType':'','jumpoCode':'','jumpoLotto':'','jumpoToto':'','jumpoCash':'','jumpoHour':'','jumpoCafe':'','jumpoDelivery':'','jumpoBakery':'','jumpoFry':'','jumpoMultiDevice':'','jumpoPosCash':'','jumpoBattery':'','jumpoAdderss':'','jumpoSido':'경기도','jumpoGugun':'','jumpodong':'','user_id':'','sido':'경기도','Gugun':'','jumpoName':''}
cu_dong_payload = {'pageIndex':'1','listType':'','jumpoCode':'','jumpoLotto':'','jumpoToto':'','jumpoCash':'','jumpoHour':'','jumpoCafe':'','jumpoDelivery':'','jumpoBakery':'','jumpoFry':'','jumpoMultiDevice':'','jumpoPosCash':'','jumpoBattery':'','jumpoAdderss':'','jumpoSido':'경기도','jumpoGugun':'가평군','jumpodong':'','user_id':'','sido':'경기도','Gugun':'가평군','jumpoName':''}
cu_store_payload = {'pageIndex':'1', 'listType':'', 'jumpoCode':'', 'jumpoLotto':'', 'jumpoToto':'', 'jumpoCash':'', 'jumpoHour':'', 'jumpoCafe':'', 'jumpoDelivery':'', 'jumpoBakery':'', 'jumpoFry':'', 'jumpoMultiDevice':'', 'jumpoPosCash':'', 'jumpoBattery':'', 'jumpoAdderss':'', 'jumpoSido':'경기도', 'jumpoGugun':'가평군', 'jumpodong':'가평읍', 'user_id':'', 'sido':'경기도', 'Gugun':'가평군', 'jumpoName':''}

for sido in bs.find(id = 'sido').findAll('option')[1:] :
    sido_list.append(sido['value'])
    
    # 시도값 설정
    cu_gu_payload['jumpoSido'] = sido['value']
    cu_gu_payload['sido'] = sido['value']
    cu_dong_payload['jumpoSido'] = sido['value']
    cu_dong_payload['sido'] = sido['value']
    cu_store_payload['jumpoSido'] = sido['value']
    cu_store_payload['sido'] = sido['value']
    
    cu_gu_r = requests.post(cu_gu_api, data = cu_gu_payload)
    for gugun in cu_gu_r.json()['GugunList'] :
        
        # 구군값 설정
        cu_dong_payload['jumpoGugun'] = gugun['CODE_NAME']
        cu_dong_payload['Gugun'] = gugun['CODE_NAME']
        cu_store_payload['jumpoGugun'] = gugun['CODE_NAME']
        cu_store_payload['Gugun'] = gugun['CODE_NAME']
        
        cu_dong_r = requests.post(cu_dong_api, data = cu_dong_payload)
        for dong in cu_dong_r.json()['GugunList'] :
            
            #동값 설정
            cu_store_payload['jumpodong'] = dong['CODE_NAME']
            store_r = requests.post(cu_store_api, data = cu_store_payload)
            bs_store_r = BS(store_r.text)
            for store in bs_store_r.find('div', {'class' : 'detail_store'}).findAll('tr')[1:] :
                try :
                    store_name = store.find('span').text
                    offer_list = []
                    
                    # 중복된 값인지 판단 후 중복되지 않은 것으로 판단되면 데이터 저장
                    if store_name not in has_cu_store_name and store.find('a').text not in has_cu_store_addr :
                        for idx, li in enumerate(store.findAll('li')) :
                            if len(li['class']) == 2 :
                                offer_list.append(cu_offer_service[idx])
                        cu_store_data.append({'offeringService': offer_list, 'shopCode': None, 'longs': None, 'address': store.find('a').text, 'shopName': store_name, 'lat': None,'brand' : 'CU'})
                        has_cu_store_name.append(store_name)
                        has_cu_store_addr.append(store.find('a').text)
                except :
                    print(sido['value'], gugun['CODE_NAME'], dong['CODE_NAME'], store)

