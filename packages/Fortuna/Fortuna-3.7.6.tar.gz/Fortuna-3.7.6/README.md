# Fortuna: A Collection of Random Value Generators for Python3
Fortuna's main goal is to provide a quick and easy way to build custom random-value generators for your data.

The core functionality of Fortuna is based on the RNG Storm engine. While Storm is a high quality random engine, Fortuna is not appropriate for cryptography of any kind. Fortuna is meant for games, data science, A.I. and experimental programming, not security.

Suggested Installation: `$ pip install Fortuna`

Precompiled for MacOS, installation on other platforms may require building from source.

Support this project: https://www.patreon.com/brokencode


### Table of Contents:
- Numeric Limits
- Project Terminology
- Random Generators:
    - Value Generators
        - `RandomValue(Collection) -> Callable -> Value`
        - `TruffleShuffle(Collection) -> Callable -> Value`
        - `QuantumMonty(Collection) -> Callable -> Value`
        - `CumulativeWeightedChoice(Table) -> Callable -> Value`
        - `RelativeWeightedChoice(Table) -> Callable -> Value`
        - `FlexCat(Matrix) -> Callable -> Value`
    - Integer Generators
        - `random_below(Integer) -> Integer`
        - `random_int(Integer, Integer) -> Integer`
        - `random_range(Integer, Integer, Integer) -> Integer`
        - `d(Integer) -> Integer`
        - `dice(Integer, Integer) -> Integer`
        - `plus_or_minus(Integer) -> Integer`
        - `plus_or_minus_linear(Integer) -> Integer`
        - `plus_or_minus_gauss(Integer) -> Integer`
    - Index Generators: 
        - ZeroCool Specification: `f(N) -> [0, N)` or `f(-N) -> [-N, 0)`
        - `random_index(Integer) -> Integer`
        - `front_gauss(Integer) -> Integer`
        - `middle_gauss(Integer) -> Integer`
        - `back_gauss(Integer) -> Integer`
        - `quantum_gauss(Integer) -> Integer`
        - `front_poisson(Integer) -> Integer`
        - `middle_poisson(Integer) -> Integer`
        - `back_poisson(Integer) -> Integer`
        - `quantum_poisson(Integer) -> Integer`
        - `front_geometric(Integer) -> Integer`
        - `middle_geometric(Integer) -> Integer`
        - `back_geometric(Integer) -> Integer`
        - `quantum_geometric(Integer) -> Integer`
        - `quantum_monty(Integer) -> Integer`
    - Float Generators
        - `canonical() -> Float`
        - `random_float(Float, Float) -> Float`
    - Boolean Generator
        - `percent_true(Float) -> Boolean`
    - Shuffle Algorithms, Inplace & Destructive
        - `shuffle(List) -> None`
        - `knuth(List) -> None`
        - `fisher_yates(List) -> None`
- Test Suite
    - `distribution_timer(Callable, *args, **kwargs) -> None`
    - `quick_test() -> None`
- Development Log
- Test Suite Output
- Legal Information


#### Numeric Limits:
- Integer: 64 bit signed integer.
    - Input & Output Range: `(-2**63, 2**63)` or approximately +/- 9.2 billion billion.
    - Minimum: -9223372036854775807
    - Maximum:  9223372036854775807
- Float: 64 bit floating point.
    - Minimum: -1.7976931348623157e+308
    - Maximum:  1.7976931348623157e+308
    - Epsilon Below Zero: -5e-324
    - Epsilon Above Zero:  5e-324


#### Project Terminology:
- Value: Almost anything in Python can be a Value.
    - Expressions, Generators, and F-strings should be wrapped in a lambda for dynamic evaluation.
- Callable: Any callable object, function, method or lambda.
- Collection: A group of Values.
    - List, Tuple, Set, etc... Any object that can be converted into a list via `list(some_object)`.
    - Comprehensions that produce a Collection also qualify.
    - Fortuna classes that wrap a Collection can wrap a Collection, Sequence or generator.
    - Fortuna functions that take a Collection as input will always require a Sequence.
- Sequence: An ordered Collection.
    - List, tuple or list comprehension.
    - A Sequence is an ordered Collection that can be indexed like a list, without conversion.
    - All Sequences are Collections but not all Collections are Sequences.
- Pair: Collection of two Values.
- Table: Collection of Pairs.
- Matrix: Dictionary of Collections.
- Inclusive Range.
    - `[1, 10] -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
- Exclusive Range.
    - `(0, 11) -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
- Partially Exclusive Range.
    - `[1, 11) -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
    - `(0, 10] -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
- Automatic Flattening.
    - Works with: RandomValue, TruffleShuffle, QuantumMonty, WeightedChoice & FlexCat.
    - Lazy Evaluation. All Random Value Generator Classes in Fortuna will recursively call or "flatten" callable objects returned from the data at call time.
    - Mixing callable objects with un-callable objects is fully supported, but it can look a bit messy.
    - Nested callable objects are fully supported. Because `lambda(lambda) -> lambda` fixes everything for arbitrary values of 'because', 'fixes' and 'everything'.
    - To disable automatic flattening, pass the optional keyword argument `flat=False` to the constructor.
    - **Under development:** It will soon be possible to auto-flatten callable objects that require multiple arguments. RandomValue already supports this feature.


## Random Value Generators

### Fortuna.RandomValue
`Fortuna.RandomValue(data: Collection, flat=True) -> Callable -> Value`
- @param data :: Collection of Values.
- @param flat :: Bool. Default: True. Option to automatically flatten callable values with lazy evaluation.
- @return :: Callable Object. `Callable(*args, zero_cool=random_index, range_to=0, **kwargs) -> Value`
    - @param zero_cool :: Optional ZeroCool Method, kwarg only. Default = random_index().
    - @param range_to :: Optional Integer in range [-N, N] where N is the length of the Collection. 
        - Default = 0, kwarg only. Parameter for ZeroCool Method.
        - Negative values of range_to indicate ranging from the back of the Collection. 
    - @param *args, **kwargs :: Optional arguments used to flatten the return Value.
    - @return Value or Value(*args, **kwargs) if it's Callable.

```python
from Fortuna import RandomValue, front_linear, back_linear

# Data Setup
random_apple = RandomValue(("Delicious", "Empire", "Granny Smith", "Honey Crisp", "Macintosh"))
random_fruit = RandomValue((
    lambda: f"Apple, {random_apple()}",
    "Banana",
    "Cherry",
    "Grapes",
    "Orange",
))

# Usage
print(random_fruit())
# prints a random fruit with the default flat uniform distribution

print(random_fruit(zero_cool=back_linear))
# prints a random fruit with a back_linear distribution

print(random_fruit(range_to=3))
# prints a random fruit of the first 3

print(random_fruit(zero_cool=front_linear, range_to=-3))
# prints a random fruit of the last 3 with a front_linear distribution of that range.
```


### TruffleShuffle
`Fortuna.TruffleShuffle(data: Collection, flat=True) -> Callable -> Value`
- Non-destructive, copies the data once.
- @param data :: Collection of Values. Set recommended but not required.
- @param flat :: Bool. Default: True. Option to automatically flatten callable values with lazy evaluation.
- @return :: Callable
    - @return :: Random value from the list with a **Wide Uniform Distribution**. The average width of the output distribution will naturally scale up with the size of the set.

**Wide Uniform Distribution**: *"Wide"* refers to the average distance between consecutive occurrences of the same value in the output sequence. The goal of this type of distribution is to keep the output sequence free of clumps or streaks of the same value, while maintaining randomness and uniform probability. This is not the same as a *flat uniform distribution*. The two distributions over time will be statistically similar for any given set, but the repetitiveness of the output sequence will be very different.

#### TruffleShuffle, Basic Use
```python
from Fortuna import TruffleShuffle

# Data Setup
list_of_values = { 1, 2, 3, 4, 5, 6 }
truffle_shuffle = TruffleShuffle(list_of_values)

# Usage
print(truffle_shuffle())  # this will print one of the numbers 1-6, 
# over time it will produce a wide distribution.
```

