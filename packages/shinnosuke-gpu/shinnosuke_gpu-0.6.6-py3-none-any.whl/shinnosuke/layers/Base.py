from .Core import Layer
import cupy as cp


class Input(Layer):
    def __init__(self,shape,value=None):
        super(Input,self).__init__()
        self.input_shape=shape
        self.output_shape=self.input_shape
        self.output_tensor=value
        self.require_grads=False



    def connect(self,prev_layer):
        if prev_layer is not None:
            self.input_shape=prev_layer.output_shape
            self.output_shape=self.input_shape




    def forward(self,is_training):
        self.output_tensor=self.input_tensor
        super(Input,self).forward(is_training)



    def backward(self):
        pass





class Reshape(Layer):
    def __init__(self,output_shape,**kwargs):
        super(Reshape,self).__init__(**kwargs)
        self.output_shape=output_shape



    def connect(self,prev_layer):
        if prev_layer is not None:
            self.input_shape=prev_layer.output_shape
        else:
            assert self.input_shape is not None

        assert cp.prod(self.input_shape[1:]) == cp.prod(self.output_shape[1:]), "can not change the element's number"
        Layer.connect(self, prev_layer)



    def __call__(self, layers):
        if layers is not None:
            self.input_shape=layers.output_shape
        else:
            assert self.input_shape is not None
        assert cp.prod(self.input_shape[1:])==cp.prod(self.output_shape[1:]),"can not change the element's number"
        super(Reshape, self).__call__(layers)

        return self



    def forward(self,is_training):
        N=self.input_tensor.shape[0]
        self.output_shape[0]=N
        self.output_tensor=self.input_tensor.reshape(self.output_shape)
        if is_training:
            self.input_shape[0]=N
        super(Reshape,self).forward(is_training)



    def backward(self):
        for layer in self.inbounds:
            if layer.require_grads:
                layer.grads += cp.reshape(self.grads, self.input_shape)
            else:
                layer.grads = self.grads