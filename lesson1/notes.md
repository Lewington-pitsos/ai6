# Lesson 1

## Convoloutional Neural network


### What is?

Lets explain what this is in the context of image recognition, specifically, telling a sexy lady from a horse. Humans do this very well. When we see an image of a horse for instance, we extrapolate it into a bunch of abstract features (body shape, number of legs, head shape, etc), and by applying some simple analysis on these (wrong number of legs), tell that we aren't looking at a sexy lady (damn!).

Computers don't have the same luxury (at least innately). They read images as arrays of positive integers. These are a lot harder to analyse, in fact, pretty much impossible to analyse. So how can we train our computers to tell horses from sexy ladies? The answer in this context is *convolution*: turning coarser, hard-to-analyse data into mon you're abstract, easier-to-reason-about data. 

For example, you get the computer to abstract the integers into a map of edges and curves. Then you get it to abstract this further into shapes, or foreground vs background, and so on, until it's able to analyse the image in a way that's similar to how humans would.

### What kind of abstractions?

Current **CNN** best practices are to chain a bunch of standard abstractions together until you get something analyse-able. A common chain might look something like this:

We'll go through each of these processes below.

#### Convolutional Layer

You take raw image (let's assume it's black and white, so a 2-D nested array of integers), try to find small things like edges and curves in it, and record where in the images those edges and curves sit. Lets say our raw image is 480x480 pixels, so 480x480 integers sitting there in a 2-D plain:

OK, so for example, let's say we're looking for straight, vertical lines. What we do first is create a **filter** (**neuron**, **kernel**) that matches a small, straight vertical line. A good example might be this:

What the heck is it? It's an array containing 5 arrays, each of which contains 5 integers (these are sometimes called **weights**). If you converted each weight into a pixel and represented the array as an image, what you'd get, true to form, would be a small vertical line. What will we do with this filter? The idea is simple: we will extract *every* possible 5x5 2-D array from the raw image array (so 3824 possible sub-arrays, which are sometimes called **receptive field**'s). We will then pair each 5x5 receptive field with our filter (integer-to-integer), and multiply these paired integers together to build a third array.

Finally we add all the values on this third array up into a single number. This number represents how well the recptive field matched the filter. If the two (receptive field and filter) were very similar, the resulting single number will be very high, if the two weren't so similar, say the receptive field happened to map over a portion of the original raw image that contained a horizontal line, the score would be much lower.

Because our filter is supposed to represent a straight vertical line, the resulting integer sum can be thought of as a measure of how *straight-vertical-liney* a given receptive field is. The last step in the Convolutional layer is to compile all these *lineyness* scores into a their own 2-D array, each corresponding to where the relevant receptive field sat in the original raw image array. 

And Kapow! We now have a slightly more abstract representation of the image called a **feature map** or **activation map**. We're no longer dealing with 2-D array of near-meaningless integers representing *whiteness*. Instead we have a similar 2-D array of near-meaningless integers representing *lineyness*, which is, get this, *ever so slightly* easier to reason about. Looking at the original array, it's pretty hard to tell anything. Looking at the feature map we can at least tell, without too much headache, where the lines are (ok, to be fair because we're talking about lines, we probably could have worked out where they were by looking at the original pixel integers, but you get the idea: we can look for fancier things like curves and whatnot).

You can (and quite often probably should) make multiple feature maps from a given raw image using different filters. So for instance you might make curve feature map to go with the straight line feature map using a filter that looked like this:

... and so on. Layering lots of these feature maps on top of each other can give you some nice, rich data for the next stages (multiple feature maps layered on top of each other are usually just called a feature map, which is annoying). Just keep in mind: in reality usually people mostly use 3x3 filters on the raw image data, and the weightings are usually numbers like `-1`, `0` or `2`. You can google exactly why of you're keen. 

OK: so that's a convolutional later. 

Literally the **ENTIRETY** of CNN is build around chaining these guys together. I.e. you create a simple feature map, representing the location and degree of basic features in the image (lines, curves, blobs, whatever), and then create a more complex feature map *from that feature map* which detects slightly more complex features like parallel lines, circles, etc. After repeating this process a bunch of time, you might be able to identify some properly meaningful features of the image. 

Also, fun fact: as you get further along this chain, the filters (and thus the receptive fields) often get larger, allowing the network to identify larger features in the image.

#### Rectifier Layer

Basically what this is/does is to clear up some of the natural, unwanted distortions that are likely to exist in our feature maps due to the convolutional process. We're going to be running multiple further convolutional steps on these feature maps after all, so it's important that these stay close to the original raw image, or else the end result won't really represent anything useful.

#### Pool

#### Fully Connected Layer

Ok, so lets say we've gotten to the end of our chain and we feel like we're ready to actually apply some analysis to the current feature map, how the bejesus do we do that? Well in this case, if you recall, we're trying to work out whether the image we've been given depicts a horse or a sexy lady. In CNN terms, these would both be considered **classes**, in this case the only classes in consideration. A class is basically a list of expected features and a weighting for each feature. So for instance the `sexy lady` class would probably have expected features like `forehead`, `hands`, and `nose`. 

To construct the fully connected layer, you compare the feature scores present on the current feature map to the features, and generate a probability score for each class depending on how well the feature map matches its features. In this case, we'd see that our feature map has very low scores for `forehead`, `nose` and `hands` and higher scores for `mane` and `nostrils`, so we would assign a higher probability to the `horse` class. In the end we'll have an output that looks a bit like this:

    [0.16, 0.84]

Meaning that our CNN has concluded that there's an 84% chance we're looking at a horse, and only a 16% chance we're looking at a sexy lady (so there's still hope).


### Training

All well and good.