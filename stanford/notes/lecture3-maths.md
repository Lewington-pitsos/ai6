# Norm

Imagine a vector. 

Good. It has a length and width, x and y values respectively. The norm of a vector is `sqrt(x^2 + y^2)` (which is just basic pythagoras). I.e. the line that actually represents the arrow-bit of the vector running diagonally away from the 0 at the middle of the graph. It's norm can be said to be it's "length". 

You can also think of the norm of a vector `v` as being  `sqrt((x1^2 + y1^2) - (x2^2 + y2^2))` where `x2` and `y2` make up the starting **point** of `v`. In the canonical example of a vector, `x2` and `y2` are 0, so we can just ignore them.

# Polynomial

These are a subset of all mathematical expressions.

They are all the expressions that equal the sum of of one or more (but still a finite number of) terms, where each term consists of a **coefficient** whose variable is being raised to a *NON NEGATIVE** and **INTEGER** value.

So these are polynomials

    6 (because 6 is a polynomial whose variable is being raised to the 0th power and 0 is non-negative)
    2x^7 + 70y
    9 + 10y + xy^4

And these are not

    2x^y
    2x^2x
    2x^-9

## degree

The degree of a polynomial is the value of *highest* power to which any term in the polynomial is raised. So the highest degree polynomial we have so far is `2x^7 + 70y` and it has a degree of 7.
    

# Term

This is any mathematical expression which consists of:

1. a number, or
2. a variable, or
3. a chain of numbers or variables multiplied together

So these are all single terms:

    x
    2
    2yx
    7y^4

These are NOT single terms

    x + 4 <<< it is not any of those three things, it is a variable plus another number
    2x / 5 
    7xy^5 - 8


# Coefficient 

According to google it is

    a numerical or constant quantity placed before and multiplying the variable in an algebraic expression

So there are no coefficients in the following expressions:

    5 
    x + 7
    7 * 54 + x
    xy + 88
    y^5

This is because nowhere there is there a constant quantity (like a number `4`, `6`, `213`, or a constant `e` or `pie`) multiplying a variable. We have variables multiplying variables, but neither counts as a coefficient. Even the last one has no coefficient. nowhere is `y` being multiplied by anything other than more `y`

These are coefficients

    7x (the 7)
    -47xyz + 8 (the -47)
    67x^2 (the 67)
    9

Even the last one can be considered a coefficient, because we could write it as

    9x^0

So it still fits the bill.


# softmax

This is a function which takes a bunch of numbers `yn` and for each number `y`



Raises the special maths number `e` to the `y`

        e^y = whatever
        e^3.1 = 24.5325301971
        e^5.1 = 164.0219073

You can use python numpy to do this easily

    np.exp(3.1) = 24.5325301971

And then sums all these raised numbers. 

And finally divides each by that sum. The idea behind this is we actually end up with a **probability distribution**, a vector where all the numbers sum to 1, from our original random vector.

For example take the vector

    [4.5, 6.7, 1.1]

Lets calculate a softmax

    S([4.5, 6.7, 1.1])

So get the exponent (or whatever it's called) of all three

    [90.0171313 , 812.40582517,   3.00416602]

Get the sum of this

    sum([90.0171313 , 812.40582517,   3.00416602]) = 905.4271224920116

Divide each of the exponentiated numbers by this sum:

    [90.0171313 , 812.40582517,   3.00416602] / 905.4271224920116 = [0.09941952, 0.89726252, 0.00331795]

And that's the output:

     S([4.5, 6.7, 1.1]) = [0.09941952, 0.89726252, 0.00331795]