#### RandomValue with Auto Flattening Callable Objects
```python
from Fortuna import RandomValue


auto_flat = RandomValue([lambda: 1, lambda: 2, lambda: 3])
print(auto_flat())  # will print the value 1, 2 or 3.
# Note: the lambda will not be called until call time and stays dynamic for the life of the object.

auto_flat_with = RandomValue([lambda x: x, lambda x: x + 1, lambda x:  x + 2])
print(auto_flat_with(2))  # will print the value 2, 3 or 4
# Note: if this is called with no args it will simply return the lambda in an uncalled state.

un_flat = RandomValue([lambda: 1, lambda: 2, lambda: 3], flat=False)
print(un_flat()())  # will print the value 1, 2 or 3, 
# mind the double-double parenthesis, they are required to manually unpack the lambdas

auto_un_flat = RandomValue([lambda x: x, lambda x: x + 1, lambda x:  x + 2], flat=False)
# Note: flat=False is not required here because the lambdas can not be called without input x satisfied.
# It is still recommended to specify flat=False if non-flat output is intend.
print(auto_un_flat()(1))  # will print the value 1, 2 or 3, mind the double-double parenthesis
```

#### Mixing Static Objects with Callable Objects
```python
from Fortuna import RandomValue


""" With automatic flattening active, lambda() -> int can be treated as an int. """
mixed_flat = RandomValue([1, 2, lambda: 3])
print(mixed_flat())  # will print 1, 2 or 3

mixed_un_flat = RandomValue([1, 2, lambda: 3], flat=False) # this pattern is not recommended.
print(mixed_flat())  # will print 1, 2 or "Function <lambda at some_address>"
# This pattern is not recommended because you wont know the nature of what you get back.
# This is almost always not what you want, and it can give rise to messy logic in other areas of your code.
```

#### Dynamic Strings
To successfully express a dynamic string, and keep it dynamic, at least one level of indirection is required. Without an indirection the f-string would collapse into a static string too soon.

```python
from Fortuna import RandomValue, d


# d() is a simple dice function, d(n) -> [1, n] flat uniform distribution.
dynamic_string = RandomValue((
    # while the probability of all A == all B == all C, individual probabilities of each possible string will differ based on the number of possible outputs of each category.
    lambda: f"A{d(2)}",  # -> A1 - A2, each are twice as likely as any particular B, and three times as likely as any C.
    lambda: f"B{d(4)}",  # -> B1 - B4, each are half as likely as any particular A, and 3/2 as likely as any C.
    lambda: f"C{d(6)}",  # -> C1 - C6, each are 1/3 as likely as any particular A and 2/3 as likely of any B.
))

print(dynamic_string())  # prints a random dynamic string, flattened at call time.

"""
>>> distribution_timer(dynamic_string)
Output Analysis: RandomValue(collection)()
Typical Timing: 875 ± 15 ns
Distribution of 100000 Samples:
 A1: 16.657%
 A2: 16.777%
 B1: 8.408%
 B2: 8.266%
 B3: 8.334%
 B4: 8.203%
 C1: 5.635%
 C2: 5.641%
 C3: 5.468%
 C4: 5.537%
 C5: 5.528%
 C6: 5.546%
 """
```

#### Nesting Dolls
```python
from Fortuna import RandomValue

# Data Setup
nesting_dolls = RandomValue({
    RandomValue({"A", "B", "C", "D", "E"}),
    RandomValue({"F", "G", "H", "I", "J"}),
    RandomValue({"K", "L", "M", "N", "O"}),
    RandomValue({"P", "Q", "R", "S", "T"}),
    ...
})

# Usage
print(nesting_dolls())  # prints one of the letters A-T
```

### QuantumMonty
`Fortuna.QuantumMonty(data: Collection, flat=True) -> Callable -> Value`
- @param data :: Collection of Values.
- @param flat :: Bool. Default: True. Option to automatically flatten callable values with lazy evaluation.
- @return :: Callable Object with Monty Methods for producing various distributions of the data.
    - @return :: Random value from the data. The instance will produce random values from the list using the selected distribution model or "monty". The default monty is the Quantum Monty Algorithm.

```python
from Fortuna import QuantumMonty

# Data Setup
list_of_values = [1, 2, 3, 4, 5, 6]
monty = QuantumMonty(list_of_values)

# Usage
print(monty())               # prints a random value from the list_of_values.
                             # uses the default Quantum Monty Algorithm.

print(monty.flat_uniform())  # prints a random value from the list_of_values.
                             # uses the "flat_uniform" monty.
                             # equivalent to random.choice(list_of_values).
```
The QuantumMonty class represents a diverse collection of strategies for producing random values from a sequence where the output distribution is based on the method you choose. Generally speaking, each value in the sequence will have a probability that is based on its position in the sequence. For example: the "front" monty produces random values where the beginning of the sequence is geometrically more common than the back. Given enough samples the "front" monty will always converge to a 45 degree slope down for any list of unique values.

There are three primary method families: linear, gaussian, and poisson. Each family has three base methods; 'front', 'middle', 'back', plus a 'quantum' method that incorporates all three base methods. The quantum algorithms for each family produce distributions by overlapping the probability waves of the other methods in their family. The Quantum Monty Algorithm incorporates all nine base methods.

```python
import Fortuna

# Data Setup
monty = Fortuna.QuantumMonty(
    ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
)

# Usage
# Each of the following methods will return a random value from the sequence.
# Each method has its own unique distribution model.
""" Flat Base Case """
monty.flat_uniform()        # Flat Uniform Distribution
""" Geometric Positional """
monty.front_linear()        # Linear Descending, Triangle
monty.middle_linear()       # Linear Median Peak, Equilateral Triangle
monty.back_linear()         # Linear Ascending, Triangle
monty.quantum_linear()      # Linear Overlay, 3-way monty.
""" Gaussian Positional """
monty.front_gauss()         # Front Gamma
monty.middle_gauss()        # Scaled Gaussian
monty.back_gauss()          # Reversed Gamma
monty.quantum_gauss()       # Gaussian Overlay, 3-way monty.
""" Poisson Positional """
monty.front_poisson()       # 1/4 Mean Poisson
monty.middle_poisson()      # 1/2 Mean Poisson
monty.back_poisson()        # 3/4 Mean Poisson
monty.quantum_poisson()     # Poisson Overlay, 3-way monty.
""" Quantum Monty Algorithm """
monty()                     # Quantum Monty Algorithm, 9-way monty.
monty.quantum_monty()       #  same as above
```

### Weighted Choice: Base Class
Weighted Choice offers two strategies for selecting random values from a sequence where programmable rarity is desired. Both produce a custom distribution of values based on the weights of the values.

The choice to use one strategy over the other is purely about which one suits you or your data best. Relative weights are easier to understand at a glance. However, many RPG Treasure Tables map rather nicely to a cumulative weighted strategy.

#### Cumulative Weighted Choice
`Fortuna.CumulativeWeightedChoice(weighted_table: Table, flat=True) -> Callable -> Value`
- @param weighted_table :: Table of weighted pairs.
- @param flat :: Bool. Default: True. Option to automatically flatten callable values with lazy evaluation.
- @return :: Callable Instance
    - @return :: Random value from the weighted_table, distribution based on the weights of the values.

_Note: Logic dictates Cumulative Weights must be unique!_

```python
from Fortuna import CumulativeWeightedChoice

# Data Setup
cum_weighted_choice = CumulativeWeightedChoice((
    (7, "Apple"),
    (11, "Banana"),
    (13, "Cherry"),
    (23, "Grape"),
    (26, "Lime"),
    (30, "Orange"),  # same as relative weight 4 because 30 - 26 = 4
))
# Usage
print(cum_weighted_choice())  # prints a weighted random value
```

