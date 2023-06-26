# 高考志愿填报系统flask后端

## 1、创建项目，构建mvc基本框架

![image-20230305213404728](C:\Users\13939\AppData\Roaming\Typora\typora-user-images\image-20230305213404728.png)

## 2、后台账户模块

### 2.1、认证功能

![image-20230306162426524](C:\Users\13939\AppData\Roaming\Typora\typora-user-images\image-20230306162426524.png)

------

#### 用户登录

1. `web/controller`下创建`User.py`并注册

   >`User`是仪表盘页面对当前登录用户进行编辑，查看，登出，登录操作的文件

2. 创建管理员数据表

   ![image-20230305230941787](C:\Users\13939\AppData\Roaming\Typora\typora-user-images\image-20230305230941787.png)

   ```sql
   CREATE TABLE `user` (
     `uid` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户uid',
     `nickname` varchar(100) NOT NULL DEFAULT '' COMMENT '用户名',
     `mobile` varchar(20) NOT NULL DEFAULT '' COMMENT '手机号码',
     `email` varchar(100) NOT NULL DEFAULT '' COMMENT '邮箱地址',
     `sex` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1：男 2：女 0：没填写',
     `avatar` varchar(64) NOT NULL DEFAULT '' COMMENT '头像',
     `login_name` varchar(20) NOT NULL DEFAULT '' COMMENT '登录用户名',
     `login_pwd` varchar(32) NOT NULL DEFAULT '' COMMENT '登录密码',
     `login_salt` varchar(32) NOT NULL DEFAULT '' COMMENT '登录密码的随机加密秘钥',
     `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1：有效 0：无效',
     `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
     `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
     PRIMARY KEY (`uid`),
     UNIQUE KEY `login_name` (`login_name`)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表（管理员）';
   ```

3. 创建`User` `model`模型

   ```bash
   flask-sqlacodegen "mysql://root:123456@127.0.0.1/user" --table user --outfile "common/models/User.py" --flask
   ```

   

4. 登录功能

   - 后端

     ```python
     @route_user.route("/login", methods=["GET", "POST"])
     def login():
         # 获取页面
         if request.method == "GET":
             return ops_render("user/login.html")
     
         # 登录
         resp = {'code': 200, 'msg': '登陆成功', 'data': {}}
         req = request.values
         login_name = req['login_name'] if 'login_name' in req else ''
         login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
     
         if login_name is None or len(login_name) < 1:
             resp['code'] = -1
             resp['msg'] = '请输入正确的用户名'
             return jsonify(resp)
     
         if login_pwd is None or len(login_pwd) < 1:
             resp['code'] = -1
             resp['msg'] = '请输入正确的密码'
             return jsonify(resp)
     
         user_info = User.query.filter_by(login_name=login_name).first()
         if not user_info:
             resp['code'] = -1
             resp['msg'] = '请输入正确的用户登陆名和密码'
             return jsonify(resp)
     
         if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
             resp['code'] = -1
             resp['msg'] = '请输入正确的用户登陆名和密码 -2'
             return jsonify(resp)
     
         if user_info.status != 1:
             resp['code'] = -1
             resp['msg'] = '账号已被禁用，请联系管理员'
             return jsonify(resp)
     
         response = make_response(json.dumps(resp))
         response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))
     
         return response
     ```

     

   - 前端模板文件`user/index.html`

     ```html
     {% extends "common/layout_user.html" %}
     {% block content %}
         <div class="loginColumns animated fadeInDown">
             <div class="row">
                 <div class="col-md-6 text-center">
                     <h3 class="font-bold">{{ config.SEO_TITLE }}</h3>
                     <div class="row">
                         <div class="col-xs-6 col-md-6">
                             <a href="javascript:void(0);" class="thumbnail">
                                 <img src="{{ buildStaticUrl('/images/common/mini_qrcode.jpg') }}" width="200px">
                             </a>
                             <p>小程序码</p>
                         </div>
                         <div class="col-xs-6 col-md-6">
                             <a href="javascript:void(0);" class="thumbnail">
                                 <img src="{{ buildStaticUrl('/images/common/qrcode.jpg') }}" width="200px">
                             </a>
                             <p>公众号码</p>
                         </div>
                     </div>
     
                 </div>
                 <div class="col-md-6">
                     <div class="ibox-content">
                         <div class="m-t login_wrap">
                             <div class="form-group text-center">
                                 <h2 class="font-bold">登录</h2>
                             </div>
                             <div class="form-group">
                                 <input type="text" name="login_name" class="form-control" placeholder="请输入登录用户名">
                             </div>
                             <div class="form-group">
                                 <input type="password" name="login_pwd" class="form-control" placeholder="请输入登录密码">
                             </div>
                             <button type="button" class="btn btn-primary block full-width m-b do-login">登录</button>
                             <h3>账号和密码请关注左侧公众号码 回复"<span class="text-danger">订餐小程序</span>"获取，每日更新一次 </h3>
                         </div>
                     </div>
                 </div>
             </div>
             <hr>
             <div class="row">
                 <div class="col-md-6">
                     {{ config.SEO_TITLE }} <a href="{{ buildUrl('/') }}" target="_blank"> 技术支持 </a>
                 </div>
                 <div class="col-md-6 text-right">
                     <small>© 2018</small>
                 </div>
             </div>
         </div>
     {% endblock %}
     {% block js %}
         <script src="{{ buildStaticUrl('/js/user/login.js') }}"></script>
     {% endblock %}
     ```

   - 登录`js`文件`user/login.js`

     ```javascript
     ;
     var user_login_ops = {
         init: function () {
             this.eventBind();
         },
         eventBind: function () {
             $(".login_wrap .do-login").click(function () {
                 var btn_target = $(this);
                 if (btn_target.hasClass("disabled")) {
                     common_ops.alert("正在处理!!请不要重复提交~~");
                     return;
                 }
     
                 var login_name = $(".login_wrap input[name=login_name]").val();
                 var login_pwd = $(".login_wrap input[name=login_pwd]").val();
     
                 if (login_name == undefined || login_name.length < 1) {
                     common_ops.alert("请输入正确的登录用户名~~");
                     return;
                 }
                 if (login_pwd == undefined || login_pwd.length < 1) {
                     common_ops.alert("请输入正确的密码~~");
                     return;
                 }
                 btn_target.addClass("disabled");
                 $.ajax({
                     url: common_ops.buildUrl("/user/login"),
                     type: 'POST',
                     data: {'login_name': login_name, 'login_pwd': login_pwd},
                     dataType: 'json',
                     success: function (res) {
                         btn_target.removeClass("disabled");
                         var callback = null;
                         if (res.code == 200) {
                             callback = function () {
                                 window.location.href = common_ops.buildUrl("/");
                             }
                         }
                         common_ops.alert(res.msg, callback);
                     },
                     error: function (error) {
                         btn_target.removeClass("disabled");
                         var callback = null;
                         if (res.code == -1) {
                             callback = function () {
                                 window.location.href = window.location.href;
                             }
                         }
                         common_ops.alert(error.msg, callback);
                     }
                 });
             });
         }
     };
     
     $(document).ready(function () {
         user_login_ops.init();
     });
     ```

5. 新建拦截器判断是否已登陆

   - `interceptors/AuthInterceptors`

     ```python
     from flask import request, redirect, g
     import re
     
     from application import app
     from config.User import User
     from common.libs.user.UserService import UserService
     from common.libs.UrlManager import UrlManager
     # from common.libs.LogService import LogService
     
     
     @app.before_request
     def before_request():
         """
         检测登录拦截器
         :return: 继续请求
         """
         ignore_urls = app.config['IGNORE_URLS']
         ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
     
         path = request.path
     
         # 排除不需要检测的请求（登陆页面请求、api请求）
         pattern = re.compile("%s" % "|".join(ignore_check_login_urls))
         if pattern.match(path):
             return
     
         # 排除不需要检测的请求（静态资源请求、api请求）
         pattern = re.compile("%s" % "|".join(ignore_urls))
         if pattern.match(path):
             return
     
         if "/api" in path:
             return
     
         user_info = check_login()
     
         g.current_user = None
     
         if not user_info:
             return redirect(UrlManager.buildUrl("/user/login"))
         else:
             g.current_user = user_info
     
         # 添加日志
         # LogService.addAccessLog()
         return
     
     
     def check_login():
         """
         检查是否登录
         :return: 已登陆：当前登录对象，未登录：false
         """
         cookies = request.cookies
         auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None
         if auth_cookie is None:
             return False
     
         # auth_cookie： AuthCode#uid
         auth_info = auth_cookie.split("#")
         if (len(auth_info)) != 2:
             return False
     
         try:
             user_info = User.query.filter_by(uid=auth_info[1]).first()
         except Exception:
             return False
     
         if user_info is None:
             return False
     
         if auth_info[0] != UserService.geneAuthCode(user_info):
             return False
     
         if user_info.status != 1:
             return False
     
         return user_info
     ```

   - `base_config`

     ```python
     # 过滤url认证拦截
     IGNORE_URLS = [
         "^/user/login",
         "/api"
     ]
     
     IGNORE_CHECK_LOGIN_URLS = [
         "^/static",
         "^/favicon.ico",
         "^/api"
     ]
     ```

   - `www.py`注册拦截器

     ```python
     from web.interceptors.Authinterceptor import *
     ```

------

#### 用户登出

1. `controller`中注册方法

   ```python
   @route_user.route("/logout")
   def logout():
       response = make_response(redirect(UrlManager.buildUrl('/user/login')))
       response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
       # 删除了cookie之后，拦截器判断为未登录状态，则返回登陆页
       return response
   ```

------

#### 编辑信息

1. `controller`中注册方法

   ```python
   @route_user.route("/edit", methods=["GET", "POST"])
   def edit():
       # 获取页面
       if request.method == 'GET':
           return ops_render("user/edit.html", {'current': 'edit'})
   
       # 提交修改信息
       resp = {'code': 200, 'msg': '用户信息修改成功', 'data': {}}
       req = request.values
       nickname = req['nickname'] if 'nickname' in req else ''
       email = req['email'] if 'email' in req else ''
   
       if nickname is None or len(nickname) < 1:
           resp['code'] = -1
           return jsonify(resp)
   
       if email is None or len(email) < 1:
           resp['code'] = -1
           return jsonify(resp)
   
       user_info = g.current_user
       user_info.nickname = nickname
       user_info.email = email
       user_info.updated_time = getCurrentDate()
   
       db.session.add(user_info)
       db.session.commit()
       return jsonify(resp)
   ```

2. `user/edit.html`页面

   ```html
   {% extends "common/layout_main.html" %}
   {% block content %}
       {% include "common/tab_user.html" %}
       <div class="row m-t  user_edit_wrap">
           <div class="col-lg-12">
               <h2 class="text-center">账号信息编辑</h2>
               <div class="form-horizontal m-t m-b">
                   <div class="form-group">
                       <label class="col-lg-2 control-label">手机:</label>
                       <div class="col-lg-10">
                           <input type="text" name="mobile" class="form-control" placeholder="请输入手机~~" readonly=""
                                  value="{{ current_user.mobile }}">
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
   
                   <div class="form-group">
                       <label class="col-lg-2 control-label">姓名:</label>
                       <div class="col-lg-10">
                           <input type="text" name="nickname" class="form-control" placeholder="请输入姓名~~"
                                  value="{{ current_user.nickname }}">
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
   
                   <div class="form-group">
                       <label class="col-lg-2 control-label">邮箱:</label>
                       <div class="col-lg-10">
                           <input type="text" name="email" class="form-control" placeholder="请输入邮箱~~"
                                  value="{{ current_user.email }}">
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
                   <div class="form-group">
                       <div class="col-lg-4 col-lg-offset-2">
                           <button class="btn btn-w-m btn-outline btn-primary save">保存</button>
                       </div>
                   </div>
               </div>
           </div>
       </div>
   {% endblock %}
   {% block js %}
       <script src="{{ buildStaticUrl('/js/user/edit.js') }}"></script>
   {% endblock %}
   ```

3. 页面对应`javascript`文件

   ```javascript
   ;
   var user_edit_ops = {
       init: function () {
           this.eventBind();
       },
       eventBind: function () {
           $(".user_edit_wrap .save").click(function () {
               var btn_target = $(this);
               if (btn_target.hasClass("disabled")) {
                   common_ops.alert("正在处理!!请不要重复提交~~");
                   return;
               }
   
               var nickname_target = $(".user_edit_wrap input[name=nickname]");
               var nickname = nickname_target.val()
   
               var email_target = $(".user_edit_wrap input[name=email]");
               var email = email_target.val()
   
               if (!nickname || nickname.length < 2) {
                   common_ops.tip("请输入符合规范的姓名", nickname_target);
               }
   
               if (!email || email.length < 2) {
                   common_ops.tip("请输入符合规范的姓名", email_target);
               }
   
               btn_target.addClass('disabled');
   
               var data = {
                   nickname: nickname,
                   email: email
               }
   
               $.ajax({
                   url: common_ops.buildUrl("/user/edit"),
                   type: 'POST',
                   data: data,
                   dataType: 'json',
                   success: function (res) {
                       btn_target.removeClass("disabled");
                       var callback = null;
                       if (res.code == 200) {
                           callback = function () {
                               window.location.href = window.location.href;
                           }
                       }
                       common_ops.alert(res.msg, callback);
                   },
                   error: function (error) {
                       btn_target.removeClass("disabled");
                       var callback = null;
                       if (res.code == -1) {
                           callback = function () {
                               window.location.href = window.location.href;
                           }
                       }
                       common_ops.alert(res.msg, callback);
                   }
               })
   
           });
       }
   };
   
   $(document).ready(function () {
       user_edit_ops.init();
   })
   ```

------

#### 修改密码

1. `controller`中注册方法

   ```python
   @route_user.route("/reset-pwd", methods=["GET", "POST"])
   def resetPwd():
       if request.method == 'GET':
           return ops_render("user/reset_pwd.html", {'current': 'reset-pwd'})
   
       resp = {'code': 200, 'msg': '密码修改成功', 'data': {}}
       req = request.values
       old_password = req['old_password'] if 'old_password' in req else ''
       new_password = req['new_password'] if 'new_password' in req else ''
   
       if old_password is None or len(old_password) < 1:
           resp['code'] = -1
           resp['msg'] = "请输入符合规范的原密码"
           return jsonify(resp)
   
       if new_password is None or len(new_password) < 1:
           resp['code'] = -1
           resp['msg'] = "请输入符合规范的新密码"
           return jsonify(resp)
   
       if new_password == old_password:
           resp['code'] = -1
           resp['msg'] = "新密码不应与原密码相同"
           return jsonify(resp)
   
       user_info = g.current_user
   
       if UserService.genePwd(old_password, user_info.login_salt) != user_info.login_pwd:
           resp['code'] = -1
           resp['msg'] = "原密码输入错误"
           return jsonify(resp)
   
       user_info.login_pwd = UserService.genePwd(new_password, user_info.login_salt)
       user_info.updated_time = getCurrentDate()
   
       db.session.add(user_info)
       db.session.commit()
   
       response = make_response(json.dumps(resp))
       response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))
       return response
   ```

2. `user/edit.html`页面

   ```html
   {% extends "common/layout_main.html" %}
   {% block content %}
       {% include "common/tab_user.html" %}
       <div class="row m-t  user_reset_pwd_wrap">
           <div class="col-lg-12">
               <h2 class="text-center">修改密码</h2>
               <div class="form-horizontal m-t m-b">
                   <div class="form-group">
                       <label class="col-lg-2 control-label">账号:</label>
                       <div class="col-lg-10">
                           <label class="control-label">{{ current_user.nickname }}</label>
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
                   <div class="form-group">
                       <label class="col-lg-2 control-label">手机:</label>
                       <div class="col-lg-10">
                           <label class="control-label">{{ current_user.mobile }}</label>
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
   
                   <div class="form-group">
                       <label class="col-lg-2 control-label">原密码:</label>
                       <div class="col-lg-10">
                           <input type="password" id="old_password" class="form-control" value="">
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
   
                   <div class="form-group">
                       <label class="col-lg-2 control-label">新密码:</label>
                       <div class="col-lg-10">
                           <input type="password" id="new_password" class="form-control" value="">
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
                   <div class="form-group">
                       <div class="col-lg-4 col-lg-offset-2">
                           <button class="btn btn-w-m btn-outline btn-primary" id="save">保存</button>
                       </div>
                   </div>
               </div>
           </div>
       </div>
   {% endblock %}
   {% block js %}
       <script src="{{ buildStaticUrl('/js/user/reset_pwd.js') }}"></script>
   {% endblock %}
   ```

3. 页面对应`javascript`文件

   ```javascript
   ;
   var user_reset_pwd_ops = {
       init: function () {
           this.eventBind();
       },
       eventBind: function () {
           $("#save").click(function () {
               var btn_target = $(this);
               if (btn_target.hasClass("disabled")) {
                   common_ops.alert("正在处理!!请不要重复提交~~");
                   return;
               }
   
               var old_password_target = $("#old_password");
               var old_password = old_password_target.val();
   
               var new_password_target = $("#new_password");
               var new_password = new_password_target.val();
   
               if (!old_password || old_password.length < 2) {
                   common_ops.tip("请输入原密码", old_password_target);
               }
   
               if (!new_password || new_password.length < 2) {
                   common_ops.tip("请输入新密码", new_password_target);
               }
   
               btn_target.addClass('disabled');
   
               var data = {
                   old_password: old_password,
                   new_password: new_password
               }
   
               $.ajax({
                   url: common_ops.buildUrl("/user/reset-pwd"),
                   type: 'POST',
                   data: data,
                   dataType: 'json',
                   success: function (res) {
                       btn_target.removeClass("disabled");
                       var callback = null;
                       if (res.code == 200) {
                           callback = function () {
                               window.location.href = window.location.href;
                           }
                       }
                       common_ops.alert(res.msg, callback);
                   },
                   error: function (error) {
                       btn_target.removeClass("disabled");
                       var callback = null;
                       if (res.code == -1) {
                           callback = function () {
                               window.location.href = window.location.href;
                           }
                       }
                       common_ops.alert(error.msg, callback);
                   }
               })
   
           });
       }
   };
   
   $(document).ready(function () {
       user_reset_pwd_ops.init();
   })
   ```

------

### 2.2、账户管理

#### 用户操作日志功能

1. 创建用户操作日志表

- `app_access_log`

  ![image-20230306161556629](C:\Users\13939\AppData\Roaming\Typora\typora-user-images\image-20230306161556629.png)

  ```sql
  CREATE TABLE `member` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `nickname` varchar(100) NOT NULL DEFAULT '' COMMENT '会员名',
    `mobile` varchar(11) NOT NULL DEFAULT '' COMMENT '会员手机号码',
    `sex` tinyint(1) NOT NULL DEFAULT '0' COMMENT '性别 1：男 2：女',
    `avatar` varchar(200) NOT NULL DEFAULT '' COMMENT '会员头像',
    `salt` varchar(32) NOT NULL DEFAULT '' COMMENT '随机salt',
    `reg_ip` varchar(100) NOT NULL DEFAULT '' COMMENT '注册ip',
    `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1：有效 0：无效',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
    PRIMARY KEY (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员表';
  ```

