# C7 — Recovering Neural Network Models

This Python proof of concept recovers the parameters of a randomly
generated 10–10–1 ReLU network from black-box queries that return a
scalar floating-point output. It adapts the differential extraction
method in Section 4.2 of Carlini, Jagielski, and Mironov, CRYPTO 2020.

## Requirements

Python 3.10 or newer. The implementation uses the Python standard library.

## Run

Run these commands from the repository root.

```sh
python build.py
python -B src/benchmark.py
```

`build.py` checks syntax and runs one end-to-end recovery test.
`benchmark.py` runs 100 target seeds and reports success rate, attack
query count, runtime, and maximum parameter and output errors.

## Model assumptions

The hidden-layer input weights are nonnegative and sum to one for each
neuron. This public normalization fixes the positive scaling ambiguity
of ReLU neurons. The attack receives only the query function. The
evaluator uses the true parameters to compare recovered neurons after
aligning them by hidden bias.

## Use of Generative AI

OpenAI ChatGPT was used to assist with understanding the general approach and assist in writing the toy examples and build script.

ChatGPT also helped debug an implementation issue: a recovered hidden bias was computed but never stored.  The initial README text and this disclosure were also drafted with ChatGPT. 

## Reference

Carlini, N., Jagielski, M., and Mironov, I. (2020).
[Cryptanalytic Extraction of Neural Network Models](https://doi.org/10.1007/978-3-030-56877-1_7).