#### Relative Weighted Choice
`Fortuna.RelativeWeightedChoice(weighted_table: Table) -> Callable -> Value`
- @param weighted_table :: Table of weighted pairs.
- @param flat :: Bool. Default: True. Option to automatically flatten callable values with lazy evaluation.
- @return :: Callable Instance
    - @return :: Random value from the weighted_table, distribution based on the weights of the values.

```python
from Fortuna import RelativeWeightedChoice

# Data
population = ["Apple", "Banana", "Cherry", "Grape", "Lime", "Orange"]
rel_weights = [7, 4, 2, 10, 3, 4]

# Setup
rel_weighted_choice = RelativeWeightedChoice(zip(rel_weights, population))

# Usage
print(rel_weighted_choice())  # prints a weighted random value
```

### FlexCat
`Fortuna.FlexCat(dict_of_lists: Matrix, key_bias="front_linear", val_bias="truffle_shuffle", flat=True) -> Callable -> Value`
- @param dict_of_lists :: Keyed Matrix of Value Sequences.
- @parm key_bias :: String indicating the name of the algorithm to use for random key selection.
- @parm val_bias :: String indicating the name of the algorithm to use for random value selection.
- @param flat :: Bool. Default: True. Option to automatically flatten callable values with lazy evaluation.
- @return :: Callable Instance
    - @param cat_key :: Optional String. Default is None. Key selection by name. If specified, this will override the key_bias for a single call.
    - @return :: Value. Returns a random value generated with val_bias from a random sequence generated with key_bias.

FlexCat is like a two dimensional QuantumMonty, or a QuantumMonty of QuantumMontys.

The constructor takes two optional keyword arguments to specify the algorithms to be used to make random selections. The algorithm specified for selecting a key need not be the same as the one for selecting values. An optional key may be provided at call time to bypass the random key selection. Keys passed in this way must exactly match a key in the Matrix.

By default, FlexCat will use key_bias="front_linear" and val_bias="truffle_shuffle", this will make the top of the data structure geometrically more common than the bottom and it will truffle shuffle the sequence values. This config is known as TopCat, it produces a descending-step, micro-shuffled distribution sequence. Many other combinations are available.

Algorithmic Options: _See QuantumMonty & TruffleShuffle for more details._
- "front_linear", Linear Descending
- "middle_linear", Linear Median Peak
- "back_linear", Linear Ascending
- "quantum_linear", Linear 3-way monty
- "front_gauss", Gamma Descending
- "middle_gauss", Scaled Gaussian
- "back_gauss", Gamma Ascending
- "quantum_gauss", Gaussian 3-way monty
- "front_poisson", Front 1/3 Mean Poisson
- "middle_poisson", Middle Mean Poisson
- "back_poisson", Back 1/3 Mean Poisson
- "quantum_poisson", Poisson 3-way monty
- "quantum_monty", Quantum Monty Algorithm, 9-way monty
- "flat_uniform", uniform flat distribution
- "truffle_shuffle", TruffleShuffle, wide uniform distribution

```python
from Fortuna import FlexCat, d
#
#
#                           |- Collection Generator, does not require lambda.
#                           |  Cat_A is equivalent to Cat_B
# Data                      |
matrix_data = {#            $                         |- Dynamic Value Expression
    "Cat_A": (f"A{i}" for i in range(1, 6)),  #       |  Lazy evaluation, 1 of 4
    "Cat_B": ("B1", "B2", "B3", "B4", "B5"),  #       $
    "Cat_C": ("C1", "C2", "C3", f"C4.{d(2)}", lambda: f"C5.{d(4)}")}
#    $       $       $              $                        $
#    |       |       |- Value       |                        |- Fair die method
#    |       |                      |
#    |       |- Collection          |- Static Value Expression, evaluated only once.
#    |                              |  Eager evaluation, 1 of 2 permanently
#    |- Collection Key, "cat_key"
#                                   |- Collection Selection  |- Value Selection
# Setup                             $  Y-axis                $  X-axis
flex_cat = FlexCat(matrix_data, key_bias="front_linear", val_bias="flat_uniform")
#    $       $       $
#    |       |       |- Matrix, Dictionary of Collections
#    |       |
#    |       |- Constructor
#    |       
#    |- Callable
#
# Usage
flex_cat()  # returns a Value from the Matrix.
flex_cat(cat_key="Cat_B")  # returns a Value specifically from the "Cat_B" Collection.
```

### Random Integer Generators
`Fortuna.random_below(number: int) -> int`
- @param number :: Any Integer
- @return :: Returns a random integer in the range...
    - `random_below(number) -> [0, number)` for positive values.
    - `random_below(number) -> (number, 0]` for negative values.
    - `random_below(0) -> 0` Always returns zero when input is zero
- Flat uniform distribution.


`Fortuna.random_int(left_limit: int, right_limit: int) -> int`
- @param left_limit :: Any Integer
- @param right_limit :: Any Integer
- @return :: Returns a random integer in the range [left_limit, right_limit]
    - `random_int(1, 10) -> [1, 10]`
    - `random_int(10, 1) -> [1, 10]` same as above.
    - `random_int(A, B)` Always returns A when A == B
- Flat uniform distribution.


`Fortuna.random_range(start: int, stop: int = 0, step: int = 1) -> int`
- @param start :: Required starting point.
    - `random_range(0) -> [0]`
    - `random_range(10) -> [0, 10)` from 0 to 9. Same as `Fortuna.random_index(N)`
    - `random_range(-10) -> [-10, 0)` from -10 to -1. Same as `Fortuna.random_index(-N)`
- @param stop :: Zero by default. Optional range bound. With at least two arguments, the order of the first two does not matter.
    - `random_range(0, 0) -> [0]`
    - `random_range(0, 10) -> [0, 10)` from 0 to 9.
    - `random_range(10, 0) -> [0, 10)` same as above.
- @param step :: One by default. Optional step size.
    - `random_range(0, 0, 0) -> [0]`
    - `random_range(0, 10, 2) -> [0, 10) by 2` even numbers from 0 to 8.
    - The sign of the step parameter controls the phase of the output. Negative stepping will flip the inclusively.
    - `random_range(0, 10, -1) -> (0, 10]` starts at 10 and ranges down to 1.
    - `random_range(10, 0, -1) -> (0, 10]` same as above.
    - `random_range(10, 10, 0) -> [10]` a step size or range size of zero always returns the first parameter.
- @return :: Returns a random integer in the range [A, B) by increments of C.
- Flat uniform distribution.


`Fortuna.d(sides: int) -> int`
- Represents a single roll of a given size die.
- @param sides :: Any Integer. Represents the size or number of sides, most commonly six.
- @return :: Returns a random integer in the range [1, sides].
- Flat uniform distribution.


`Fortuna.dice(rolls: int, sides: int) -> int`
- Represents the sum of multiple rolls of the same size die.
- @param rolls :: Any Integer. Represents the number of times to roll the die.
- @param sides :: Any Integer. Represents the die size or number of sides, most commonly six.
- @return :: Returns a random integer in range [X, Y] where X = rolls and Y = rolls * sides.
- Geometric distribution based on the number and size of the dice rolled.
- Complexity scales primarily with the number of rolls, not the size of the dice.


`Fortuna.plus_or_minus(number: int) -> int`
- @param number :: Any Integer.
- @return :: Returns a random integer in range [-number, number].
- Flat uniform distribution.


`Fortuna.plus_or_minus_linear(number: int) -> int`
- @param number :: Any Integer.
- @return :: Returns a random integer in range [-number, number].
- Linear geometric, 45 degree triangle distribution centered on zero.


`Fortuna.plus_or_minus_gauss(number: int) -> int`
- @param number :: Any Integer.
- @return :: Returns a random integer in range [-number, number].
- Stretched gaussian distribution centered on zero.


### Random Index, ZeroCool Specification
ZeroCool Methods are used to generate random Sequence indices.

