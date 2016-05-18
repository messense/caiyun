# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import collections

import click
import requests
import lxml.etree
import baidupcsapi

import caiyun


session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',  # NOQA
    'Connection': 'keep-alive',
}
Resource = collections.namedtuple('Resource', ['name', 'url'])


@click.command()
@click.version_option(version=caiyun.__version__)
@click.argument('url', nargs=1)
@click.option('--zimuzu-username',
              required=True,
              help=u'字幕组用户名')
@click.option('--zimuzu-password',
              required=True,
              help=u'字幕组密码')
@click.option('--baidu-username',
              required=True,
              help=u'百度云盘用户名')
@click.option('--baidu-password',
              required=True,
              help=u'百度云盘密码')
@click.option('-f',
              '--format',
              default='HR-HDTV',
              show_default=True,
              help=u'资源格式')
@click.option('-t',
              '--type',
              default='ed2k',
              show_default=True,
              help=u'资源类型')
@click.option('-p',
              '--path',
              default=u'/我的视频',
              show_default=True,
              help=u'百度云下载路径')
def main(url, zimuzu_username, zimuzu_password, baidu_username,
         baidu_password, format, type, path):
    u"""字幕组资源下载至百度云盘

    URL: 字幕组资源下载页面地址
    """
    zimuzu_login(zimuzu_username, zimuzu_password)
    res = session.get(url)
    try:
        res.raise_for_status()
    except requests.RequestException:
        click.echo(u'获取字幕组资源失败！', err=True)
        sys.exit(1)

    success_count = 0
    failure_count = 0
    resources = parse_resources(res.text, format, type)
    pcs = baidupcsapi.PCS(baidu_username, baidu_password.encode('utf-8'))
    if not path.startswith(u'/'):
        path = u'/{}'.format(path)
    for resource in resources:
        file_path = os.path.join(path, resource.name)
        try:
            pcs.add_download_task(resource.url, file_path)
        except:
            failure_count += 1
            click.echo(u'添加下载任务失败：{}'.format(resource.name), err=True)
        else:
            success_count += 1
            click.echo(u'添加下载任务成功：{}'.format(resource.name))

    click.echo(u'成功：{}个，失败：{}个。'.format(success_count, failure_count))


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

    click.echo(u'登录字幕组账号成功！')


def parse_resources(source, format, type):
    page = lxml.etree.HTML(source)
    media_list = page.xpath(
        '//div[@class="media-list"]/ul/li[@format="{}"]'.format(
            format.upper(),
        )
    )
    if not media_list:
        click.echo(u'找不过任何资源！')
        sys.exit(1)

    for media in media_list:
        name_a = media.xpath('div[@class="fl"]/a')
        if not name_a:
            continue
        name = name_a[0].attrib['title']
        link_a = media.xpath('div[@class="fr"]/a[@type="{}"]'.format(type.lower()))
        if not link_a:
            continue
        url = link_a[0].attrib['href']
        yield Resource(name=name, url=url)
