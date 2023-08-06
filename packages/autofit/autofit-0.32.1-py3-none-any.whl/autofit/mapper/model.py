import copy

from autofit.mapper.model_object import ModelObject
from autofit.tools.promise import Promise


class AbstractModel(ModelObject):
    def __add__(self, other):
        instance = self.__class__()

        def add_items(item_dict):
            for key, value in item_dict.items():
                if isinstance(value, list) and hasattr(instance, key):
                    setattr(instance, key, getattr(instance, key) + value)
                else:
                    setattr(instance, key, value)

        add_items(self.__dict__)
        add_items(other.__dict__)
        return instance

    def copy(self):
        return copy.deepcopy(self)

    def populate(
            self,
            collection
    ):
        return populate(self, collection)

    def object_for_path(self, path: (str,)) -> object:
        """
        Get the object at a given path.

        Parameters
        ----------
        path
            A tuple describing the path to an object in the model tree

        Returns
        -------
        object
            The object
        """
        instance = self
        for name in path:
            instance = getattr(instance, name)
        return instance

    def instances_of(self, cls: type) -> [object]:
        """
        Traverse the model tree returning all instances of the class

        Parameters
        ----------
        cls
            The type of objects to return

        Returns
        -------
        instances
            A list of instances of the type
        """
        return [
            instance for source in
            [
                list(self.__dict__.values())
            ] +
            [
                ls for ls in self.__dict__.values() if
                isinstance(
                    ls,
                    list
                )
            ] for
            instance in
            source if isinstance(
                instance,
                cls
            )
        ]

    def path_instance_tuples_for_class(self, cls: type, ignore_class=None):
        """
        Tuples containing the path tuple and instance for every instance of the class
        in the model tree.

        Parameters
        ----------
        ignore_class
            Children of instances of this class are ignored
        cls
            The type to find instances of

        Returns
        -------
        path_instance_tuples: [((str,), object)]
            Tuples containing the path to and instance of objects of the given type.
        """
        return path_instances_of_class(self, cls, ignore_class=ignore_class)

    def tuples_with_type(self, class_type):
        return list(filter(lambda t: t[0] != "id" and isinstance(t[1], class_type),
                           self.__dict__.items()))


def populate(obj, collection):
    if isinstance(obj, list):
        return [
            populate(item, collection)
            for item in obj
        ]
    if isinstance(obj, dict):
        return {
            key: populate(value, collection)
            for key, value in obj.items()
        }
    if isinstance(obj, Promise):
        return obj.populate(collection)
    try:
        new = copy.deepcopy(obj)
        for key, value in obj.__dict__.items():
            setattr(
                new,
                key,
                populate(value, collection)
            )
        return new
    except (AttributeError, TypeError):
        return obj


def path_instances_of_class(obj, cls, ignore_class=None):
    if ignore_class is not None and isinstance(obj, ignore_class):
        return []
    if isinstance(obj, cls):
        return [(tuple(), obj)]
    results = []
    try:
        for key, value in obj.__dict__.items():
            for item in path_instances_of_class(value, cls, ignore_class=ignore_class):
                results.append(((key, *item[0]), item[1]))
        return results
    except AttributeError:
        return []


class ModelInstance(AbstractModel):
    """
    An object to hold model instances produced by providing arguments to a model mapper.

    @DynamicAttrs
    """

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __getitem__(self, item):
        return self.items[item]

    @property
    def items(self):
        return list(self.dict.values())

    @property
    def dict(self):
        return {key: value for key, value in self.__dict__.items() if
                key not in ("id", "component_number", "item_number")}

    def __len__(self):
        return len(self.items)

    def as_variable(
            self,
            variable_classes=tuple()
    ):
        from autofit.mapper.prior_model.abstract import AbstractPriorModel
        return AbstractPriorModel.from_instance(
            self,
            variable_classes
        )
