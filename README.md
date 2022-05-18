# DanmakuProtobufToXML

本Python脚本用于将基于protocol buffer的新版b站历史弹幕文件`seg.so`转换为旧版的`xml`弹幕文件。

需求来源：本人有收集b站历史弹幕然后放进bililocal里播放的**无聊**需求，因为不花里胡哨又能解析protobuf二进制弹幕文件的播放器我找不到，只能继续依靠xml来过活。

## 参考列表

[https://blog.csdn.net/freeking101/article/details/123131304](https://blog.csdn.net/freeking101/article/details/123131304)

[https://zhuanlan.zhihu.com/p/392931611](https://zhuanlan.zhihu.com/p/392931611)

`dm.proto`文件来自：[https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/grpc_api/bilibili/community/service/dm/v1/dm.proto](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/grpc_api/bilibili/community/service/dm/v1/dm.proto)

详细原理请看以上文章以及Google的protocol buffer文档（[URL](https://developers.google.com/protocol-buffers/docs/overview)）~~我也没咋搞懂~~

## 使用方法

*本脚本只支持从url获取seg.so并且转换为xml文件输出，并不支持批量获取、爬取全弹幕等功能 。*

确保电脑上装有Python3以及`requests`第三方库。

```shell
$ pip install requests
```

之后，需要去 https://github.com/protocolbuffers/protobuf 下载`Protobuf-Python`来获取在Python中处理Protobuf必要的包。

下载后解压进入其中的`Python`目录，该目录下能看到一个`setup.py`。

在该目录下执行以下命令来进行安装：

```shell
python setup.py clean
python setup.py build
python setup.py install
```

之后，应该会在你`pip`包的安装目录下出现一个`protobuf`开头的包

---

在项目根目录（run.sh在的那个目录）新建一个`cookie.json`文件，用Editthiscookie（[URL](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en)）浏览器插件导出B站的cookie并且复制进`cookie.json`文件里。

打开`run.bat`文件，把这行

```batch
python ./main.py {oid} {date}
```

中的{oid}改成视频的cid，{date}改成具体的历史弹幕日期（YYYY-MM-DD）,大括号也要去掉。

cid的具体获取方法可以参考这篇专栏（[URL](https://www.bilibili.com/read/cv6570091)）。

更改完成后点击`run.bat`运行即可。

XML会输出在根目录的`output`文件夹下。命名规则为`{oid}.{date}.xml`

## 已知问题

不知道为什么开着clash的系统代理获取会出问题，建议把`*.bilibili.com`加入系统代理的白名单
