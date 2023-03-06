# 高考志愿填报系统flask后端

## 1、创建项目，构建mvc基本框架

![image-20230305213404728](C:\Users\13939\AppData\Roaming\Typora\typora-user-images\image-20230305213404728.png)

## 2、后台账户模块

![image-20230305230155705](C:\Users\13939\AppData\Roaming\Typora\typora-user-images\image-20230305230155705.png)

------

### 用户登录

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
     from common.models.User import User
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

### 用户登出

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

### 编辑信息

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

### 修改密码

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





