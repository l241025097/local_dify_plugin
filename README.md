# local_dify_plugin
自己写的dify插件 **注意** 仅限测试环境或内部使用，屏蔽安全参数风险自行承担。
## local_mineru
### 背景
langgenius官方的mineru插件无法与自签名证书的dify服务器互通，报错：
```bash
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1000)
```
#### 尝试1
- 配置dify的FILE_URL为http服务，解决“认证问题”，但是会引入新的问题-应用自定义的图标会消失。
- 原因为：dify的web服务是https，而dify的文件服务是http，浏览器拒绝http服务的解析。
- 解决：还是得把FILE_URL配置为https。
#### 尝试2
- 下载langgenius官方的mineru源码，给tools/parse.py的所有requests请求都加上了verify=False的参数，依然报错。
- 原因为：file.blob的FILE类，涉及到get操作，封装在dify_plugin库里，无法修改。
```python
file_data = {
    "file": (file.filename, file.blob),
}
```
- 解决：查看file.blob的返回，发现是读取文件的bytes，自己写request，将file.blob改成自己请求回来的bytes，解决了文件下载问题。
```python
res = get(file.url, verify=False)
file_data = {
    "file": (file.filename, res.content),
}
```
#### 尝试3
- 当涉及解析带有“图片”的pdf时，依然报错。
- 原因为：解析的“图片”需要上传至dify，上传操作，封装在dify_plugin库里，无法修改。
```python
images = []
for file_name, encoded_image_data in file_obj.items():
    base64_data = encoded_image_data.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    # 以下代码报错：
    file_res = self.session.file.upload(file_name, image_bytes, "image/jpeg")
    images.append(file_res)
```
- 解决：在tools/parse.py中重写upload方法，配置verify=False。
```python
# Rewrite the file upload method (refer to the `upload` method in dify_plugin.invocations.file.File).
def upload_file(self, filename: str, content: bytes, mimetype: str) -> UploadFileResponse:
    """
    Upload a file

    :param filename: file name
    :param content: file content
    :param mimetype: file mime type

    :return: file id
    """
    for response in self.session.file._backwards_invoke(
        InvokeType.UploadFile,
        dict,
        {
            "filename": filename,
            "mimetype": mimetype,
        },
    ):
        url = response.get("url")
        if not url:
            raise Exception("upload file failed, could not get signed url")

        # 修改以下代码，配置verify=False
        response = post(url, files={"file": (filename, content, mimetype)}, verify=False)  # noqa: S113
        if response.status_code != 201:
            raise Exception(f"upload file failed, status code: {response.status_code}, response: {response.text}")

        return UploadFileResponse(**response.json())

    raise Exception("upload file failed, empty response from server")
```
```python
images = []
for file_name, encoded_image_data in file_obj.items():
    base64_data = encoded_image_data.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    # 修改以下代码：
    file_res = self.upload_file(file_name, image_bytes, "image/jpeg")
    images.append(file_res)
```
#### 尝试4
- 自己打包的dify插件，无法安装，报认证错误。
- 原因为：dify服务启用了FORCE_VERIFYING_SIGNATURE=true，只有官方签名的插件能够安装。
```shell
PluginDaemonBadRequestError: plugin verification has been enabled, and the plugin you want to install has a bad signature
```
- 解决1：在dify服务的.env文件中设置FORCE_VERIFYING_SIGNATURE=false，并重启dify服务。
- 解决2：启用第三方签名认证，给打包文件签名再安装。
##### 执行流程
1、参考docs/command.txt步骤执行打包成本地文件 \
2、通过“本地插件”安装
##### 参数说明
`REMOTE_DIFY`是指远端的dify plugin_daemon 服务器 \
PROJECT_PATH=/path/to/local_dify_plugin \
REMOTE_DIFY_HOST=xxx.xxx.xxx.xxx \
REMOTE_DIFY_PORT=22 \
REMOTE_DIFY_USER=username \
`REMOTE_DIFY_REAL_PATH`参考dify部署的docker-compose.yml，plugin_daemon服务的volume映射关系 \
REMOTE_DIFY_REAL_PATH=/remote/dify/plugin_daemon/real/path \
REMOTE_DIFY_DOCKER_VOLUME=/app/storage/public_keys
