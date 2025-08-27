import pkgutil
import importlib
from telegram.ext import Dispatcher

def register_all_message_handlers(dispatcher: Dispatcher):
    """
    自动发现并注册所有消息处理器。
    Automatically discovers and registers all message handlers.
    """
    package_path = __path__
    package_name = __name__

    for _, module_name, _ in pkgutil.iter_modules(package_path):
        module = importlib.import_module(f".{module_name}", package_name)
        
        if hasattr(module, 'register') and callable(module.register):
            module.register(dispatcher)
