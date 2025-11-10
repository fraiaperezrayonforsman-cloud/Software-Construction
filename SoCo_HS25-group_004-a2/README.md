# Interpreter 

**HS25  SoCo-group  004**

## Project Introduction 
The goal of our project was to extend LGL (Little German Language) Interpreter built during lectures by adding more functions and visual tracing functionality. 

## Step 01
In the first step we implemented arithmetic, comparison and boolean operaions. In each function, we included the assert to ensure that the number of arguments is sufficient for the function to operate correctly. 
Additionally, since our boolean functions operate on values from the set {0, 1}, we included another assert to ensure that only these values are passed as input.
Our do..until function behaves similarly to the well-known do..while loop — it executes the body of the function first and then evaluates the condition.

In the extensions.lgl file we implemented three algorithms: 
- Even or odd - subtracts 2 from a given natural number _n_ until we get number that is less than 2. When the number is even the output is 0, when it is odd the output is 1.
- Sum up to - given a natural number _n_, computes the sum of the natural numbers up to _n_. Variable _s_ in the algorithm represents the sum and _i_ is incremented in each iteration. The output is _s_.
- Factorial - given a non-negative integer _n_, computes the product of all positive integers less than or equal to _n_. 

Each algorithm is called using do_call function. 

## Step 02

## Step 03 

do_map:
The first lines check if the arguments are valid. The current environment is retrieved and the assertions make sure that the first argument is really an array and the second is a function. The function is separated into params and body. In the loop an environment stack is used, so that each element runs in a local context to avoid conflicts. The result is appended to a separate list so the original array is not modified. 

do_reduce:
The same method is used here with using local environments and using pop for each reduction step. The code checks at the beginning if the call is handled as an already built-in function or a user-defined one. 

do_filter:
The assert makes sure that the second argument is a function for filter to work. The method here is similar to do_map and do_reduce with a True check to add the filtered elements to a result list. 

## Step 04 

## Authors 
Julie Truc Dao

Fraia Pérez-Rayón

Natalia Piegat (missbo-cyber is my github account I connected with gitlab, when I do "git-push" from Visual Studio Code this nickname appears)