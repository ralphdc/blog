#!/usr/bin/env python3

import os
import hashlib
from datetime import timedelta

class Default():


    BLOG_NAME = '天涯飞鸿'

    BLOG_TITLE = '董超的个人博客'

    BLOG_KEYWORDS = '董超，平安科技，云计算，智能运维，php,python,redis,mysql,mariadb,keepalived,maxscale,运维开发，devops,aiops,zabbix,saltstack,tidb,docker,openstack,kubernetes'

    BLOG_CONTENT = '博主从事先后从事php中大型网站开发，python运维开发等工作，至今已有十年工作经验。欢迎广大网友留言，交流合作。'

    BLOG_HEADER = '我们都是普通人，努力工作只是为了更好的明天！'

    SECRET_KEY = hashlib.md5(os.urandom(24)).hexdigest()

    #设置session有效期；
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)


    BASICSET_COLLECTION = 'setting'

    FLASKY_POST_PER_PAGE = 10