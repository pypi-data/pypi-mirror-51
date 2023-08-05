from collections import UserList


class Path(UserList):
    """Absolute path manipulation in a nested object.
    
    A path is a global (starts with '/') address in a nested object.
    Items at each level are separated by '/'.
    """
    def __init__(self, items=None):
        if items is None:
            items = []
        else:
            if isinstance(items, Path):
                items = items.data
            elif isinstance(items, str):
                if items[0] != '/':
                    raise ValueError('Path class only supports absolute paths')
                items = items.strip('/').split('/')
                if items == ['']: items = []
        super().__init__(items)

    def __str__(self):
        return '/' + '/'.join(self)

    def __repr__(self):
        return f'<Path({str(self)})>'

    def __truediv__(self, other):
        return Path(self + str(other).strip('/').split('/'))

    #def __iter__(self):
    #    """Iterate over items"""
    #    keys = self._path.strip('/').split('/')
    #    if keys == ['']: keys = []
    #    return iter(keys)

    #def __contains__(self, item):
    #    """`for item in p` must yield items, in order"""
    #    return str(item) in list(self)
    #    
    #def __eq__(self, other):
    #    """Compare equal paths"""
    #    return self._path == other._path

    #def __getitem__(self, key):
    #    """Access list of items"""
    #    return list(self)[key]

    #def __setitem__(self, key, value):
    #    """Set items separated by index"""
    #    items = list(self)
    #    items[key] = value
    #    self._path = '/'.join(items)

    @property
    def parent(self):
        """Get parent of path. Equivalent to `dirname`.
        
        If path is /, raise IndexError by analogy with [].pop()
        """
        if len(self) == 0:
            raise IndexError("Root '/' has no parent")
        split_path = [key for key in self]
        return Path('/' + '/'.join(split_path[:-1]))

    def startswith(self, other):
        """Check if path contains other from root /"""
        return str(self).startswith(str(other))