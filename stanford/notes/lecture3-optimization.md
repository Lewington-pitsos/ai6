# Optimization

OK, so nowe we have

1. A classifier, that takes a `W` and spits out some scores
2. A loss function, that takes some scores and a correct score, and spits out how good of a score that was

What we want is to find the perfect `W`. At the moment, all we can do is keep trying random `W`'s. If we do this enough, and the space of all possible `W`'s is finite, we will eventually get the perfect `W`. But in reality this space is very big so we need another method.

Theoretically you could compute it in your head; just do all the maths, taking into account all possible images and what effects different `W`'s will have on them, and eventually just intuit the best `W`. But you'd have to be like, alan turing or something. 

## Optimization strategy: iterative soloution

You have an algorithm that can take any `W` and spit out a slightly better `W`, or at least a `W` that has a high-ish chance of being better. Aaaaand just keep doing this.

## Gradient

OK, so let's imagine we're dealing with a classifier which has a single class. Combined this makes a function that takes a bunch of parameters `W` and an image, and gives us a bunch of predictions `p` (only one in this case. Combine that with a loss function `Lf` that takes `p` and gives us a loss `l`, and assume a constant image and we have an encompassing function `Ef` that takes `W`, and returns `l`.

    Ef(W) = l

This function could be mapped into a graph.

We should be able to calculate the gradient for any given point on this graph, because hey, it's a function after all. If we can calculate the gradient, we can work out which way `Ef` is "sloping" i.e. whether `l` is going to rise or fall for a greater `W`. 

### example

Let's say `Ef(4) = 1.5`

We now want to work out the gradient of `Ef` at this point. We can do this by making a finite addition to our `W` (i.e. 4) and checking what effect this has on the `l`. Lets say our finite addition is 1, lets run it again.

    Ef(4 + 2) = 2.5 (let's say)

Ok, so according to the gradient theorum:

    df(x)/dx = (f(x + h) - f(x)) / h

Plugging that in:

    (Ef(4 + 2) - Ef(4)) / 2 = (2.5 - 1.5) / 2 = 1/2

So the gradient of `Ef(4)` is 0.5. 

It looks like at the moment then, increasing `W` increases `l`, so if we want to minimize loss, we should decrease `W`.

### So what?

So now we have a kind of heuristic for finding good `W`'s among the infinite space of all `W`'s: 

1. Find the loss for some `W`
2. Calculate the gradient for `Ef` and that `W`
3. Depending on whether the gradient is negative or positive, increase or decrease `W` to further minimize the loss

Simply wash, rinse and repeat until you have an acceptable loss, or whatever. 

How much should you decrease or increase `W` by? That's an important question, but the main thing is to increase it in the direction of the gradient (or rather in the opposite direction, because we want to minimize loss.)

## Complex W's

OK, we have an issue though. We've been assuming that `W` is just a single integer. It's not. `W` is a complex vector of integers. This is still ok though. We just do exactly the same thing *but* we calculate the gradient of each integer in `W` separately, and similarly adjust each integer in `W` separately. 

### example

let `W` be [4, 5, 6]

Our ultimate aim is to now find a better `W` with a lower loss.

We first calculate the loss for `W`

    Ef([4, 5, 6]) = 3.5

Ok, great, now we need a gradient. The *overall* gradient for this `W` is not too interesting to us. Instead we want to calculate the gradient for each parameter in `W`. Let's try it for the first.

Ok, so we increase that parameter by some `h`, say 2, and recalculate the loss

    Ef([4 + 2, 5, 6]) = 3 (let's imagine)
    dy/dx = (3 - 3.5 / 2) = -0.25

OK, so the gradient is pointing in a negative direction, which means increasing the first parameter of `W` probably decreases the loss, so we'll keep that number in a vector of adjustments `A`.

Now let's do the same thing for the second parameter


    Ef([4, 5 + 2, 6]) = 4.5 (let's imagine)
    dy/dx = (4.5 - 3.5 / 2) = 0.5

In this case the gradient was positive, increasing the second parameter seems to increase the loss. Lets just store that gradient in `A` for now, now on to param number 3.

    Ef([4, 5, 6 + 2]) = 4 (let's imagine)
    dy/dx = (4 - 3.5 / 2) = 0.25

Ok, great now `A` looks like this: [-0.25, 0.5, 0.25]. We know then that we'll probably get a better `W` if we increase the first parameter and decrease the next two, probably. We could increase and decrease these guys all by 1, but a more elegant approach is to add each gradient (it's negative, since we're trying minimize loss, not maximize it) to the corresponding parameter. This way parameters that seem to be having a big impact on the loss are adjusted more in the next `W` and hopefully we'll arrive at a better `W` sooner.

Applying `A` to `W`, we get [4.25, 4.5, 5.75] as out next `W`. Now all we have to do is wash rinse and repeat until we hit some predefined standard for `W`.

## Enter calculus

In reality the above approach isn't actually feasible though. `W` tends to have hundreds of parameters, maybe even thousands, so computing the loss for slight adjustments to all of these would take a fair time, and you'd need to do that for every single trial of finding a good `W`, so it would just take way too long.

Turns out though that you can use calculus to work out gradients much faster and more precisely, so we should definitely do that. 

One thing the non-calculus method *is* good for though, is testing your calculus method. Generally you create a gradient-working-out function then make sure it's giving the same results as he good old fashioned method above.

## Gradient descent

Finally we're here. the heart of machine learning. This is a simple method for finding a "good enough" `W`, which works like this:

1. Select a random `W`
1. Select a step size `s`
2. Define your loss function `L`
3. Construct a function which takes `W`, some images and `L` and returns a loss `l`
4. Select a random bunch of training images `i` (not too large so we can iterate through this process quickly)
5. Calculate the negative gradient `g` (which will be a vector gradient consisting of lots of values) of the above function for the inputs `W` and `i`
6. Take each value in `g`, multiply it `s`, and add the resulting vector, value-for-value, to `W` to get the next `W`, `W2`
7. return to `5.` with `W2` and repeat until some condition is met.

Step size, also called **learning rate** is a very important hyperparameter. It can be a constant, or something much fancier.