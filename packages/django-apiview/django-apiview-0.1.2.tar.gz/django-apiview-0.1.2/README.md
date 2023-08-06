# django-apiview

Restful API view utils.


## Install

    pip install django-apiview


## Settings

    INSTALLED_APPS = [
        ......
        'apiview',
        ......
    ]


## Exports

- apiview.annotations
    - String
    - Integer
    - Boolean
    - Bytes

- apiview.views
    - apiview

- apiviews.utils
    - DjangoJsonEncoder


## Releases

### v0.1.2

- Fix, 修正form处理过程中的错误。

### v0.1.1

- apiview允许使用PAYLOAD的字段进行注入，但字段优先级较低。

### v0.1.0

- First release
