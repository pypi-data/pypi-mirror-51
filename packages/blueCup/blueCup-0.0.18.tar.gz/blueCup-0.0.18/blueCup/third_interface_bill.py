import argparse
import re
from functools import partial
from typing import Mapping, Any, Callable

import pandas as pd
from blueCup.task_notification import send_dingding_markdown
from muzha.shuhemofang import network_triple_elements as shmf_network_triple_elements
from nezha.aliyun.uemail import Email
from nezha.file import File
from nezha.uexcel import to_excel
from nezha.umongo import insert_one, find, find_one
from nezha.utime import strftime
from nezha.utime import yesterday

from .celery import app

partial_yesterday = partial(yesterday, precision='day')


class NotErrorArgumentParser(argparse.ArgumentParser):

    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        return args


from celery.signals import task_failure

DB = 'third_interface'
COLLECTION = 'bill'
MONGO_HOST = '47.103.51.193'
MONGO_USERNAME = 'root'
parser = NotErrorArgumentParser()
parser.add_argument('--mongo_pwd')
parser.add_argument('--ding_robot')
args = parser.parse_args()
partial_insert_one = lambda x: x
partial_find = lambda x: x
if args.mongo_pwd and args.ding_robot:
    print('*' * 10, f'got option from cmdline {args.mongo_pwd} {args.ding_robot}', '*' * 50)
    MONGO_PWD = args.mongo_pwd
    R_BLADE = args.ding_robot
    _email_info = find_one({'block': 'default'},
                           'email_notification_config',
                           DB,
                           MONGO_HOST,
                           27017,
                           MONGO_USERNAME,
                           MONGO_PWD,
                           'admin')['email_info']
    EMAIL = Email(_email_info['mail_user'], _email_info['mail_pass'], _email_info['sender'])
    RECEIVERS = _email_info['receiver']
    partial_insert_one = partial(insert_one,
                                 db=DB,
                                 host=MONGO_HOST,
                                 port=27017,
                                 username=MONGO_USERNAME,
                                 password=MONGO_PWD,
                                 authSource='admin')

    partial_find = partial(find,
                           db=DB,
                           host=MONGO_HOST,
                           port=27017,
                           username=MONGO_USERNAME,
                           password=MONGO_PWD,
                           authSource='admin')


@app.task(name='bill_shuhemofang_network_triple_elements',
          bind=True, autoretry_for=(Exception,),
          retry_kwargs={'max_retries': 2, 'countdown': 0.5})
def bill_shuhemofang_network_triple_elements(self: Any,
                                             third_interface_name: str,
                                             boolean_order_id: str,
                                             supplier_order_id: str,
                                             supplier_response: Mapping,
                                             biz_data: Mapping,
                                             call_time: str = '',
                                             stored_func: Callable = partial_insert_one,
                                             supplier_uuid: str = 'shuhemofang',
                                             supplier_name: str = '数盒魔方',
                                             product_uuid: str = 'network_triple_elements',
                                             product_name: str = '运营商三要素') -> None:
    product_price = shmf_network_triple_elements.how_much_should_pay(supplier_response)
    supplier_status = True if product_price else False
    data = locals().copy()
    data['call_time'] = strftime()
    list(map(lambda x: data.pop(x), ('self', 'stored_func')))
    stored_func(data, COLLECTION)


@app.task(name='bill_someday_count',
          bind=True, autoretry_for=(Exception,),
          retry_kwargs={'max_retries': 2, 'countdown': 0.5})
def bill_someday_count(self: Any, someday: Callable = partial_yesterday):
    """
    :param self:
    :param someday: callable, result style like: 2019-08-18
    :return:
    """
    someday = someday()
    print('@' * 50, f'[bill_yesterday_count] self.task_id {self.request.id} umongo.yesterday {someday}')
    all_iter = partial_find({'call_time': re.compile(f'{someday}.*')}, 'bill')
    result = []
    for one_record in all_iter:
        if isinstance(one_record, dict):
            not_display_keys = {'_id', 'supplier_response', 'supplier_uuid', 'product_uuid', 'third_interface_name'}
            tuple(map(lambda key: one_record.get(key) and one_record.pop(key), not_display_keys))
            result.append(one_record)
        else:
            print(f'one_record {one_record} is unexpected')
    p_columns = {
        'boolean_order_id': '布尔订单号',
        'call_time': '调用时间',
        'product_name': '产品名称',
        'product_price': '产品单价',
        'supplier_name': '供应商名称',
        'supplier_order_id': '供应商订单号',
        'supplier_status': '状态',
    }
    p_header = ('布尔订单号', '供应商订单号', '供应商名称', '产品名称', '产品单价', '调用时间', '状态')
    df = pd.DataFrame(result, columns=p_columns)
    df.rename(columns=p_columns, inplace=True)
    xlsx = File.join_path(File.this_dir(__file__), f'{someday}.xlsx')
    to_excel(df, xlsx, columns=p_header)
    EMAIL.send_email_attach(f'{someday} 供应商调用统计', f'{strftime()} auto-sent', xlsx, RECEIVERS)


@task_failure.connect(sender=None)
def task_failure_handler(task_id=None, exception=None, traceback=None, einfo=None, *args, **kwargs):
    print(f'task_failure_handler catch exception {task_id} {exception}')
    template = f"""# 供应商对账系统告警
- **celery task_id:** {task_id}
- **异常：** {exception}
- **堆栈信息** {einfo}
- **参数信息**
- **args** {args}
- **kwargs** {kwargs}
"""
    send_dingding_markdown.apply_async(args=(
        R_BLADE, '供应商对账系统告警', template),
        queue='notification')
