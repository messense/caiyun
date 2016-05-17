# -*- coding: utf-8 -*-
from __future__ import absolute_import
import click

import caiyun


@click.command()
@click.version_option(version=caiyun.__version__)
def main():
    u"""字幕组资源下载至百度云盘"""
