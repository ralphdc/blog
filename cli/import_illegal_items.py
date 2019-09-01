#!/usr/bin/env python3


from config import Config
from app.utils import *
import os


class import_illegal_items():


    _file = None

    _local_file_path = Config().LOCAL_FILE_PATH

    _file_path = None

    def __init__(self, **kwargs):

        self._file = kwargs.get('fname')

        if not self._file:
            raise Exception("[Error] - 未知的解析文件！")

        self._file_path = self._local_file_path + '/' + self._file

        if not os.path.isfile(self._file_path):
            raise Exception("[Error] - 解析文件不存在！")

    def run(self):

        print("Begin to parse file...")

        with open(self._file_path, encoding='UTF-8') as f:
            for fline in f:
                fline = fline.strip()
                if fline:
                    check_sql = "SELECT `item_id` FROM `cli_illegal_items` WHERE `item_content`=%s"
                    fetch_one = mysql_fetch_one(check_sql, (fline))
                    if fetch_one and fetch_one.get('item_id'):
                        print("[INFO] - {} existed! - passed".format(fline))
                    else:
                        insert_sql = "INSERT INTO `cli_illegal_items`(`item_content`) VALUES(%s)"
                        rt = mysql_execute(insert_sql, (fline))
                        if rt > 0:
                            print("[SUCCESS] - {} - OK!".format(fline))
                        else:
                            print("[ERROR] - {} - failed!".format(fline))
                else:
                    print("[Warning] - fline is empty, passed!")


        print("[INFO] - insert table finished------------------")


