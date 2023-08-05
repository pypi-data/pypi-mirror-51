from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import twodlearn as tdl
import twodlearn.core


class Normalizer(tdl.core.TdlModel):
    @tdl.core.InputParameter
    def loc(self, value):
        if isinstance(value, np.ndarray):
            return tf.Variable(value, trainable=False,
                               dtype=tdl.core.global_options.float.tftype)
        else:
            return value

    @tdl.core.InputParameter
    def scale(self, value):
        if isinstance(value, np.ndarray):
            return tf.Variable(value, trainable=False,
                               dtype=tdl.core.global_options.float.tftype)
        else:
            return value

    def __init__(self, loc, scale, name='Normalizer'):
        super(Normalizer, self).__init__(
            loc=loc, scale=scale, name=name, options=None)

    class NormalizerOutput(tdl.core.OutputModel):
        @tdl.core.InferenceInput
        def inputs(self, value):
            return value

    @tdl.ModelMethod(['y', 'value'], ['inputs'], NormalizerOutput)
    def normalize(self, object, inputs):
        inputs = tf.convert_to_tensor(inputs)
        y = (inputs - self.loc) / self.scale
        return y, y

    @tdl.ModelMethod(['y', 'value'], ['inputs'])
    def denormalize(self, object, inputs):
        inputs = tf.convert_to_tensor(inputs)
        y = (self.scale * inputs) + self.loc
        return y, y

    def __call__(self, x, name=None):
        return self.normalize(inputs=x, name=None)


class NormalizeLayer(tdl.core.Layer):
    @tdl.core.InputArgument
    def input_shape(self, value):
        if value is None:
            raise tdl.core.exceptions.ArgumentNotProvided(self)
        if not isinstance(value, tf.TensorShape):
            value = tf.TensorShape(value)
        return value

    @tdl.core.InputParameter
    def loc(self, value):
        if isinstance(value, np.ndarray):
            return tf.Variable(value, trainable=False,
                               dtype=tdl.core.global_options.float.tftype)
        else:
            return value

    @tdl.core.InputParameter
    def scale(self, value):
        if isinstance(value, np.ndarray):
            return tf.Variable(value, trainable=False,
                               dtype=tdl.core.global_options.float.tftype)
        else:
            return value

    def __init__(self, loc, scale, name=None):
        super(NormalizeLayer, self).__init__(
            loc=loc, scale=scale, name=name)

    def call(self, inputs):
        inputs = tf.convert_to_tensor(inputs)
        y = (inputs - self.loc) / self.scale
        return y
