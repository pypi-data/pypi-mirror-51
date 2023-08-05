import re
import logging
import collections

from ...vendor.Qt import QtCore, QtWidgets
from ...vendor import qtawesome as awesome
from ... import io
from ... import style

log = logging.getLogger(__name__)


class Node(dict):
    """A node that can be represented in a tree view.

    The node can store data just like a dictionary.

    >>> data = {"name": "John", "score": 10}
    >>> node = Node(data)
    >>> assert node["name"] == "John"

    """

    def __init__(self, data=None):
        super(Node, self).__init__()

        self._children = list()
        self._parent = None

        if data is not None:
            assert isinstance(data, dict)
            self.update(data)

    def childCount(self):
        return len(self._children)

    def child(self, row):

        if row >= len(self._children):
            log.warning("Invalid row as child: {0}".format(row))
            return

        return self._children[row]

    def children(self):
        return self._children

    def parent(self):
        return self._parent

    def row(self):
        """
        Returns:
             int: Index of this node under parent"""
        if self._parent is not None:
            siblings = self.parent().children()
            return siblings.index(self)

    def add_child(self, child):
        """Add a child to this node"""
        child._parent = self
        self._children.append(child)


class TreeModel(QtCore.QAbstractItemModel):

    COLUMNS = list()
    NodeRole = QtCore.Qt.UserRole + 1

    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)
        self._root_node = Node()

    def rowCount(self, parent):
        if parent.isValid():
            node = parent.internalPointer()
        else:
            node = self._root_node

        return node.childCount()

    def columnCount(self, parent):
        return len(self.COLUMNS)

    def data(self, index, role):

        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:

            node = index.internalPointer()
            column = index.column()

            key = self.COLUMNS[column]
            return node.get(key, None)

        if role == self.NodeRole:
            return index.internalPointer()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """Change the data on the nodes.

        Returns:
            bool: Whether the edit was successful
        """

        if index.isValid():
            if role == QtCore.Qt.EditRole:

                node = index.internalPointer()
                column = index.column()
                key = self.COLUMNS[column]
                node[key] = value

                # passing `list()` for PyQt5 (see PYSIDE-462)
                self.dataChanged.emit(index, index, list())

                # must return true if successful
                return True

        return False

    def setColumns(self, keys):
        assert isinstance(keys, (list, tuple))
        self.COLUMNS = keys

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:
            if section < len(self.COLUMNS):
                return self.COLUMNS[section]

        super(TreeModel, self).headerData(section, orientation, role)

    def flags(self, index):
        return (
            QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsSelectable
        )

    def parent(self, index):

        node = index.internalPointer()
        parent_node = node.parent()

        # If it has no parents we return invalid
        if parent_node == self._root_node or not parent_node:
            return QtCore.QModelIndex()

        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        """Return index for row/column under parent"""

        if not parent.isValid():
            parentNode = self._root_node
        else:
            parentNode = parent.internalPointer()

        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def add_child(self, node, parent=None):
        if parent is None:
            parent = self._root_node

        parent.add_child(node)

    def column_name(self, column):
        """Return column key by index"""

        if column < len(self.COLUMNS):
            return self.COLUMNS[column]

    def clear(self):
        self.beginResetModel()
        self._root_node = Node()
        self.endResetModel()


class TasksModel(TreeModel):
    """A model listing the tasks combined for a list of assets"""

    COLUMNS = ["name", "count"]

    def __init__(self):
        super(TasksModel, self).__init__()
        self._num_assets = 0
        self._icons = {
            "__default__": awesome.icon("fa.male", color=style.colors.default)
        }

        self._get_task_icons()

    def _get_task_icons(self):
        # Get the project configured icons from database
        project = io.find_one({"type": "project"})
        tasks = project['config'].get('tasks', [])
        for task in tasks:
            icon_name = task.get("icon", None)
            if icon_name:
                icon = awesome.icon("fa.{}".format(icon_name),
                                    color=style.colors.default)
                self._icons[task["name"]] = icon

    def set_assets(self, asset_ids):
        """Set assets to track by their database id

        Arguments:
            asset_ids (list): List of asset ids.

        """

        assets = list()
        for asset_id in asset_ids:
            asset = io.find_one({"_id": asset_id, "type": "asset"})
            assert asset, "Asset not found by id: {0}".format(asset_id)
            assets.append(asset)

        self._num_assets = len(assets)

        tasks = collections.Counter()
        for asset in assets:
            asset_tasks = asset.get("data", {}).get("tasks", [])
            tasks.update(asset_tasks)

        self.clear()
        self.beginResetModel()

        default_icon = self._icons["__default__"]
        for task, count in sorted(tasks.items()):
            icon = self._icons.get(task, default_icon)

            node = Node({
                "name": task,
                "count": count,
                "icon": icon
            })

            self.add_child(node)

        self.endResetModel()

    def headerData(self, section, orientation, role):

        # Override header for count column to show amount of assets
        # it is listing the tasks for
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 1:  # count column
                    return "count ({0})".format(self._num_assets)

        return super(TasksModel, self).headerData(section, orientation, role)

    def data(self, index, role):

        if not index.isValid():
            return

        # Add icon to the first column
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                return index.internalPointer()['icon']

        return super(TasksModel, self).data(index, role)


class DeselectableTreeView(QtWidgets.QTreeView):
    """A tree view that deselects on clicking on an empty area in the view"""

    def mousePressEvent(self, event):

        index = self.indexAt(event.pos())
        if not index.isValid():
            # clear the selection
            self.clearSelection()
            # clear the current index
            self.setCurrentIndex(QtCore.QModelIndex())

        QtWidgets.QTreeView.mousePressEvent(self, event)


class ExactMatchesFilterProxyModel(QtCore.QSortFilterProxyModel):
    """Filter model to where key column's value is in the filtered tags"""

    def __init__(self, *args, **kwargs):
        super(ExactMatchesFilterProxyModel, self).__init__(*args, **kwargs)
        self._filters = set()

    def setFilters(self, filters):
        self._filters = set(filters)

    def filterAcceptsRow(self, source_row, source_parent):

        # No filter
        if not self._filters:
            return True

        else:
            model = self.sourceModel()
            column = self.filterKeyColumn()
            idx = model.index(source_row, column, source_parent)
            data = model.data(idx, self.filterRole())
            if data in self._filters:
                return True
            else:
                return False


class RecursiveSortFilterProxyModel(QtCore.QSortFilterProxyModel):
    """Filters to the regex if any of the children matches allow parent"""
    def filterAcceptsRow(self, row, parent):

        regex = self.filterRegExp()
        if not regex.isEmpty():
            pattern = regex.pattern()
            model = self.sourceModel()
            source_index = model.index(row, self.filterKeyColumn(), parent)
            if source_index.isValid():

                # Check current index itself
                key = model.data(source_index, self.filterRole())
                if re.search(pattern, key, re.IGNORECASE):
                    return True

                # Check children
                rows = model.rowCount(source_index)
                for i in range(rows):
                    if self.filterAcceptsRow(i, source_index):
                        return True

                # Otherwise filter it
                return False

        return super(RecursiveSortFilterProxyModel,
                     self).filterAcceptsRow(row, parent)
