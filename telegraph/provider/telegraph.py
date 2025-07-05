from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class TelegraphProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证提供的 Telegraph Access Token 是否有效。
        尝试使用该 token 创建一个测试页面。
        如果验证失败，应抛出 ToolProviderCredentialValidationError 异常。
        """
        access_token = credentials.get("telegraph_access_token")
        if not access_token:
            raise ToolProviderCredentialValidationError("Telegraph Access Token 不能为空。")
        try:
            # 尝试执行一个需要凭证的简单操作来验证
            from telegraph import Telegraph
            ph = Telegraph(access_token=access_token)
            # 尝试创建一个临时的、无害的页面作为验证手段
            # 注意：更好的验证方式可能是调用 API 的 'getAccountInfo' 等只读方法（如果存在）
            test_page = ph.create_page(title="Dify Validation Test", html_content="This is a test page created by Dify plugin validation.")
            # 如果需要，可以考虑立即编辑或删除这个测试页面，但这会增加复杂性
            print(f"Validation successful. Test page created: {test_page}")
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
