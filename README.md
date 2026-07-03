# POC 仓库

批量漏洞检测 PoC（Proof-of-Concept）脚本集合，用于快速验证多种软件产品的安全漏洞。

## 目录

| 目录 | 分类 | 漏洞数 |
|------|------|--------|
| [CMS/](./CMS) | 内容管理系统漏洞 | 4 |
| [Frame/](./Frame) | 框架漏洞 | 1 |
| [Iot/](./Iot) | 物联网设备漏洞 | 2 |
| [中间件/](./中间件) | 中间件漏洞 | 1 |
| [开发组件/](./开发组件) | 开发组件漏洞 | 1 |

## 使用方式

```bash
pip install requests
cd 漏洞目录/
python main.py
```

每个 PoC 从 `url.txt` 读取目标 URL（每行一个，`#` 开头为注释），检测结果记录在 `log/log.txt`（全部）和 `log/success.txt`（仅成功）中。

## 漏洞列表

| 漏洞名称 | 分类 | 类型 |
|----------|------|------|
| AspCMS commentList.asp SQL注入 | CMS | SQL注入 |
| BSPHP index.php 未授权访问 信息泄露 | CMS | 未授权访问 |
| 狮子鱼CMS ApiController.class.php SQL注入 | CMS | SQL注入 |
| 狮子鱼CMS ApigoodController.class.php SQL注入 | CMS | SQL注入 |
| AstrBot 任意文件读取 | Frame | 文件读取 |
| NetMizer 日志管理系统 cmd.php 远程命令执行 | Iot | RCE |
| NetMizer 日志管理系统 data 目录遍历 | Iot | 目录遍历 |
| GlassFish 任意文件读取 | 中间件 | 文件读取 |
| kkFileView getCorsFile 任意文件读取 CVE-2021-43734 | 开发组件 | 文件读取 |

## 通用约定

- Python 3，仅依赖 `requests`
- SSL 验证跳过（`verify=False`），超时 10 秒
- URL 无 scheme 时自动添加 `http://`
- 日志文件使用 `utf-8` 编码
