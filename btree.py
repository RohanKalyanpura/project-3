# btree.py
from node import Node
from utils import MAX_KEYS, T

class BTree:
    def __init__(self, index_file):
        self.ifile = index_file
        self.node_cache = {}
        self.cache_access_order = []

    def _cache_node(self, node):
        if node.block_id not in self.node_cache:
            if len(self.node_cache) >= 3:
                # Remove LRU
                lru = self.cache_access_order.pop(0)
                self._flush_node(self.node_cache[lru])
                del self.node_cache[lru]
            self.node_cache[node.block_id] = node
            self.cache_access_order.append(node.block_id)
        else:
            self.cache_access_order.remove(node.block_id)
            self.cache_access_order.append(node.block_id)

    def _flush_node(self, node):
        node.write_to_file(self.ifile.f)

    def _get_node(self, block_id):
        if block_id == 0:
            return None
        if block_id in self.node_cache:
            self.cache_access_order.remove(block_id)
            self.cache_access_order.append(block_id)
            return self.node_cache[block_id]

        node = Node.read_from_file(self.ifile.f, block_id)
        self._cache_node(node)
        return node

    def _put_node(self, node):
        self._cache_node(node)

    def initialize_empty_tree(self):
        root_id = self.ifile.allocate_new_block()
        root = Node(block_id=root_id, parent_id=0, num_keys=0)
        self._put_node(root)
        self.ifile.root_block_id = root_id
        self.ifile.update_header()

    def load_root(self):
        pass

    def close(self):
        for n in self.node_cache.values():
            self._flush_node(n)
        self.node_cache.clear()
        self.ifile.close()

    def search(self, key):
        return self._search_node(self.ifile.root_block_id, key)

    def _search_node(self, block_id, key):
        if block_id == 0:
            return None
        node = self._get_node(block_id)
        i = 0
        while i < node.num_keys and key > node.keys[i]:
            i += 1
        if i < node.num_keys and node.keys[i] == key:
            return node.values[i]
        if node.children[i] == 0:
            return None
        else:
            return self._search_node(node.children[i], key)

    def insert(self, key, value):
        root_id = self.ifile.root_block_id
        if root_id == 0:
            self.initialize_empty_tree()
            root_id = self.ifile.root_block_id

        root = self._get_node(root_id)
        if root.num_keys == MAX_KEYS:
            new_root_id = self.ifile.allocate_new_block()
            new_root = Node(block_id=new_root_id, parent_id=0, num_keys=0)
            new_root.children[0] = root.block_id
            root.parent_id = new_root_id
            self._put_node(root)
            self._put_node(new_root)
            self._split_child(new_root, 0)
            self._insert_nonfull(new_root, key, value)
            self.ifile.root_block_id = new_root_id
            self.ifile.update_header()
        else:
            self._insert_nonfull(root, key, value)

    def _insert_nonfull(self, node, key, value):
        i = node.num_keys - 1
        if node.children[0] == 0:
            # Leaf
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                node.values[i+1] = node.values[i]
                i -= 1
            node.keys[i+1] = key
            node.values[i+1] = value
            node.num_keys += 1
            self._put_node(node)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            child = self._get_node(node.children[i])
            if child.num_keys == MAX_KEYS:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            child = self._get_node(node.children[i])
            self._insert_nonfull(child, key, value)

    def _split_child(self, parent, i):
        full_child = self._get_node(parent.children[i])
        new_child_id = self.ifile.allocate_new_block()
        new_child = Node(block_id=new_child_id, parent_id=parent.block_id, num_keys=T-1)

        for j in range(T-1):
            new_child.keys[j] = full_child.keys[j+T]
            new_child.values[j] = full_child.values[j+T]

        if full_child.children[0] != 0:
            for j in range(T):
                new_child.children[j] = full_child.children[j+T]

        full_child.num_keys = T-1

        for j in range(parent.num_keys, i, -1):
            parent.children[j+1] = parent.children[j]
        parent.children[i+1] = new_child.block_id

        for j in range(parent.num_keys-1, i-1, -1):
            parent.keys[j+1] = parent.keys[j]
            parent.values[j+1] = parent.values[j]

        parent.keys[i] = full_child.keys[T-1]
        parent.values[i] = full_child.values[T-1]
        parent.num_keys += 1

        self._put_node(full_child)
        self._put_node(new_child)
        self._put_node(parent)

    def print_all(self):
        if self.ifile.root_block_id == 0:
            return
        self._print_inorder(self.ifile.root_block_id)

    def _print_inorder(self, block_id):
        if block_id == 0:
            return
        node = self._get_node(block_id)
        for i in range(node.num_keys):
            self._print_inorder(node.children[i])
            print(f"{node.keys[i]}, {node.values[i]}")
        self._print_inorder(node.children[node.num_keys])

    def extract_all(self, filename):
        pairs = []
        self._inorder_collect(self.ifile.root_block_id, pairs)
        if pairs:
            with open(filename, "w") as f:
                for k,v in pairs:
                    f.write(f"{k},{v}\n")

    def _inorder_collect(self, block_id, lst):
        if block_id == 0:
            return
        node = self._get_node(block_id)
        for i in range(node.num_keys):
            self._inorder_collect(node.children[i], lst)
            lst.append((node.keys[i], node.values[i]))
        self._inorder_collect(node.children[node.num_keys], lst)