from collections.abc import Generator
from typing import Any
from telegraph import Telegraph # 导入我们使用的库

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class TelegraphTool(Tool):
    """
    一个简单的 Telegraph 发布工具。
    """

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        根据输入的标题和内容，创建一个新的 Telegraph 页面。

        Args:
            tool_parameters: 一个包含工具输入参数的字典:
                - p_title (str): Telegraph 页面的标题。
                - p_content (str): 要发布的 Markdown 格式的内容。

        Yields:
            ToolInvokeMessage: 包含成功创建的 Telegraph 页面 URL 的消息。

        Raises:
            Exception: 如果页面创建失败，则抛出包含错误信息的异常。
        """
        # 1. 从运行时获取凭证
        try:
            access_token = self.runtime.credentials["telegraph_access_token"]
        except KeyError:
            raise Exception("Telegraph Access Token 未配置或无效。请在插件设置中提供。")

        # 2. 获取工具输入参数
        title = tool_parameters.get("p_title", "Untitled") # 使用 .get 提供默认值
        content = tool_parameters.get("p_content", "")

        if not content:
            raise Exception("发布内容不能为空。")

        # 3. 调用库执行操作
        try:
            telegraph = Telegraph(access_token=access_token)  # 初始化 Telegraph API
            ph_link = telegraph.create_page(title=title, html_content=content) # 创建页面
        except Exception as e:
            # 如果库调用失败，抛出异常
            raise Exception(f"调用 Telegraph API 失败: {e}")

        # 4. 返回结果
        # 使用 create_link_message 生成一个包含链接的输出消息
        yield self.create_link_message(ph_link["url"])