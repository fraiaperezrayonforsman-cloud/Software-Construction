Step 3 

do_map:
The first lines check if the arguments are valid. The current environment is retrieved and the assertions make sure that the first argument is really an array and the second is a function. The function is separated into params and body. In the loop an environment stack is used, so that each element runs in a local context to avoid conflicts. The result is appended to a separate list so the original array is not modified. 

do_reduce:
The same method is used here with using local environments and using pop for each reduction step. The code checks at the beginning if the call is handled as an already built-in function or a user-defined one. 

do_filter:
The assert makes sure that the second argument is a function for filter to work. The method here is similar to do_map and do_reduce with a True check to add the filtered elements to a result list. 