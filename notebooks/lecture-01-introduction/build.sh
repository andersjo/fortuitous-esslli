#!/usr/bin/env bash
name=$(echo $1 | cut -f 1 -d '.')
pandoc --standalone --slide-level 2 --variable width="1200" --variable height="900" --variable theme="simple" \
--mathjax="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" \
  -t revealjs+raw_html --bibliography refs.bib $1 -o ${name}.html