- `app_error_log`

  ![image-20230306161620874](C:\Users\13939\AppData\Roaming\Typora\typora-user-images\image-20230306161620874.png)

  ```sql
  CREATE TABLE `app_error_log` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `referer_url` varchar(255) NOT NULL DEFAULT '' COMMENT '当前访问的refer',
    `target_url` varchar(255) NOT NULL DEFAULT '' COMMENT '访问的url',
    `query_params` text NOT NULL COMMENT 'get和post参数',
    `content` longtext NOT NULL COMMENT '日志内容',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
    PRIMARY KEY (`id`)
  ) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COMMENT='app错误日表';
  ```

2. 创建`LogService`操作`model`

- ```python
  class LogService:
      @staticmethod
      def addAccessLog():
          target = AppAccessLog()
          target.target_url = request.url
          target.refer_url = request.referrer
          target.ip = request.remote_addr
          target.query_params = json.dumps(request.values.to_dict())
          if 'current_user' in g and g.current_user is not None:
              target.uid = g.current_user.uid
          target.ua = request.headers.get("User-Agent")
          target.created_time = getCurrentDate()
          db.session.add(target)
          db.session.commit()
          return True
  
      @staticmethod
      def addErrorLog(error):
          target = AppErrorLog()
          target.target_url = request.url
          target.refer_url = request.referrer
          target.query_params = json.dumps(request.values.to_dict())
          target.content = error
          target.created_time = getCurrentDate()
          db.session.add(target)
          db.session.commit()
          return True
  ```

