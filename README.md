# local_dify_plugin
自己写的dify插件
## local_mineru
langgenius官方的mineru插件无法访问自签名证书的dify服务，修改了程序，给所有的requests请求都加上了verify=False的参数 
**注意**
仅限测试环境或内部使用，屏蔽安全参数风险自行承担 
### 执行流程
1、参考docs/command.txt步骤执行打包成本地文件 
2、通过“本地插件”安装 
### 参数说明
`REMOTE_DIFY`是指远端的dify plugin_daemon 服务器 
PROJECT_PATH=/path/to/local_dify_plugin 
REMOTE_DIFY_HOST=xxx.xxx.xxx.xxx 
REMOTE_DIFY_PORT=22 
REMOTE_DIFY_USER=username 
`REMOTE_DIFY_REAL_PATH`参考dify部署的docker-compose.yml，plugin_daemon服务的volume映射关系 
REMOTE_DIFY_REAL_PATH=/remote/dify/plugin_daemon/real/path 
REMOTE_DIFY_DOCKER_VOLUME=/app/storage/public_keys 
