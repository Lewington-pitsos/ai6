# Simple classifiers

Let's just come up with a super basic strategy for classifying images, just to get a feel for what we're going to be doing in the long run. We'll use the cfar-10 image set, which consists of a grotesquely immense set of 32x32 labelled images. 

These images are separated into a training set and a test set. The idea is: you teach your algorithm to label the images in the training set correctly, and then test it to see how well it can label the test images (none of which are in the practice set). Let's try something basic.

# Nearest Neighbor

This is an algorithm that actually doesn't involve any training. The nearest neighbor algorithm simply states that you can compute the similarity (or distance) between two (equally sized) images `a` and `b` simply by:

1. Comparing the pixels of two images, pixel to pixel
2. Performing some simple operation to generate a third image `c` from a pixel-by-pixel comparison between the two
3. Agglomorating all of `c`'s pixels into a single value

And concluding that that value represents the distance between `a` and `b`. For instance a very simple version of the nearest neighbor uses the  **l1** or **manhatten** **distance metric** to calculate the distance value between images `a` and `b`.

1. Subtract each pixel in `a` from the corresponding pixel in `b` to create a *new* image `c`
2. Convert all of `c`'s values to absolute values (some of `b`'s pixel values may have been higher than `a`'s pixel values)
3. Add all of `c`'s values together. 

Boom, we have our distance value between `a` and `b`, with lower values meaning less distance.

In the context of cifar this means that to label a given test image `t` we must:

1. Take `t` and line it up with the first image of our training set `i1`
2. Apply the l1 algorithm to get the sum of the absolute value of  `t` - `i1` (where subtraction occurs pixel-to-pixel) i.e. the **l1 distance**.
3. Repeat for **EVERY SINGLE IMAGE** in the training set.
4. find the training image with the lowest l1 distance from the test image
5. return it's label

As you can imagine, this is pretty inaccurate (for cifar it seems to get the correct label 25% of the time). There are a few ways we can make this a bit better though.

## Improvements

Putting aside how terrible nearest neighbor is in general, one of its more subtle issues is that we're only ever considering the closest training image. Lets say we have a test image `t` of a horse. If we're a little lucky the training image with the lowest l1 distance will also be of a horse and we'll label it correctly. However, in a huge training set of 1 million images or whatever, there's a chance that there will also be an image `c` of a car or something, which just so happens to share a lot of pixels with `t`. If `c` actually has the lowest l1 distance, we'll get a mislabel because the single lowest l1 distance is all we ever care about, no matter how many very similar horse images there might have been. 

So, a fun way to prevent this is to select your nearest neighbor "democratically".

 1. grab the 5 lowest l1 distance training images for `t`
 2. grab the *single* lowest l1 distance training image for each of *them*
 3. of these indirectly selected training images, choose the one which appears most often, and label `t` by whatever label that image has

 This way, even though `c` is among the closest 5 images, chances are some of the other 4 images will have a horse as *their* nearest neighbor, so we might label things correctly this time. At the very least we're a lot less likely to have our prediction skewed by randomly similar images. For me it bumped the accuracy up from 0.25 to 0.28.

 ## A nice mental model

 Picture this: every single possible black and white image represented as an integer. This is possible! For each possible image you could:

 1. Convert it to an array of integers (all still unique)
 2. Raise each element to the power of its index
 3. Add the resulting numbers up, and hey presto (still unique i'm 99999.9% sure).

 Or something like that. Anyway, point is you could represent each image as a number. That being the case, you could arrange them all in the field of the natural numbers. 

 Ok, cool beans. Now let's imagine every training image as a single point on that field. OK whatever, point is we can represent our "problem space" like this.

 ### Other Distance metrics

 We can also substitute other things for the l1 algorithm. For instance, you can use **l2**, or the **euclidean** distance to calculate the distance, and hence nearest neighbor (or neighbors) for a given image. Depending on what the medium we're working in this might be more effective (although in my case it turned out to make things worse yielding, 18% correct predictions).

## How do we choose?

How can you tell though, which distance metric to use? Or how many neighbors to pick when using the democratic method? Questions like these, i.e. about which algorithms to plug-and-play are said to deal with **hyperparameters**. Generally which are best will depend on the problem at hand, but a common thing people do is just trial and error them.

## How to trial and error

An intuitive idea is: "ok, I'll pick a set of hyperparameters `h` and teach my algorithm using the training data. I'll then test it on the test data and see how accurate I got. I'll then choose a second set of hyperparameters `h2` and repeat the same process and compare which set preformed better on the tests data. Turns out this is not a good idea.

Why? The whole point of test data is that you *never ever try to optimize your algorithm for it*. Using the above process we can never know if we've *actually* picked a good set of hyperparameters unless we go ahead and test it on a *NEW* set of test data that we didn't optimize for and it ALSO performs well. But then our original test data isn't even test data anymore, we've just turned it into more training data.

The actual solution is to split your data into 3 sets:

1. training
2. validation
3. test

Train your algorithm on the training data. Trial and error hyperparameters on your validation data (could you just train the hyperparameters???), and finally only ever test (once preferably, you shouldn't really test till you're fully done) on your test data. 

In line with this idea is something called **cross validation**, which basically means:
1. separate your training data into `n` folds
2. train on `n - 1` of them and use the final one for validation
3. rotate them around so you're now validating against a new fold

Basically that seems to make sense, but sometimes it turns out to be a bit too expensive to actually do.

## collecting data

Basically:

1. collect it ALL
2. randomly (make sure its random) divvy it up


## Things bad with the nearest neighbor classifier

It doesn't need any training, but it has to look at every single training image every time it runs, so it's very very very slow in practice.

ALso, think back to that idea of putting all possible images on a graph, and our training images being scattered around it, with "near" (in the sense of l1 distance) images being close to one another. Imagine we only have like 3 training images on this  whole big graph. Clearly our classifier won't work very well, because lots of very widely varying images are all going to be classified in the same way, since they share a common nearest neighbor (that's ages away). So, in reality we'd need a lot of images for this to be any good. 

BUT: fun fact, we'd actually need an immense number of images because there are just so many possible images. AND the more dimensions the images have (i.e. colored images have 3 dimensions while black and white one have only 1), the more immense this number becomes. :(. You want to **densly cover the problem space** and you can't.