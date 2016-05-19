# caiyun

字幕组资源离线下载至百度云盘

## 安装

```bash
$ pip install -U caiyun
```

## 使用方法

```bash
$ caiyun --help
```

```
Usage: caiyun [OPTIONS] URL

  字幕组资源下载至百度云盘

  URL: 字幕组资源下载页面地址

Options:
  --version                       Show the version and exit.
  --zimuzu-username TEXT          字幕组用户名  [required]
  --zimuzu-password TEXT          字幕组密码  [required]
  --baidu-username TEXT           百度云盘用户名  [required]
  --baidu-password TEXT           百度云盘密码  [required]
  -f, --format [HR-HDTV|MP4|HDTV|720P|1080P|DVD|WEB-DL|BD-720P|BD-1080P|DVDSCR|RMVB]
                                  资源格式  [default: HR-HDTV]
  -t, --type [ed2k|magnet]        资源类型  [default: ed2k]
  -p, --path TEXT                 百度云下载路径  [default: /我的视频]
  -s, --season TEXT               第几季
  -h, --help                      Show this message and exit.
```

## License

The MIT License (MIT)

Copyright (c) 2016 messense

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
