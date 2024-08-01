# Hello Frappe 

A hello world frappe application. 

## Background 

Basically on bench the idea of a site and of an app are decoupled. You can
create a site, create an app and add the add to the site. If you recreate the
site, it loses all the apps, but the app still remains - you just have to
re-add it to the site. 

And a `doctype` is basically a feature of an app. The models, UI and middleware
needed to handle getting user input, storing it in the db, and reading it back
to display as a list. 

## Quick start 

```
$ bench get-app https://github.com/frappe/press --init-bench
$ cd press-bench
$ bench new-site --admin-password admin test_site
$ bench --site test_site install-app press
$ bench --site test_site add-to-hosts 
$ bench --site test_site set-config allow_tests true
$ bench set-config -g developer_mode 1
$ bench start 
```

Now once you login (User: Administrator, password: your-db-admin-password) you
should be able to 
1. View the press doctypes when you search in the UI/awesomebar for Doctype listings
2. Call APIs
```
$ curl test_site:8000/api/method/press.www.dashboard.get_context_for_dev -X POST 
{"message":{"frappe_version":"16.0.0-dev","press_frontend_sentry_dsn":"","press_dashboard_sentry_dsn":"","press_frontend_posthog_host":"","press_frontend_posthog_project_id":"","press_site_name":null,"site_name":"test_site","default_team":null,"valid_teams":[],"is_system_user":false,"verify_cards_with_micro_charge":"No","free_credits_inr":"0","free_credits_usd":"0"}}
```
3. Update your site's `site_config.json` (in the bench dir, i.e `press-bench/sites/test_site/site-config.json` to `ignore_csrf`
```
{
 "allow_tests": true,
  ...
 "ignore_csrf": 1
}

````
This can also be done with 
```
$ bench --site test_site set-config ignore_csrf 1
```
4. Run the frontend 
```
$ cd ~/src/github.com/bprashanth/frappe/press/dashboard
$ source env/bin/activate
$ yarn run dev --host test_site
```
5. Navigate to `http://test_site:8000/dashboard`


## Prereqs


