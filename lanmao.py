import argparse
import copy
import time
import requests
import json

with open("config.json", "r") as config:
    config_data = json.load(config)
"""
    appointmentDate: 预约的日期
    emulatorStoreId： 门面的Id。 清湖懒猫10， 沙井实体车24， 布吉实体车25。
    drivingSchoolId： 驾校
    identityNumber： 身份证
"""


def get_emulator_time_list(days, StoreId, id):
    appointed_day = str(int(time.strftime("%d")) + days).zfill(2)
    appointed_time = time.strftime("%Y-%m-" + str(appointed_day))
    payload = json.dumps({
        "appointmentDate": appointed_time,
        "emulatorStoreId": StoreId,
        "drivingSchoolId": 1,
        "identityNumber": id,
        "page": 1
    })

    res_time_list = ["8:00", "10:00", "12:00", "14:00", "16:00", "18:00"]
    response = requests.request("POST", config_data["url_list"], headers=config_data["headers"],
                                data=payload, proxies=config_data["proxies"])
    res = json.loads(response.text)
    res_list = []
    for _ in res['data']:
        res_dict = {}
        copy_time_list = copy.deepcopy(res_time_list)
        for one_line_data in _['appointmentList']:
            copy_time_list.remove(one_line_data['startTime'])
        res_dict['emulatorId'] = _['id']
        res_dict['emulatorName'] = _['name']
        res_dict['leftTime'] = copy_time_list
        res_dict['appointed_date'] = appointed_time

        res_list.append(res_dict)
    return res_list


def add_appointment(start_time, days, id, StoreId, subject):
    if start_time is None:
        start_time = ["14:00", "16:00"]
    if days is None:
        days = [2]
    for day in days:
        emulator_time_list = get_emulator_time_list(day, StoreId, id)
        # print(emulator_time_list)
        for time_list in emulator_time_list:
            if set(start_time) < set(time_list['leftTime']):
                for start in start_time:
                    payload = json.dumps({
                        "startTime": start,
                        "appointmentDate": time_list['appointed_date'],
                        "emulatorId": time_list['emulatorId'],
                        "identityNumber": id,
                        "emulatorStoreId": StoreId,
                        "subject": subject
                    })
                    response = requests.request("POST", config_data["url_add"], headers=config_data["headers"],
                                                data=payload, proxies=config_data["proxies"])
                    print(response.text)
            else:
                if len(time_list['leftTime']) > 0:
                    print("该时间段已有人占领，现在只剩：", time_list)


def cancel_appointment(lession_id=96635):
    payload = json.dumps({
        "id": lession_id
    })
    response = requests.request("POST", config_data["url_cancel"], headers=config_data["headers"],
                                data=payload, proxies=config_data["proxies"])
    print(response.text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", default=None, nargs="*", type=int, help="预约哪一天，0表今天，1表明天")
    parser.add_argument("--store_id", default=25, help="门面id")
    parser.add_argument("--start_time", default=None, nargs="*", type=str, help="预约时间 时间格式：12:00")
    parser.add_argument("--id", default=430426200411200536, help="身份证")
    parser.add_argument("--subject", default="科目三", help="预约科目")
    parser.add_argument("--appointment", default=None, nargs="?", help="已经预约的课程")
    parser.add_argument("--lession_id", default=None, nargs="?", help="取消预约id")
    args = parser.parse_args()
    add_appointment(args.start_time, args.days, args.id, args.store_id, args.subject)
    # print(get_emulator_time_list(args.days, args.store_id, args.id))


if __name__ == "__main__":
    main()
