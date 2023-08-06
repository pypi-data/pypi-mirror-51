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

### v0.1.3

- Add logging while getting result failed in @apiview.
- Add Map, List annotations.

### v0.1.2

- Fix form process problem.

### v0.1.1

- Add PAYLOAD injection, PAYLOAD field has low priority.

### v0.1.0

- First release,
