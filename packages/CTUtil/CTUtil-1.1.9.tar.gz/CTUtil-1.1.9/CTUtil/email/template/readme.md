### 邮件模块

```python3
# demo
from typing import List
from CTUtil.email import send_cingta_email, BaseEmail
from CTUtil.types import FuncCallBack

# your_word_dir/template/template.html

class YourEmail(BaseEmail):
    template = 'template.html'
    work_dir: str = 'your_work_dir' # default run project dir

# run you model
def run_your_model_emali():
    if send_cingta_email(
        title='email title',
        model=YourEmail,
        to_email=['example@email.com', 'example2@email.com'],
        ) == FunCallBack.SUCCESS:
        return '发送成功'
    else:
        return '发送失败'

def run_send_email():
    if send_cingta_email(
        title='email title',
        to_email=['example@email.com', 'example2@email.com'],
        ) == FunCallBack.SUCCESS:
        return '发送成功'
    else:
        return '发送失败'
```

#### args

| 参数            | 类型                     | 是否必须 | 详细                                                           |
| --------------- | ------------------------ | --------- | -------------------------------------------------------------- |
| title           | string                   | 是        | 邮件标题                                                       |
| to_email        | list                     | 是        | 发送邮件列表                                                   |
| model           | string/None              | 否        | 发送默认邮件类型模版, 可直接填自定义html文件路径,default=_NEED |
| msg             | string/None              | 否        | 发送邮件字符串,填写该参数正文为msg, 而不是html                 |
| from_eamil_name | string/default: 'cingta' | 否        | 发送邮件人姓名或其他                                          |
| html_string     | string                   | 否        | 发送html字符串, 若填写msg该项无效                            |
