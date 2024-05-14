import os
import importlib
import inspect
from logger.transforms.transform import Transform
from logger.readers.reader import Reader
from logger.listener.listener import Listener
from logger.writers.writer import Writer

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


def list_subclasses_and_mixins_args(base_dir, base_class):
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
                            # Get the constructor arguments for each class
                            args = inspect.signature(obj.__init__).parameters
                            arg_names = [p.name for p in args.values() if p.name != 'self']  # Exclude 'self'
                            subclasses_and_mixins.append((module_name, name, arg_names))
                except Exception as e:
                    print(f"Error importing module '{module_path}': {e}")
                    
    return subclasses_and_mixins

# Example usage:
name_set = set()
subclasses_and_mixins = list_subclasses_and_mixins_args('./logger/transforms', Transform)
for module_name, class_name, args in subclasses_and_mixins:    
    print(f"Module: {module_name} {args}")
    name_set.add((module_name, "transform", args))


# subclasses_and_mixins = list_subclasses_and_mixins('./logger/readers', Reader)
# for module_name, class_name in subclasses_and_mixins:    
#     print(f"Module: {module_name}")
#     name_set.add((module_name, 'reader'))


subclasses_and_mixins = list_subclasses_and_mixins('./logger/listener', Listener)
for module_name, class_name in subclasses_and_mixins:    
    print(f"Module: {module_name}")
    name_set.add((module_name, 'listener'))


# subclasses_and_mixins = list_subclasses_and_mixins('./logger/writers', Writer)
# for module_name, class_name in subclasses_and_mixins:    
#     print(f"Module: {module_name}")
#     name_set.add((module_name, 'writers'))


print(name_set)
for p in name_set:
    print(f"{p[0]}, {p[1]}, {p[2]}")

