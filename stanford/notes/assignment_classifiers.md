# SVM classifier

Stands for **Multiclass Support Vector Machine loss**. The intuition is that we want the correct class to have the highest score (i.e. higher than each other class) by some safety margin. The sum of all scores from incorrect classes to the extent that they score *above* this safety margin constitutes the loss (this includes incorrect classes that actually score *higher* than the correct class). 

# Softmax Classifier

The softmax classifier (named after the **softmax** function) scores all the classes just like the SVM classifier, but instead of calculating a svm or **hinge** loss directly it first converts all the scores into a **probability distribution** and then calculates **cross entropy loss**.

Many many fun terms, but it's supposed to give us a nice interpretation as the machine assigning each class a probability of being the correct one.

## Probability Distribution:

This is any vector such that:

1. All the scores now have 0 < values < 1
2. The sum of all scores is 1

## Softmax Function

See the very end of *lecture3-maths.md*, but essentially: 

1. You have a vector of class scores `v`
2. You generate the **exponent** of each element in `v` 

    ev^i

3. You now have a vector of exponents `vE`
4. You sum all of these exponents to get `s`
5. Finally you divide each of the exponents (`vE^i`) form `vE` by `s`

    vE^i /s 

6. And the resulting vector is the output, this will always be a probability distribution.

## Cross Entropy Loss

This isn't really so important. It's just a way of getting from our probability distributions to a nice, scalar loss. 

If `p` is a probability distribution and `cp` is the probability score of the correct class, the cross entropy loss of `p` is 

    -log(cp)

This has some nice qualities:

1. CEL can never be 0, since this would require that the original vector we passed to the softmax function had 0 scores for all incorrect classes and an *infinite* score for the correct one.
2. CEL can be very very high, since as `cp` approachs 0, `-log(cp)` approaches infinity.

## Numerical instability

Computers are bad at handling certain numerical interactions (not sure exactly why). One of these is when you divide by very large numbers. The softmax function involves division of numbers that tend to be very large, and this can cause problems.

The solution is to use algebra to find equivalent expressions that involve smaller numbers. Turns out that, for any given `c`

    vE^i / s = (vE^i) * c / s * c

And it turns out that it's also equivalent to subtract any given `c` from all the elements in the original class score vector, (i.e. all the `v^i`'s) before starting. By convention we usually use the highest value in `v` as `c`. Having done this the numbers never get large enough to be an issue.

```python

f = np.array([123, 456, 789]) # example with 3 classes and each having large scores
p = np.exp(f) / np.sum(np.exp(f)) # Bad: Numeric problem, potential blowup

# instead: first shift the values of f so that the highest number is 0:
f -= np.max(f) # f becomes [-666, -333, 0]
p = np.exp(f) / np.sum(np.exp(f)) # safe to do, gives the correct answer

```

## "probability"

It might be a bit hasty to call the vector given by the softmax function a "probability distribution" since the "peakyness" (i.e. diffuseness) of the distribution is usually directly effected by the regularization penalty.

For simple l2 regularization (where we square all the weights, multiply by reg and add this to loss), larger weights are penalized. 

Larger weights mean more diffuse softmax outcomes though, so the probabilities given are heavily influenced by regularization (which wouldn't really be the case if they were real probabilities).

## Multivariable chain rule

A pretty snazzy bit of theory which states that if a variable is present in multiple points in an equation, the gradient of that variable with respect to the outcome of the equation will be the sum of all the gradients of each of the points where it was used. So for example, if we have

    f(x) = x + 3 / 4x

You would calculate the gradient of the x above the division line, calculate the gradient of the x below the division line, and sum those two gradients to get the overall gradient of x.