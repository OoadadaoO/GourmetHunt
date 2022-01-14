import googlemaps
import pandas
import random
from time import sleep
import os
google_key = 'AIzaSyDODOcHvdTli-zDJXGPVDqlam5M-Y1LRXE'
gclient = googlemaps.Client(key = google_key)
def randomrestaurant(place,keyword='-1',distant=500,money=0,rating=0):
    uniPlace = str(place.encode('unicode_escape'))
    uniPlace = uniPlace.replace("'", '')
    uniPlace = uniPlace.replace('\\', '')
    uniKeyword = str(keyword.encode('unicode_escape'))
    uniKeyword = uniKeyword.replace("'", '')
    uniKeyword = uniKeyword.replace('\\', '')
    filename='./crawl/nearrestaurant/'+uniPlace+'_'+uniKeyword+'_'+str(distant)+'_'+str(money)+'.csv'
    # print(filename)
    imgpath='./crawl/temprestimg.png'
    if os.path.isfile(filename):
        pass

    else:
        weizi_id=gclient.find_place(input=place,input_type='textquery')['candidates'][0]['place_id']
        print('請稍候')
        lat_lng=gclient.place(place_id=weizi_id,language='zh-TW')['result']['geometry']['location']
        lat=lat_lng['lat']
        lng=lat_lng['lng']
        ziliaoshu=0
        if keyword=='-1':
            if money!=0:
                can_place=gclient.places(location=(lat,lng),type='restaurant',language='zh-TW',radius=distant,max_price=money)
            else:
                can_place=gclient.places(location=(lat,lng),type='restaurant',language='zh-TW',radius=distant)
        else:
            if money!=0:
                can_place=gclient.places(query=keyword,location=(lat,lng),type='restaurant',language='zh-TW',radius=distant,max_price=money)
            else:
                can_place=gclient.places(query=keyword,location=(lat,lng),type='restaurant',language='zh-TW',radius=distant)
        nextpage=0
        try:
            nextpage=can_place['next_page_token']

        except:
            pass
        a=can_place['results']
        ziliaoshu+=20
        print ('目前資料小於'+str(ziliaoshu)+'筆')
        n=0
        while nextpage!=0:
            n+=1
            sleep(3)
            can_place=gclient.places(page_token=nextpage)
            try:
                nextpage=can_place['next_page_token']
            except:
                break
            if can_place['results'][0] in a:
                break
            if n>5:
                break
            ziliaoshu+=20
            a.extend(can_place['results'])
            print ('目前資料'+str(ziliaoshu)+'筆')
        # print('finded')
        data=pandas.DataFrame(a)
        # print('transed')
        data.to_csv(filename)
        # print('saved')
    rawdata=pandas.read_csv(filename)
    # print('readed')
    ratedata=rawdata.copy()
    # print('copied')
    for i in reversed(range(len(rawdata))):
        # print(rawdata.iloc[i][12])
        try:
            if int(rawdata.iloc[i][12])<=rating:
                ratedata=ratedata.drop(index=i)
        except:
            pass
    # print('rated')
    # print(imgpath)

    ran=random.random()
    ran=int(ran*len(ratedata))
    #print(ran)
    #print(len(ratedata))
    #print(ratedata.iloc[ran][9])
    try:
        urlstart=ratedata.iloc[ran][9].find('Aap')
        urlend=ratedata.iloc[ran][9].find('width')
        photo_reference=ratedata.iloc[ran][9][urlstart:urlend-4]
        # print(photo_reference)
        with open(imgpath, 'wb') as f:
            for chunk in gclient.places_photo(photo_reference,max_width=10000):
                if chunk:
                    f.write(chunk)
    except:
        pass

    try:
        return {'name':ratedata.iloc[ran][7],'url':'https://www.google.com/maps/search/?api=1&query='+place+'&query_place_id='+ratedata.iloc[ran][10],'path':imgpath}
    except:
        return('附近沒有評分這麼高的餐廳')

# print(randomrestaurant(place='台大',money=0,keyword='火鍋'))