ZeroCool methods must have the following properties:
- Any distribution model is acceptable.
- The method or function must take exactly one Integer parameter N.
- The method returns a random int in range `[0, N)` for positive values of N.
- The method returns a random int in range `[N, 0)` for negative values of N.
- This symmetry matches how python can index a list from the back for negative index values or from the front for positive index values.


```python
from Fortuna import random_index


some_list = [i for i in range(100)]

print(some_list[random_index(10)])  # prints one of the first 10 items of some_list, [0, 9]
print(some_list[random_index(-10)])  # prints one of the last 10 items of some_list, [90, 99]
```
### ZeroCool Methods
- `Fortuna.random_index(size: int) -> int` Flat uniform distribution
- `Fortuna.front_gauss(size: int) -> int` Gamma Distribution: Front Peak
- `Fortuna.middle_gauss(size: int) -> int` Stretched Gaussian Distribution: Median Peak
- `Fortuna.back_gauss(size: int) -> int` Gamma Distribution: Back Peak
- `Fortuna.quantum_gauss(size: int) -> int` Quantum Gaussian: Three-way Monty
- `Fortuna.front_poisson(size: int) -> int` Poisson Distribution: Front 1/3 Peak
- `Fortuna.middle_poisson(size: int) -> int` Poisson Distribution: Middle Peak
- `Fortuna.back_poisson(size: int) -> int` Poisson Distribution: Back 1/3 Peak
- `Fortuna.quantum_poisson(size: int) -> int` Quantum Poisson: Three-way Monty
- `Fortuna.front_geometric(size: int) -> int` Linear Geometric: 45 Degree Front Peak
- `Fortuna.middle_geometric(size: int) -> int` Linear Geometric: 45 Degree Middle Peak
- `Fortuna.back_geometric(size: int) -> int` Linear Geometric: 45 Degree Back Peak
- `Fortuna.quantum_geometric(size: int) -> int` Quantum Geometric: Three-way Monty
- `Fortuna.quantum_monty(size: int) -> int` Quantum Monty: Twelve-way Monty

```python
from Fortuna import front_gauss, middle_gauss, back_gauss, quantum_gauss


some_list = [i for i in range(100)]

# Each of the following prints one of the first 10 items of some_list with the appropriate distribution
print(some_list[front_gauss(10)])
print(some_list[middle_gauss(10)])
print(some_list[back_gauss(10)])
print(some_list[quantum_gauss(10)])

# Each of the following prints one of the last 10 items of some_list with the appropriate distribution
print(some_list[front_gauss(-10)])  
print(some_list[middle_gauss(-10)])  
print(some_list[back_gauss(-10)])  
print(some_list[quantum_gauss(-10)])
```

### Random Float Generators
`Fortuna.canonical() -> float`
- @return :: random float in range [0.0, 1.0), flat uniform.


`Fortuna.random_float(a: Float, b: Float) -> Float`
- @param a :: Float
- @param b :: Float
- @return :: random Float in range [a, b), flat uniform distribution.


`Fortuna.triangular(low Float, high Float, mode Float) -> Float`
- @param low :: Float, minimum output
- @param high :: Float, maximum output
- @param mode :: Float, most common output, mode must be in range `[low, high]`
- @return :: random number in range `[low, high]` with a linear distribution about the mode.


### Random Truth Generator
`Fortuna.percent_true(truth_factor: Float = 50.0) -> bool`
- @param truth_factor :: The probability of True as a percentage. Default is 50 percent.
- @return :: Produces True or False based on the truth_factor.
    - Always returns False if num is 0 or less
    - Always returns True if num is 100 or more.


### Shuffle Algorithms
`Fortuna.shuffle(array: list) -> None`
- Knuth B shuffle algorithm. Destructive, in-place shuffle.
- @param array :: Must be a mutable list.

`Fortuna.knuth(array: list) -> None`
- Knuth A shuffle algorithm. Destructive, in-place shuffle.
- @param array :: Must be a mutable list.

`Fortuna.fisher_yates(array: list) -> None`
- Fisher-Yates shuffle algorithm. Destructive, in-place shuffle.
- @param array :: Must be a mutable list.


### Test Suite
`Fortuna.distribution_timer(func, *args, **kwargs)`
- Logs the output statistics, distribution and timing of a pure function as func(*args, **kwargs).

`Fortuna.quick_test(num_cycles=10000)`
- Runs distribution_timer for all relevant functions.


## Fortuna Development Log
##### Fortuna 3.7.6
- Install script update.

##### Fortuna 3.7.5 - internal
- Storm 3.1.1 Update
- Added triangular function.

##### Fortuna 3.7.4
- Fixed: missing header in the project manifest, this may have caused building from source to fail.

##### Fortuna 3.7.3
- Storm Update

##### Fortuna 3.7.2
- Storm Update

##### Fortuna 3.7.1
- Bug fixes

##### Fortuna 3.7.0 - internal
- flatten_with() is now the default flattening algorithm for all Fortuna classes.

##### Fortuna 3.6.5
- Documentation Update
- RandomValue: New flatten-with-arguments functionality.

##### Fortuna 3.6.4
- RandomValue added for testing

##### Fortuna 3.6.3
- Developer Update

##### Fortuna 3.6.2
- Installer Script Update

##### Fortuna 3.6.1
- Documentation Update

##### Fortuna 3.6.0
- Storm Update
- Test Update
- Bug fix for random_range(), negative stepping is now working as intended. This bug was introduced in 3.5.0.
- Removed Features
    - lazy_cat(): use QuantumMonty class instead.
    - flex_cat(): use FlexCat class instead.
    - truffle_shuffle(): use TruffleShuffle class instead.

##### Fortuna 3.5.3 - internal
- Features added for testing & development
    - ActiveChoice class
    - random_rotate() function

##### Fortuna 3.5.2
- Documentation Updates

##### Fortuna 3.5.1
- Test Update

##### Fortuna 3.5.0
- Storm Update
- Minor Bug Fix: Truffle Shuffle
- Deprecated Features
    - lazy_cat(): use QuantumMonty class instead.
    - flex_cat(): use FlexCat class instead.
    - truffle_shuffle(): use TruffleShuffle class instead.

##### Fortuna 3.4.9
- Test Update

##### Fortuna 3.4.8
- Storm Update

##### Fortuna 3.4.7
- Bug fix for analytic_continuation.

##### Fortuna 3.4.6
- Docs Update

##### Fortuna 3.4.5
- Docs Update
- Range Tests Added, see extras folder.

##### Fortuna 3.4.4
- ZeroCool Algorithm Bug Fixes
- Typos Fixed

##### Fortuna 3.4.3
- Docs Update

##### Fortuna 3.4.2
- Typos Fixed

##### Fortuna 3.4.1
- Major Bug Fix: random_index()

##### Fortuna 3.4.0 - internal
- ZeroCool Poisson Algorithm Family Updated

##### Fortuna 3.3.8 - internal
- Docs Update

##### Fortuna 3.3.7
- Fixed Performance Bug: ZeroCool Linear Algorithm Family

##### Fortuna 3.3.6
- Docs Update

##### Fortuna 3.3.5
- ABI Updates
- Bug Fixes

##### Fortuna 3.3.4
- Examples Update

##### Fortuna 3.3.3
- Test Suite Update

##### Fortuna 3.3.2 - internal
- Documentation Update

##### Fortuna 3.3.1 - internal
- Minor Bug Fix

##### Fortuna 3.3.0 - internal
- Added `plus_or_minus_gauss(N: int) -> int` random int in range [-N, N] Stretched Gaussian Distribution

##### Fortuna 3.2.3
- Small Typos Fixed

##### Fortuna 3.2.2
- Documentation update.

##### Fortuna 3.2.1
- Small Typo Fixed

##### Fortuna 3.2.0
- API updates:
    - QunatumMonty.uniform -> QunatumMonty.flat_uniform
    - QunatumMonty.front -> QunatumMonty.front_linear
    - QunatumMonty.middle -> QunatumMonty.middle_linear
    - QunatumMonty.back -> QunatumMonty.back_linear
    - QunatumMonty.quantum -> QunatumMonty.quantum_linear
    - randindex -> random_index
    - randbelow -> random_below
    - randrange -> random_range
    - randint   -> random_int

