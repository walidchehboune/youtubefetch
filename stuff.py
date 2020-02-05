
from requests import *
from json import *
from re import *
url="media/videos"
array_world_to_find=[
    ""
]
array_url=[
    """List of your videos"""




]

min_like=100
s=Session()
array_username=[]
array_like=[]
array_appear=[]
array_comment=[]


for full_url in array_url:
    obj=s.get(full_url+"&pbj=1",headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "X-YouTube-Client-Name":"1",

    },
          cookies=s.cookies.get_dict())

    obj=s.get(full_url,headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "X-YouTube-Client-Name":"1",

    },
          cookies=s.cookies.get_dict())
    XSRF_TOKEN=findall("XSRF_TOKEN\":\"([a-zA-Z0-9\-\_:\,;=\%]+)",obj.text)[0]
    continuation=findall("continuation\":\"([a-zA-Z0-9\-\,\._:;=\%]+)",obj.text)[0]


    print("[+] xsrf token : "+XSRF_TOKEN)
    print("[+] continuation :"+continuation)
    comments=s.post("https://www.youtube.com/comment_service_ajax?action_get_comments=1&pbj=1&ctoken="+continuation+"&continuation="+continuation,headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "X-YouTube-Client-Name":"1",

    },
          cookies=s.cookies.get_dict(),data={"session_token":XSRF_TOKEN})



    js=loads(comments.text)
    XSRF_TOKEN=js["xsrf_token"]

    next_url="https://www.youtube.com/comment_service_ajax?action_get_comments=1&pbj=1&ctoken="+js["response"]["continuationContents"]["itemSectionContinuation"]["continuations"][0]["nextContinuationData"]["continuation"]+"&continuation="+js["response"]["continuationContents"]["itemSectionContinuation"]["continuations"][0]["nextContinuationData"]["continuation"]


    for item in js["response"]["continuationContents"]["itemSectionContinuation"]["contents"]:
        if item["commentThreadRenderer"]["comment"]["commentRenderer"]["likeCount"] > min_like:
            print("[-] user-name :"+item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"]+"like count : "+str(item["commentThreadRenderer"]["comment"]["commentRenderer"]["likeCount"])+" ======> "+item["commentThreadRenderer"]["comment"]["commentRenderer"]["contentText"]["runs"][0]["text"])
            if item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"] in array_username:
                array_appear[array_username.index(item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"])] = array_appear[array_username.index(item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"])] + 1
                array_comment[array_username.index(item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"])]=array_comment[array_username.index(item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"])]+"|"+item["commentThreadRenderer"]["comment"]["commentRenderer"]["contentText"]["runs"][0]["text"]
            else:
                array_appear.append(1)
                array_username.append(item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"])
                array_like.append(str(item["commentThreadRenderer"]["comment"]["commentRenderer"]["likeCount"]))
                array_comment.append(item["commentThreadRenderer"]["comment"]["commentRenderer"]["contentText"]["runs"][0]["text"])


    while next_url != None:
        comments=s.post(
            next_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",

            },
            cookies=s.cookies.get_dict(), data={"session_token": XSRF_TOKEN})

        js = loads(comments.text)
        js["xsrf_token"]
        try:
            continuation = js["endpoint"]["urlEndpoint"]["url"].split("?")[1].split("&")[1].split("=")[1]
            next_url = "https://www.youtube.com/comment_service_ajax?action_get_comments=1&pbj=1&ctoken=" + js["response"]["continuationContents"]["itemSectionContinuation"]["continuations"][0]["nextContinuationData"]["continuation"] + "&continuation=" + js["response"]["continuationContents"]["itemSectionContinuation"]["continuations"][0]["nextContinuationData"]["continuation"]
            for item in js["response"]["continuationContents"]["itemSectionContinuation"]["contents"]:
                if item["commentThreadRenderer"]["comment"]["commentRenderer"]["likeCount"] > min_like:
                    print("[-] user-name :" + item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"]+"like count : "+str(item["commentThreadRenderer"]["comment"]["commentRenderer"]["likeCount"])+" ======> "+item["commentThreadRenderer"]["comment"]["commentRenderer"]["contentText"]["runs"][0]["text"])

                    if item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"][
                        "simpleText"] in array_username:
                        array_appear[array_username.index(
                            item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"])] = array_appear[array_username.index(item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"])] + 1
                        array_comment[array_username.index(
                            item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"])] = \
                        array_comment[array_username.index(
                            item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"][
                                "simpleText"])] + "|" + \
                        item["commentThreadRenderer"]["comment"]["commentRenderer"]["contentText"]["runs"][0]["text"]
                    else:
                        array_appear.append(1)
                        array_username.append(
                            item["commentThreadRenderer"]["comment"]["commentRenderer"]["authorText"]["simpleText"])
                        array_like.append(str(item["commentThreadRenderer"]["comment"]["commentRenderer"]["likeCount"]))
                        array_comment.append(
                            item["commentThreadRenderer"]["comment"]["commentRenderer"]["contentText"]["runs"][0][
                                "text"])


        except KeyError:
            next_url=None


for i,j,k in zip(array_username,array_appear,array_comment):
    if j > 1:
        print("["+i+"] ")
        print("------------")
        for o in k.split("|"):
            print("[*] "+o)


