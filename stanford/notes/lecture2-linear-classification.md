
# linear classification

Unlike NN, this is actually kind of good/usable. In fact it is actually used. 

## Parametric approach

One of the really gay things about NN was that you had to literally look at EVERY SINGLE TRAINING IMAGE to come up with a classification for a single test image. The parametric approach says you can distill what you know about the training data into a bunch of parameters, and at test time you just use these parameters (along with your specially crafted function) to classify the test image. This is about a billion times cheaper.

So, before we had a function which took an immense pile of labelled images and a single test image and returned a label

    f(pile, test) -> label

Now, we want to take in some parameters instead of the pile, and we want to output a bunch of "label scores" (i.e. estimated likelihood the test image having this label)

    f(parameters, test) -> label scores

The test image is still exactly the same. The parameters can be whatever we want, as long as they work with the function. For now we're going to use a very simple approach where `f` is a linear function, and `parameters` are just a big template

## What kind of big template?

Lets start simple and assume there's only one label: horse. All we want our simple linear classifier to do is tell us a score for how *horsey* an image is. In this case we might make our parameters very simple: just a single image of a horse. All we'd do is, pass in this image, line it up with the test image and calculate the l1 score between the two. The result would represent the **horse-distance**, i.e. the higher the score, the less horsey the image is. Badda bim badda boom, we've got ourselves a very bad linear classifier.

Of course, what we really want is to make a good linear classifier, and we want to have more labels...

## Add More labels

This is easy. We could simply add one image for each label. Grab a ship, a car a deer, etc and add these images as parameters too. Now when we pass in a test image, we just calculate the l1 score of it vs every parameter image and we've got our array of label scores. 

It's still terrible though.

## Make it less terrible

Ok, so lets think logically. The problem with comparing every test image to the one image of this horse is that there are probably a lot of pictures of horses with pixels in different places. Those pictures will get hight l1 distance scores when compared to this original horse, and hence low horse scores. 

Do you think though, that there might possibly be *some* image out there that might give low l1 distances for most pictures of horses? There *are* probably a bunch general patterns of pixels that you'd expect to occur in most images of horses right? A large lump of brown pixels in the middle might be a good start for instance, maybe green pixels down the bottom because horses are often found in fields of grass? Theoretically one might try to grab all those patterns, or a few of them, and plonk them in an image. That image would probably do better than just some random horse image right?

But how do we work out which patterns to include? Intuition is nice, but that's more of a 19th century thing. Nowdays we have these fancy things called computers...

## Training

The idea is: start by generating a totally random image. Totally random. No cheating. This is your horse template. Doesn't much look like a horse right now, but give it time. Now you run it past your training images...

## Issues with linear classifiers

So lets imagine we're trying to make a linear classifier for coconuts. There are two pretty distinct states a coconut can be in: a brown hairy ball or a smooth, white half bowl. We would want our classifier to classify both as coconuts, but it's going to be very hard to pass in parameters that will match both these things. Like, for example, what color would you make its pixels, white or dark brown? A mix  between the two seems kind of reasonable, but then there's a  chance you'll start matching light brown things too.