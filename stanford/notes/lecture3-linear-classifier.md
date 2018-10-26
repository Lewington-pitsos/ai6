# Linear Classifiers

Another way of thinking of these sets of parameters or **templates**: Lets say we are classifying black and white images. the template is a matrix of the same size as the images we're testing or training against, such that every integer in that matrix represents how important the corresponding pixel is to the overall score of the relevant class. For instance, if we're talking about an image of a plane, it is quite important that the pixels at the top of the screen be a light color. Therefore a good plane template in a linear classifier would have high weightings for pixels near thr top of the image, so that images which have light (i.e. high valued) pixels near the top get a boost in score, and those that do not get a (relative) drop.

High (negative or positive) integer values in a template mean that the value of the corresponding pixels are important to the class. Lower (closer to 0) values correspond to pixels whose values don't tell us much about whether we are looking at an example of the class or not. 

In a colored image, different colors of pixels will get different weightings. If you're looking for clifford the big red dog, the weightings of red pixels will probably have high positive values, especially near the center. The weightings of green pixels near the edges will probably have lower values, since these could just be parts of the background, there are probably around as many images of clifford with pixels like this in them as without.


## Training linear classifiers

We can call these templates, or rather a single class template a **W**, because maths people hate naming things. the W is the big important thing we're dealing with here. In particular, how do we create a W such that our linear classifier function

    f(x, W) = p
    f(image, templates) = predictions

gives us good predictions (i.e. `predictions` where the actual class of `image` scores the highest).

## Loss function

