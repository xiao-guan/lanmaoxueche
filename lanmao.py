import argparse
import copy
import csv
import datetime
import os
from datetime import datetime as dt
import time
import requests
import json

with open("config.json", "r", encoding="utf8") as config:
    config_data = json.load(config)


def get_emulator_time_list(StoreId, days=0):
    appointed_time = str(datetime.date.today() + datetime.timedelta(days=days))
    config_data["payload_schedule"]["appointmentDate"] = appointed_time
    config_data["payload_schedule"]["emulatorStoreId"] = StoreId
    payload = json.dumps(config_data["payload_schedule"])

    res_time_list = ["8:00", "10:00", "12:00", "14:00", "16:00", "18:00"]
    response = requests.request("POST", config_data["url_emulator_list"], headers=config_data["headers"],
                                data=payload)
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
    if days == 2:
        days = [2]
    for day in days:
        emulator_time_list = get_emulator_time_list(StoreId, day)
        for time_list in emulator_time_list:
            if set(start_time) < set(time_list['leftTime']):
                for _ in start_time:
                    config_data["payload_appointment"]["startTime"] = _
                    config_data["payload_appointment"]["appointmentDate"] = time_list['appointed_date']
                    config_data["payload_appointment"]["emulatorId"] = time_list['emulatorId']
                    config_data["payload_appointment"]["identityNumber"] = id
                    config_data["payload_appointment"]["emulatorStoreId"] = StoreId
                    config_data["payload_appointment"]["subject"] = subject
                    print(config_data["payload_appointment"])
                    payload = json.dumps(config_data["payload_appointment"])
                    response = requests.request("POST", config_data["url_add"], headers=config_data["headers"],
                                                data=payload)
                    print(response.text)
            else:
                if len(time_list['leftTime']) > 0:
                    print("该时间段已有人占领，现在只剩：", time_list)
                else:
                    print(f"{time_list['appointed_date']}全天占满！")


def cancel_appointment(lession_id=96635):
    payload = json.dumps({
        "id": lession_id
    })
    response = requests.request("POST", config_data["url_cancel"], headers=config_data["headers"],
                                data=payload)
    print(response.text)


def my_schedule():
    payload = json.dumps({
        "page": 1
    })
    response = requests.request("POST", config_data["url_appointmentRecord_list"], headers=config_data["headers"],
                                data=payload)
    res = json.loads(response.text)
    res_list = []
    for _ in res["data"]:
        if _["statusName"] == "待签到":
            res_dict = {
                'id': _["id"],
                'startTime': _["startTime"],
                'createTime': _["createTime"],
                'appointmentDate': _["appointmentDate"],
                'emulatorName': _["emulatorName"]
            }
            res_list.append(res_dict)
    return res_list


def one_day_schedule(StoreId, appointed_time="2023-07-26", days=0):
    if isinstance(days, list):
        if days[0] < 3:
            appointed_time = str(datetime.date.today() + datetime.timedelta(days=days[0]))
    else:
        if days < 3:
            appointed_time = str(datetime.date.today() + datetime.timedelta(days=days))
    config_data["payload_schedule"]["appointmentDate"] = appointed_time
    config_data["payload_schedule"]["emulatorStoreId"] = StoreId
    payload = json.dumps(config_data["payload_schedule"])
    response = requests.request("POST", config_data["url_emulator_list"], headers=config_data["headers"],
                                data=payload)
    res = json.loads(response.text)
    schedule_list = []
    res_list = []
    dict_temp = {}
    for _ in res["data"]:
        for index, schedule in enumerate(_["appointmentList"]):
            schedule_dict = dict_temp.copy()
            time_scope = schedule["startTime"] + "~" + schedule["endTime"]
            schedule_dict["time_scope"] = time_scope
            schedule_dict["name"] = schedule["name"]
            schedule_dict["createTime"] = schedule["createTime"]
            schedule_dict["appointmentDate"] = schedule["appointmentDate"]
            schedule_dict["identityNumber"] = schedule["identityNumber"]
            schedule_dict["phone"] = schedule["phone"]
            schedule_dict["emulatorName"] = schedule["emulatorName"]
            schedule_dict["top"] = index
            schedule_list.append(schedule_dict)
        schedule_list = sorted(schedule_list, key=lambda x: dt.strptime(x['time_scope'].split('~')[0], '%H:%M'))
        res_list.append(schedule_list.copy())
        schedule_list.clear()
    return res_list


