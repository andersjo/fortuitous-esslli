% Fortuitous data
% ESSLLI 2016, Day 1
% Željko Agić, Anders Johannsen, Barbara Plank 
# The course

<style type="text/css">
p { text-align: left; }
</style>

# Motivation

## Ultimate goal: NLP for everyone

![Languages used on the Internet](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/WebsiteContentLanguages.svg/447px-WebsiteContentLanguages.svg.png){ width=90% }

## Example

![Tagging Twitter #hard](pics/twitter.png){ width=90% }

## Labeled data is **scarce**

![Training data sparsity](pics/datapool.png){ width=90% }

## Labeled data is **biased**

For a long while main resource: Wall Street Journal (WSJ), texts from late 80s.

<larger>
``*it is an uncomfortable fact that the text in **many of our most frequently-used corpora** was written and edited predominantly **by working-age white men***’’ [@eisenstein:2013:bad]
</larger>

![Training data sparsity](pics/wsj.png){ width=60% }


## Still newswire?

![**Training data sparsity:** subset of treebanks from Universal Dependencies v1.2 [@UDLREC] for which domain/genre info is available [@plank:2016:konvens]](pics/domains-lang.png){ width=90% }

<div class="notes">
Data is weird. Researchers make invalid assumptions. Results become inflated.

- One very good example. 

It used to be the case that language data = articles published in the Wall Street Journal around 1986.
</div>

## What if language technology could start over?

- English newswire has advanced our field, but also introduced impercetible biases
- Why is newswire more **canonical** than other text types?
- If NLP could start over, what would be our canon?


<div class="notes">
- Notion of canonical data.
- UD/Wall street bias. 
- Languages. 

How would we avoid making the same mistakes again? Wikipedia is biased, social media commentary is biased. 
</div>


## What’s in a **domain**?

POS tagging accuracies versus OOV rate/POS bigram KL divergence

![](pics/oov-acc.png){ width=49% }\ ![](pics/kl-acc.png){ width=49% }



## Data mismatch - dichotomy:

![Train/application time](pics/xdom.png){ width=100% }

- Train <> Test
- Source <> Target

Really a dichotomy?

## The variety space

Where do our data come from?

…

Our datasets $\mathcal{D}$ are sampled from a **variety space**

<larger>
$$\mathcal{D} \sim P(X, Y|V)$$
</larger>

Is there such a variety space? What would the factors be?

. . .

![Possible dimensions for the variety space](pics/variety.png){ width=70%, style="border: none"}

## General statement of the problem

Whatever we consider **canonical**, the challenge remains: processing non-canonical data is hard.

## Silly problem with simple solution?

### Proposal 1: Annotate more?

Could we simply make sure that we annotate the right data? And more data. [@eisenstein:2013:bad]

<div class="notes">
Unsustainable, for many reasons. 

(We cannot annotate *enough* data for every single task that we wish to solve). 
- take language and domain; cross-product; huge space
- our ways of communication change, so does our data; social media is a moving target 
- there is data out there, however it's unlabeled
</div>


### Map to canonical form?

Example: spelling normalisation. [e.g. @han:baldwin:2013]

<div class="notes">
A more powerful version of this is *invariant representations*. 
</div>


### Domain adaptation

Example: Importance weighting. 

Not final answer. Often, in reality, we don't know the target domain. And we don't like the term "domain". 

(Hal Daume, 2007 - or Weiss paper on transfer learning).

## Fortuitous data (this course)

![Fortuitous](pics/fortuitous-def.png){ width=100% }

Annotate more: reuse data that was not explicitly annotated. 

Learn invariant representations of data.

Learn invariant representations of data.

# Overview of the course

The shape of things to come.

## Monday

### A typology of data mismatch
### Overview of semi-supervised learning

## Tuesday

### Structured prediction

## Wednesday

### your very own fortuitous learner (hands on).

## Thursday

### Learning from related tasks

## Friday

### Transfer learning in the extreme 

# Learning inside and outside the shire
# 

# References

## References {.allowframebreaks}