##### Fortuna 3.1.0
- `discrete()` has been removed, see Weighted Choice.
- `lazy_cat()` added.
- All ZeroCool methods have been raised to top level API, for use with lazy_cat()

##### Fortuna 3.0.1
- minor typos.

##### Fortuna 3.0.0
- Storm 2 Rebuild.

##### Fortuna 2.1.1
- Small bug fixes.
- Test updates.

##### Fortuna 2.1.0, Major Feature Update
- Fortuna now includes the best of RNG and Pyewacket.

##### Fortuna 2.0.3
- Bug fix.

##### Fortuna 2.0.2
- Clarified some documentation.

##### Fortuna 2.0.1
- Fixed some typos.

##### Fortuna 2.0.0b1-10
- Total rebuild. New RNG Storm Engine.

##### Fortuna 1.26.7.1
- README updated.

##### Fortuna 1.26.7
- Small bug fix.

##### Fortuna 1.26.6
- Updated README to reflect recent changes to the test script.

##### Fortuna 1.26.5
- Fixed small bug in test script.

##### Fortuna 1.26.4
- Updated documentation for clarity.
- Fixed a minor typo in the test script.

##### Fortuna 1.26.3
- Clean build.

##### Fortuna 1.26.2
- Fixed some minor typos.

##### Fortuna 1.26.1
- Release.

##### Fortuna 1.26.0 beta 2
- Moved README and LICENSE files into fortuna_extras folder.

##### Fortuna 1.26.0 beta 1
- Dynamic version scheme implemented.
- The Fortuna Extension now requires the fortuna_extras package, previously it was optional.

##### Fortuna 1.25.4
- Fixed some minor typos in the test script.

##### Fortuna 1.25.3
- Since version 1.24 Fortuna requires Python 3.7 or higher. This patch corrects an issue where the setup script incorrectly reported requiring Python 3.6 or higher.

##### Fortuna 1.25.2
- Updated test suite.
- Major performance update for TruffleShuffle.
- Minor performance update for QuantumMonty & FlexCat: cycle monty.

##### Fortuna 1.25.1
- Important bug fix for TruffleShuffle, QuantumMonty and FlexCat.

##### Fortuna 1.25
- Full 64bit support.
- The Distribution & Performance Tests have been redesigned.
- Bloat Control: Two experimental features have been removed.
    - RandomWalk
    - CatWalk
- Bloat Control: Several utility functions have been removed from the top level API. These function remain in the Fortuna namespace for now, but may change in the future without warning.
    - stretch_bell, internal only.
    - min_max, not used anymore.
    - analytic_continuation, internal only.
    - flatten, internal only.

##### Fortuna 1.24.3
- Low level refactoring, non-breaking patch.

##### Fortuna 1.24.2
- Setup config updated to improve installation.

##### Fortuna 1.24.1
- Low level patch to avoid potential ADL issue. All low level function calls are now qualified.

##### Fortuna 1.24
- Documentation updated for even more clarity.
- Bloat Control: Two naïve utility functions that are no longer used in the module have been removed.
    - n_samples -> use a list comprehension instead. `[f(x) for _ in range(n)]`
    - bind -> use a lambda instead. `lambda: f(x)`

##### Fortuna 1.23.7
- Documentation updated for clarity.
- Minor bug fixes.
- TruffleShuffle has been redesigned slightly, it now uses a random rotate instead of swap.
- Custom `__repr__` methods have been added to each class.

##### Fortuna 1.23.6
- New method for QuantumMonty: quantum_not_monty - produces the upside down quantum_monty.
- New bias option for FlexCat: not_monty.

##### Fortuna 1.23.5.1
- Fixed some small typos.

##### Fortuna 1.23.5
- Documentation updated for clarity.
- All sequence wrappers can now accept generators as input.
- Six new functions added:
    - random_float() -> float in range [0.0..1.0) exclusive, uniform flat distribution.
    - percent_true_float(num: float) -> bool, Like percent_true but with floating point precision.
    - plus_or_minus_linear_down(num: int) -> int in range [-num..num], upside down pyramid.
    - plus_or_minus_curve_down(num: int) -> int in range [-num..num], upside down bell curve.
    - mostly_not_middle(num: int) -> int in range [0..num], upside down pyramid.
    - mostly_not_center(num: int) -> int in range [0..num], upside down bell curve.
- Two new methods for QuantumMonty:
    - mostly_not_middle
    - mostly_not_center
- Two new bias options for FlexCat, either can be used to define x and/or y axis bias:
    - not_middle
    - not_center

##### Fortuna 1.23.4.2
- Fixed some minor typos in the README.md file.

##### Fortuna 1.23.4.1
- Fixed some minor typos in the test suite.

##### Fortuna 1.23.4
- Fortuna is now Production/Stable!
- Fortuna and Fortuna Pure now use the same test suite.

##### Fortuna 0.23.4, first release candidate.
- RandomCycle, BlockCycle and TruffleShuffle have been refactored and combined into one class: TruffleShuffle.
- QuantumMonty and FlexCat will now use the new TruffleShuffle for cycling.
- Minor refactoring across the module.

##### Fortuna 0.23.3, internal
- Function shuffle(arr: list) added.

##### Fortuna 0.23.2, internal
- Simplified the plus_or_minus_curve(num: int) function, output will now always be bounded to the range [-num..num].
- Function stretched_bell(num: int) added, this matches the previous behavior of an unbounded plus_or_minus_curve.

##### Fortuna 0.23.1, internal
- Small bug fixes and general clean up.

##### Fortuna 0.23.0
- The number of test cycles in the test suite has been reduced to 10,000 (down from 100,000). The performance of the pure python implementation and the c-extension are now directly comparable.
- Minor tweaks made to the examples in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.22.2, experimental features
- BlockCycle class added.
- RandomWalk class added.
- CatWalk class added.

##### Fortuna 0.22.1
- Fortuna classes no longer return lists of values, this behavior has been extracted to a free function called n_samples.

##### Fortuna 0.22.0, experimental features
- Function bind added.
- Function n_samples added.

##### Fortuna 0.21.3
- Flatten will no longer raise an error if passed a callable item that it can't call. It correctly returns such items in an uncalled state without error.
- Simplified `.../fortuna_extras/fortuna_examples.py` - removed unnecessary class structure.

##### Fortuna 0.21.2
- Fix some minor bugs.

##### Fortuna 0.21.1
- Fixed a bug in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.21.0
- Function flatten added.
- Flatten: The Fortuna classes will recursively unpack callable objects in the data set.

##### Fortuna 0.20.10
- Documentation updated.

##### Fortuna 0.20.9
- Minor bug fixes.

##### Fortuna 0.20.8, internal
- Testing cycle for potential new features.

##### Fortuna 0.20.7
- Documentation updated for clarity.

##### Fortuna 0.20.6
- Tests updated based on recent changes.

##### Fortuna 0.20.5, internal
- Documentation updated based on recent changes.

##### Fortuna 0.20.4, internal
- WeightedChoice (both types) can optionally return a list of samples rather than just one value, control the length of the list via the n_samples argument.

##### Fortuna 0.20.3, internal
- RandomCycle can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.2, internal
- QuantumMonty can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.1, internal
- FlexCat can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.0, internal
- FlexCat now accepts a standard dict as input. The ordered(ness) of dict is now part of the standard in Python 3.7.1. Previously FlexCat required an OrderedDict, now it accepts either and treats them the same.

##### Fortuna 0.19.7
- Fixed bug in `.../fortuna_extras/fortuna_examples.py`.

##### Fortuna 0.19.6
- Updated documentation formatting.
- Small performance tweak for QuantumMonty and FlexCat.

##### Fortuna 0.19.5
- Minor documentation update.

##### Fortuna 0.19.4
- Minor update to all classes for better debugging.