def heart_girl(appointed_time, days=2):
    if isinstance(days, list):
        if days[0] < 3:
            appointed_time = str(datetime.date.today() + datetime.timedelta(days=days[0]))
    else:
        if days < 3:
            appointed_time = str(datetime.date.today() + datetime.timedelta(days=days))
    StoreId = [24, 25]
    wonderful_time = []
    found = False
    for s_id in StoreId:
        res = one_day_schedule(s_id, appointed_time=appointed_time, days=days)
        for _ in res:
            for one_line in _:
                if one_line["name"] == "大聪明":
                    wonderful_time.append(one_line)
                    found = True
    if found:
        print(wonderful_time)
        print("heart girl has appeared!")
    else:
        print(f"sorry!not today:{appointed_time}")


def get_student_data(days=-120):
    csv_file = "unique_data.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
        first_row = True
    else:
        first_row = False
    schedule_list = []
    for day in range(days, 3):
        appointed_time = str(datetime.date.today() + datetime.timedelta(days=day))
        for emulatorStoreId in [24, 25]:
            for drivingSchoolId in [1, 2, 3]:
                time.sleep(0.5)
                config_data["payload_schedule"]["appointmentDate"] = appointed_time
                config_data["payload_schedule"]["emulatorStoreId"] = emulatorStoreId
                config_data["payload_schedule"]["drivingSchoolId"] = drivingSchoolId
                payload = json.dumps(config_data["payload_schedule"])
                response = requests.request("POST", config_data["url_emulator_list"], headers=config_data["headers"],
                                            data=payload)
                res = json.loads(response.text)
                for _ in res["data"]:
                    for schedule in _["appointmentList"]:
                        schedule_dict = {}
                        schedule_dict["name"] = schedule["name"]
                        schedule_dict["identityNumber"] = schedule["identityNumber"]
                        schedule_dict["phone"] = schedule["phone"]
                        schedule_list.append(schedule_dict)
                unique_data_list = [dict(item) for item in set(tuple(sorted(d.items())) for d in schedule_list)]
                # 将去重后的数据写入CSV文件
                with open(csv_file, mode="a+", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    if first_row:
                        first_row = False
                        writer.writerow(unique_data_list[0].keys())  # 写入CSV文件的标题行，使用第一个字典的键作为标题
                    for item in unique_data_list:
                        writer.writerow(item.values())  # 写入去重后的数据
                schedule_list.clear()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", default=2, nargs="*", type=int, help="预约哪一天，0表今天，1表明天")
    parser.add_argument("--store_id", default=25, help="门面id")
    parser.add_argument("--start_time", default=None, nargs="*", type=str, help="预约时间 时间格式：12:00")
    parser.add_argument("--id", default=12345678901234567489, help="身份证")
    parser.add_argument("--subject", default="科目三", help="预约科目")
    parser.add_argument("--appointment", default=None, nargs="?", help="已经预约的课程")
    parser.add_argument("--lession_id", default=None, nargs="?", help="取消预约id")
    parser.add_argument("--appointed_time", default="2023-07-26", help="预约日期")
    args = parser.parse_args()
    # add_appointment(args.start_time, args.days, args.id, args.store_id, args.subject)
    heart_girl(args.appointed_time, args.days)


if __name__ == "__main__":
    # now = time.strftime("%H:%M:%S")
    # while now != "19:11:11":
    #     now = time.strftime("%H:%M:%S")
    #     time.sleep(0.5)
    #     print(f"没到时间: {now}")
    # else:
    #     print(f"到时间了: {now}")
    #     for i in range(5):
    #         time.sleep(0.5)
    main()
    # res = get_emulator_time_list(StoreId=10, days=2)
    # print(res)
    # appointed_time = str(datetime.date.today() + datetime.timedelta(days=2))
    # print(appointed_time)
    # res = one_day_schedule(StoreId=25, days=1)
    # for _ in res:
    #     for x in _:
    #         print(x)
    # print(res)
    # cancel_appointment(111015)
    # res = my_schedule()
    # print(res)
    # heart_girl()
    # get_student_data()