3. 在认证拦截器中加入添加日志功能

- ```python
  @app.before_request
  def before_request():
      """
      检测登录拦截器
      :return: 继续请求
      """
      ignore_urls = app.config['IGNORE_URLS']
      ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
  
      path = request.path
  
      # 排除不需要检测的请求（登陆页面请求、api请求）
      pattern = re.compile("%s" % "|".join(ignore_check_login_urls))
      if pattern.match(path):
          return
  
      # 排除不需要检测的请求（静态资源请求、api请求）
      pattern = re.compile("%s" % "|".join(ignore_urls))
      if pattern.match(path):
          return
  
      if "/api" in path:
          return
  
      user_info = check_login()
  
      g.current_user = None
  
      if not user_info:
          return redirect(UrlManager.buildUrl("/user/login"))
      else:
          g.current_user = user_info
  
      # 添加日志
      LogService.addAccessLog()
      return
  ```

------

#### 分页

1. 在配置文件中加入分页的参数设置

   ```python
   # 分页
   PAGE_SIZE = 5
   PAGE_DISPLAY = 10
   
   # 分类字段
   STATUS_MAPPING = {
       "1": "正常",
       "0": "已删除"
   }
   ```

2. 在`libs/Helper.py`文件中加入分页

   ```python
   def iPagination(params):
       """
       自定义分页
       :param params:
       :return:
       """
       import math
   
       ret = {
           "is_prev": 1,
           "is_next": 1,
           "from": 0,
           "end": 0,
           "current": 0,
           "total_pages": 0,
           "page_size": 0,
           "total": 0,
           "url": params['url']
       }
   
       total = int(params['total'])
       page_size = int(params['page_size'])
       page = int(params['page'])
       display = int(params['display'])
       total_pages = int(math.ceil(total / page_size))
       total_pages = total_pages if total_pages > 0 else 1
       if page <= 1:
           ret['is_prev'] = 0
   
       if page >= total_pages:
           ret['is_next'] = 0
   
       semi = int(math.ceil(display / 2))
   
       if page - semi > 0:
           ret['from'] = page - semi
       else:
           ret['from'] = 1
   
       if page + semi <= total_pages:
           ret['end'] = page + semi
       else:
           ret['end'] = total_pages
   
       ret['current'] = page
       ret['total_pages'] = total_pages
       ret['page_size'] = page_size
       ret['total'] = total
       ret['range'] = range(ret['from'], ret['end'] + 1)
       return ret
   ```

