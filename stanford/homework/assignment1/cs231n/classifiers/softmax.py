import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
   
  input_count = X.shape[0]
    
  # First we want to compute the dot product of all the inputs and the weights.
  # This should give us a (n, 10) matrix where n is the number of inputs

  score_vectors = X.dot(W) 
  # print(score_vectors.shape) # (500, 10) 
  
  # Next we want to subtract the highest value from each score vector from every
  # value in that vector.
  # NOTE: this is just to prevent numerical instability, it will not effect the
  # outcome at all (so no need to think about this when calculating gradients)
    
  # Find all of the highest values  
  highest_values = np.choose(np.argmax(score_vectors, axis=1), score_vectors.T)
  # print(highest_values.shape)
  # print(highest_values)
  
  # Subtract all of the highest values from each vector
  # print(np.sum(score_vectors))
  score_vectors = np.subtract(score_vectors, highest_values[:, np.newaxis])  
  # print(np.sum(score_vectors)) # Should be negative and much lower

  # Ok, now we turn our score vectors into softmax probability distributions. 
    
  # Firstly we take all the values in each vector and exponentiate them.

  exponential_vectors = np.exp(score_vectors) # Thanks numpy!
  # print(np.sum(exponential_vectors)) # should be larger than `np.sum(score_vectors)` and positive

  # Next we generate a 1-D array of the sums of each exponential vector
    
  exponential_sums = np.sum(exponential_vectors, axis=1)
  # print(exponential_sums.shape) # should be (500,)
    
  # Finally we divide each exponential vector by the corresponding exponential sum

  probability_dists = np.divide(exponential_vectors, exponential_sums[:, np.newaxis])
  print(probability_dists.shape) # should be (500, 10)
  print(np.sum(probability_dists)) # should be the number of inputs
    
  # Now just calculate the cross entropy loss for each probability distribution and 
  # sum these to get the overall loss
  
  # First get all of the correct probabily values
  correct_probabilities = probability_dists[np.arange(input_count), y]
  # print(correct_probabilities.shape) # should be (500,)
 
  # Next get the cross entropy loss for each of these
  log_values = np.log(correct_probabilities)
  loss_values = np.negative(log_values)
  # print(loss_values.shape) # should be (500,)
    
  # Finally sum to get overall loss
  loss = np.sum(loss_values)
    
  # Finally just average this loss and then apply regularization
  
  loss /= input_count
  
  # Regularization
  sum_squared_weights = np.sum(W * W)
  reg_penalty = reg * sum_squared_weights

  loss += reg_penalty
    
  # ----------------------------------- GRADIENT ---------------------------- #
   
  d_probability_dists = np.copy(probability_dists)
  d_probability_dists[np.arange(input_count), y] -= 1
  dW = np.dot(X.T, d_probability_dists)
    
  dW /= input_count

  reg_grad = reg * 2 * W
  dW += reg_grad
    
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
   
  input_count = X.shape[0]
    
  # First we want to compute the dot product of all the inputs and the weights.
  # This should give us a (n, 10) matrix where n is the number of inputs

  score_vectors = X.dot(W) 
  # print(score_vectors.shape) # (500, 10) 
  
  # Next we want to subtract the highest value from each score vector from every
  # value in that vector.
  # NOTE: this is just to prevent numerical instability, it will not effect the
  # outcome at all (so no need to think about this when calculating gradients)
    
  # Find all of the highest values  
  highest_values = np.choose(np.argmax(score_vectors, axis=1), score_vectors.T)
  # print(highest_values.shape)
  # print(highest_values)
  
  # Subtract all of the highest values from each vector
  # print(np.sum(score_vectors))
  score_vectors = np.subtract(score_vectors, highest_values[:, np.newaxis])  
  # print(np.sum(score_vectors)) # Should be negative and much lower

  # Ok, now we turn our score vectors into softmax probability distributions. 
    
  # Firstly we take all the values in each vector and exponentiate them.

  exponential_vectors = np.exp(score_vectors) # Thanks numpy!
  # print(np.sum(exponential_vectors)) # should be larger than `np.sum(score_vectors)` and positive

  # Next we generate a 1-D array of the sums of each exponential vector
    
  exponential_sums = np.sum(exponential_vectors, axis=1)
  # print(exponential_sums.shape) # should be (500,)
    
  # Finally we divide each exponential vector by the corresponding exponential sum

  probability_dists = np.divide(exponential_vectors, exponential_sums[:, np.newaxis])
  print(probability_dists.shape) # should be (500, 10)
  print(np.sum(probability_dists)) # should be the number of inputs
    
  # Now just calculate the cross entropy loss for each probability distribution and 
  # sum these to get the overall loss
  
  # First get all of the correct probabily values
  correct_probabilities = probability_dists[np.arange(input_count), y]
  # print(correct_probabilities.shape) # should be (500,)
 
  # Next get the cross entropy loss for each of these
  log_values = np.log(correct_probabilities)
  loss_values = np.negative(log_values)
  # print(loss_values.shape) # should be (500,)
    
  # Finally sum to get overall loss
  loss = np.sum(loss_values)
    
  # Finally just average this loss and then apply regularization
  
  loss /= input_count
  
  # Regularization
  sum_squared_weights = np.sum(W * W)
  reg_penalty = reg * sum_squared_weights

  loss += reg_penalty
    
  # ----------------------------------- GRADIENT ---------------------------- #
   
  d_probability_dists = np.copy(probability_dists)
  d_probability_dists[np.arange(input_count), y] -= 1
  dW = np.dot(X.T, d_probability_dists)
    
  dW /= input_count

  reg_grad = reg * 2 * W
  dW += reg_grad
    
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

