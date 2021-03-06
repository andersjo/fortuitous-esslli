% Fortuitous data
% ESSLLI 2016, Day 3
% https://fortuitousdata.github.io/

# Representations and learning from related tasks

## Today

1. Neural Networks: Graph view
2. Representations 
4. Multi-task learning
5. Fortuitous NLP
    * Part-of-speech tagging with bi-LSTMs and auxiliary loss
    * Keystroke dynamics as source for syntactic chunking

----

# Neural Networks - Graph view

After this part you should:
* know about the different equivalent formulizations of a neural network 
* understand the computational graph abstraction

## Feed-forward Neural Network

 $$y= NN(\mathbf{x}) $$

input: $\mathbf{x}$ (vector with $d_{in}$ dimensions)

output: $\mathbf{y}$ (output with $d_{out}$ classes)

----

## Example

Formalization and corresponding visualization:

$$NN_{MLP1}(\mathbf{x})=\sigma(g(\mathbf{xW^1+b^1})\mathbf{W^2}+\mathbf{b^2})$$

![](pics/nn.png)

## Computational graph:

- nodes are operations
- gray boxes are parameters

$$NN_{MLP1}(\mathbf{x})=g(\mathbf{xW^1+b^1})\mathbf{W^2}+\mathbf{b^2}$$ 

 ![](pics/compgraph1.png){ width=15%}



## Where do the weights come frome?

It's an **optimization** problem. 

![](pics/mountains_at_home.jpg){width=60%}

. . .

We need:

1. a loss function $l(\tilde y, y)$
2. a way to change the model (parameters) to get closer to a good model (hint: SGD)

## Minimize loss using gradient-based method