______

#### 账户首页

1. `Account/index.html`

   ```python
   {% extends "common/layout_main.html" %}
   {% block content %}
       {% include "common/tab_account.html" %}
       <div class="row">
           <div class="col-lg-12">
               <form class="form-inline wrap_search">
                   <div class="row m-t p-w-m">
                       <div class="form-group">
                           <select name="status" class="form-control inline">
                               <option value="-1">请选择状态</option>
                               {% for value in status_mapping %}
                                   <option value="{{ value }}" {% if value == search_con['status'] %}
                                           selected {% endif %}>{{ status_mapping[value] }}</option>
                               {% endfor %}
                           </select>
                       </div>
   
                       <div class="form-group">
                           <div class="input-group">
                               <input type="text" name="mix_kw" placeholder="请输入姓名或者手机号码" class="form-control"
                                      value="{{ search_con['mix_kw'] }}">
                               <input type="hidden" name="p" value="{{ search_con['p'] }}">
                               <span class="input-group-btn">
                               <button type="button" class="btn btn-primary search">
                                   <i class="fa fa-search"></i>搜索
                               </button>
                           </span>
                           </div>
                       </div>
                   </div>
                   <hr>
                   <div class="row">
                       <div class="col-lg-12">
                           <a class="btn btn-w-m btn-outline btn-primary pull-right"
                              href="{{ buildUrl('/account/set') }}">
                               <i class="fa fa-plus"></i>账号
                           </a>
                       </div>
                   </div>
               </form>
               <table class="table table-bordered m-t">
                   <thead>
                   <tr>
                       <th>序号</th>
                       <th>姓名</th>
                       <th>手机</th>
                       <th>邮箱</th>
                       <th>操作</th>
                   </tr>
                   </thead>
                   <tbody>
                   {% if list %}
                       {% for item in list %}
                           <tr>
                               <td>{{ item.uid }}</td>
                               <td>{{ item.nickname }}</td>
                               <td>{{ item.mobile }}</td>
                               <td>{{ item.email }}</td>
                               <td>
                                   <a href="{{ buildUrl('/account/info') }}?id={{ item.uid }}">
                                       <i class="fa fa-eye fa-lg"></i>
                                   </a>
                                   {% if item.status==1 %}
                                       <a class="m-l" href="{{ buildUrl('/account/set') }}?id={{ item.uid }}">
                                           <i class="fa fa-edit fa-lg"></i>
                                       </a>
   
                                       <a class="m-l remove" href="javascript:void(0);" data="{{ item.uid }}">
                                           <i class="fa fa-trash fa-lg"></i>
                                       </a>
                                   {% else %}
                                       <a class="m-l recover" href="javascript:void(0);" data="{{ item.uid }}">
                                           <i class=" fa fa-rotate-left fa-lg"></i>
                                       </a>
                                   {% endif %}
                               </td>
                           </tr>
                       {% endfor %}
                   {% else %}
                       <tr>
                           <td colspan="5">暂无数据~</td>
                       </tr>
                   {% endif %}
                   </tbody>
               </table>
   
               <!--分页代码已被封装到统一模板文件中-->
               {% include "common/pagenation.html" %}
           </div>
       </div>
   {% endblock %}
   {% block js %}
       <script src="{{ buildStaticUrl('/js/account/index.js') }}"></script>
   {% endblock %}
   ```

