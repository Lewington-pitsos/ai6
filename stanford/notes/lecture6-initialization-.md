# Initialization

How exactly do we choose the weights?

If you initialize each weight to the same value, then they will all have exactly the same gradient with respect to the loss, meaning that they will all update to exactly the same value, and so on. We need different values for sure.

So what do we do?

## Small random numbers

Everything around 0.01.

This works well for small networks.

But not so well for deeper networks.

This is obvious when you think about it, let's say you have 10 layers. That means you're going to take the image integer values, and multiply each by a very small decimal, resulting in small values. Next layer you're going to multiply those small values by yet more small decimals (since the second layer was initialized in the same way), leading to probably small decimals. And so on until layer 10, where everything is nearly 0.

In addition, because our outputs are getting smaller and smaller 10 times, the effect of any given input on the loss will be miniscule, so the gradients, and hence the updates to the initial weights will be very small indeed. Same as the forward pass, you multiply the first gradient of 1 with 10 layers of tiny gradients :(.

## large random numbers

If the numbers are too large (and we're using **tanh** for the non-linear layers) the gradients for each number will be very small (since large changes in conv layer outputs have a very small impact on the tanh outputs). This means very small updates along all the layers.

## xavier initialization

    W = np.random.randn(fan_in, fan_out) / np.sqrt(fan_in)

Basically you want the distribution/variance of the weights to be larger if their inputs are smaller and smaller if their inputs are larger. 

This won't work for the ReLU though. Relu kills half of all your inputs and so halves the variance of the input at each step.

## He et al.

in 2015 someone published a paper on how you can make the xavier initialization work for ReLU by just doubling the weight values of the xavier initialization (and thus creating roughly twice as much variation).

## Proper initialization 

No one knows how the heck to do it right, still an active area of research and very very important.