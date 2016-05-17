# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys

import click
import requests
import lxml.etree
from baidupcsapi import PCS as BaiduPCS

import caiyun


session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',  # NOQA
    'Connection': 'keep-alive',
}


@click.command()
@click.version_option(version=caiyun.__version__)
@click.argument('url', nargs=1)
@click.option('--zimuzu-username', required=True, help=u'字幕组用户名')
@click.option('--zimuzu-password', required=True, help=u'字幕组密码')
@click.option('--baidu-username', required=True, help=u'百度云盘用户名')
@click.option('--baidu-password', required=True, help=u'百度云盘密码')
@click.option('-f', '--format', default='HR-HDTV', help=u'资源格式')
@click.option('-t', '--type', default='ed2k', help='资源类型')
def main(url, zimuzu_username, zimuzu_password,
         baidu_username, baidu_password, format, type):
    u"""字幕组资源下载至百度云盘"""
    zimuzu_login(zimuzu_username, zimuzu_password)
    res = session.get(url)
    try:
        res.raise_for_status()
    except requests.RequestException:
        click.echo(u'获取字幕组资源失败！', err=True)
        sys.exit(1)

    resources = parse_resources(res.text, format, type)
    pcs = BaiduPCS(baidu_username, baidu_password.encode('utf-8'))
    for resource in resources:
        pcs.add_download_task(resource, u'/我的资源/测试')
        click.echo(u'成功添加下载任务：{}'.format(resource))


def zimuzu_login(username, password):
    login_url = 'http://www.zimuzu.tv/User/Login/ajaxLogin'
    res = session.post(
        login_url,
        data={
            'account': username,
            'password': password,
            'remember': '1',
            'url_back': '',
        },
        headers=headers,
    )
    try:
        res.raise_for_status()
    except requests.RequestException:
        click.echo(u'登录字幕组账号失败！', err=True)
        sys.exit(1)

    res = res.json()
    if res['status'] != 1:
        click.echo(res['info'], err=True)
        sys.exit(1)


def parse_resources(source, format, type):
    page = lxml.etree.HTML(source)
    media_list = page.xpath(
        '//div[@class="media-list"]/ul/li[@format="{}"]/div[@class="fr"]/a[@type="{}"]'.format(
            format.upper(),
            type.lower(),
        )
    )
    if not media_list:
        click.echo(u'找不过任何资源！')
        sys.exit(1)

    for media in media_list:
        yield media.attrib['href']
