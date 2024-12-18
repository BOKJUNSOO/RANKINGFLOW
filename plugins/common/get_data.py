def get_data(api_key,**kwargs):
        # schedule 부하 줄이기
        import time
        import requests
        import json
        from pprint import pprint
        pprint("common fuction의 데이터 수집 함수를 호출합니다.")
        # airflow에서 Batch 시점(data_interval_end)에 한국시간
        target_date = kwargs["data_interval_end"].in_timezone("Asia/Seoul").strftime("%Y-%m-%d")
        # 배치일 6시
        pprint(f"{target_date} 의 rankingdata 호출을 시작합니다.")
        # 호출 헤더
        headers = {
        "x-nxopen-api-key" : f"{api_key}",
        "User-agent" : "Mozilla/5.0"
        }
        # json 파일을 담을 객체
        mydata = []
        # 1페이지당 200명의 랭킹정보
        for i in range(1,2):
            if i % 20 == 0:
                time.sleep(15)
                url = f"https://open.api.nexon.com/maplestory/v1/ranking/overall?date={target_date}&world_name=%EC%97%98%EB%A6%AC%EC%8B%9C%EC%9B%80&page={i}"
                req = requests.get(url = url, headers = headers)
                data = req.json()
                mydata.append(data)
            else:
                # 페이지 정보 추가
                url = f"https://open.api.nexon.com/maplestory/v1/ranking/overall?date={target_date}&world_name=%EC%97%98%EB%A6%AC%EC%8B%9C%EC%9B%80&page={i}"
                req = requests.get(url = url, headers = headers)
                data = req.json()
                mydata.append(data)
        pprint(mydata)
        # 호출된 데이터 객체를 data 디렉토리에 저장
        file_path = f"/opt/airflow/data/ranking_{target_date}.json"
        with open (file_path, "w", encoding = "UTF-8-SIG") as f:
            json.dump(mydata
                      ,f
                      ,ensure_ascii=False
                      ,indent='\t'
                        )
        print("done")