![](https://upload.wikimedia.org/wikipedia/commons/6/6d/Error_surface_of_a_linear_neuron_with_two_input_weights.png)

## Skeleton of gradient descent:
    
**Input**: training set, loss function $l$

Repeat for number of iterations (**epochs**): 
 
* compute loss on data: $l(X,Y)$
* compute gradients: $\mathbf{g} = \frac{\partial}{\partial \theta} l(X,Y)$ with respect to $\theta$
* move parameters in direction of the negative gradient: $\theta \pm -\eta \mathbf{g}$

## Backprop


* backward pass: gradient computations (through chain rule) 


## Summary: Equivalent formulizations 

![Complete Neural Network](pics/compgraphcomplete.png){ width=50%}

## Loss

![](pics/yoav.png){ width=80%}


----


. . .

However, what is the input **$x$**?

# Representations

## Feature representations

> Probably the biggest jump when moving from traditional linear models with sparse inputs to deep neural networks is to stop representing each feature as a unique dimension, but instead represent them as **dense vectors** [@goldberg-primer].

. . . 

**discrete representation**

$$\mathbf{x}_{cat} = [0,0,0,0,0,0,1] $$
$$\mathbf{x}_{dog} = [0,0,0,0,1,0,0] $$

**similarity** on discrete representations? 

. . .

$$sim(\mathbf{x}_{cat},\mathbf{x}_{dog}) = 0$$

## Word embeddings

<center>**"You shall know a word by the company it keeps"** (Firth, J. R. 1957:11)</center>

----

![](pics/flødebolle.png){width=100%}

## Approaches

> 1. Traditional approach: LSA (SVD) on word-coocurrence matrix
> 
> 2. word2vec

----

## LSA - Latent Semantic Analysis 

Approximate a matrix $\mathbf{C}$ through a decomposition into three submatrices (**of smaller dimensionality**) - Singular Value Decomposition (SVD):

$$\mathbf{C} \approx \mathbf{U \sum V^T}$$

![by Simon Paarlberg](https://simonpaarlberg.com/posts/2012-06-28-latent-semantic-analyses/box2.png)

NB. $=$ should be $\approx$

----

![](pics/space.png)

## word2vec

Main idea:

* instead of capturing co-occurence statistics of words
* **predict context** (surrounding words of every word); in particular, predict words in a window of length $m$ around current word 

since SVD computation cost scales quadratically with size of co-occurence matrix

----

![@mikolov2013](pics/skipgram.png){width=50%}

. . . 

NB. denominator $\sum$ over all words! $\rightarrow$ *negative sampling* or *hierarchical softmax*


----

Note: embeddings are not specific to **words**



## Sparse vs dense 

![@goldberg-primer](pics/sparse-vs-dense.png){width=77%}

## Dense feature spaces

A common choice for $c$ is **concatenation**:

$$\mathbf{x} = c(f_1, f_2, f_3) = [v(f_1); v(f_2); v(f_3)] $$

----

Other representations:

. . . 

**sum **:

$$\mathbf{x} = c(f_1, f_2, f3) = [v(f_1)+v(f_2)+v(f_3)] $$

**mean**:

$$\mathbf{x} = c(f_1, f_2, f3) = [mean(v(f_1),v(f_2),v(f_3))] $$

----

![$$x$$ sparse, dense or both](pics/compgraphcomplete.png){ width=70%}


# Multi-task learning

## Key idea

The idea of **multi-task learning** [@caruana1998multitask, @Collobert:ea:2011] to exploit the training signal of **other tasks**. 


## Example: Card game

- you are in beautiful Italy and want to get acquainted with local card games. You hear about 'scala 40', and are eager to learn it

- The input space are cards, and the output space are configuations (hands) of your cards. 

- You know already how to play poker. Rather than starting from scratch (**tabula rasa**), you use your internal knowledge of poker (or generally how to play a card game) to learn how to play 'scala 40'.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Royal_straight_flush.jpg/1920px-Royal_straight_flush.jpg){width=30%}


## Embeddings as fortuitous data in Transfer learning 


- want: model that works better on other variety of data
- pool of unlabeled data, estimate embeddings (word2vec)

. . . 

Why would using embeddings work?

----

- embeddings provide latent space $\mathcal{Z}$, **side benefit** of optimising another objective (language model)
- add to feature space $\phi(x)$, latent space $\mathcal{Z}$ 
    * add to one-hot vector
    * initialize embeddings in dense 





## Multi-task learning

![](pics/mtl.png)



## Why does MTL work? 


![Reduced capacity [@caruana1998multitask]](pics/Edible_fungi_in_basket_2012_G1.jpg){width=80%}


----

![Eavesdropping](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Henri_Adolphe_Laissement_Kardin%C3%A4le_im_Vorzimmer_1895.jpg/1920px-Henri_Adolphe_Laissement_Kardin%C3%A4le_im_Vorzimmer_1895.jpg){width=70%}

----


![scikit - denoising filters](http://www.scipy-lectures.org/_images/plot_filter_coins_1.png)

Noise in extra outputs might be less harmful than in extra input [@caruana1998multitask] (also: **weighting** of loss)


----

![](pics/mtl-loss.png)

. . . 

**Joint training with:**
 
1. jointly labeled data, but also
2. distinct sources (!) [for NLP first noted in @collobert:weston:2008]

----

## Deep Joint Training 

[@collobert:weston:2008]

1. Select the next task.
2. Select a random training example for this task. 
3. Update the NN for this task by taking a gradient step with respect to this example.
4. Go to 1.


# Successful MTL

## The first self-driving car

![CMU Alvinn MTL [@caruana1998multitask]](pics/alvinn.png)


----

![CMU Alvinn MTL [@caruana1998multitask]](pics/alvinn-mtl.png)

**Note**: here all task labels computable from data


----

![CMU Alvinn MTL [@caruana1998multitask]](pics/alvinn-mtl-result.png)


## Using the future to predict the present

![[@caruana1998multitask] Using future lab results as extra outputs](pics/caruana-future.png){width=70%}


## First approaches in NLP

![@collobert:weston:2008](pics/collobert-weston-2008.png)

----

![@collobert:weston:2008](pics/collobert-weston-2008-plot.png)

## Open domain name error detection

![@cheng2015open](pics/ostendorf.png){width=50%}

----

## Encoder Decoder models / Sequence to Sequence


![@luong2016multi](pics/encdec.png)

----

##  Sequence to Sequence multi-task learning model

![@luong2016multi](pics/encdecmtl.png)


## All that glitters is not ...


- more computation

- difficulty of defining task relatedness, really knowing when it works

- does not always work 



# Fortuitous NLP 


## Multilingual POS tagging with auxiliary loss 


How affected are neural network-based taggers by...?

> - representation
>
> - language
>
> - data set size

[@plank:ea:2016]

## RNN-based tagger

![Karpathy](pics/rnn-overview.png)


## Model

![@plank:ea:2016](pics/plank-model1.png)


## Results 

![](pics/plank-results1.png)

----

![](pics/plank-results2.png)

## Learning curves

![](pics/plank-res1.png)

(more learning curves in paper)

## Auxiliary loss

![@plank:ea:2016](pics/plank-model2.png)

----

![](pics/plank-res2.png)

## Take-home message

- LSTM-based tagger less suspectible to large data requirement than assumed

- Char embeddings especially helpful for Slavic and non-IE languages

- Alternative view of data (fortuitous data!) via multi-task learning helpful!

## Example 2: Are keystroke logs informative for NLP?

. . . 

![](pics/keystrokes1.png)

## Typology of fortuitous data

![](pics/typology.png)


----

## Motivation
![](pics/keystrokes2.png)


----

![](pics/keystrokes3.png)

----

![](pics/keystrokes4.png)

----

![](pics/keystrokes5.png)

----

![](pics/keystrokes6.png)

## From keystrokes to labels

![](pics/keystrokes7.png)


## Word pauses and POS

![](pics/keystrokes8.png)

## Multi-task learning

![](pics/keystrokes9.png)


## Model

![](pics/keystrokes10.png)

----

## Results

![](pics/keystrokes11.png)

----
![](pics/keystrokes12.png)

(also promising results for CCG tagging)



# References

## References {.allowframebreaks}
