from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import mxnet as mx
import numpy as np



def _Conv(data, num_filter, kernel, stride, pad, name, no_bias=False, workspace=256):
    _weight = mx.symbol.Variable(name+'_weight')
    _bias = mx.symbol.Variable(name+'_bias', lr_mult=2.0, wd_mult=0.0)
    body = mx.sym.Convolution(data=data, weight = _weight, bias = _bias, num_filter=num_filter, kernel=kernel, stride=stride, pad=pad, no_bias = no_bias, workspace = workspace, name = name)
    return body

def Conv(**kwargs):
    name = kwargs.get('name')
    _weight = mx.symbol.Variable(name+'_weight')
    _bias = mx.symbol.Variable(name+'_bias', lr_mult=2.0, wd_mult=0.0)
    body = mx.sym.Convolution(weight = _weight, bias = _bias, **kwargs)
    return body


def Act(data, name):
    body = mx.sym.LeakyReLU(data = data, act_type='prelu', name = name)
    return body

def resnet_unit0(data, num_filter, name, workspace = 256):
  bn_mom = 0.9
  body = Conv(data=data, num_filter=num_filter, kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn')
  body = Act(data=body, name=name+'_relu')
  return body

def resnet_unit1(data, num_filter, name, dim_match=True, workspace = 256):
  bn_mom = 0.9
  shortcut = data
  body = Conv(data=data, num_filter=num_filter, kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv1", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn1')
  body = Act(data=body, name=name+'_relu1')
  body = Conv(data=body, num_filter=num_filter, kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv2", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn2')
  if dim_match:
    body = body+shortcut
  body = Act(data=body, name=name+'_relu2')
  return body

def resnet_unit2(data, num_filter, name, dim_match=True, workspace = 256):
  bn_mom = 0.9
  shortcut = data
  body = mx.sym.BatchNorm(data=data, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn1')
  body = Act(data=body, name=name+'_relu1')
  body = Conv(data=body, num_filter=num_filter, kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv1", workspace=workspace)
  #body = mx.symbol.Dropout(data=body, p=0.2)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn2')
  body = Act(data=body, name=name+'_relu2')
  body = Conv(data=body, num_filter=num_filter, kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv2", workspace=workspace)
  if dim_match:
    body = body+shortcut
  return body

def resnet_unit3(data, num_filter, name, dim_match=True, workspace = 256):
  bn_mom = 0.9
  shortcut = data
  body = mx.sym.BatchNorm(data=data, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn1')
  body = Conv(data=body, num_filter=num_filter, kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv1", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn2')
  body = Act(data=body, name=name+'_relu1')
  body = Conv(data=body, num_filter=num_filter, kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv2", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn3')
  if dim_match:
    body = body+shortcut
  return body

def resnet_unit4(data, num_filter, name, dim_match=True, workspace = 256):
  bn_mom = 0.9
  shortcut = data
  body = mx.sym.BatchNorm(data=data, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn1')
  body = Act(data=body, name=name+'_relu1')
  body = Conv(data=data, num_filter=int(num_filter*0.25), kernel=(1,1), stride=(1,1), pad=(0,0),
                            name=name+"_conv1", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn2')
  body = Act(data=body, name=name+'_relu2')
  body = Conv(data=body, num_filter=int(num_filter*0.25), kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv2", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn3')
  body = Act(data=body, name=name+'_relu3')
  body = Conv(data=body, num_filter=num_filter, kernel=(1,1), stride=(1,1), pad=(0, 0),
                            name=name+"_conv3", workspace=workspace)
  if dim_match:
    body = body+shortcut
  return body

def resnet_unit5(data, num_filter, name, dim_match=True, workspace = 256):
  bn_mom = 0.9
  shortcut = data
  body = Conv(data=data, num_filter=int(num_filter*0.5), kernel=(1,1), stride=(1,1), pad=(0,0),
                            name=name+"_conv1", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn1')
  body = Act(data=body, name=name+'_relu1')
  body = Conv(data=body, num_filter=int(num_filter*0.5), kernel=(3,3), stride=(1,1), pad=(1, 1), num_group=32,
                            name=name+"_conv2", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn2')
  body = Act(data=body, name=name+'_relu2')
  body = Conv(data=body, num_filter=num_filter, kernel=(1,1), stride=(1,1), pad=(0,0),
                            name=name+"_conv3", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn3')
  if dim_match:
    body = body+shortcut
  body = Act(data=body, name=name+'_relu3')
  return body

def resnet_unit6(data, num_filter, name, dim_match=True, workspace = 256):
  bn_mom = 0.9
  shortcut = data
  body = Conv(data=data, num_filter=num_filter*4, kernel=(1,1), stride=(1,1), pad=(0,0),
                            name=name+"_conv1", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn1')
  body = Act(data=body, name=name+'_relu1')
  body = Conv(data=body, num_filter=num_filter*4, kernel=(3,3), stride=(1,1), pad=(1, 1), num_group=32,
                            name=name+"_conv2", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn2')
  body = Act(data=body, name=name+'_relu2')
  body = Conv(data=body, num_filter=num_filter, kernel=(1,1), stride=(1,1), pad=(0,0),
                            name=name+"_conv3", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn3')
  if dim_match:
    body = body+shortcut
  body = Act(data=body, name=name+'_relu3')
  return body

def resnet_unit7(data, num_filter, name, dim_match=True, workspace = 256):
  #se block
  bn_mom = 0.9
  shortcut = data
  body = mx.sym.BatchNorm(data=data, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn1')
  body = Conv(data=body, num_filter=num_filter, kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv1", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn2')
  body = Act(data=body, name=name+'_relu1')
  body = Conv(data=body, num_filter=num_filter, kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv2", workspace=workspace)
  res = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn3')

  body = mx.sym.Pooling(data=res, global_pool=True, kernel=(7, 7), pool_type='avg', name=name+'_se_pool1')
  body = Conv(data=body, num_filter=num_filter//16, kernel=(1,1), stride=(1,1), pad=(0,0),
                            name=name+"_se_conv1", workspace=workspace)
  body = Act(data=body, name=name+'_se_relu1')
  body = Conv(data=body, num_filter=num_filter, kernel=(1,1), stride=(1,1), pad=(0,0),
                            name=name+"_se_conv2", workspace=workspace)
  body = mx.symbol.Activation(data=body, act_type='sigmoid', name=name+"_se_sigmoid")
  body = mx.symbol.broadcast_mul(res, body)

  if dim_match:
    body = body+shortcut
  return body

def resnet_unit100(data, num_filter, name, dim_match=True, workspace = 256):
  bn_mom = 0.9
  body = mx.sym.BatchNorm(data=data, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn1')
  body = Conv(data=body, num_filter=num_filter, kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv1", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn2')
  act = Act(data=body, name=name+'_relu1')
  body = Conv(data=act, num_filter=num_filter, kernel=(3,3), stride=(1,1), pad=(1, 1),
                            name=name+"_conv2", workspace=workspace)
  body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name+'_bn3')
  if not dim_match:
    shortcut = Conv(data=act, num_filter=num_filter, kernel=(1,1), pad=(0,0), name=name+"_shortcut", workspace=workspace)
  else:
    shortcut = data
  body = body+shortcut
  return body

def resnet_unit(rtype, data, num_filter, name, dim_match=True, workspace = 256):
  if rtype==1:
    return resnet_unit1(data=data, num_filter=num_filter, name=name, dim_match=dim_match, workspace=workspace)
  elif rtype==2:
    return resnet_unit2(data=data, num_filter=num_filter, name=name, dim_match=dim_match, workspace=workspace)
  elif rtype==3:
    return resnet_unit3(data=data, num_filter=num_filter, name=name, dim_match=dim_match, workspace=workspace)
  elif rtype==4:
    return resnet_unit4(data=data, num_filter=num_filter, name=name, dim_match=dim_match, workspace=workspace)
  elif rtype==5:
    return resnet_unit5(data=data, num_filter=num_filter, name=name, dim_match=dim_match, workspace=workspace)
  elif rtype==6:
    return resnet_unit6(data=data, num_filter=num_filter, name=name, dim_match=dim_match, workspace=workspace)
  elif rtype==7:
    return resnet_unit7(data=data, num_filter=num_filter, name=name, dim_match=dim_match, workspace=workspace)
  elif rtype==100:
    return resnet_unit100(data=data, num_filter=num_filter, name=name, dim_match=dim_match, workspace=workspace)
  else:
    assert(False)

def resnet(data, units, filters, rtype, workspace):
  body = resnet_unit0(data=data, num_filter=32, name="stage%d_unit%d"%(0, 0))
  for i in xrange(len(units)):
    f = filters[i]
    dim_match = False
    if i==0:
      dim_match = True
    if rtype>=100:
      body = resnet_unit(rtype=rtype, data=body, num_filter=f, name="stage%d_unit%d"%(i+1, 0), dim_match=dim_match) # do not connect to last layer, dim not match
    else:
      body = resnet_unit0(data=body, num_filter=f, name="stage%d_unit%d"%(i+1, 0)) # do not connect to last layer, dim not match
    body = mx.sym.Pooling(data=body, kernel=(2, 2), stride=(2,2), pad=(0,0), pool_type='max', name="stage%d_pool"%(i+1))
    for j in xrange(units[i]):
      body = resnet_unit(rtype=rtype, data=body, num_filter=f, name="stage%d_unit%d"%(i+1, j+1), dim_match=True)

  return body

def get_symbol(num_classes, num_layers, conv_workspace=256):
    data = mx.symbol.Variable('data')
    bn_mom = 0.9
    if num_layers<29:
      data = mx.sym.BatchNorm(data=data, fix_gamma=True, eps=2e-5, momentum=bn_mom, name='bn_data')
    else:
      data = data-127.5
      data = data*0.0078125
    units = [1,2,5,3] # all number of layers = sum(units)*2+len(units)+1
    filter_list = [64, 128, 256, 512]
    rtype = 1
    ftype = 1
    if num_layers==27:
      rtype = 1
    elif num_layers==28:
      rtype = 2
    elif num_layers==29:
      rtype = 3
      #use_last_bn = False
      #use_dropout = False
    elif num_layers==30:
      filter_list = [64, 256, 512, 1024]
      rtype = 3
    elif num_layers==31:
      rtype = 100
    elif num_layers==51:
      units = [2,3,15,3]
      rtype = 3
    elif num_layers==52:
      filter_list = [64, 256, 512, 1024]
      units = [2,3,15,3]
      rtype = 3
    elif num_layers==53: #se block
      units = [2,3,15,3]
      rtype = 7
    elif num_layers==74:
      units = [2,3,15,3]
      rtype = 4
    elif num_layers==75:
      units = [2,3,15,3]
      rtype = 5
    elif num_layers==76:
      filter_list = [16, 32, 64, 128]
      units = [2,3,15,3]
      rtype = 6
    else:
      assert(False)

    body = resnet(data = data, units = units, filters = filter_list, rtype=rtype, workspace = conv_workspace)
    _weight = mx.symbol.Variable("fc1_weight")
    _bias = mx.symbol.Variable("fc1_bias", lr_mult=2.0, wd_mult=0.0)
    if ftype==0:
      fc1 = mx.sym.FullyConnected(data=body, weight=_weight, bias=_bias, num_hidden=num_classes, name='fc1')
    elif ftype==1:
      body = mx.symbol.Dropout(data=body, p=0.4)
      fc1 = mx.sym.FullyConnected(data=body, weight=_weight, bias=_bias, num_hidden=num_classes, name='pre_fc1')
      fc1 = mx.sym.BatchNorm(data=fc1, fix_gamma=True, eps=2e-5, momentum=bn_mom, name='fc1')
    else:
      body = mx.sym.BatchNorm(data=body, fix_gamma=False, eps=2e-5, momentum=bn_mom, name='bn1')
      body = mx.sym.Activation(data=body, act_type='relu', name='relu1')
      body = mx.sym.Pooling(data=body, global_pool=True, kernel=(7, 7), pool_type='avg', name='pool1')
      body = mx.sym.Flatten(data=body)
      fc1 = mx.sym.FullyConnected(data=body, weight=_weight, bias=_bias, num_hidden=num_classes, name='fc1')

    return fc1

def init_weights(sym, data_shape_dict, num_layers):
  arg_name = sym.list_arguments()
  aux_name = sym.list_auxiliary_states()
  arg_shape, aaa, aux_shape = sym.infer_shape(**data_shape_dict)
  #print(data_shape_dict)
  #print(arg_name)
  #print(arg_shape)
  arg_params = {}
  aux_params = None
  #print(aaa)
  #print(aux_shape)
  arg_shape_dict = dict(zip(arg_name, arg_shape))
  aux_shape_dict = dict(zip(aux_name, aux_shape))
  #print(aux_shape)
  #print(aux_params)
  #print(arg_shape_dict)
  for k,v in arg_shape_dict.iteritems():
    #print('find', k)
    if k.endswith('_weight') and k.find('_conv')>=0:
      if not k.find('_unit0_')>=0:
        arg_params[k] = mx.random.normal(0, 0.01, shape=v)
        print('init', k)
    if k.endswith('_bias'):
      arg_params[k] = mx.nd.zeros(shape=v)
      print('init', k)
  return arg_params, aux_params

