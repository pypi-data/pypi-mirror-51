# -*- coding: utf-8 -*-

from pywe_token import BaseToken, final_access_token


class User(BaseToken):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(User, self).__init__(appid=appid, secret=secret, token=token, storage=storage)
        # 用户标签管理, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140837
        # 标签管理
        # 1. 创建标签
        self.WECHAT_TAGS_CREATE = self.API_DOMAIN + '/cgi-bin/tags/create?access_token={access_token}'
        # 2. 获取公众号已创建的标签
        self.WECHAT_TAGS_GET = self.API_DOMAIN + '/cgi-bin/tags/get?access_token={access_token}'
        # 3. 编辑标签
        self.WECHAT_TAGS_UPDATE = self.API_DOMAIN + '/cgi-bin/tags/update?access_token={access_token}'
        # 4. 删除标签
        self.WECHAT_TAGS_DELETE = self.API_DOMAIN + '/cgi-bin/tags/delete?access_token={access_token}'
        # 5. 获取标签下粉丝列表
        self.WECHAT_USER_TAG_GET = self.API_DOMAIN + '/cgi-bin/user/tag/get?access_token={access_token}'
        # 用户管理
        # 1. 批量为用户打标签
        self.WECHAT_TAGS_MEMBERS_BATCHTAGGING = self.API_DOMAIN + '/cgi-bin/tags/members/batchtagging?access_token={access_token}'
        # 2. 批量为用户取消标签
        self.WECHAT_TAGS_MEMBERS_BATCHUNTAGGING = self.API_DOMAIN + '/cgi-bin/tags/members/batchuntagging?access_token={access_token}'
        # 3. 获取用户身上的标签列表
        self.WECHAT_TAGS_GETIDLIST = self.API_DOMAIN + '/cgi-bin/tags/getidlist?access_token={access_token}'
        # 设置用户备注名, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140838
        self.WECHAT_USER_INFO_UPDATE_REMARK = self.API_DOMAIN + '/cgi-bin/user/info/updateremark?access_token={access_token}'
        # 获取用户基本信息(UnionID机制), Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140839
        # 获取用户基本信息（包括UnionID机制）
        self.WECHAT_USER_INFO = self.API_DOMAIN + '/cgi-bin/user/info?access_token={access_token}&openid={openid}&lang={lang}'
        # 批量获取用户基本信息
        self.WECHAT_USER_INFO_BATCHGET = self.API_DOMAIN + '/cgi-bin/user/info/batchget?access_token={access_token}'
        # 获取用户列表, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140840
        self.WECHAT_USER_GET = self.API_DOMAIN + '/cgi-bin/user/get?access_token={access_token}&next_openid={next_openid}'
        # 黑名单管理, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1471422259_pJMWA
        # 1. 获取公众号的黑名单列表
        self.WECHAT_TAGS_MEMBERS_GETBLACKLIST = self.API_DOMAIN + '/cgi-bin/tags/members/getblacklist?access_token={access_token}'
        # 2. 拉黑用户
        self.WECHAT_TAGS_MEMBERS_BATCHBLACKLIST = self.API_DOMAIN + '/cgi-bin/tags/members/batchblacklist?access_token={access_token}'
        # 3. 取消拉黑用户
        self.WECHAT_TAGS_MEMBERS_BATCHUNBLACKLIST = self.API_DOMAIN + '/cgi-bin/tags/members/batchunblacklist?access_token={access_token}'

    def tags_create(self, name, appid=None, secret=None, token=None, storage=None):
        """
        :param name: 标签名（30个字符以内）
        """
        return self.post(
            self.WECHAT_TAGS_CREATE.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'tag': {
                    'name': name[:30],
                },
            },
        )

    def tags_get(self, appid=None, secret=None, token=None, storage=None):
        return self.get(self.WECHAT_TAGS_GET, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage))

    def tags_update(self, tagid, name, appid=None, secret=None, token=None, storage=None):
        """
        :param name: 标签名（30个字符以内）
        """
        return self.post(
            self.WECHAT_TAGS_UPDATE.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'tag': {
                    'id': tagid,
                    'name': name[:30],
                },
            },
        )

    def tags_delete(self, tagid, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_TAGS_DELETE.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'tag': {
                    'id': tagid,
                },
            },
        )

    def get_tag_users(self, tagid, appid=None, secret=None, token=None, storage=None, next_openid=''):
        """
        {
            "count": 2,
            "data": {
                "openid": ["OPENID1", "OPENID2"]
            },
            "next_openid": "NEXT_OPENID"
        }
        """
        return self.post(
            self.WECHAT_USER_TAG_GET.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'tagid': tagid,
                'next_openid': next_openid,
            },
        )

    def get_tag_all_users(self, tagid, appid=None, secret=None, token=None, storage=None, users_func=None, authorizer_appid=None):
        goon = True
        next_openid = ''
        while goon:
            infos = get_tag_users(tagid, appid=appid, secret=secret, token=token, storage=storage, next_openid=next_openid)
            if users_func:
                users_func(authorizer_appid, infos)
            next_openid = infos.get('next_openid', '')
            if not next_openid:
                goon = False

    def members_batchtagging(self, tagid, openids, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_TAGS_MEMBERS_BATCHTAGGING.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'tagid': tagid,
                'openids': openids,
            },
        )

    def members_batchuntagging(self, tagid, openids, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_TAGS_MEMBERS_BATCHUNTAGGING.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'tagid': tagid,
                'openids': openids,
            },
        )

    def tags_getidlist(self, openid, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_TAGS_GETIDLIST.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'openid': openid,
            },
        )

    def update_remark(self, openid, remark, appid=None, secret=None, token=None, storage=None):
        """
        :param remark: 新的备注名，长度必须小于30字符
        """
        return self.post(
            self.WECHAT_USER_INFO_UPDATE_REMARK.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'openid': openid,
                'remark': remark[:30],
            },
        )

    def get_user_info(self, openid, lang='zh_CN', appid=None, secret=None, token=None, storage=None):
        """
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        """
        return self.get(self.WECHAT_USER_INFO, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage), openid=openid, lang=lang)

    def batchget_user_info(self, users, appid=None, secret=None, token=None, storage=None):
        """
        {
            "user_list": [
                {
                    "openid": "otvxTs4dckWG7imySrJd6jSi0CWE",
                    "lang": "zh_CN"
                },
                {
                    "openid": "otvxTs_JZ6SEiP0imdhpi50fuSZg",
                    "lang": "zh_CN"
                }
            ]
        }
        """
        return self.post(
            self.WECHAT_USER_INFO_BATCHGET.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'user_list': users,
            },
        )

    def get_users(self, appid=None, secret=None, token=None, storage=None, next_openid=''):
        """
        {
            "total": 2,
            "count": 2,
            "data": {
                "openid": ["OPENID1", "OPENID2"]
            },
            "next_openid": "NEXT_OPENID"
        }
        """
        return self.get(self.WECHAT_USER_GET, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage), next_openid=next_openid)

    def get_all_users(self, appid=None, secret=None, token=None, storage=None, users_func=None, authorizer_appid=None):
        goon = True
        next_openid = ''
        while goon:
            infos = get_users(appid=appid, secret=secret, token=token, storage=storage, next_openid=next_openid)
            if users_func:
                users_func(authorizer_appid, infos)
            next_openid = infos.get('next_openid', '')
            if not next_openid:
                goon = False

    def get_blacks(self, appid=None, secret=None, token=None, storage=None, begin_openid=''):
        """
        {
            "total": 2,
            "count": 2,
            "data": {
                "openid": ["OPENID1", "OPENID2"]
            },
            "next_openid": "NEXT_OPENID"
        }
        """
        return self.post(
            self.WECHAT_TAGS_MEMBERS_GETBLACKLIST.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'begin_openid': begin_openid,
            },
        )

    def get_all_blacks(self, appid=None, secret=None, token=None, storage=None, users_func=None, authorizer_appid=None):
        goon = True
        next_openid = ''
        while goon:
            infos = get_blacks(appid=appid, secret=secret, token=token, storage=storage, begin_openid=next_openid)
            if users_func:
                users_func(authorizer_appid, infos)
            next_openid = infos.get('next_openid', '')
            if not next_openid:
                goon = False

    def mambers_batchblacklist(self, openids, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_TAGS_MEMBERS_BATCHBLACKLIST.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'openid_list': openids,
            },
        )

    def mambers_batchunblacklist(self, openids, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_TAGS_MEMBERS_BATCHUNBLACKLIST.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'openid_list': openids,
            },
        )


user = User()
tags_create = user.tags_create
tags_get = user.tags_get
tags_update = user.tags_update
tags_delete = user.tags_delete
get_tag_users = user.get_tag_users
get_tag_all_users = user.get_tag_all_users
members_batchtagging = user.members_batchtagging
members_batchuntagging = user.members_batchuntagging
tags_getidlist = user.tags_getidlist
update_remark = user.update_remark
get_user_info = user.get_user_info
batchget_user_info = user.batchget_user_info
get_users = user.get_users
get_all_users = user.get_all_users
get_blacks = user.get_blacks
get_all_blacks = user.get_all_blacks
mambers_batchblacklist = user.mambers_batchblacklist
mambers_batchunblacklist = user.mambers_batchunblacklist
