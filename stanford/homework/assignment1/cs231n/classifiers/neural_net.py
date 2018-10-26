from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

class TwoLayerNet(object):
  """
  A two-layer fully-connected neural network. The net has an input dimension of
  N, a hidden layer dimension of H, and performs classification over C classes.
  We train the network with a softmax loss function and L2 regularization on the
  weight matrices. The network uses a ReLU nonlinearity after the first fully
  connected layer.

  In other words, the network has the following architecture:

  input - fully connected layer - ReLU - fully connected layer - softmax

  The outputs of the second fully-connected layer are the scores for each class.
  """

  def __init__(self, input_size, hidden_size, output_size, std=1e-4):
    """
    Initialize the model. Weights are initialized to small random values and
    biases are initialized to zero. Weights and biases are stored in the
    variable self.params, which is a dictionary with the following keys:

    W1: First layer weights; has shape (D, H)
    b1: First layer biases; has shape (H,)
    W2: Second layer weights; has shape (H, C)
    b2: Second layer biases; has shape (C,)

    Inputs:
    - input_size: The dimension D of the input data.
    - hidden_size: The number of neurons H in the hidden layer.
    - output_size: The number of classes C.
    """
    self.params = {}
    self.params['W1'] = std * np.random.randn(input_size, hidden_size)
    self.params['b1'] = np.zeros(hidden_size)
    self.params['W2'] = std * np.random.randn(hidden_size, output_size)
    self.params['b2'] = np.zeros(output_size)

  def loss(self, X, y=None, reg=0.0):
    """
    Compute the loss and gradients for a two layer fully connected neural
    network.

    Inputs:
    - X: Input data of shape (N, D). Each X[i] is a training sample.
    - y: Vector of training labels. y[i] is the label for X[i], and each y[i] is
      an integer in the range 0 <= y[i] < C. This parameter is optional; if it
      is not passed then we only return scores, and if it is passed then we
      instead return the loss and gradients.
    - reg: Regularization strength.

    Returns:
    If y is None, return a matrix scores of shape (N, C) where scores[i, c] is
    the score for class c on input X[i].

    If y is not None, instead return a tuple of:
    - loss: Loss (data loss and regularization loss) for this batch of training
      samples.
    - grads: Dictionary mapping parameter names to gradients of those parameters
      with respect to the loss function; has the same keys as self.params.
    """
    # Unpack variables from the params dictionary
    W1, b1 = self.params['W1'], self.params['b1']
    W2, b2 = self.params['W2'], self.params['b2']
    N, D = X.shape

    # Compute the forward pass
    scores = None
    #############################################################################
    # TODO: Perform the forward pass, computing the class scores for the input. #
    # Store the result in the scores variable, which should be an array of      #
    # shape (N, C).                                                             #
    #############################################################################
    
    # First we get the dot product of the input and the W1
    # print(np.sum(X))
    hidden_values = np.dot(X, W1)
    # print(np.sum(hidden_values)) # should be at least close to the sum above
    
    # Next we apply the biases
    biased_hidden_values = hidden_values + b1
    # print(np.sum(biased_hidden_values)) # should be a bit larger than the above
    
    # Next the Relu layer
    relu_values = biased_hidden_values.clip(0)
    # print(np.sum(relu_values)) # slightly larger again hopefully

    # Apply second hidden layer
    score_values = np.dot(relu_values, W2)
    # print(score_values.shape) # should (N, C), (5, 3) for the dummy one
    
    # Apply second layer biases
    biased_score_values = score_values + b2
    
    # And now we have our correct scores
    scores = biased_score_values
    
    #############################################################################
    #                              END OF YOUR CODE                             #
    #############################################################################
    
    # If the targets are not given then jump out, we're done
    if y is None:
      return scores

    # Compute the loss
    loss = None
    #############################################################################
    # TODO: Finish the forward pass, and compute the loss. This should include  #
    # both the data loss and L2 regularization for W1 and W2. Store the result  #
    # in the variable loss, which should be a scalar. Use the Softmax           #
    # classifier loss.                                                          #
    #############################################################################
    
    # The loss is a softmax loss
    
    # First remove numerical instability yo
    scores -= np.amax(scores, axis=1)[:, np.newaxis]
    
    # First exponentiate the scores
    exp_scores = np.exp(scores)
    # print(exp_scores[0]) # should be a bunch of positive numbers
    
    # Then find the sum of the exponeitated scores for each input
    summed_exp_scores = np.sum(exp_scores, axis=1)
    # print(summed_exp_scores.shape) # should be (N,), so (5,) for the dummy
    
    # Next divide the exponents by the summed exponents
    probability_dists = exp_scores / summed_exp_scores[:, np.newaxis]
    # print(np.sum(probability_dists)) # Should be very very close to N, so 5 for dummy
    
    # Next get the negative log of all the correct scores. 
    correct_probs = np.choose(y, probability_dists.T)
    correct_probs[correct_probs == 0] = 1e-20
    # print(correct_probs.shape) # Should be (N,)
    log_cps = - np.log(correct_probs)
    # print(log_cps) # should all be positive and a little larger than 1
    
    # Lastly we sum all of these and divie by the input count
    
    pre_reg_loss = np.sum(log_cps) / N
    
    # Now we calculate the regularization losses for both weights
    
    reg_pen_1 = reg * np.sum(W1 * W1)
    reg_pen_2 = reg * np.sum(W2 * W2)
    
    # Add these to the data loss to get the actual loss
    loss = pre_reg_loss + reg_pen_1 + reg_pen_2
    
    pass
    #############################################################################
    #                              END OF YOUR CODE                             #
    #############################################################################

    # Backward pass: compute gradients
    grads = {}
    #############################################################################
    # TODO: Compute the backward pass, computing the derivatives of the weights #
    # and biases. Store the results in the grads dictionary. For example,       #
    # grads['W1'] should store the gradient on W1, and be a matrix of same size #
    #############################################################################
    
    # The gradients for the scores with regard to the overall
    # softmax loss equate to the probability distributuons, but with 1 subrtacted
    # from each of the correct probabilities.
    
    d_scores = np.copy(probability_dists)
    d_scores[np.arange(N), y] -= 1
    d_avg_scores = d_scores / N
    # print(d_scores[0]) # should be small positives and one small negative
    
    # Summed, and averaged these are the exact gradients for the second lot of biases
    grads['b2'] = np.sum(d_avg_scores, axis=0)
    
    # W2 gradients are just these multiplied by the hidden values. 
    # Keep in mind that the biases have a gradient of 1
    # We also need to add the W2 regularization gradient.
    # print(W2.shape)
    d_W2 = np.dot(relu_values.T, d_avg_scores)
    # print(d_W2.shape) # should be (H, C) i.e. the same shape as W2
    d_W2_reg = reg * 2 * W2
    grads["W2"] = d_W2 + d_W2_reg
    
    # On the other hand, the gradients for the post-relu hidden values are the opposite
    # of this: the dot product between the incoming gradients and W2 itself.
    
    d_relu = np.dot(d_avg_scores, W2.T)
    
    # Next the gradient for the ReLU node, which is just the incoming gradient
    # multiplied by a mask where hidden_values values > 0 are replaced with 0's
    # note that the `relu_values` already are this exactly
    d_relu[relu_values <= 0] = 0
    
    # The gradients of the first biases are just these valaues averaged
    grads['b1'] = np.sum(d_relu, axis=0)
    
    # Finally the W1 gradients are just the dot product of `d_relu` and the input
    # Also remember regularization
    d_W1 = np.dot(X.T, d_relu)
    d_W1_reg = reg * 2 * W1
    grads['W1'] = d_W1 + d_W1_reg
    
    pass
    #############################################################################
    #                              END OF YOUR CODE                             #
    #############################################################################

    return loss, grads

  def train(self, X, y, X_val, y_val,
            learning_rate=1e-3, learning_rate_decay=0.95,
            reg=5e-6, num_iters=100,
            batch_size=200, verbose=False):
    """
    Train this neural network using stochastic gradient descent.

    Inputs:
    - X: A numpy array of shape (N, D) giving training data.
    - y: A numpy array f shape (N,) giving training labels; y[i] = c means that
      X[i] has label c, where 0 <= c < C.
    - X_val: A numpy array of shape (N_val, D) giving validation data.
    - y_val: A numpy array of shape (N_val,) giving validation labels.
    - learning_rate: Scalar giving learning rate for optimization.
    - learning_rate_decay: Scalar giving factor used to decay the learning rate
      after each epoch.
    - reg: Scalar giving regularization strength.
    - num_iters: Number of steps to take when optimizing.
    - batch_size: Number of training examples to use per step.
    - verbose: boolean; if true print progress during optimization.
    """
    num_train = X.shape[0]
    iterations_per_epoch = max(num_train / batch_size, 1)

    # Use SGD to optimize the parameters in self.model
    loss_history = []
    train_acc_history = []
    val_acc_history = []

    for it in range(num_iters):
      selected_indices = np.random.choice(num_train, batch_size)
      X_batch = X[selected_indices]
      y_batch = y[selected_indices]

      # Compute loss and gradients using the current minibatch
      loss, grads = self.loss(X_batch, y=y_batch, reg=reg)
      loss_history.append(loss)

      #########################################################################
      # TODO: Use the gradients in the grads dictionary to update the         #
      # parameters of the network (stored in the dictionary self.params)      #
      # using stochastic gradient descent. You'll need to use the gradients   #
      # stored in the grads dictionary defined above.                         #
      #########################################################################
      for parameter in grads:
        self.params[parameter] += - learning_rate * grads[parameter] 
        
      pass
      #########################################################################
      #                             END OF YOUR CODE                          #
      #########################################################################

      if verbose and it % 100 == 0:
        print('iteration %d / %d: loss %f' % (it, num_iters, loss))

      # Every epoch, check train and val accuracy and decay learning rate.
      if it % iterations_per_epoch == 0:
        # Check accuracy
        train_acc = (self.predict(X_batch) == y_batch).mean()
        val_acc = (self.predict(X_val) == y_val).mean()
        train_acc_history.append(train_acc)
        val_acc_history.append(val_acc)

        # Decay learning rate
        learning_rate *= learning_rate_decay

    return {
      'loss_history': loss_history,
      'train_acc_history': train_acc_history,
      'val_acc_history': val_acc_history,
    }

  def predict(self, X):
    """
    Use the trained weights of this two-layer network to predict labels for
    data points. For each data point we predict scores for each of the C
    classes, and assign each data point to the class with the highest score.

    Inputs:
    - X: A numpy array of shape (N, D) giving N D-dimensional data points to
      classify.

    Returns:
    - y_pred: A numpy array of shape (N,) giving predicted labels for each of
      the elements of X. For all i, y_pred[i] = c means that X[i] is predicted
      to have class c, where 0 <= c < C.
    """
    y_pred = None

    ###########################################################################
    # TODO: Implement this function; it should be VERY simple!                #
    ###########################################################################
    scores = self.loss(X, y=None)
    return np.argmax(scores, axis=1)
    pass
    ###########################################################################
    #                              END OF YOUR CODE                           #
    ###########################################################################

    return y_pred