##### Fortuna 0.19.3
- Updated plus_or_minus_curve to allow unbounded output.

##### Fortuna 0.19.2
- Internal development cycle.
- Minor update to FlexCat for better debugging.

##### Fortuna 0.19.1
- Internal development cycle.

##### Fortuna 0.19.0
- Updated documentation for clarity.
- MultiCat has been removed, it is replaced by FlexCat.
- Mostly has been removed, it is replaced by QuantumMonty.

##### Fortuna 0.18.7
- Fixed some more README typos.

##### Fortuna 0.18.6
- Fixed some README typos.

##### Fortuna 0.18.5
- Updated documentation.
- Fixed another minor test bug.

##### Fortuna 0.18.4
- Updated documentation to reflect recent changes.
- Fixed some small test bugs.
- Reduced default number of test cycles to 10,000 - down from 100,000.

##### Fortuna 0.18.3
- Fixed some minor README typos.

##### Fortuna 0.18.2
- Fixed a bug with Fortuna Pure.

##### Fortuna 0.18.1
- Fixed some minor typos.
- Added tests for `.../fortuna_extras/fortuna_pure.py`

##### Fortuna 0.18.0
- Introduced new test format, now includes average call time in nanoseconds.
- Reduced default number of test cycles to 100,000 - down from 1,000,000.
- Added pure Python implementation of Fortuna: `.../fortuna_extras/fortuna_pure.py`
- Promoted several low level functions to top level.
    - `zero_flat(num: int) -> int`
    - `zero_cool(num: int) -> int`
    - `zero_extreme(num: int) -> int`
    - `max_cool(num: int) -> int`
    - `max_extreme(num: int) -> int`
    - `analytic_continuation(func: staticmethod, num: int) -> int`
    - `min_max(num: int, lo: int, hi: int) -> int`

##### Fortuna 0.17.3
- Internal development cycle.

##### Fortuna 0.17.2
- User Requested: dice() and d() functions now support negative numbers as input.

##### Fortuna 0.17.1
- Fixed some minor typos.

##### Fortuna 0.17.0
- Added QuantumMonty to replace Mostly, same default behavior with more options.
- Mostly is depreciated and may be removed in a future release.
- Added FlexCat to replace MultiCat, same default behavior with more options.
- MultiCat is depreciated and may be removed in a future release.
- Expanded the Treasure Table example in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.16.2
- Minor refactoring for WeightedChoice.

##### Fortuna 0.16.1
- Redesigned fortuna_examples.py to feature a dynamic random magic item generator.
- Raised cumulative_weighted_choice function to top level.
- Added test for cumulative_weighted_choice as free function.
- Updated MultiCat documentation for clarity.

##### Fortuna 0.16.0
- Pushed distribution_timer to the .pyx layer.
- Changed default number of iterations of tests to 1 million, up form 1 hundred thousand.
- Reordered tests to better match documentation.
- Added Base Case Fortuna.fast_rand_below.
- Added Base Case Fortuna.fast_d.
- Added Base Case Fortuna.fast_dice.

##### Fortuna 0.15.10
- Internal Development Cycle

##### Fortuna 0.15.9
- Added Base Cases for random_value()
- Added Base Case for randint()

##### Fortuna 0.15.8
- Clarified MultiCat Test

##### Fortuna 0.15.7
- Fixed minor typos.

##### Fortuna 0.15.6
- Fixed minor typos.
- Simplified MultiCat example.

##### Fortuna 0.15.5
- Added MultiCat test.
- Fixed some minor typos in docs.

##### Fortuna 0.15.4
- Performance optimization for both WeightedChoice() variants.
- Cython update provides small performance enhancement across the board.
- Compilation now leverages Python3 all the way down.
- MultiCat pushed to the .pyx layer for better performance.

##### Fortuna 0.15.3
- Reworked the MultiCat example to include several randomizing strategies working in concert.
- Added Multi Dice 10d10 performance tests.
- Updated sudo code in documentation to be more pythonic.

##### Fortuna 0.15.2
- Fixed: Linux installation failure.
- Added: complete source files to the distribution (.cpp .hpp .pyx).

##### Fortuna 0.15.1
- Updated & simplified distribution_timer in `fortuna_tests.py`
- Readme updated, fixed some typos.
- Known issue preventing successful installation on some linux platforms.

##### Fortuna 0.15.0
- Performance tweaks.
- Readme updated, added some details.

##### Fortuna 0.14.1
- Readme updated, fixed some typos.

##### Fortuna 0.14.0
- Fixed a bug where the analytic continuation algorithm caused a rare issue during compilation on some platforms.

##### Fortuna 0.13.3
- Fixed Test Bug: percent sign was missing in output distributions.
- Readme updated: added update history, fixed some typos.

##### Fortuna 0.13.2
- Readme updated for even more clarity.

##### Fortuna 0.13.1
- Readme updated for clarity.

##### Fortuna 0.13.0
- Minor Bug Fixes.
- Readme updated for aesthetics.
- Added Tests: `.../fortuna_extras/fortuna_tests.py`

##### Fortuna 0.12.0
- Internal test for future update.

##### Fortuna 0.11.0
- Initial Release: Public Beta

##### Fortuna 0.10.0
- Module name changed from Dice to Fortuna

##### Dice 0.1.x - 0.9.x
- Experimental Phase


