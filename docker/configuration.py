import importlib.util
import sys
from os import scandir
from os.path import abspath, isfile


def _import(module_name, path, loaded):
    spec = importlib.util.spec_from_file_location('', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[module_name] = module
    loaded.insert(0, module)
    print(f"loaded config '{path}'")


def read_configurations(config_module, config_dir, main_config):
    loaded = []
    main_path = abspath(f'{config_dir}/{main_config}.py')
    if isfile(main_path):
        _import(f'{config_module}.{main_config}', main_path, loaded)
    else:
        print(f"Main configuration '{main_path}' not found.")

    with scandir(config_dir) as it:
        for f in sorted(it, key=lambda x: x.name):
            if not f.is_file():
                continue
            if f.name.startswith('__') or not f.name.endswith('.py'):
                continue
            if f.name in (f'{main_config}.py', f'{config_dir}.py'):
                continue
            module_name = f'{config_module}.{f.name[:-3]}'.replace('.', '_')
            _import(module_name, f.path, loaded)

    if not loaded:
        raise ImportError(f"No configuration files found in '{config_dir}'.")
    return loaded


_loaded_configurations = read_configurations(
    config_dir='/etc/netbox/config/',
    config_module='netbox.configuration',
    main_config='configuration',
)


def __getattr__(name):
    for config in _loaded_configurations:
        try:
            return getattr(config, name)
        except AttributeError:
            pass
    raise AttributeError


def __dir__():
    names = []
    for config in _loaded_configurations:
        names.extend(dir(config))
    return names