2. `account/index.js`

   ```javascript
   ;
   var account_index_ops = {
       init: function () {
           this.eventBind()
       },
       eventBind: function () {
           var that = this;
           $(".wrap_search .search").click(function () {
               $(".wrap_search").submit();
           });
   
           $(".remove").click(function () {
               that.ops("remove", $(this).attr("data"));
           });
   
           $(".recover").click(function () {
               that.ops("recover", $(this).attr("data"));
           });
       },
       ops: function (act, id) {
           var callback = {
               'ok': function () {
                   $.ajax({
                       url: common_ops.buildUrl("/account/ops"),
                       type: 'POST',
                       data: {
                           act: act,
                           id: id
                       },
                       dataType: 'json',
                       success: function (res) {
                           var callback = null;
                           if (res.code == 200) {
                               callback = function () {
                                   window.location.href = window.location.href;
                               }
                           }
                           common_ops.alert(res.msg, callback);
                       },
                       error: function (error) {
                           var callback = null;
                           if (res.code == -1) {
                               callback = function () {
                                   window.location.href = window.location.href;
                               }
                           }
                           common_ops.alert(error.msg, callback);
                       }
                   });
               },
               'cancel': function () {
                   window.location.href = window.location.href;
               }
           };
           common_ops.confirm((act == "remove" ? "确定删除该数据" : "确定恢复该数据"), callback)
       }
   };
   
   $(document).ready(function () {
       account_index_ops.init()
   });
   ```

