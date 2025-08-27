import pkgutil
import importlib
from telegram.ext import Dispatcher


def register_all_commands(dispatcher: Dispatcher):
    """
    自动发现并注册所有命令处理器。
    Automatically discovers and registers all command handlers.
    """
    # 获取当前包的路径 / Get the path of the current package
    package_path = __path__
    # 获取当前包的名称 / Get the name of the current package
    package_name = __name__

    # 遍历包中的所有模块 / Iterate over all modules in the package
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        # 动态导入模块 / Dynamically import the module
        module = importlib.import_module(f".{module_name}", package_name)

        # 检查模块中是否有 register 函数，如有则调用
        # Check if the module has a 'register' function, and if so, call it
        if hasattr(module, "register") and callable(module.register):
            module.register(dispatcher)
