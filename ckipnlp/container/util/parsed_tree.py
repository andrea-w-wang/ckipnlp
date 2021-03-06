#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides tree containers for sentence parsing.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'


from collections import (
    deque as _deque,
    OrderedDict as _OrderedDict,
)

from typing import (
    NamedTuple as _NamedTuple,
)

from treelib import (
    Tree as _Tree,
    Node as _Node,
)

from ckipnlp.data.parsed import (
    SUBJECT_ROLES as _SUBJECT_ROLES,
    NEUTRAL_ROLES as _NEUTRAL_ROLES,
)

from ..base import (
    Base as _Base,
    BaseTuple as _BaseTuple,
)

################################################################################################################################

class _ParsedNodeData(_NamedTuple):
    role: str = None
    pos: str = None
    word: str = None

class ParsedNodeData(_BaseTuple, _ParsedNodeData):
    """A parser node.

    Attributes
    ----------
        role : str
            the semantic role.
        pos : str
            the POS-tag.
        word : str
            the text term.

    Note
    ----
        This class is an subclass of :class:`tuple`. To change the attribute, please create a new instance instead.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`from_text` and :meth:`to_text`.

            .. code-block:: python

                'Head:Na:中文字'  # role / POS-tag / text-term

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                {
                    'role': 'Head',   # role
                    'pos': 'Na',      # POS-tag
                    'word': '中文字',  # text term
                }

        List format
            Not implemented.
    """

    from_list = NotImplemented
    to_list = NotImplemented

    @classmethod
    def from_text(cls, data):
        """Construct an instance from text format.

        Parameters
        ----------
            data : str
                text such as ``'Head:Na:中文字'``.

        .. note::

            - ``'Head:Na:中文字'`` -> **role** = ``'Head'``, **pos** = ``'Na'``, **word** = ``'中文字'``
            - ``'Head:Na'``       -> **role** = ``'Head'``, **pos** = ``'Na'``, **word** = ``None``
            - ``'Na'``            -> **role** = ``None``,   **pos** = ``'Na'``, **word** = ``None``
        """
        if ':' in data:
            fields = data.split(':')
            return cls(*fields)
        return cls(pos=data)  # pylint: disable=no-value-for-parameter

    def to_text(self):
        return ':'.join(filter(None, self))

################################################################################################################################

class ParsedNode(_Base, _Node):
    """A parser node for tree.

    Attributes
    ----------
        data : :class:`ParsedNodeData`

    See Also
    --------
        treelib.tree.Node: Please refer `<https://treelib.readthedocs.io/>`_ for built-in usages.

    .. admonition:: Data Structure Examples

        Text format
            Not implemented.

        Dict format
            Used for :meth:`to_dict`.

            .. code-block:: python

                {
                    'role': 'Head',   # role
                    'pos': 'Na',      # POS-tag
                    'word': '中文字',  # text term
                }

        List format
            Not implemented.
    """

    data_class = ParsedNodeData

    from_dict = NotImplemented

    from_text = NotImplemented
    to_text = NotImplemented
    from_list = NotImplemented
    to_list = NotImplemented

    def __repr__(self):
        return '{name}(tag={tag}, identifier={identifier})'.format(
            name=self.__class__.__name__,
            tag=self.tag,
            identifier=self.identifier,
        )

    def to_dict(self):
        return _OrderedDict(id=self.identifier, data=self.data.to_dict())

################################################################################################################################

class _ParsedRelation(_NamedTuple):
    head: ParsedNode
    tail: ParsedNode
    relation: ParsedNode

class ParsedRelation(_Base, _ParsedRelation):
    """A parser relation.

    Attributes
    ----------
        head : :class:`ParsedNode`
            the head node.
        tail : :class:`ParsedNode`
            the tail node.
        relation : :class:`ParsedNode`
            the relation node. (the semantic role of this node is the relation.)

    Notes
    -----
        The parent of the relation node is always the common ancestor of the head node and tail node.

    .. admonition:: Data Structure Examples

        Text format
            Not implemented.

        Dict format
            Used for :meth:`to_dict`.

            .. code-block:: python

                {
                    'tail': { 'role': 'Head', 'pos': 'Nab', 'word': '中文字' }, # head node
                    'tail': { 'role': 'particle', 'pos': 'Td', 'word': '耶' }, # tail node
                    'relation': 'particle',  # relation
                }

        List format
            Not implemented.
    """

    from_dict = NotImplemented

    from_text = NotImplemented
    to_text = NotImplemented
    from_list = NotImplemented
    to_list = NotImplemented

    def __repr__(self):
        ret = '{name}(head={head}, tail={tail}, relation={relation})' if self.head_first \
         else '{name}(tail={tail}, head={head}, relation={relation})'
        return ret.format(
            name=type(self).__name__,
            head=(self.head.tag, self.head.identifier,),
            tail=(self.tail.tag, self.tail.identifier,),
            relation=(self.relation.data.role, self.relation.identifier,),
        )

    @property
    def head_first(self):  # pylint: disable=missing-docstring
        return self.head.identifier <= self.tail.identifier

    def to_dict(self):
        return _OrderedDict(head=self.head.to_dict(), tail=self.head.to_dict(), relation=self.relation.data.role)