## Fortuna Distribution and Performance Test Suite
```
Fortuna Test Suite: RNG Storm Engine


Numeric Round-trip Limits:

Internal 64 bit Integer Type: <long long>
Min Integer: -9223372036854775807
Max Integer:  9223372036854775807

Internal 64 bit Float Type: <double>
Min Float:   -1.7976931348623157e+308
Max Float:    1.7976931348623157e+308
Neg Epsilon: -5e-324
Pos Epsilon:  5e-324


Output Range Tests: Success!

-------------------------------------------------------------------------

Fortuna Quick Test

Random Sequence Values:

some_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Base Case
Output Analysis: Random.choice(some_list)
Typical Timing: 750 ± 24 ns
Statistics of 256 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.328125
 Std Deviation: 2.9321995357831736
Distribution of 100000 Samples:
 0: 9.874%
 1: 9.99%
 2: 10.072%
 3: 10.057%
 4: 10.025%
 5: 9.964%
 6: 10.107%
 7: 9.924%
 8: 10.017%
 9: 9.97%

Output Analysis: random_value(some_list)
Typical Timing: 63 ± 6 ns
Statistics of 256 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.2578125
 Std Deviation: 2.925871329914507
Distribution of 100000 Samples:
 0: 10.02%
 1: 10.024%
 2: 10.157%
 3: 10.087%
 4: 9.914%
 5: 9.865%
 6: 10.024%
 7: 9.929%
 8: 10.033%
 9: 9.947%

Output Analysis: TruffleShuffle(collection)()
Typical Timing: 532 ± 6 ns
Statistics of 256 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.30078125
 Std Deviation: 2.9076234104606504
Distribution of 100000 Samples:
 0: 9.935%
 1: 10.01%
 2: 9.983%
 3: 10.057%
 4: 10.035%
 5: 9.983%
 6: 10.008%
 7: 10.006%
 8: 10.033%
 9: 9.95%

Output Analysis: QuantumMonty(collection)()
Typical Timing: 532 ± 10 ns
Statistics of 256 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.328125
 Std Deviation: 2.9468743827063584
Distribution of 100000 Samples:
 0: 10.881%
 1: 9.09%
 2: 8.903%
 3: 9.614%
 4: 11.536%
 5: 11.587%
 6: 9.557%
 7: 9.133%
 8: 8.846%
 9: 10.853%

Output Analysis: RandomValue(collection)()
Typical Timing: 344 ± 16 ns
Statistics of 256 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.69921875
 Std Deviation: 2.941148130990918
Distribution of 100000 Samples:
 0: 9.864%
 1: 10.044%
 2: 10.05%
 3: 9.94%
 4: 10.137%
 5: 10.016%
 6: 10.101%
 7: 9.763%
 8: 9.966%
 9: 10.119%


Weighted Tables:

population = ('A', 'B', 'C', 'D')
cum_weights = (1, 3, 6, 10)
rel_weights = (1, 2, 3, 4)
cum_weighted_table = zip(cum_weights, population)
rel_weighted_table = zip(rel_weights, population)

Cumulative Base Case
Output Analysis: Random.choices(population, cum_weights=cum_weights)
Typical Timing: 1657 ± 15 ns
Distribution of 100000 Samples:
 A: 10.02%
 B: 19.805%
 C: 30.113%
 D: 40.062%

Output Analysis: CumulativeWeightedChoice(weighted_table)()
Typical Timing: 438 ± 6 ns
Distribution of 100000 Samples:
 A: 10.192%
 B: 19.9%
 C: 29.828%
 D: 40.08%

Output Analysis: cumulative_weighted_choice(tuple(zip(cum_weights, population)))
Typical Timing: 125 ± 14 ns
Distribution of 100000 Samples:
 A: 10.12%
 B: 19.828%
 C: 29.91%
 D: 40.142%

Relative Base Case
Output Analysis: Random.choices(population, weights=rel_weights)
Typical Timing: 2188 ± 21 ns
Distribution of 100000 Samples:
 A: 10.082%
 B: 19.976%
 C: 30.12%
 D: 39.822%

Output Analysis: RelativeWeightedChoice(weighted_table)()
Typical Timing: 407 ± 1 ns
Distribution of 100000 Samples:
 A: 10.029%
 B: 19.974%
 C: 30.077%
 D: 39.92%


Random Matrix Values:

some_matrix = {'A': (1, 2, 3, 4), 'B': (10, 20, 30, 40), 'C': (100, 200, 300, 400)}

Output Analysis: FlexCat(matrix_data, key_bias='flat_uniform', val_bias='flat_uniform')()
Typical Timing: 750 ± 6 ns
Statistics of 256 Samples:
 Minimum: 1
 Median: (20, 30)
 Maximum: 400
 Mean: 94.30859375
 Std Deviation: 131.85396885315373
Distribution of 100000 Samples:
 1: 8.292%
 2: 8.362%
 3: 8.357%
 4: 8.247%
 10: 8.323%
 20: 8.526%
 30: 8.372%
 40: 8.233%
 100: 8.174%
 200: 8.383%
 300: 8.332%
 400: 8.399%


Random Integers:

Base Case
Output Analysis: Random.randrange(10)
Typical Timing: 813 ± 26 ns
Statistics of 256 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.453125
 Std Deviation: 2.9382117410585162
Distribution of 100000 Samples:
 0: 10.047%
 1: 10.05%
 2: 10.078%
 3: 9.961%
 4: 9.988%
 5: 9.916%
 6: 9.995%
 7: 9.996%
 8: 9.885%
 9: 10.084%

Output Analysis: random_below(10)
Typical Timing: 63 ± 1 ns
Statistics of 256 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.6328125
 Std Deviation: 2.816954533381264
Distribution of 100000 Samples:
 0: 9.976%
 1: 10.014%
 2: 10.102%
 3: 9.987%
 4: 9.944%
 5: 9.909%
 6: 10.086%
 7: 9.997%
 8: 9.902%
 9: 10.083%

Output Analysis: random_index(10)
Typical Timing: 63 ± 6 ns
Statistics of 256 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.24609375
 Std Deviation: 2.850177905524014
Distribution of 100000 Samples:
 0: 10.111%
 1: 10.041%
 2: 9.875%
 3: 10.043%
 4: 10.137%
 5: 9.988%
 6: 9.84%
 7: 9.955%
 8: 9.974%
 9: 10.036%

Output Analysis: random_range(10)
Typical Timing: 63 ± 16 ns
Statistics of 256 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.515625
 Std Deviation: 2.8778651537445694
Distribution of 100000 Samples:
 0: 10.063%
 1: 9.993%
 2: 9.774%
 3: 10.139%
 4: 9.881%
 5: 9.931%
 6: 10.09%
 7: 10.164%
 8: 9.982%
 9: 9.983%

Output Analysis: random_below(-10)
Typical Timing: 63 ± 16 ns
Statistics of 256 Samples:
 Minimum: -9
 Median: (-5, -4)
 Maximum: 0
 Mean: -4.3828125
 Std Deviation: 2.8329187989719413
Distribution of 100000 Samples:
 -9: 9.887%
 -8: 10.109%
 -7: 9.949%
 -6: 10.097%
 -5: 9.974%
 -4: 9.911%
 -3: 9.887%
 -2: 10.129%
 -1: 10.01%
 0: 10.047%

Output Analysis: random_index(-10)
Typical Timing: 63 ± 16 ns
Statistics of 256 Samples:
 Minimum: -10
 Median: -6
 Maximum: -1
 Mean: -5.4921875
 Std Deviation: 2.958526643780783
Distribution of 100000 Samples:
 -10: 9.945%
 -9: 10.115%
 -8: 10.008%
 -7: 10.108%
 -6: 10.0%
 -5: 9.888%
 -4: 9.993%
 -3: 9.928%
 -2: 9.969%
 -1: 10.046%

Output Analysis: random_range(-10)
Typical Timing: 94 ± 1 ns
Statistics of 256 Samples:
 Minimum: -10
 Median: -6
 Maximum: -1
 Mean: -6
 Std Deviation: 2.7553868807746578
Distribution of 100000 Samples:
 -10: 10.127%
 -9: 9.878%
 -8: 10.06%
 -7: 9.914%
 -6: 10.011%
 -5: 10.094%
 -4: 9.998%
 -3: 10.003%
 -2: 10.02%
 -1: 9.895%

Base Case
Output Analysis: Random.randrange(1, 10)
Typical Timing: 1063 ± 26 ns
Statistics of 256 Samples:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 5.02734375
 Std Deviation: 2.524242145053193
Distribution of 100000 Samples:
 1: 11.234%
 2: 11.062%
 3: 11.246%
 4: 11.027%
 5: 11.086%
 6: 11.007%
 7: 11.041%
 8: 11.04%
 9: 11.257%

Output Analysis: random_range(1, 10)
Typical Timing: 63 ± 14 ns
Statistics of 256 Samples:
 Minimum: 1
 Median: 6
 Maximum: 9
 Mean: 5.31640625
 Std Deviation: 2.5662753155298907
Distribution of 100000 Samples:
 1: 11.235%
 2: 10.998%
 3: 11.104%
 4: 11.19%
 5: 11.168%
 6: 11.272%
 7: 10.93%
 8: 10.934%
 9: 11.169%

Output Analysis: random_range(10, 1)
Typical Timing: 63 ± 8 ns
Statistics of 256 Samples:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 4.94140625
 Std Deviation: 2.5453695704160526
Distribution of 100000 Samples:
 1: 11.017%
 2: 11.279%
 3: 11.025%
 4: 11.235%
 5: 11.298%
 6: 10.999%
 7: 11.061%
 8: 11.119%
 9: 10.967%

Base Case
Output Analysis: Random.randint(-5, 5)
Typical Timing: 1188 ± 21 ns
Statistics of 256 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.00390625
 Std Deviation: 3.156689811135312
Distribution of 100000 Samples:
 -5: 9.112%
 -4: 9.129%
 -3: 9.233%
 -2: 9.185%
 -1: 9.015%
 0: 9.038%
 1: 9.15%
 2: 8.958%
 3: 9.005%
 4: 9.077%
 5: 9.098%

Output Analysis: random_int(-5, 5)
Typical Timing: 63 ± 6 ns
Statistics of 256 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: -0.1171875
 Std Deviation: 3.137680156533786
Distribution of 100000 Samples:
 -5: 8.917%
 -4: 9.23%
 -3: 8.995%
 -2: 9.155%
 -1: 9.048%
 0: 9.024%
 1: 9.169%
 2: 9.065%
 3: 9.172%
 4: 9.226%
 5: 8.999%

Base Case
Output Analysis: Random.randrange(1, 20, 2)
Typical Timing: 1250 ± 24 ns
Statistics of 256 Samples:
 Minimum: 1
 Median: 9
 Maximum: 19
 Mean: 10.0078125
 Std Deviation: 5.421809398795087
Distribution of 100000 Samples:
 1: 9.95%
 3: 10.021%
 5: 9.92%
 7: 9.876%
 9: 10.0%
 11: 10.041%
 13: 9.947%
 15: 10.16%
 17: 9.994%
 19: 10.091%

Output Analysis: random_range(1, 20, 2)
Typical Timing: 63 ± 14 ns
Statistics of 256 Samples:
 Minimum: 1
 Median: 9
 Maximum: 19
 Mean: 9.671875
 Std Deviation: 5.787219692106555
Distribution of 100000 Samples:
 1: 9.956%
 3: 10.007%
 5: 9.959%
 7: 9.956%
 9: 9.881%
 11: 10.158%
 13: 10.1%
 15: 10.091%
 17: 9.884%
 19: 10.008%

Output Analysis: random_range(1, 20, -2)
Typical Timing: 94 ± 1 ns
Statistics of 256 Samples:
 Minimum: 2
 Median: 10
 Maximum: 20
 Mean: 10.578125
 Std Deviation: 5.710134609175336
Distribution of 100000 Samples:
 2: 10.121%
 4: 10.044%
 6: 9.886%
 8: 10.095%
 10: 9.899%
 12: 10.018%
 14: 9.893%
 16: 10.077%
 18: 10.082%
 20: 9.885%

Output Analysis: d(10)
Typical Timing: 63 ± 6 ns
Statistics of 256 Samples:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.421875
 Std Deviation: 2.742860607782592
Distribution of 100000 Samples:
 1: 10.08%
 2: 10.081%
 3: 10.01%
 4: 9.909%
 5: 9.986%
 6: 10.031%
 7: 9.884%
 8: 9.987%
 9: 10.131%
 10: 9.901%

Output Analysis: dice(3, 6)
Typical Timing: 94 ± 16 ns
Statistics of 256 Samples:
 Minimum: 4
 Median: 11
 Maximum: 18
 Mean: 10.54296875
 Std Deviation: 2.9648445673970043
Distribution of 100000 Samples:
 3: 0.477%
 4: 1.401%
 5: 2.811%
 6: 4.616%
 7: 6.931%
 8: 9.836%
 9: 11.548%
 10: 12.428%
 11: 12.433%
 12: 11.613%
 13: 9.864%
 14: 6.85%
 15: 4.632%
 16: 2.774%
 17: 1.356%
 18: 0.43%

Output Analysis: ability_dice(4)
Typical Timing: 188 ± 15 ns
Statistics of 256 Samples:
 Minimum: 4
 Median: 12
 Maximum: 18
 Mean: 12.015625
 Std Deviation: 2.9238287415312003
Distribution of 100000 Samples:
 3: 0.079%
 4: 0.302%
 5: 0.819%
 6: 1.62%
 7: 2.907%
 8: 4.716%
 9: 6.895%
 10: 9.567%
 11: 11.389%
 12: 12.791%
 13: 13.355%
 14: 12.353%
 15: 9.973%
 16: 7.434%
 17: 4.25%
 18: 1.55%

Output Analysis: plus_or_minus(5)
Typical Timing: 63 ± 1 ns
Statistics of 256 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: -0.03125
 Std Deviation: 3.137221200799379
Distribution of 100000 Samples:
 -5: 9.175%
 -4: 9.003%
 -3: 9.155%
 -2: 9.046%
 -1: 9.039%
 0: 9.102%
 1: 9.003%
 2: 9.108%
 3: 9.1%
 4: 9.054%
 5: 9.215%

Output Analysis: plus_or_minus_linear(5)
Typical Timing: 63 ± 15 ns
Statistics of 256 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.10546875
 Std Deviation: 2.392924491610427
Distribution of 100000 Samples:
 -5: 2.806%
 -4: 5.548%
 -3: 8.316%
 -2: 11.038%
 -1: 13.733%
 0: 16.603%
 1: 14.25%
 2: 11.101%
 3: 8.336%
 4: 5.555%
 5: 2.714%

Output Analysis: plus_or_minus_gauss(5)
Typical Timing: 94 ± 16 ns
Statistics of 256 Samples:
 Minimum: -4
 Median: 0
 Maximum: 5
 Mean: 0.0625
 Std Deviation: 1.6221505938166185
Distribution of 100000 Samples:
 -5: 0.204%
 -4: 1.152%
 -3: 4.399%
 -2: 11.546%
 -1: 20.43%
 0: 24.479%
 1: 20.255%
 2: 11.568%
 3: 4.562%
 4: 1.206%
 5: 0.199%


Random Floats:

Base Case
Output Analysis: Random.random()
Typical Timing: 32 ± 12 ns
Statistics of 256 Samples:
 Minimum: 0.0020837360045939946
 Median: (0.47975224050387044, 0.48112180271454275)
 Maximum: 0.9981014398945902
 Mean: 0.484465122688263
 Std Deviation: 0.28291159985115466
Post-processor Distribution of 100000 Samples using round():
 0: 49.825%
 1: 50.175%

Output Analysis: canonical()
Typical Timing: 32 ± 16 ns
Statistics of 256 Samples:
 Minimum: 0.003514087015539945
 Median: (0.5417336601328223, 0.5582447160186764)
 Maximum: 0.99747294590086
 Mean: 0.5271668611204686
 Std Deviation: 0.2785288410842707
Post-processor Distribution of 100000 Samples using round():
 0: 50.035%
 1: 49.965%

Output Analysis: random_float(0.0, 10.0)
Typical Timing: 32 ± 16 ns
Statistics of 256 Samples:
 Minimum: 0.0322744674146184
 Median: (5.044865340057636, 5.14481631494972)
 Maximum: 9.990749698361423
 Mean: 5.145187888125204
 Std Deviation: 2.8983614038655148
Post-processor Distribution of 100000 Samples using floor():
 0: 10.022%
 1: 10.074%
 2: 9.909%
 3: 9.916%
 4: 10.059%
 5: 10.098%
 6: 9.957%
 7: 10.013%
 8: 9.978%
 9: 9.974%


Random Booleans:

Output Analysis: percent_true(33.33)
Typical Timing: 32 ± 14 ns
Statistics of 256 Samples:
 Minimum: False
 Median: False
 Maximum: True
 Mean: 0.34375
 Std Deviation: 0.4758892604748442
Distribution of 100000 Samples:
 False: 66.617%
 True: 33.383%


Shuffle Performance:

some_small_list = [i for i in range(10)]
some_med_list = [i for i in range(100)]
some_large_list = [i for i in range(1000)]

Base Case:
Random.shuffle()
Typical Timing: 7000 ± 94 ns
Typical Timing: 68125 ± 557 ns
Typical Timing: 687875 ± 5912 ns

Test Case 1:
Fortuna.fisher_yates()
Typical Timing: 875 ± 58 ns
Typical Timing: 6375 ± 58 ns
Typical Timing: 74375 ± 164 ns

Test Case 2:
Fortuna.knuth()
Typical Timing: 875 ± 1 ns
Typical Timing: 6250 ± 45 ns
Typical Timing: 74750 ± 124 ns

Test Case 3:
Fortuna.shuffle() knuth_b algorithm
Typical Timing: 250 ± 45 ns
Typical Timing: 3000 ± 58 ns
Typical Timing: 29500 ± 111 ns


-------------------------------------------------------------------------
Total Test Time: 3.784 seconds

```


## Legal Information
Fortuna © 2019 Broken aka Robert W Sharp, all rights reserved.

Fortuna is licensed under a Creative Commons Attribution-NonCommercial 3.0 Unported License.

See online version of this license here: <http://creativecommons.org/licenses/by-nc/3.0/>
