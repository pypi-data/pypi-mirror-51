# Winney 面向对象的 HTTP 请求  

## Tutorial
``` python
wy = Winney(host="www.baidu.com")
wy.add_url(method="get", uri="/", function_name="download")
wy.download()
t = wy.get_bytes()
print(t)
```

## The Best Practice
``` python
from winney import Winney

from config import ZEUS_HOST, ZEUS_PORT, APP_TYPE, ZEUS_TOKEN_HEADER, ZEUS_TOKEN_VALUE


class Zeus(object):
    def __init__(self, host, port):
        self.winney = Winney(host=host, port=port, headers={ZEUS_TOKEN_HEADER: ZEUS_TOKEN_VALUE})
        self.init_functions()
    
    def init_functions(self):
        self.winney.add_url(method="get", uri="/zeus/app_types/",           function_name="get_types")
        self.winney.add_url(method="get", uri="/zeus/app_types/{type_id}",  function_name="get_type")
        self.winney.add_url(method="get", uri="/zeus/accounts/{user_id}",   function_name="get_user_info")
        self.winney.add_url(method="get", uri="/zeus/application/{app_id}", function_name="get_app_info")
        self.winney.add_url(method="get", uri="/zeus/applications/",        function_name="get_apps")
    
    def get_data(self, r):
        if not r.ok():
            return None
        data = r.get_json()
        if data["code"] != 0:
            print("Failed to get zeus data, response = ", data)
            return None
        return data["data"]
    
    def get_apps(self, user_id):
        r = self.winney.get_apps(headers={"Authorization": "Token {}".format(user_id)}, user_id=user_id)
        return self.get_data(r)

    def get_types(self):
        r = self.winney.get_types()
        return self.get_data(r)
    
    def get_type_by_id(self, type_id):
        r = self.winney.get_type(type_id=type_id)
        return self.get_data(r)
    
    def get_user_info(self, user_id):
        r = self.winney.get_user_info(user_id=user_id)
        return self.get_data(r)
    
    def get_app_info(self, app_id):
        r = self.winney.get_app_info(app_id=app_id)
        return self.get_data(r)


zeus = Zeus(host=ZEUS_HOST, port=ZEUS_PORT)
zeus.get_app_info("123456)

```