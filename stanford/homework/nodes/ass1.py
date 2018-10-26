import numpy as np
from node import Node, confirm_shape

class Score(Node):
    def __init__(self, inputs):
        Node.__init__(self)
        self.inputs = inputs
        confirm_shape(inputs, (500, 3073))

    def forwards(self, weights: np.ndarray) -> np.ndarray:
        confirm_shape(weights, (3073, 10))

        # Each of the 10 weight matrices represents a class.
        # For each input we calculate a score for each class by multiplying
        # the input against the weight matrix for that class.
        output = np.dot(self.inputs, weights)

        # We should end up with 10 class scores for each input.
        confirm_shape(output, (500, 10))
        self.output = output
        return output

    def backwards(self, gradient) -> np.ndarray:
        confirm_shape(gradient, (500, 10))

        # First we want to calculate the gradient for each weight value
        # with respect to each input. So: how much did that
        # particular weight value effect the score for that input?
        all_input_grads = gradient[:, :, np.newaxis] * self.inputs[:, np.newaxis] 

        # Then, to get an overall gradient, i.e. how much did each weight
        # effect the scores overall. 
        # We get this just by summing all the values for each weight over
        # all the inputs. 
        output = np.sum(all_input_grads, axis=0)

        confirm_shape(output, (10, 3073))
        return output


class MatMult(Node):
    def __init__(self, input):
        Node.__init__(self)
        self.input = input
        confirm_shape(inputs, (3073))

    def forwards(self, weights: np.ndarray) -> np.ndarray:
        confirm_shape(weights, (3073, 10))

        # Each of the 10 weight matrices represents a class.
        # We calculate a score for each class by multiplying the        
        # input against the weight matrix for that class.
        output = weights * self.input

        confirm_shape(output, (10))
        self.output = output
        return output
    
    def backwards(self, gradient) -> np.ndarray:
        # The gradient coming back is an array of 10 integers

        # We want to work out what impact each individual weight
        # had on each integer. 
        # In this case it is the relevent input weight, multiplied by
        # the corresponding integer.

        grad = self.inputs * gradient[:, np.newaxis]
        return grad



