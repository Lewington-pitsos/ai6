# Learning rate

## Some strats

You don't have to have a constant learning rate throughout the whole process of training. Near the beginning it is often good to take larger steps, so sometimes you just reduce step size after the 100,000th step or something like that, or decay the learning rate slowly.

Step decay is often common, where if the loss starts to plateau, you drop the learning rate, and this make helps your algorithm narrow in on the bottom of a small area of optima

## Alternative way to pick a good learning rate

Something to do with a **Hessian matrix**.

## Second rank hyperparamater

You could think of learning rate decay as its own hyperparameter, but in practice some things matter less than others and you should focus on the important ones first. You can think of the less important hyperparameters as "second rank" hyperparameters. You probably don't need to bother with these as much, and maybe only after you have all the first rank hyperparameters down pat.

Learning rate is very important and a good example of a first rank hyperparameter, learning rate decay is a good example of something that is second rank.