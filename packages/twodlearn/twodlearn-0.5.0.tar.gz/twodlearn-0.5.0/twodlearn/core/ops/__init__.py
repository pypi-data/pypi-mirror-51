#  ***********************************************************************
#   Description: This file loads custom defined operations for use on
#
#
#   Created by: Daniel L. Marino (marinodl@vcu.edu)
#    Modern Heuristics Research Group (MHRG)
#    Virginia Commonwealth University (VCU), Richmond, VA
#    http://www.people.vcu.edu/~mmanic/
#
#   ***********************************************************************

import os
import twodlearn
import tensorflow as tf
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import math_ops


# old: os.environ['TWODLEARN_HOME']
TDL_HOME = os.path.dirname(os.path.abspath(twodlearn.__file__))

# -----------------  load my_matmul -------------------- #
_my_matmul_module = tf.load_op_library(os.path.join(
    TDL_HOME, 'core/ops/kernels/my_matmul_op.so'))
my_matmul = _my_matmul_module.my_matmul


@tf.RegisterGradient("MyMatmul")
def _my_matmul_grad(op, dl_dc):
    a = op.inputs[0]
    b = op.inputs[1]

    # dl_da = math_ops.matmul( dl_dc, array_ops.transpose(b, [1,0]))
    # dl_db = math_ops.matmul( array_ops.transpose(a, [1,0]), dl_dc )
    dl_da = my_matmul(dl_dc, array_ops.transpose(b, [1, 0]))
    dl_db = my_matmul(array_ops.transpose(a, [1, 0]), dl_dc)

    return dl_da, dl_db


# # -----------------  load gmm_model -------------------- #
# _gmm_model_module = tf.load_op_library(os.path.join(
#     TDL_HOME, 'ops/kernels/bin/gmm_model_op.so'))
# gmm_model = _gmm_model_module.gmm_model
#
#
# @tf.RegisterGradient("GmmModel")
# def _gmm_model_grad(op, dl_dp, dl_dgauss, dl_daux2):
#     x = op.inputs[0]
#     w = op.inputs[1]
#     mu = op.inputs[2]
#     sigma = op.inputs[3]
#
#     p_x = op.outputs[0]
#     gaussians = op.outputs[1]
#     sigma_inv_x_mu = op.outputs[2]
#
#     dl_dp = array_ops.expand_dims(dl_dp, -1)
#
#     x_shape_np = x.get_shape()  # array_ops.get_shape(x)
#     mu_shape_np = mu.get_shape()  # array_ops.get_shape(mu)
#     x_shape = array_ops.shape(x)
#     mu_shape = array_ops.shape(mu)
#
#     n_samples = x_shape[0]
#     n_params = mu_shape_np[0]
#     n_kernels = mu_shape_np[1]
#     n_dims = mu_shape[2]
#
#     #print("x_shape: ", x_shape)
#     #print("n_samples: ", n_samples)
#     #print("n_dims: ", n_dims)
#     #pi= 3.14159265358979323846
#     #norm_const = math_ops.inv( math_ops.sqrt((math_ops.pow(2.0*pi, math_ops.to_float(n_dims))) * math_ops.reduce_prod(sigma, 2)))
#
#     # 1/x element-wise, shape: [sample_id, kernel_id, sigma...]
#     sigma_inv = math_ops.reciprocal(sigma)
#
#     # x_mu = array_ops.reshape(x, [n_samples, 1, n_dims]) - mu # shape: [sample_id, kernel_id, x-mu]
#
#     #sigma_inv_x_mu = math_ops.mul( x_mu, sigma_inv )
#
#     #gaussians = math_ops.mul( norm_const, math_ops.exp( -0.5* math_ops.reduce_sum( x_mu * sigma_inv_x_mu, 2 ) ) )
#
#     # gradient computation
#     # derivative with respect w
#     if n_kernels == 1:
#         dl_dw = 0 * w
#     else:
#         dl_dw = math_ops.multiply(dl_dp, gaussians)
#
#     # derivative with respect mu
#     w_gaussians = math_ops.multiply(w, gaussians)
#     # dgmm_dmu: tensor of shape: [samples, kernel, dim]
#     dp_dmu = math_ops.multiply(array_ops.expand_dims(
#         w_gaussians, -1), sigma_inv_x_mu)
#     # de_dmu: tensor of shape: [samples, kernel, dim]
#     dl_dmu = math_ops.multiply(array_ops.expand_dims(dl_dp, -1), dp_dmu)
#
#     # derivative with respect sigma
#     # dgmm_dmu: tensor of shape: [samples, kernel, dim]
#     dp_dsigma = math_ops.pow(sigma_inv_x_mu, 2.0) - sigma_inv
#     dp_dsigma = 0.5 * \
#         math_ops.multiply(array_ops.expand_dims(w_gaussians, -1), dp_dsigma)
#     # de_dmu: tensor of shape: [samples, kernel, dim]
#     dl_dsigma = math_ops.multiply(array_ops.expand_dims(dl_dp, -1), dp_dsigma)
#
#     # derivative with respect x
#     dl_dx = math_ops.reduce_sum(-dl_dmu, 1)
#
#     if n_params == 1:
#         dl_dw = math_ops.reduce_sum(dl_dw, 0)
#         dl_dw = array_ops.expand_dims(dl_dw, 0)
#
#         dl_dmu = math_ops.reduce_sum(dl_dmu, 0)
#         dl_dmu = array_ops.expand_dims(dl_dmu, 0)
#
#         dl_dsigma = math_ops.reduce_sum(dl_dsigma, 0)
#         dl_dsigma = array_ops.expand_dims(dl_dsigma, 0)
#
#     return dl_dx, dl_dw, dl_dmu, dl_dsigma
