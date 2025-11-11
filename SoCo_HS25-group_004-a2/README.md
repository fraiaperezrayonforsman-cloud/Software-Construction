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
We add several functions to include arrays and sets in to the environment. 
Besides the common assertion to check the expected number of arguments the functions have the following functionalities: 
- do_array: creates a new array of length defined by argument in position 0. It asserts that the argument in postion 0 is of type integer and that it is equal or larger than 0. It returns an array with the defined size.
- do_value_at: it retrieves the desired array from the environment. It checks whether it is indeed an array and if its length is longer than 0. Moreover, it retrieves a desired index and checks whether the index is within the length of the array. If it is it returns the value at the defined index.
- do_set_value: it retrieves the desired array from the environment. It checks whether it is indeed an array and if its length. If the length is 0 it checks that the index defined at position 1, is also equal to 0. Otherwise it returns an assertion error since the index does not exist in the array. There are two cases when the value, defined at position 1, is simply appended to the array; when the array is of length 0
or when the index equals the length of the array. If the index is within the length of the array, then the value is set at the respective index. Lastly, the array is updated in the environment with the env_set function.
- do_array_size: retrieves the desired array, checks that it is indeed an array and returns the length of the array.
- do_array_concat: retrieves two desired arrays from the environment, checks that both are indeed arrays and returns array_2 concatenated to array_1.
- do_new_set: returns an empty set. 
- do_insert_set: retrieves the desired set defined at position 0 from the environment and asserts that it is indeed a set. It asserts that the defined value at position 1 is not yet present in the set. If it is not yet present, it adds the value. Lastly it updates the set in the environment.
- do_exist: retrives the desired set defined at position 0 from the environment. It checks whether the value defined at position 1 exists in the set. It returns a boolean answering this question.
- do_merge_set: retrieves the two desired sets defined at positions 1 and 2 from the environment. Asserts that they are both of type set and unites them. Lastly it adds this new set to the environment. 
- do_string (additional): helper function to print the name the name of the variable in use.

## Step 03 
do_map:
The first lines check if the arguments are valid. The current environment is retrieved and the assertions make sure that the first argument is really an array and the second is a function. The function is separated into params and body. In the loop an environment stack is used, so that each element runs in a local context to avoid conflicts. The result is appended to a separate list so the original array is not modified. 

do_reduce:
The same method is used here with using local environments and using pop for each reduction step. The code checks at the beginning if the call is handled as an already built-in function or a user-defined one. 

do_filter:
The assert makes sure that the second argument is a function for filter to work. The method here is similar to do_map and do_reduce with a True check to add the filtered elements to a result list. 

## Step 04 
main():
In the first step there is a check if the program is started with --trace. After that, we got

TRACE: a list which stores each function call & the data 
DEPTH: current nesting level for indentation 
TRACING: boolean 

do_call() & do_print():
The time is measured with time.time(). Each function call appends an entry to TRACE that stores the name, depth and duration. There is a variable index to update the right entry after nested calls. DEPTH is increased before the body to resemble the new nesting level. It is decremented after the function finishes to restore the previous indentation level. 

print_trace():
This function is to format the output as a tree. 

## ChatGPT Prompts
"Troubleshooting built-in calls not working in do_reduce"
"Give me tips/a guide on how to approach Step 04"

## Authors 
Julie Truc Dao

Fraia Pérez-Rayón

Natalia Piegat (missbo-cyber is my github account I connected with gitlab, when I do "git-push" from Visual Studio Code this nickname appears)