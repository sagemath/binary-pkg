import os


def safe_search_path(root_path):
    """
    Return PATH with all subdirectories of ``root_path`` removed
    """
    PATH = os.environ.get('PATH', '')
    components = PATH.split(':')
    good = [d for d in components if not d.startswith(root_path)]
    return ':'.join(good)
