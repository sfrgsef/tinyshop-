import importlib
from core.logger import logger
from core.variable_pool import variable_pool
from typing import Callable, List, Dict, Any


class HookManager:
    def __init__(self):
        self._hooks = {
            "before_request": [],
            "after_request": [],
            "before_test": [],
            "after_test": [],
            "before_suite": [],
            "after_suite": []
        }

    def register_hook(self, hook_type: str, hook_func: Callable):
        """
        注册钩子函数
        """
        if hook_type in self._hooks:
            self._hooks[hook_type].append(hook_func)
            logger.info(f"注册钩子: {hook_type} -> {hook_func.__name__}")
        else:
            logger.warning(f"未知的钩子类型: {hook_type}")

    def execute_hooks(self, hook_type: str, *args, **kwargs) -> List[Any]:
        """
        执行指定类型的钩子函数
        """
        results = []
        if hook_type in self._hooks:
            for hook_func in self._hooks[hook_type]:
                try:
                    result = hook_func(*args, **kwargs)
                    results.append(result)
                    logger.debug(f"执行钩子: {hook_func.__name__}")
                except Exception as e:
                    logger.error(f"钩子执行失败: {hook_func.__name__}, 错误: {e}")
                    results.append(None)
        return results

    def clear_hooks(self, hook_type: str = None):
        """
        清空钩子函数
        """
        if hook_type:
            if hook_type in self._hooks:
                self._hooks[hook_type].clear()
                logger.info(f"清空钩子: {hook_type}")
        else:
            for hook_type in self._hooks:
                self._hooks[hook_type].clear()
            logger.info("清空所有钩子")

    def get_hook_count(self, hook_type: str) -> int:
        """
        获取指定类型钩子的数量
        """
        return len(self._hooks.get(hook_type, []))

    def list_hooks(self) -> Dict[str, List[str]]:
        """
        列出所有钩子函数
        """
        hook_names = {}
        for hook_type, hooks in self._hooks.items():
            hook_names[hook_type] = [hook.__name__ for hook in hooks]
        return hook_names

# 全局钩子管理器实例
hook_manager = HookManager()


def execute_hooks(hooks, response_data=None):
    """执行钩子函数"""
    if not hooks:
        return

    for hook in hooks:
        try:
            # 格式: module.function(arg1,arg2)
            if '(' in hook and ')' in hook:
                func_name = hook.split('(')[0]
                args_str = hook.split('(')[1].split(')')[0]
                args = [arg.strip() for arg in args_str.split(',')] if args_str else []

                # 解析模块和函数名
                if '.' in func_name:
                    module_name, func_name = func_name.rsplit('.', 1)
                    module = importlib.import_module(module_name)
                    func = getattr(module, func_name)
                else:
                    func = globals()[func_name]

                # 处理特殊参数
                resolved_args = []
                for arg in args:
                    if arg == "response_data":
                        resolved_args.append(response_data)
                    elif arg.startswith('"') and arg.endswith('"'):
                        resolved_args.append(arg[1:-1])
                    elif arg.startswith("variable_pool."):
                        var_name = arg.split('.')[1]
                        resolved_args.append(variable_pool.get(var_name))
                    else:
                        resolved_args.append(arg)

                # 执行函数
                logger.info(f"执行钩子: {hook}")
                func(*resolved_args)
            else:
                logger.warning(f"钩子格式错误: {hook}")
        except Exception as e:
            logger.error(f"钩子执行失败: {hook}, 错误: {str(e)}")


# 常用钩子函数
def save_token_to_pool(token):
    """保存token到变量池"""
    if token:
        variable_pool.set("token", token)
        logger.info(f"Token已保存: {token[:10]}...")


def save_user_id_to_pool(user_id):
    """保存用户ID到变量池"""
    if user_id:
        variable_pool.set("user_id", user_id)
        logger.info(f"用户ID已保存: {user_id}")


def clear_token():
    """清除token"""
    variable_pool.set("token", None)
    logger.info("Token已清除")