This is a function that takes a W, and the classifier function, and an image and returns how *bad* that W was i.e. how it's predictions were

    lf(image, function, W, actual_label) = how bad W is (i.e. it's Loss)
    lf(x, f, W, r) = l

Once we have a good loss function, we could just apply it to all possible W's, and eventually we'd find the best W, and then we'd make that our template and everybody is happy. There are a low of possible W's though. Iterating through all of them would be impractical. We'd also have to feed every possible W to every possible image too to see which one is the best overall (not just for the one image).

As well as a good loss function, what we really need is a way of working out which W's are likely to be better, based on the ones we've already tested and hence which ones to test with our loss function. If we can find decent heuristic we should be able to *narrow in* on better and better W's and eventually we'll have a decent one.

That's what **training** means by the way.

## Formalizing loss function

Given a set of examples of size `N`, where each example has the form

    (x, y)

Where `x` is an image and `y` is a label, which is probably just an integer.

And `f` is our linear classifier function, which takes an image (`x`) and a set of templates (`W`) and makes a prediction (`p`)

    f(x, W) = p

Our loss function `Li` will take in the predictions for a given `f(x, W)` and `y`, and return `L`: the loss value for that `W`. 

    Li(f(x, W), y) = L

Technically you could just pass in any prediction `p` as the first argument to `Li` to get an arbetrary `L` but you only care about an `L` relative to a `W` so there probs isn't much point. 

## Example loss function: multi-class svm loss

Of course this loss function could take a number of forms. A simple one we're going to jerry-rig up (called **multi-class svm loss** ) will go as follows:

1. Where `c` is the correct class, and its score is `sc` 
2. Take every other class score `s^n`, and find the greater of (0 or `s^n` - `sc`)
3. Sum all the results of `2.` together, and you have your loss

So according to this function, any `W` which generates a prediction set where the score for the correct prediction is higher than each of the incorrect predictions, has a loss of `0` (so, "good enough"). 

Actually we're going to make this a bit more stringent, and make the second step (`s^n` + 1) - `sc` or 0. We can think of the extra 1 as a kind of safety margin in this case. We don't want to consider any `W` "good enough" unless the correct class is out-scoring the each of the other classes by a decent margin.

If you test your algorithm on a whole bunch of images and calculate the loss for each image, you usually get the loss for that data-set by averaging out the loss for each image.

Another fun fact: when we start training you usually start with a `W` of small random values. Such a `W` would be expected to have a loss of about `s - 1` where `s` is the number of classes. If you get a different loss at the beginning of training then it's a sign something has probably gone wrong.

Lastly, if we also calculated (0 or `(sc + 1) - sc`) while we're calculating it for all other `s^n`, we'd end up with a minimum loss of `1`. This wouldn't really change our calculations, we could still happily use the saftey margin as our minimum loss, but by convention we like to use `0` because it's clean.

We could also use `mean` instead of `sum`. This would change the loss value, but the relative loss values would remain the same (this is because both `mean` and `sum` are linear. Using `^2` before summing would skew the relative values, making large losses comparatively much more large). Because of this, we'd end up picking the same `W` whether or not we use `mean` or `sum` (except for the constant `1` safety margin).

## Interlude: Hinge Loss

A function that returns the higher of (`a` - `b`) or  0 is often referred to as a **hinge loss** function, because this is what it looks like on a graph. Imagine `b` is the x axis and the output `0` of the hinge loss function is the y axis. In this case we're going to get this "backslash" type line that slopes downwards forever on our graph. As soon as `b` is higher than a certain quantity though (whatever `a` is, to be precise), the graph line will hit `0`, and continue to be flat forever after. Basically it looks a bit like a hinge with an obtuse angle. 

## Why is 0 loss good enough?

We could, of course, be super stringent, and demand that out `W` get far higher scores in order to be considered "good enough". A simple way to do this would be to increase the safety margin to like, 100, or multiply all the incorrect scores by 2 before subtracting `sc` from them. What this would do though, is:

1. Take longer to train an acceptable classifier
2. Only accept classifiers that fit the training data *really* well. 

`2.` is quite problematic because it might mean we end up creating a classifier that matches the 100 odd horses we're training against super well, but fails to match other images of horses. E.g. all our horses happen to be in fields, so our classifier learns to categorically reject anything not in a field (super high scores for high green valued pixels at the bottom of the screen).  

## Regularization

In fact, **over-fitting**, training an algorithm too narrowly to fit training data is a big problem in machine learning as a whole. To try to prevent over-fitting we often add a **regularization** expression to any loss function.

The idea behind this expression is that it will just add extra loss for more complex `W`'s. This way the `W`'s we end up choosing are more likely to be simple and general, which might mean they fit the training data less perfectly, but will probably mean they're going to fit the test data (and indeed the huge set of all data) better.

Regularization depends on hyperparameters, so it's one of those tricky things you're going to have to trial and error a bit probably, how simple/general to force your `W`'s to be.

A common example of a regularization function is just to sum all the values in `W`. This would penalize `W`'s that have high weights, which makes sense, since we can see how `W`'s like that could over-fit the training data more easily.

In all cases the regularization function `R` will form part of the loss function and take in the `W` itself as an argument.

    R(W)

### Bias regularization

For some creepy reason when people try to regularize bias terms it generally performs worse. Just don't bother (probably something to do with them not having any effect on the gradients maybe).

## Another loss function: Multinomial logistic regression

Also known as a **softmax classifier**, basically what you do is take the set of predictions `p`, and generate a **probability distribution** from it using the **softmax function** `sp`. 

You then compare `sp` to the *actual* probability distribution (which, since we know the real class of the image we're classifying, is like [0, 0, 0, 1, 0, 0, 0, 0]), to get the loss function. Because we know the actual probability distribution always  looks like this though, we can just apply some maths to `cp` the probability from `sp` of the actual correct label to get the loss. Namely, you get it's **negative log**:

    -log(cp) = loss

The minimum loss here is 0 still (where `cp` is one) and the maximum is ininifte, since `-log(x)` gets infinitly larger as `x` approaches 0 (which it could easily, if our classifier is like, an anti-classifier). 

To *actually* get a 1 for `cp` though, you'd have to generate a `p` where the correct prediction scores infinity, and the incorrect ones score -infinity so... good luck with that.

Again, on the first round when `p` is basically randomized and sitting near 0, we can expect the softmax classifier loss function to give us around `-log(1/n)` where `n` is the number of classes that are scored for in `p`. Which is actually the same as `log(n)` as it turns out.

This is used a lot more often than the svm loss function, but they do tend to perform more or less as well as each other.

You'll never get a perfect score with the softmax classifier.

