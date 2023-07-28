import sys

def is_virtual_environment():
    # 检查是否处于虚拟环境
    print(sys.prefix)
    print(sys.base_prefix)
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

if is_virtual_environment():
    print("Current Python environment is Virtual Environment.")
else:
    print("Current Python environment is Not Virtual Environment.。")