3. 后端代码

   ```python
   @route_account.route("/index")
   def index():
       resp_data = {}
       query = User.query
       req = request.values
       page = int(req['p']) if ('p' in req and req['p']) else 1
   
       # 搜索功能
       if 'mix_kw' in req:
           rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])),
                      User.mobile.ilike("%{0}%".format(req['mix_kw'])))
           query = query.filter(rule)
   
       if 'status' in req and int(req['status']) > -1:
           query = query.filter(User.status == req['status'])
   
       # 分页功能
       page_params = {
           'total': query.count(),
           'page_size': app.config['PAGE_SIZE'],
           'page': page,
           'display': app.config['PAGE_DISPLAY'],
           'url': request.full_path.replace("&p={}".format(page), "")
       }
       pages = iPagination(page_params)
       offset = (page - 1) * app.config['PAGE_SIZE']
       limit = app.config['PAGE_SIZE'] * page
   
       list = query.order_by(User.uid.desc()).all()[offset:limit]
       resp_data['list'] = list
       resp_data['pages'] = pages
       resp_data['search_con'] = req
       resp_data['status_mapping'] = app.config['STATUS_MAPPING']
   
       return ops_render("account/index.html", resp_data)
   ```

------

#### 账户详细信息

1. `info.html`

   ```html
   {% extends "common/layout_main.html" %}
   {% block content %}
       {% include "common/tab_account.html" %}
       <div class="row m-t">
           <div class="col-lg-12">
               <div class="row">
                   <div class="col-lg-12">
                       <div class="m-b-md">
                           <a class="btn btn-outline btn-primary pull-right"
                              href="{{ buildUrl('/account/set') }}?id={{ info.uid }}">
                               <i class="fa fa-pencil"></i>编辑
                           </a>
                           <h2>账户信息</h2>
                       </div>
                   </div>
               </div>
               <div class="row">
                   <div class="col-lg-2 text-center">
                       <img class="img-circle circle-border" src="{{ buildStaticUrl('/images/common/avatar.png') }}"
                            width="100px" height="100px">
                   </div>
                   <div class="col-lg-10">
                       <p class="m-t">姓名：{{ info.nickname }}</p>
                       <p>手机：{{ info.mobile }}</p>
                       <p>邮箱：{{ info.email }}</p>
                   </div>
               </div>
               <div class="row m-t">
                   <div class="col-lg-12">
                       <div class="panel blank-panel">
                           <div class="panel-heading">
                               <div class="panel-options">
                                   <ul class="nav nav-tabs">
                                       <li class="active">
                                           <a href="javascript:void(0);" data-toggle="tab" aria-expanded="false">访问记录</a>
                                       </li>
                                   </ul>
                               </div>
                           </div>
                           <div class="panel-body">
                               <div class="tab-content">
                                   <div class="tab-pane active">
                                       <table class="table table-bordered">
                                           <thead>
                                           <tr>
                                               <th>访问时间</th>
                                               <th>访问Url</th>
                                               <th>访问ip</th>
                                           </tr>
                                           </thead>
                                           <tbody>
                                           {% if access_list %}
                                               {% for item in access_list %}
                                                   <tr>
                                                       <td>{{ item.created_time }}</td>
                                                       <td>{{ item.target_url }}</td>
                                                       <td>{{ item.ip }}</td>
                                                   </tr>
                                               {% endfor %}
                                           {% else %}
                                               <tr>
                                                   <td colspan="2">暂无数据~~</td>
                                               </tr>
                                           {% endif %}
                                           </tbody>
                                       </table>
                                   </div>
                               </div>
                           </div>
                       </div>
                   </div>
               </div>
           </div>
       </div>
   {% endblock %}
   ```

2. 后端代码

   ```python
   @route_account.route("/info")
   def info():
       resp_data = {}
       req = request.args
       uid = int(req.get('id', 0))
       if uid < 1:
           return redirect(UrlManager.buildUrl("/account/index"))
   
       info = User.query.filter_by(uid=uid).first()
       access_list = AppAccessLog.query.filter_by(uid=uid).order_by(AppAccessLog.id.desc()).limit(10).all()
   
       if not info:
           return redirect(UrlManager.buildUrl("/account/index"))
   
       resp_data['info'] = info
       resp_data['access_list'] = access_list
       return ops_render("account/info.html", resp_data)
   ```

-------

#### 修改账户信息

