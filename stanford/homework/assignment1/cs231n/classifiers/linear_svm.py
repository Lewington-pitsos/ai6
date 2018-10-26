import numpy as np
from random import shuffle

def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).

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
  dW = np.zeros(W.shape) # initialize the gradient as zero
  # compute the loss and the gradient
  num_classes = W.shape[1]

  num_train = X.shape[0]
  loss = 0.0
  loss_grad = 1/num_train
    
  for i in range(num_train):
    scores = X[i].dot(W)
    temp_loss = 0
    temp_grads = np.zeros(scores.shape)
    correct_class_score = scores[y[i]]
    num_loss_margins = 0
    for j in range(num_classes):
      if j == y[i]:
        continue
      margin = scores[j] - correct_class_score + 1 # note delta = 1
      if margin > 0:
        num_loss_margins += 1
        temp_grads[j] = (1 * loss_grad)
        temp_loss += margin
    
    # print(temp_loss)
    temp_grads[y[i]] = -1 * loss_grad * num_loss_margins
    X_temp_grads = temp_grads * X[i][:, np.newaxis]
    dW += X_temp_grads
    # print("gradient: {}".format(np.sum(dW)))
    # print("X sum: {}".format(np.sum(X[i])))
    
    
    loss += temp_loss

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  W_sum = np.sum(W * W)
  loss += reg * W_sum
    
  final_loss_grad = 1
  W_sum_grad = final_loss_grad * reg
  W_sq_grad = 2 * W * W_sum_grad
  dW += W_sq_grad
  # print(dW)

  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################


  return loss, dW


def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  loss = 0.0
  input_count = X.shape[0]
  dW = np.zeros(W.shape) # initialize the gradient as zero
  # print(y.shape)

  # Calculate the class scores for each input and store each in a vector
  all_scores = np.dot(X, W)
  # print(all_scores.shape)
    
    
  # Remove all the correct scores from any of these class-score vectors

  correct_class_scores = np.choose(y, all_scores.T)

  # print(correct_class_scores)
    
  # Create new class score vectors, which are exactly the same except each element has the correct score
  # subtracted from it    
  score_differences = all_scores.T - correct_class_scores + 1

  # print(score_differences)

  # re-create the same vectors exept all negative values are replaced with 0
  relu_score_differences = score_differences.clip(0)

  #print(relu_score_differences)

  # sum these losses to get the total loss
  # also subtract 1 for each correct score, since each correct score would have incurred a loss of 1
  total_loss = np.sum(relu_score_differences) - input_count
  # print(total_loss)
    
  # devide these losses by the input number
  average_loss = total_loss / input_count
  # print(average_loss)

  # add regularization penalty.     
  penalty = reg * np.sum(W * W)
  loss =  average_loss + penalty
  # print(loss)
  
  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################

  # compute the regularization gradient
  
  # Note: nodes that just contain addition can kind of be ignored
  pen_grad = (reg * (2 * W))

  # compute the main gradient
    
  # compute the gradient from the overall to average loss
    
  avg_grad = (1 / input_count)

  # What we want to do now is: 
  # 1. Find the gradient between the eventual loss and all the temp_losses (spolier, it's just 1)
  # 2. Find the gradient between the temp_loss and the loss vector it came from
  #    2.1 first step here is that the gradient between the temp_loss and any vector values that were >= 0, is 0
    
  margins = relu_score_differences.T
    
  # 2.2 next we want to work out the gradient for all the vector values which represented incorrect classifiactions
  # and ended up actually causing some kind of loss (rather than just being 0). Luckily these all just have a 
  # gradient of 1, since they (or rather the result of them - the actual score + 1, all of which linear as fuck) 
  # just get added together to make the temp loss
    
  margins[margins > 0] = 1
    
  # 2.3 lastly we want to work out the gradient for the correct vector value. This is just -1 * the number of
  # incorerct values which are larger than this value if you add 1 (since the loss decreases as this rises and
  # it decreases more for each such incorrect value)

  # print(margins.shape)
    
  # so for each score vecotr we need to work out
  # 1. how many incorrect but > 0
  
  incorrect_count_per_input = np.count_nonzero(margins == 1, axis=1) - 1
  # print(incorrect_count_per_input)
  
  # 2. which is the correct one
  margins[np.arange(input_count), y] = -incorrect_count_per_input
  # print(margins)
  
  dW = X.T.dot(margins)

  dW *= avg_grad
   
  dW += pen_grad 

  pass
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
