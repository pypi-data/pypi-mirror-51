# coding: utf-8

"""
    FeersumNLU API

    This is the HTTP API for Feersum NLU. See https://github.com/praekelt/feersum-nlu-api-wrappers for examples of how to use the API.  # noqa: E501

    OpenAPI spec version: 2.0.37
    Contact: nlu@feersum.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class SynonymEntityExtractorInstanceDetail(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'id': 'str',
        'long_name': 'str',
        'desc': 'str',
        'readonly': 'bool',
        'training_accuracy': 'float',
        'training_f1': 'float',
        'validation_accuracy': 'float',
        'validation_f1': 'float',
        'testing_accuracy': 'float',
        'testing_f1': 'float',
        'training_stamp': 'str',
        'num_training_samples': 'int',
        'num_testing_samples': 'int',
        'threshold': 'float'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'long_name': 'long_name',
        'desc': 'desc',
        'readonly': 'readonly',
        'training_accuracy': 'training_accuracy',
        'training_f1': 'training_f1',
        'validation_accuracy': 'validation_accuracy',
        'validation_f1': 'validation_f1',
        'testing_accuracy': 'testing_accuracy',
        'testing_f1': 'testing_f1',
        'training_stamp': 'training_stamp',
        'num_training_samples': 'num_training_samples',
        'num_testing_samples': 'num_testing_samples',
        'threshold': 'threshold'
    }

    def __init__(self, name=None, id=None, long_name=None, desc=None, readonly=None, training_accuracy=None, training_f1=None, validation_accuracy=None, validation_f1=None, testing_accuracy=None, testing_f1=None, training_stamp=None, num_training_samples=None, num_testing_samples=None, threshold=None):  # noqa: E501
        """SynonymEntityExtractorInstanceDetail - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._id = None
        self._long_name = None
        self._desc = None
        self._readonly = None
        self._training_accuracy = None
        self._training_f1 = None
        self._validation_accuracy = None
        self._validation_f1 = None
        self._testing_accuracy = None
        self._testing_f1 = None
        self._training_stamp = None
        self._num_training_samples = None
        self._num_testing_samples = None
        self._threshold = None
        self.discriminator = None

        self.name = name
        self.id = id
        if long_name is not None:
            self.long_name = long_name
        if desc is not None:
            self.desc = desc
        if readonly is not None:
            self.readonly = readonly
        if training_accuracy is not None:
            self.training_accuracy = training_accuracy
        if training_f1 is not None:
            self.training_f1 = training_f1
        if validation_accuracy is not None:
            self.validation_accuracy = validation_accuracy
        if validation_f1 is not None:
            self.validation_f1 = validation_f1
        if testing_accuracy is not None:
            self.testing_accuracy = testing_accuracy
        if testing_f1 is not None:
            self.testing_f1 = testing_f1
        if training_stamp is not None:
            self.training_stamp = training_stamp
        if num_training_samples is not None:
            self.num_training_samples = num_training_samples
        if num_testing_samples is not None:
            self.num_testing_samples = num_testing_samples
        if threshold is not None:
            self.threshold = threshold

    @property
    def name(self):
        """Gets the name of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The sluggy-url-friendly-name of the instance.  # noqa: E501

        :return: The name of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SynonymEntityExtractorInstanceDetail.

        The sluggy-url-friendly-name of the instance.  # noqa: E501

        :param name: The name of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def id(self):
        """Gets the id of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The unique id of a specific version of the model instance.  # noqa: E501

        :return: The id of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SynonymEntityExtractorInstanceDetail.

        The unique id of a specific version of the model instance.  # noqa: E501

        :param id: The id of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def long_name(self):
        """Gets the long_name of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The human-friendly-name of the instance.  # noqa: E501

        :return: The long_name of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._long_name

    @long_name.setter
    def long_name(self, long_name):
        """Sets the long_name of this SynonymEntityExtractorInstanceDetail.

        The human-friendly-name of the instance.  # noqa: E501

        :param long_name: The long_name of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: str
        """

        self._long_name = long_name

    @property
    def desc(self):
        """Gets the desc of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The longer existential description of this instance's purpose in life.  # noqa: E501

        :return: The desc of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._desc

    @desc.setter
    def desc(self, desc):
        """Sets the desc of this SynonymEntityExtractorInstanceDetail.

        The longer existential description of this instance's purpose in life.  # noqa: E501

        :param desc: The desc of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: str
        """

        self._desc = desc

    @property
    def readonly(self):
        """Gets the readonly of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        Indicates if the model is readonly and not editable.  # noqa: E501

        :return: The readonly of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: bool
        """
        return self._readonly

    @readonly.setter
    def readonly(self, readonly):
        """Sets the readonly of this SynonymEntityExtractorInstanceDetail.

        Indicates if the model is readonly and not editable.  # noqa: E501

        :param readonly: The readonly of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: bool
        """

        self._readonly = readonly

    @property
    def training_accuracy(self):
        """Gets the training_accuracy of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The accuracy of the model as measured on the training set.  # noqa: E501

        :return: The training_accuracy of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: float
        """
        return self._training_accuracy

    @training_accuracy.setter
    def training_accuracy(self, training_accuracy):
        """Sets the training_accuracy of this SynonymEntityExtractorInstanceDetail.

        The accuracy of the model as measured on the training set.  # noqa: E501

        :param training_accuracy: The training_accuracy of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: float
        """

        self._training_accuracy = training_accuracy

    @property
    def training_f1(self):
        """Gets the training_f1 of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The average F-score of the model as measured on the training set.  # noqa: E501

        :return: The training_f1 of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: float
        """
        return self._training_f1

    @training_f1.setter
    def training_f1(self, training_f1):
        """Sets the training_f1 of this SynonymEntityExtractorInstanceDetail.

        The average F-score of the model as measured on the training set.  # noqa: E501

        :param training_f1: The training_f1 of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: float
        """

        self._training_f1 = training_f1

    @property
    def validation_accuracy(self):
        """Gets the validation_accuracy of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The accuracy of the model as measured by cross validation on the training set.  # noqa: E501

        :return: The validation_accuracy of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: float
        """
        return self._validation_accuracy

    @validation_accuracy.setter
    def validation_accuracy(self, validation_accuracy):
        """Sets the validation_accuracy of this SynonymEntityExtractorInstanceDetail.

        The accuracy of the model as measured by cross validation on the training set.  # noqa: E501

        :param validation_accuracy: The validation_accuracy of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: float
        """

        self._validation_accuracy = validation_accuracy

    @property
    def validation_f1(self):
        """Gets the validation_f1 of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The average F-score of the model as measured by cross validation on the training set.  # noqa: E501

        :return: The validation_f1 of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: float
        """
        return self._validation_f1

    @validation_f1.setter
    def validation_f1(self, validation_f1):
        """Sets the validation_f1 of this SynonymEntityExtractorInstanceDetail.

        The average F-score of the model as measured by cross validation on the training set.  # noqa: E501

        :param validation_f1: The validation_f1 of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: float
        """

        self._validation_f1 = validation_f1

    @property
    def testing_accuracy(self):
        """Gets the testing_accuracy of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The accuracy of the model as measured on the testing set.  # noqa: E501

        :return: The testing_accuracy of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: float
        """
        return self._testing_accuracy

    @testing_accuracy.setter
    def testing_accuracy(self, testing_accuracy):
        """Sets the testing_accuracy of this SynonymEntityExtractorInstanceDetail.

        The accuracy of the model as measured on the testing set.  # noqa: E501

        :param testing_accuracy: The testing_accuracy of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: float
        """

        self._testing_accuracy = testing_accuracy

    @property
    def testing_f1(self):
        """Gets the testing_f1 of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The average F-score of the model as measured on the testing set.  # noqa: E501

        :return: The testing_f1 of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: float
        """
        return self._testing_f1

    @testing_f1.setter
    def testing_f1(self, testing_f1):
        """Sets the testing_f1 of this SynonymEntityExtractorInstanceDetail.

        The average F-score of the model as measured on the testing set.  # noqa: E501

        :param testing_f1: The testing_f1 of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: float
        """

        self._testing_f1 = testing_f1

    @property
    def training_stamp(self):
        """Gets the training_stamp of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The time when the training operation concluded.  # noqa: E501

        :return: The training_stamp of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._training_stamp

    @training_stamp.setter
    def training_stamp(self, training_stamp):
        """Sets the training_stamp of this SynonymEntityExtractorInstanceDetail.

        The time when the training operation concluded.  # noqa: E501

        :param training_stamp: The training_stamp of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: str
        """

        self._training_stamp = training_stamp

    @property
    def num_training_samples(self):
        """Gets the num_training_samples of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The model's number of training samples.  # noqa: E501

        :return: The num_training_samples of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: int
        """
        return self._num_training_samples

    @num_training_samples.setter
    def num_training_samples(self, num_training_samples):
        """Sets the num_training_samples of this SynonymEntityExtractorInstanceDetail.

        The model's number of training samples.  # noqa: E501

        :param num_training_samples: The num_training_samples of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: int
        """

        self._num_training_samples = num_training_samples

    @property
    def num_testing_samples(self):
        """Gets the num_testing_samples of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        The model's number of testing samples.  # noqa: E501

        :return: The num_testing_samples of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: int
        """
        return self._num_testing_samples

    @num_testing_samples.setter
    def num_testing_samples(self, num_testing_samples):
        """Sets the num_testing_samples of this SynonymEntityExtractorInstanceDetail.

        The model's number of testing samples.  # noqa: E501

        :param num_testing_samples: The num_testing_samples of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: int
        """

        self._num_testing_samples = num_testing_samples

    @property
    def threshold(self):
        """Gets the threshold of this SynonymEntityExtractorInstanceDetail.  # noqa: E501

        There is typically some model dependent threshold to be set upon training and which is possibly mutable post training. This is that threshold.  # noqa: E501

        :return: The threshold of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: float
        """
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        """Sets the threshold of this SynonymEntityExtractorInstanceDetail.

        There is typically some model dependent threshold to be set upon training and which is possibly mutable post training. This is that threshold.  # noqa: E501

        :param threshold: The threshold of this SynonymEntityExtractorInstanceDetail.  # noqa: E501
        :type: float
        """

        self._threshold = threshold

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(SynonymEntityExtractorInstanceDetail, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SynonymEntityExtractorInstanceDetail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