1. `Account/set.html`

   ```python
   {% extends "common/layout_main.html" %}
   {% block content %}
       {% include "common/tab_account.html" %}
       <div class="row m-t  wrap_account_set">
           <div class="col-lg-12">
               <h2 class="text-center">账号设置</h2>
               <div class="form-horizontal m-t m-b">
                   <div class="form-group">
                       <label class="col-lg-2 control-label">姓名:</label>
                       <div class="col-lg-10">
                           <input type="text" name="nickname" class="form-control" placeholder="请输入姓名~~"
                                  value="{{ user_info.nickname }}">
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
                   <div class="form-group">
                       <label class="col-lg-2 control-label">手机:</label>
                       <div class="col-lg-10">
                           <input type="text" name="mobile" class="form-control" placeholder="请输入手机~~"
                                  value="{{ user_info.mobile }}">
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
                   <div class="form-group">
                       <label class="col-lg-2 control-label">邮箱:</label>
                       <div class="col-lg-10">
                           <input type="text" name="email" class="form-control" placeholder="请输入邮箱~~"
                                  value="{{ user_info.email }}">
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
                   <div class="form-group">
                       <label class="col-lg-2 control-label">登录名:</label>
                       <div class="col-lg-10">
                           <input type="text" name="login_name" class="form-control" autocomplete="off"
                                  placeholder="请输入登录名~~" value="{{ user_info.login_name }}">
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
                   <div class="form-group">
                       <label class="col-lg-2 control-label">登录密码:</label>
                       <div class="col-lg-10">
                           <input type="password" name="login_pwd" class="form-control" autocomplete="new-password"
                                  placeholder="请输入登录密码~~" value="******">
                       </div>
                   </div>
                   <div class="hr-line-dashed"></div>
                   <div class="form-group">
                       <div class="col-lg-4 col-lg-offset-2">
                           <input type="hidden" name="id" value="{{ user_info.uid }}">
                           <button class="btn btn-w-m btn-outline btn-primary save">保存</button>
                       </div>
                   </div>
               </div>
           </div>
       </div>
   {% endblock %}
   {% block js %}
       <script src="{{ buildStaticUrl('/js/account/set.js') }}"></script>
   {% endblock %}
   ```

2. `account/set.js`

   ```javascript
   ;
   var account_set_ops = {
       init: function () {
           this.eventBind();
       },
       eventBind: function () {
           $(".wrap_account_set .save").click(function () {
               var btn_target = $(this);
               if (btn_target.hasClass("disabled")) {
                   common_ops.alert("正在处理!!请不要重复提交~~");
                   return;
               }
   
               var nickname_target = $(".wrap_account_set input[name=nickname]");
               var nickname = nickname_target.val()
   
               var mobile_target = $(".wrap_account_set input[name=mobile]");
               var mobile = mobile_target.val()
   
               var login_name_target = $(".wrap_account_set input[name=login_name]");
               var login_name = login_name_target.val()
   
               var login_pwd_target = $(".wrap_account_set input[name=login_pwd]");
               var login_pwd = login_pwd_target.val()
   
               var email_target = $(".wrap_account_set input[name=email]");
               var email = email_target.val()
   
               if (!nickname || nickname.length < 2) {
                   common_ops.tip("请输入符合规范的姓名", nickname_target);
               }
   
               if (!email || email.length < 2) {
                   common_ops.tip("请输入符合规范的邮箱", email_target);
               }
   
               if (!mobile || mobile.length < 2) {
                   common_ops.tip("请输入符合规范的手机号码", mobile_target);
               }
   
               if (!login_name || login_name.length < 2) {
                   common_ops.tip("请输入符合规范的登录名", login_name_target);
               }
   
               if (!login_pwd || login_pwd.length < 2) {
                   common_ops.tip("请输入符合规范的登陆密码", login_pwd_target);
               }
   
               btn_target.addClass('disabled');
   
               var data = {
                   id: $(".wrap_account_set input[name=id]").val(),
                   nickname: nickname,
                   email: email,
                   mobile: mobile,
                   login_name: login_name,
                   login_pwd: login_pwd
               }
   
               $.ajax({
                   url: common_ops.buildUrl("/account/set"),
                   type: 'POST',
                   data: data,
                   dataType: 'json',
                   success: function (res) {
                       btn_target.removeClass("disabled");
                       var callback = null;
                       if (res.code == 200) {
                           callback = function () {
                               window.location.href = window.location.href;
                           }
                       }
                       common_ops.alert(res.msg, callback);
                   },
                   error: function (error) {
                       btn_target.removeClass("disabled");
                       var callback = null;
                       if (res.code == -1) {
                           callback = function () {
                               window.location.href = window.location.href;
                           }
                       }
                       common_ops.alert(error.msg, callback);
                   }
               });
   
           });
       }
   };
   
   $(document).ready(function () {
       account_set_ops.init();
   })
   ```

3. 后端代码

   ```python
   @route_account.route("/set", methods=["GET", "POST"])
   def set():
       default_pwd = '******'
       if request.method == "GET":
           resp_data = {}
           req = request.args
           uid = int(req.get("id", 0))
           user_info = None
           if uid:
               user_info = User.query.filter_by(uid=uid).first()
           resp_data['user_info'] = user_info
           return ops_render("account/set.html", resp_data)
   
       resp = {'code': 200, 'msg': '修改成功', 'data': {}}
   
       req = request.values
   
       id = req['id'] if 'id' in req else 0
       nickname = req['nickname'] if 'nickname' in req else ''
       mobile = req['mobile'] if 'mobile' in req else ''
       email = req['email'] if 'email' in req else ''
       login_name = req['login_name'] if 'login_name' in req else ''
       login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
   
       if nickname is None or len(nickname) < 1:
           resp['code'] = -1
           resp['msg'] = "请输入符合规范的姓名"
           return jsonify(resp)
   
       if mobile is None or len(mobile) < 1:
           resp['code'] = -1
           resp['msg'] = "请输入符合规范的手机号"
           return jsonify(resp)
   
       if email is None or len(email) < 1:
           resp['code'] = -1
           resp['msg'] = "请输入符合规范的邮箱"
           return jsonify(resp)
   
       if login_name is None or len(login_name) < 1:
           resp['code'] = -1
           resp['msg'] = "请输入符合规范的登录名"
           return jsonify(resp)
   
       if login_pwd is None or len(login_pwd) < 1:
           resp['code'] = -1
           resp['msg'] = "请输入符合规范的登录密码"
           return jsonify(resp)
   
       has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
       if has_in:
           resp['code'] = -1
           resp['msg'] = "该登录名已存在"
           return jsonify(resp)
   
       user_info = User.query.filter_by(uid=id).first()
       if user_info:
           model_user = user_info
       else:
           model_user = User()
           model_user.created_time = getCurrentDate()
           model_user.login_salt = UserService.geneSalt()
           resp['msg'] = "添加成功"
   
       model_user.nickname = nickname
       model_user.mobile = mobile
       model_user.email = email
       model_user.login_name = login_name
       if login_pwd != default_pwd:
           model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
       model_user.updated_time = getCurrentDate()
   
       db.session.add(model_user)
       db.session.commit()
   
       return jsonify(resp)
   ```

