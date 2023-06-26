CREATE SCHEMA gaokao COLLATE latin1_swedish_ci;
use gaokao;

-- auto-generated definition
CREATE TABLE user (
    uid          BIGINT AUTO_INCREMENT COMMENT '用户uid' PRIMARY KEY,
    nickname     VARCHAR(100) DEFAULT ''                NOT NULL COMMENT '用户名',
    mobile       VARCHAR(20)  DEFAULT ''                NOT NULL COMMENT '手机号码',
    email        VARCHAR(100) DEFAULT ''                NOT NULL COMMENT '邮箱地址',
    sex          TINYINT(1)   DEFAULT 0                 NOT NULL COMMENT '1：男 2：女 0：没填写',
    avatar       VARCHAR(64)  DEFAULT ''                NOT NULL COMMENT '头像',
    login_name   VARCHAR(20)  DEFAULT ''                NOT NULL COMMENT '登录用户名',
    login_pwd    VARCHAR(32)  DEFAULT ''                NOT NULL COMMENT '登录密码',
    login_salt   VARCHAR(32)  DEFAULT ''                NOT NULL COMMENT '登录密码的随机加密秘钥',
    status       TINYINT(1)   DEFAULT 1                 NOT NULL COMMENT '1：有效 0：无效',
    updated_time TIMESTAMP    DEFAULT current_timestamp NOT NULL COMMENT '最后一次更新时间',
    created_time TIMESTAMP    DEFAULT current_timestamp NOT NULL COMMENT '插入时间',
    CONSTRAINT login_name UNIQUE (login_name)
) COMMENT '用户表（管理员）' CHARSET = utf8mb4;

INSERT INTO gaokao.user (uid, nickname, mobile, email, sex, avatar, login_name, login_pwd, login_salt, status, updated_time, created_time) VALUES (1, '', '', '', 0, '', 'root', '1c6ddc345410070b7df301ecd2675aa7', '', 1, '2023-06-26 10:32:34', '2023-06-26 10:32:34');

-- auto-generated definition
CREATE TABLE app_error_log (
    id           INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    referer_url  VARCHAR(255) DEFAULT ''                NOT NULL COMMENT '当前访问的refer',
    target_url   VARCHAR(255) DEFAULT ''                NOT NULL COMMENT '访问的url',
    query_params TEXT                                   NOT NULL COMMENT 'get和post参数',
    content      LONGTEXT                               NOT NULL COMMENT '日志内容',
    created_time TIMESTAMP    DEFAULT current_timestamp NOT NULL COMMENT '插入时间'
) COMMENT 'app错误日表' CHARSET = utf8mb4;

-- auto-generated definition
CREATE TABLE member (
    id           INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nickname     VARCHAR(100) DEFAULT ''                NOT NULL COMMENT '会员名',
    mobile       VARCHAR(11)  DEFAULT ''                NOT NULL COMMENT '会员手机号码',
    sex          TINYINT(1)   DEFAULT 0                 NOT NULL COMMENT '性别 1：男 2：女',
    avatar       VARCHAR(200) DEFAULT ''                NOT NULL COMMENT '会员头像',
    salt         VARCHAR(32)  DEFAULT ''                NOT NULL COMMENT '随机salt',
    reg_ip       VARCHAR(100) DEFAULT ''                NOT NULL COMMENT '注册ip',
    status       TINYINT(1)   DEFAULT 1                 NOT NULL COMMENT '状态 1：有效 0：无效',
    vip          TINYINT(1)   DEFAULT 0                 NOT NULL COMMENT '是否购买vip',
    updated_time TIMESTAMP    DEFAULT current_timestamp NOT NULL COMMENT '最后一次更新时间',
    created_time TIMESTAMP    DEFAULT current_timestamp NOT NULL COMMENT '插入时间'
) COMMENT '会员表' CHARSET = utf8mb4;

-- auto-generated definition
CREATE TABLE oauth_member_bind (
    id           INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    member_id    INT          DEFAULT 0                 NOT NULL COMMENT '会员id',
    client_type  VARCHAR(20)  DEFAULT ''                NOT NULL COMMENT '客户端来源类型。qq,weibo,weixin',
    type         TINYINT(3)   DEFAULT 0                 NOT NULL COMMENT '类型 type 1:wechat ',
    openid       VARCHAR(80)  DEFAULT ''                NOT NULL COMMENT '第三方id',
    unionid      VARCHAR(100) DEFAULT ''                NOT NULL,
    extra        TEXT                                   NOT NULL COMMENT '额外字段',
    updated_time TIMESTAMP    DEFAULT current_timestamp NOT NULL COMMENT '最后更新时间',
    created_time TIMESTAMP    DEFAULT current_timestamp NOT NULL COMMENT '插入时间'
) COMMENT '第三方登录绑定关系' CHARSET = utf8mb4;

CREATE INDEX idx_type_openid ON oauth_member_bind (type, openid);

-- auto-generated definition
CREATE TABLE wx_share_history (
    id           INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    member_id    INT          DEFAULT 0                 NOT NULL COMMENT '会员id',
    share_url    VARCHAR(200) DEFAULT ''                NOT NULL COMMENT '分享的页面url',
    created_time TIMESTAMP    DEFAULT current_timestamp NOT NULL COMMENT '创建时间'
) COMMENT '微信分享记录' CHARSET = utf8mb4;




