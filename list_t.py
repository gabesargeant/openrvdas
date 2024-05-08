import os
import importlib
import inspect
from logger.transforms.transform import Transform

def list_subclasses_and_mixins(base_dir, base_class):
    subclasses_and_mixins = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py') and not file.startswith('test'):
                module_name = os.path.splitext(file)[0]
                module_path = os.path.relpath(os.path.join(root, file)).replace(os.path.sep, '.')
                module_path = module_path[:-3]
                try:
                    module = importlib.import_module(module_path)
                    for name, obj in vars(module).items():
                        if isinstance(obj, type) and issubclass(obj, base_class or hasattr(obj, '__mro__') and base_class in obj.__mro__):
                            subclasses_and_mixins.append((module_name, name))
                except Exception as e:
                    print(f"Error importing module '{module_path}': {e}")
                    
    return subclasses_and_mixins

# Example usage:
subclasses_and_mixins = list_subclasses_and_mixins('./logger/transforms', Transform)
for module_name, class_name in subclasses_and_mixins:    
    print(f"Module: {module_name}, Class: {class_name}")

print(len(subclasses_and_mixins) / 2)