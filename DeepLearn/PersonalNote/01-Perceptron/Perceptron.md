# Perceptron

To begin with deep learning and nerual network, we should learn the base: perceptron

In the 1960s, Frank Rosenblatt propose a artificial neural network structure, named Perceptron. The basic unit of this netwrok can simplely describe as a formula, usually called single perceptron

for example:

![single perceptron](../images/single-perceptron.png)
$$
output =f_{a}( bias + \sum\limits_{i=1}^{3}input_{i}\times weight_{i})
$$
Here is the explain of the formula

- $output$: the output of the unit.

- $f_{a}$: the activation function of the unit.

- $bias$: the bias of the unit, one of parameter of the network

- $input_{i}$: the input singal

- $weight_{i}$: the weight of the input singal, the most important parameter of the netwrok.

In this example, we only have 3 inputs, when we have more inputs, such as we have n inputs, it will be like that:
$$
output =f_{a}( bias + \sum\limits_{i=1}^{n}input_{i}\times weight_{i})
$$

# How Percetpron Learn

Trainning means use exist date to get suitable weight and bias for the perceptron.

How weight and bias adjust? There is Delta rule:
$$
\Delta weight_{i}=learning\_rate*(target-output)*input_{i} \\
weight_{i} = \Delta weight_{i} + weight_{i}
$$
and as for bias, it will be
$$
\Delta bias = learning\_rate * (target-output) * 1 \\
bias = \Delta bias + bias
$$

> A more explain about the different between $\Delta weight$ and $\Delta bias$ 
>
> if we treat the bias as $weight_{0}$, and there is a default $input_{0}=1$, then the formula will be more succinct
> $$
> output =f_{a}(\sum\limits_{i=0}^{3}input_{i}\times weight_{i})
> $$
> for computer programming, it highly recommand because more easy to archieve; but hard for people understand
>
> and we can use Delta rule to conclude the second bias change rule.