------

#### 删除恢复操作

1. 后端代码

   ```python
   @route_account.route("/ops", methods=["POST"])
   def ops():
       resp = {'code': 200, 'msg': '操作成功', 'data': {}}
       req = request.values
   
       id = req['id'] if 'id' in req else 0
       act = req['act'] if 'act' in req else None
   
       if not id:
           resp['code'] = -1
           resp['msg'] = "操作失败"
           return jsonify(resp)
   
       if act not in ['remove', 'recover']:
           resp['code'] = -1
           resp['msg'] = "操作失败"
           return jsonify(resp)
   
       user_info = User.query.filter_by(uid=id).first()
       if not user_info:
           resp['code'] = -1
           resp['msg'] = "操作失败"
           return jsonify(resp)
   
       if act == "remove":
           user_info.status = 0
       elif act == "recover":
           user_info.status = 1
   
       user_info.updated_time = getCurrentDate()
       db.session.add(user_info)
       db.session.commit()
       return jsonify(resp)
   ```

2. `index.js`

   ```javascript
   ops: function (act, id) {
           var callback = {
               'ok': function () {
                   $.ajax({
                       url: common_ops.buildUrl("/account/ops"),
                       type: 'POST',
                       data: {
                           act: act,
                           id: id
                       },
                       dataType: 'json',
                       success: function (res) {
                           var callback = null;
                           if (res.code == 200) {
                               callback = function () {
                                   window.location.href = window.location.href;
                               }
                           }
                           common_ops.alert(res.msg, callback);
                       },
                       error: function (error) {
                           var callback = null;
                           if (res.code == -1) {
                               callback = function () {
                                   window.location.href = window.location.href;
                               }
                           }
                           common_ops.alert(error.msg, callback);
                       }
                   });
               },
               'cancel': function () {
                   window.location.href = window.location.href;
               }
           };
           common_ops.confirm((act == "remove" ? "确定删除该数据" : "确定恢复该数据"), callback)
       }
   ```

------

### 3、微信小程序会员登陆

![image-20230307105026560](C:\Users\13939\AppData\Roaming\Typora\typora-user-images\image-20230307105026560.png)

#### 1、`controller`层创建`api`包

#### 2、`__init__.py`入口文件

```python
from flask import Blueprint

route_api = Blueprint('api_page', __name__)


@route_api.route("/")
def index():
    return "Mina Api V1.0"
```

#### 3、创建`member`、`oauth_member_bind`、`wx_share_history`表

```sql 
DROP TABLE IF EXISTS `member`;

CREATE TABLE `member` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `nickname` varchar(100) NOT NULL DEFAULT '' COMMENT '会员名',
  `mobile` varchar(11) NOT NULL DEFAULT '' COMMENT '会员手机号码',
  `sex` tinyint(1) NOT NULL DEFAULT '0' COMMENT '性别 1：男 2：女',
  `avatar` varchar(200) NOT NULL DEFAULT '' COMMENT '会员头像',
  `salt` varchar(32) NOT NULL DEFAULT '' COMMENT '随机salt',
  `reg_ip` varchar(100) NOT NULL DEFAULT '' COMMENT '注册ip',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1：有效 0：无效',
  `vip` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否购买vip',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员表';

DROP TABLE IF EXISTS `oauth_member_bind`;

CREATE TABLE `oauth_member_bind` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(11) NOT NULL DEFAULT '0' COMMENT '会员id',
  `client_type` varchar(20) NOT NULL DEFAULT '' COMMENT '客户端来源类型。qq,weibo,weixin',
  `type` tinyint(3) NOT NULL DEFAULT '0' COMMENT '类型 type 1:wechat ',
  `openid` varchar(80) NOT NULL DEFAULT '' COMMENT '第三方id',
  `unionid` varchar(100) NOT NULL DEFAULT '',
  `extra` text NOT NULL COMMENT '额外字段',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`),
  KEY `idx_type_openid` (`type`,`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='第三方登录绑定关系';


DROP TABLE IF EXISTS `wx_share_history`;

CREATE TABLE `wx_share_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(11) NOT NULL DEFAULT '0' COMMENT '会员id',
  `share_url` varchar(200) NOT NULL DEFAULT '' COMMENT '分享的页面url',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='微信分享记录';
```

#### 4、创建`member`、`oauth_member_bind`、`wx_share_history`模型

```bash
flask-sqlacodegen "mysql://root:123456@127.0.0.1/gaokao" --table member --outfile "common/models/member/Member.py" --flask

flask-sqlacodegen "mysql://root:123456@127.0.0.1/gaokao" --table oauth_member_bind --outfile "common/models/member/OauthMemberBind.py" --flask

flask-sqlacodegen "mysql://root:123456@127.0.0.1/gaokao" --table wx_share_history --outfile "common/models/member/WxShareHistory.py" --flask
```





   