```
$ sudo apt-get update
$ pip3 install frappe-bench
$ sudo apt-get install redis-server mariadb-server
$ npm install --global yarn@1.22.22
$ bench init timor
$ sudo mysql_secure_installation
$ sudo apt-get install supervisor
```
and upate `/etc/mysql/my.cnf` [here](https://frappeframework.com/docs/user/en/installation)
```
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
```
And make sure you can login without `sudo` to mariadb
```
$ mysql -u root
```
If that doesn't work
```
$ sudo mysql 
MariaDB [(none)]> ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING '';
Query OK, 0 rows affected (0.005 sec)

MariaDB [(none)]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.000 sec)

MariaDB [(none)]> EXIT;
```
Now to write a Frappe app that can be deployed via Frappe Cloud, follow these steps.

## Installation 

### 1. Install Frappe Bench

First, install Frappe Bench:
```bash
$ pip install frappe-bench
$ bench init demo_frappe_bench
Installing frappe
$ /home/desinotorious/src/github.com/bprashanth/timor/demo_frappe_bench/env/bin/python -m pip install --quiet --upgrade -e /home/desinotorious/src/github.com/bprashanth/timor/demo_frappe_bench/apps/frappe 
...
SUCCESS: Bench demo_frappe_bench initialized
```
At this point you should see a default frappe app installed 
```
$ cd demo_frappe_bench/apps/frappe
```

### 2. Create a New Site

Create a new site for your app:
```bash
$ bench new-site timor.com --db-type mariadb --admin-password foo
```
Now you should see this site show up in the `demo_frappe_bench` dir with a `site-config.json` that has the relevant mariadb creds. 

"foo" is the password used to login to the site, where the default user name is `Administrator`.

To access this site you will need to edit `/etc/hosts`
```
$ bench --site timor.local add-to-hosts
$ bench set-config -g developer_mode 1
$ bench start
```
And navigate to `timor.local:8000` (`bench start` needs to be running for this to work).

### 3. Create a New App
Create a new app called "hello_world":
```bash
$ bench new-app hello_world
```

### 4. Install the App on Your Site
Install your app on the site:
```bash
$ bench --site timor.local install-app hello_world
$ bench --site timor.local list-apps

frappe
hello_world

```

### 5. Create a New DocType
Navigate to your app directory and create a new DocType:
```bash
cd apps/hello_world
bench make-doctype HelloWorld --module hello_world
```

### 6. Add Code to Display "Hello, World!"
In the `hello_world/hello_world/doctype/hello_world/hello_world.py` file:
```python
class HelloWorld(Document):
    def onload(self):
        frappe.msgprint("Hello, World!")
```

In the `hello_world/hello_world/doctype/hello_world/hello_world.json` file, define the fields for your DocType.

### 7. Create a Web Page
Create a new web page in `hello_world/www/index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Hello World</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
```

### 8. Deploy to Frappe Cloud
Ensure your app is in a GitHub repository. Then, use the Frappe Cloud interface to deploy your site, selecting the repository and branch containing your code.


### 9. Uninstall other apps 

* Remove all the preinstalled frappe doctypes 
```
$ bench --site timor.local uninstall-app frappe --dry-run
```

### Summary of Key Steps
1. **Install Frappe Bench:** Set up the development environment.
2. **Create a New Site and App:** Initialize a new site and app.
3. **Define a DocType:** Add a DocType to manage data models.
4. **Add Logic:** Implement business logic in the app.
5. **Create Web Pages:** Define static or dynamic web content.
6. **Deploy:** Push the code to GitHub and deploy via Frappe Cloud.

By following these steps, you will have a basic "Hello, World!" Frappe app ready for deployment.

## Frappe cloud architecture

```
server 1			server 2
-------				--------
frappecloud.com
	press -----------> agent -- bench 1
			      |- bench n
```
* Press is a frappe app 
* Dashboard is built with custom components 


## Appendix

* Frappe [press](https://github.com/frappe/press)
* Frappe [agent](https://github.com/frappe/agent)
* Create a site [docs](https://frappeframework.com/docs/user/en/tutorial/create-a-site)
* Running a test frappe app [docs](https://github.com/frappe/press/blob/master/guide-to-testing.md)

### API calls 

* "Let's setup account page" 
```
18:05:56 web.1         | 127.0.0.1 - - [27/Jul/2024 18:05:56] "POST /api/method/press.www.dashboard.get_context_for_dev HTTP/1.1" 417 -

```


### Backups 

```
$ bench --force --site timor.local restore ./sites/timor.local/private/backups/20240725_152942-timor_local-database.sql.gz
```


### Issues 

* bench uninstall-app looks for redis on port `11000` while `bench start` looks for it on the default 6000 whatever port 
* bench uninstall corrupts db so subsequent commands fail
```
  File "env/lib/python3.10/site-packages/pymysql/protocol.py", line 219, in raise_for_error
    err.raise_mysql_exception(self._data)
      self = <pymysql.protocol.MysqlPacket object at 0x722dbfd1dff0>
      errno = 1146
  File "env/lib/python3.10/site-packages/pymysql/err.py", line 150, in raise_mysql_exception
    raise errorclass(errno, errval)
      data = b"\xffz\x04#42S02Table '_3aff04b34e4b30d9.tabDefaultValue' doesn't exist"
      errno = 1146
      errval = "Table '_3aff04b34e4b30d9.tabDefaultValue' doesn't exist"
      errorclass = <class 'pymysql.err.ProgrammingError'>
pymysql.err.ProgrammingError: (1146, "Table '_3aff04b34e4b30d9.tabDefaultValue' doesn't exist")

```
* Why doesn't the `dry-run` uninstall cmd show this? 
* Why doesn't the `dry-run` uninstall cmd just restore from backup?
```
$ bench --version
5.22.6
```

## Logging sites 

```
18:21:45 web.1         | /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/env/lib/python3.10/site-packages/werkzeug/wrappers/request.py:190: DeprecationWarning: login: Sending `cmd` for RPC calls is deprecated, call REST API instead `/api/method/cmd`

```
* Callstack for a js -> python request 
```
18:29:30 web.1         | (Pdb)   /usr/lib/python3.10/threading.py(973)_bootstrap()
18:29:30 web.1         | -> self._bootstrap_inner()
18:29:30 web.1         |   /usr/lib/python3.10/threading.py(1016)_bootstrap_inner()
18:29:30 web.1         | -> self.run()
18:29:30 web.1         |   /usr/lib/python3.10/threading.py(953)run()
18:29:30 web.1         | -> self._target(*self._args, **self._kwargs)
18:29:30 web.1         |   /usr/lib/python3.10/socketserver.py(683)process_request_thread()
18:29:30 web.1         | -> self.finish_request(request, client_address)
18:29:30 web.1         |   /usr/lib/python3.10/socketserver.py(360)finish_request()
18:29:30 web.1         | -> self.RequestHandlerClass(request, client_address, self)
18:29:30 web.1         |   /usr/lib/python3.10/socketserver.py(747)__init__()
18:29:30 web.1         | -> self.handle()
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/env/lib/python3.10/site-packages/werkzeug/serving.py(391)handle()
18:29:30 web.1         | -> super().handle()
18:29:30 web.1         |   /usr/lib/python3.10/http/server.py(433)handle()
18:29:30 web.1         | -> self.handle_one_request()
18:29:30 web.1         |   /usr/lib/python3.10/http/server.py(421)handle_one_request()
18:29:30 web.1         | -> method()
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/env/lib/python3.10/site-packages/werkzeug/serving.py(363)run_wsgi()
18:29:30 web.1         | -> execute(self.server.app)
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/env/lib/python3.10/site-packages/werkzeug/serving.py(326)execute()
18:29:30 web.1         | -> for data in application_iter:
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/env/lib/python3.10/site-packages/werkzeug/debug/__init__.py(341)debug_application()
18:29:30 web.1         | -> app_iter = self.app(environ, start_response)
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/apps/frappe/frappe/middlewares.py(16)__call__()
18:29:30 web.1         | -> return super().__call__(environ, start_response)
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/env/lib/python3.10/site-packages/werkzeug/middleware/shared_data.py(249)__call__()
18:29:30 web.1         | -> return self.app(environ, start_response)
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/env/lib/python3.10/site-packages/werkzeug/middleware/shared_data.py(249)__call__()
18:29:30 web.1         | -> return self.app(environ, start_response)
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/apps/frappe/frappe/app.py(79)application()
18:29:30 web.1         | -> app(environ, start_response),
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/env/lib/python3.10/site-packages/werkzeug/wrappers/request.py(190)application()
18:29:30 web.1         | -> resp = f(*args[:-2] + (request,))
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/apps/frappe/frappe/app.py(114)application()
18:29:30 web.1         | -> response = frappe.api.handle(request)
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/apps/frappe/frappe/api/__init__.py(49)handle()
18:29:30 web.1         | -> data = endpoint(**arguments)
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/apps/frappe/frappe/api/v1.py(36)handle_rpc_call()
18:29:30 web.1         | -> return frappe.handler.handle()
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/apps/frappe/frappe/handler.py(49)handle()
18:29:30 web.1         | -> data = execute_cmd(cmd)
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/apps/frappe/frappe/handler.py(85)execute_cmd()
18:29:30 web.1         | -> return frappe.call(method, **frappe.form_dict)
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/apps/frappe/frappe/__init__.py(1814)call()
18:29:30 web.1         | -> return fn(*args, **newargs)
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/apps/frappe/frappe/utils/typing_validations.py(32)wrapper()
18:29:30 web.1         | -> return func(*args, **kwargs)
18:29:30 web.1         | > /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/apps/frappe/frappe/desk/page/setup_wizard/setup_wizard.py(329)load_user_details()
18:29:30 web.1         | -> "full_name": frappe.cache.hget("full_name", "signup"),
18:29:30 web.1         |   /home/desinotorious/src/github.com/bprashanth/frappe/press/press-bench/apps/frappe/frappe/utils/redis_wrapper.py(211)hget()
18:29:30 web.1         | -> def hget(self, name, key, generator=None, shared=False):

```
From logging in handler.py
```
18:45:13 web.1         | 127.0.0.1 - - [27/Jul/2024 18:45:13] "GET /api/method/frappe.desk.form.load.getdoc?doctype=Currency&name=INR&_=1722086112605 HTTP/1.1" 200 -
18:45:29 web.1         | =======================invoking frappe.call 
18:45:29 web.1         | <function load_user_details at 0x7ac66a7a6ef0>
18:45:29 web.1         | {'cmd': 'frappe.desk.page.setup_wizard.setup_wizard.load_user_details'}
18:45:29 web.1         | ========================finished invocation
```