################################################################################################################################

class ParsedTree(_Base, _Tree):
    """A parsed tree.

    See Also
    --------
        treereelib.tree.Tree: Please refer `<https://treelib.readthedocs.io/>`_ for built-in usages.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`from_text` and :meth:`to_text`.

            .. code-block:: python

                'S(Head:Nab:中文字|particle:Td:耶)'

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.
            A dictionary such as ``{ 'id': 0, 'data': { ... }, 'children': [ ... ] }``,
            where ``'data'`` is a dictionary with the same format as :meth:`ParsedNodeData.to_dict`,
            and ``'children'`` is a list of dictionaries of subtrees with the same format as this tree.

            .. code-block:: python

                {
                    'id': 0,
                    'data': {
                        'role': None,
                        'pos': 'S',
                        'word': None,
                    },
                    'children': [
                        {
                            'id': 1,
                            'data': {
                                'role': 'Head',
                                'pos': 'Nab',
                                'word': '中文字',
                            },
                            'children': [],
                        },
                        {
                            'id': 2,
                            'data': {
                                'role': 'particle',
                                'pos': 'Td',
                                'word': '耶',
                            },
                            'children': [],
                        },
                    ],
                }

        List format
            Not implemented.
    """

    node_class = ParsedNode

    from_list = NotImplemented
    to_list = NotImplemented

    @staticmethod
    def normalize_text(tree_text):
        """Text normalization.

        Remove leading number and trailing ``#``.
        """
        if '#' in tree_text:
            tree_text = tree_text.split('] ', 2)[-1].rstrip('#')
        return tree_text

    def __str__(self):
        self.to_text()

    @classmethod
    def from_text(cls, data, *, normalize=True):
        """Construct an instance from text format.

        Parameters
        ----------
            data : str
                A parsed tree in text format.
            normalize : bool
                Do text normalization using :meth:`normalize_text`.
        """
        if normalize:
            data = cls.normalize_text(data)

        tree = cls()
        node_id = 0
        node_queue = [None]
        text = ''
        ending = True

        for char in data:
            if char == '(':
                node_data = cls.node_class.data_class.from_text(text)
                tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)

                node_queue.append(node_id)
                node_id += 1
                text = ''

            elif char == ')':
                if not ending:
                    node_data = cls.node_class.data_class.from_text(text)
                    tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)
                    node_id += 1

                node_queue.pop()
                text = ''
                ending = True

            elif char == '|':
                if not ending:
                    node_data = cls.node_class.data_class.from_text(text)
                    tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)
                    node_id += 1

                text = ''
                ending = True

            else:
                ending = False
                text += char

        return tree

    def to_text(self, node_id=None):
        """Transform to plain text.

        Parameters
        ----------
            node_id : int
                Output the plain text format for the subtree under **node_id**.

        Returns
        --------
            str
        """
        if node_id is None:
            node_id = self.root

        node = self[node_id]
        tree_text = node.data.to_text()

        children_text = '|'.join((self.to_text(child.identifier) for child in self.children(node_id)))
        if children_text:
            tree_text = '{}({})'.format(tree_text, children_text)

        return tree_text

    @classmethod
    def from_dict(cls, data):
        """Construct an instance a from python built-in containers.

        Parameters
        ----------
            data : str
                A parsed tree in dictionary format.
        """
        tree = cls()

        queue = _deque()
        queue.append((data, None,))

        while queue:
            node_dict, parent_id = queue.popleft()
            node_id = node_dict['id']
            node_data = cls.node_class.data_class.from_dict(node_dict['data'])
            tree.create_node(tag=node_data.to_text(), identifier=node_id, parent=parent_id, data=node_data)

            for child in node_dict['children']:
                queue.append((child, node_id,))

        return tree

    def to_dict(self, node_id=None):
        """Construct an instance a from python built-in containers.

        Parameters
        ----------
            node_id : int
                Output the plain text format for the subtree under **node_id**.

        Returns
        -------
            str
        """
        if node_id is None:
            node_id = self.root

        tree_dict = self[node_id].to_dict()
        tree_dict['children'] = []

        for child in self.children(node_id):
            tree_dict['children'].append(self.to_dict(child.identifier))

        return tree_dict

    def show(self, *,
        key=lambda node: node.identifier,
        idhidden=False,
        **kwargs,
    ):
        """Show pretty tree."""
        _Tree.show(self, key=key, idhidden=idhidden, **kwargs)

    def get_children(self, node_id, *, role):
        """Get children of a node with given role.

        Parameters
        ----------
            node_id : int
                ID of target node.
            role : str
                the target role.

        Yields
        ------
            :class:`ParsedNode`
                the children nodes with given role.
        """
        for child in self.children(node_id):
            if child.data.role == role:
                yield child

    def get_heads(self, root_id=None, *, semantic=True, deep=True):
        """Get all head nodes of a subtree.

        Parameters
        ----------
            root_id : int
                ID of the root node of target subtree.
            semantic : bool
                use semantic/syntactic policy. For semantic mode, return ``DUMMY`` or ``head`` instead of syntactic ``Head``.
            deep : bool
                find heads recursively.

        Yields
        ------
            :class:`ParsedNode`
                the head nodes.
        """
        if root_id is None:
            root_id = self.root

        head_nodes = []
        children = list(self.children(root_id))

        # No child, choose the root node instead
        if not children:
            head_nodes.append(self[root_id])

        # Semantic mode
        if semantic:
            # Find DUMMY
            if not head_nodes:
                for child in children:
                    if child.data.role in ('DUMMY', 'DUMMY1', 'DUMMY2',):
                        head_nodes.append(child)

            # Find head
            if not head_nodes:
                for child in children:
                    if child.data.role == 'head':
                        head_nodes.append(child)

        # Find Head
        if not head_nodes:
            for child in children:
                if child.data.role == 'Head':
                    head_nodes.append(child)

        # Found no head, choose the last child instead
        if not head_nodes:
            head_nodes.append(children[-1])

        # Recursion
        for node in head_nodes:
            if deep and not node.is_leaf():
                yield from self.get_heads(node.identifier, semantic=semantic)
            else:
                yield node

    def get_relations(self, root_id=None, *, semantic=True):
        """Get all relations of a subtree.

        Parameters
        ----------
            root_id : int
                ID of the subtree root node.
            semantic : bool
                please refer :meth:`get_heads` for policy detail.

        Yields
        ------
            :class:`ParsedRelation`
                the relations.
        """
        if root_id is None:
            root_id = self.root

        children = list(self.children(root_id))
        head_children = list(self.get_heads(root_id, semantic=semantic, deep=False))

        # Get heads
        for head_node in self.get_heads(root_id, semantic=semantic):
            # Get tails
            for tail in children:
                if tail.data.role != 'Head' and tail not in head_children:
                    if tail.is_leaf():
                        yield ParsedRelation(head=head_node, tail=tail, relation=tail)  # pylint: disable=no-value-for-parameter
                    else:
                        for node in self.get_heads(tail.identifier, semantic=semantic):
                            yield ParsedRelation(head=head_node, tail=node, relation=tail)  # pylint: disable=no-value-for-parameter

        # Recursion
        for child in children:
            yield from self.get_relations(child.identifier, semantic=semantic)

    def get_subjects(self, root_id=None, *, semantic=True, deep=True):
        """Get the subject node of a subtree.

        Parameters
        ----------
            root_id : int
                ID of the root node of target subtree.
            semantic : bool
                please refer :meth:`get_heads` for policy detail.
            deep : bool
                please refer :meth:`get_heads` for policy detail.

        Yields
        ------
            :class:`ParsedNode`
                the subject node.

        Notes
        -----
            A node can be a subject if either:

            1. is a head of `NP`
            2. is a head of a subnode (`N`) of `S` with subject role
            3. is a head of a subnode (`N`) of `S` with neutral role and before the head (`V`) of `S`
        """
        if root_id is None:
            root_id = self.root
        root = self[root_id]

        if root.data.pos == 'NP':
            yield from self.get_heads(root.identifier, semantic=semantic, deep=deep)

        elif root.data.pos == 'S':
            for head in self.get_heads(root.identifier, semantic=False, deep=False):
                if head.data.pos.startswith('V'):
                    for subroot in self.children(root.identifier):
                        if subroot.data.pos.startswith('N') and ( \
                            subroot.data.role in _SUBJECT_ROLES or \
                           (subroot.data.role in _NEUTRAL_ROLES and subroot.identifier < head.identifier) \
                        ):
                            yield from self.get_heads(subroot.identifier, semantic=semantic, deep=deep)
