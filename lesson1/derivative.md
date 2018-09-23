# What the fuck even is a derivative?

First things first.

## What is a graph?

A graph represents the relationship between two things. 

Generally these things can be called x and y, after the x and y axis of a graph. So while a graph can represent the relationship (insofar as that relationship is mathematically quantifiable) between any two things, all graphs can be said to represent the relationship between x and y.

## Graphs as functions

The relationship between x and y can be thought of as a **function** from x to y (or vise versa) under the pure, mathematical definition of a function, because each value of x on a graph (or at least the simple graphs we're dealing with) will have an associated value for y. For instance the size vs weight graph maps the following relationship between x and y.

    y = x + 10

This relationship could be represented as a function of/from x:

    f(x) => x + 10 

Using this function we can compute the value of y for any value of x, for that graph.

    y = f(x)

## derivatives

In cases like this, where y can be expressed in terms of a function of x (any function of x), we can work out the **derivative** of y. y's derivative is expressed as `dx/dy`. You work out the derivative of y as follows

if 

    y = x^n

then

    dx/dy = nx^n-1 | dx/dy = ((x + h)^2 - x^2) / h

For example, the relationship between x and y in the speed vs time graph can be represented as:

    y = x^2 

So the derivative of y can be represented as:

    dx/dy = 2x^1 = 2x | dx/dy = 2(x +)

Similarly

    y = x^6 ergo dx/dy = 6x^5s

And keep in mind that since in all these cases `y = the function of x` the derivative of y is exactly the same of the derivative of the function itself. So the derivative of x^7 is 7x^6. Lastly, as a maths shorthand for actually thinking, if there are multiple terms in the function, you derive each seperately

    y = 3x^2 + 5x^5 ergo dx/dy = 6x + 25x^4

### What IS a derivative though?

if `f(x)` is the function of a graph, the derivative of `f(x)` is another function, let's call it `df(x)`. What `df(x)` represents is the **gradient** or **slopiness** of `f(x)` at a given point along the graph line (i.e. for a given value of x). 


More concretely. When finding a derivative we're trying to find out how fast the graph line is changing for any given value of x, *at that point*. So, lets take the size vs weight graph, and lets say we have an x (size) of 5.

    f(5) = 15

The question is, what is the rate-of-change in the graph at that point? Or, in simpler terms, as size increases or decreases, do we get a similar amount of weight? What is the ratio between the increase or decrease in size, and the increase or decrease in size?

Lets try to work it out. Let's add a bit to the size, check how it effects the height, and then check exactly what ratio there was between the change in height and the change in size.

    f(5 + 3) = f(8) = 18

Ok, great, so by adding `3` to size, we've got a new weight: `18`. If we subtract this from the what we had before (`f(5)`, or `15`), we will get the amount of *extra* weight we got by adding `3` to size, which is `3`. Ok, great, so we added `3` to size and got `3` extra weight. Intuitively we can see that the **slopiness** of the graph line between these two points has not changed, but mathematicians don't care about intuition. We need to formalize this somehow, and basically we do that by dividing the amount we added to `x` (`3`) by the amount that, as a result, got added to `y` (also `3`). The result in this case is `1`, so this is the derivative of the size vs weight graph: `1`. 

But this is just derivative of the graph between the values of 5 and 8. What we actually want is to find the derivative of the graph for *any value of x*, and as a nice start it would even be nice to just have the **slopiness** of the graph at the point where x is 5. But we don't even know THAT!. All we know is that the rate of change change between 5 and 8 is `1`, i.e. constant. This matches the size vs weight graph, but it might also match a graph like this:

Which would be misleading. Ideally we want to take the smallest possible value to add to x that will generate a new point on the graph, and calculate the rate of change between x and y between those two points. But because we're dealing with complete functions, every possible value of x will generate a new graph point, so the value we're looking for is infinitely small. Ultimately, all we can do is approximate.

The derivitive of x is just that formula ___, and the gradient for a given point in the graph for a given x value is

for some h.

The other formula is just kind of a shorthand for this elegant mathematical fact. If f(x) doesn't involve x^2 anywhere, then we have a graph whose rate or change is linear.


for x^3 dx/dy = 3x^2

for 2 = 36

144 / 4

(f(x + h) - f(x))/ h = 

This can be expressed as 

    f(5) = 15of
    f(5 + 3) = 18

