import copy

from nob.core import Path

__all__ = ['Tree', 'TreeView']


class _TreeUtils:
    """Tree manipulation routines, common to Trees and TreeViews"""
    def __init__(self):
        raise TypeError("This class is not meant for direct instantiation.")

    def __setitem__(self, key, value):
        """__setitem__ goes directly into the raw data"""
        path = self._find_unique(key)
        if isinstance(self._raw_data(path.parent), list):
            key = int(key)
        self._raw_data(path.parent)[key] = value

    def __iter__(self):
        """iterator always yields TreeView instances"""
        if isinstance(self._raw_data(), dict):
            for key in self._raw_data():
                yield TreeView(self._tree, self._root / key)
        else:
            for idx, val in self._raw_data():
                yield TreeView(self._tree, self._root / str(idx))

    def __getattr__(self, name):
        """Offer attribute access to simplify t.['key'] to t.key"""
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        """Offer attribute assignment to simplify t.['key'] = to t.key ="""
        if name in self.__dict__:
            self.__dict__[name] = value
        else:
            self.__setitem__(name, value)

    def __eq__(self, value):
        return self._data == value._data

    @property
    def paths(self):
        """Dynamically constitute a list of all current valid paths"""
        paths = [Path('/')]
        def rec_walk(root, root_path):
            """Recursive walk of tree"""
            if isinstance(root, dict):
                for key in root:
                    paths.append(root_path / key)
                    rec_walk(root[key], root_path / key)
            elif isinstance(root, list):
                for idx, val in enumerate(root):
                    paths.append(root_path / str(idx))
                    rec_walk(val, root_path / str(idx))

        rec_walk(self._data, Path())
        return paths

    def find(self, key):
        """Find all paths matching key"""
        if '/' in str(key):
            raise ValueError(".find only works with keys, not paths")
        return [p for p in self.paths if len(p) > 0 and p[-1] == key]
        # Dynamic not implemented yet
        #if '*' not in address:  # Static address
        #    return [p for p in paths if address in p]
        #else:                   # Dynamic address
        #    keys = [k for k in address.split('/') if k != '*']
        #    return [p for p in paths
        #            if all([k in p for k in keys])]

    def _access(self, identifier):
        """Sort out variable entry types: global address or key"""
        if type(identifier) == int:
            identifier = str(identifier)
        try:
            path = Path(identifier)
            return [p for p in self.paths if p == path]
        except ValueError:
            return self.find(identifier)
    
    def _find_unique(self, identifier):
        """Helper method to ensure unique path is found"""
        paths = self._access(identifier)
        if len(paths) != 1:
            raise KeyError(f'Identifier {identifier} yielded {len(paths)} result(s) instead of 1')
        return paths[0]

    @property
    def val(self):
        """Raw data of the tree"""
        return self._raw_data()

    def _raw_data(self, address=None):
        """Access the raw data at path"""
        if address is None: address = '/'
        path = self._find_unique(address)
        tmp = self._data
        for key in path:
            try:
                tmp = tmp[key]
            except TypeError:
                tmp = tmp[int(key)]
        return tmp

    def copy(self):
        """Return a fully separate copy of current tree"""
        return Tree(copy.deepcopy(self._data))


class Tree(_TreeUtils):
    """Container class for a nested object
    
    Nested objects are JSON-valid data: a dict, containing lists and dicts of
    integers, floats and strings.
    """
    def __init__(self, data=None):
        self.__dict__['_data'] = {} if data is None else data
        self.__dict__['_root'] = Path('/')
        self.__dict__['_tree'] = self

    def __getitem__(self, key):
        path = self._find_unique(key)
        return TreeView(self, path)


class TreeView(_TreeUtils):
    """View of a Tree object
    
    Behavec very similarly to its reference Tree object, but all actions
    are performed on the Tree memory directly.
    """
    def __init__(self, tree, path):
        self.__dict__['_tree'] = tree
        self.__dict__['_root'] = tree._find_unique(path)
    
    def __getitem__(self, key):
        path = self._find_unique(key)
        return TreeView(self._tree, self._root / path)

    def __set__(self, instance, value):
        self.set(value)

    def set(self, value):
        """Set the value of self"""
        self._tree._raw_data(self._root.parent)[self._root[-1]] = value

    def __str__(self):
        """Printable reprensentation"""
        return f'TreeView({str(self._root)})'
    
    @property
    def _data(self):
        return self._tree._raw_data(self._root)
