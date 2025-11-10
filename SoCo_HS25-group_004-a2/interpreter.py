import sys
import json
import pprint

env = dict()

def do_set(args,envs):
    assert len(args) == 2
    assert isinstance(args[0],str)
    var_name = args[0]
    var_value = do(args[1],envs)
    env_set(var_name,var_value,envs)
    return var_value

def env_set(name,value,envs):
    assert isinstance(name,str)
    envs[-1][name] = value
    
def do_get(args,envs):
    assert len(args) == 1
    assert isinstance(args[0],str)
    var_name = args[0]
    return env_get(var_name,envs)
 
def env_get(name,envs):
    assert isinstance(name,str)
    for env in reversed(envs):
        if name in env:
            return env[name]
    assert False, f"Unknown variable {name}"

def do_seq(args,envs):
    for each_ops in args:
        res = do(each_ops,envs)
    return res

def do_addieren(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left + right

def do_absolutewert(args,envs):
    assert len(args) == 1
    value = do(args[0],envs)
    if value >= 0:
        return value
    return -value

def do_subtrahieren(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left - right

def do_absolutewert(args,env):
    assert len(args) == 1
    value = do(args[0],env)
    if value >= 0:
        return value 
    return -value
    
def do_multiplizieren(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left * right 

def do_dividieren(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left/right

def do_potenzieren(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left ** right

def do_modulo(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left%right

def do_less_than(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left < right

def do_greater_than(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left > right

def do_less_than_or_equal(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left <= right

def do_greater_than_or_equal(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left >= right

def do_equal(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left == right

def do_not_equal(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left != right

def do_and(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    assert (left == 1 or left == 0) and (right == 1 or right == 0)
    if left == 1 and right == 1:
        return 1
    else:
        return 0
    
def do_or(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    assert (left == 1 or left == 0) and (right == 1 or right == 0)
    if left == 1 or right == 1:
        return 1
    else:
        return 0

def do_not(args,envs):
    assert len(args) == 1
    left = do(args[0],envs)
    assert (left == 1 or left == 0)
    if left == 1:
        return 0
    else:
        return 1
    
def do_print(args, envs):
    args = [do(a, envs) for a in args] #swapped a and env args of the do func
    print(*args)
    return None

def do_func(args, envs):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["func",params,body]

def do_until(args,envs):
    assert len(args) == 2
    cond = args[1]
    body = args[0]
    result = None
    while True:                 #do...until should execute code until condition is True 
        result = do(body,envs)
        if do(cond, envs):       #Check now if condition is True
            break               #end loop
    return result 

def do_call(args,envs):
    assert len(args) >= 1
    assert isinstance(args[0],str)
    name_func = args[0] 
    values = [do(a,envs) for a in args[1:]] #[3]

    func = env_get(name_func,envs) 
    assert isinstance(func,list) and (func[0] == "func")
    params = func[1]
    body = func[2]
    assert len(values) == len(params), f"You passed {len(values)} parameters instead of {len(params)}"

    local_env = dict() 

    for index,param_name in enumerate(params):
        local_env[param_name] = values[index]
    envs.append(local_env)
    result = do(body,envs) 
    envs.pop()

    return result

#Part 2------------------------------------------------------------
def do_array(args, envs):
    assert len(args) == 1
    size = do(args[0], envs)
    assert isinstance(size, int) and size >= 0
    return[0] * size

def do_value_at(args, envs):
    assert len(args) == 2
    array = env_get(args[0], envs)
    i = do(args[1], envs)
    assert isinstance(array, list), "variable is not an array"
    assert len(array) > 0, f"array empty"
    assert 0<= i < len(array), f"i is out of bounds" 
    return array[i]

def do_set_value(args, envs):
    assert len(args) == 3
    array = env_get(args[0], envs)
    i = do(args[1], envs)
    value = do(args[2], envs)
    assert isinstance(array, list), f"variable is not an array"
    if len(array) == 0:
        assert i == 0, f"cannot set value in index {i}, since array is empty"
        array.append(value)
    elif i == len(array):
        array.append(value)
    assert 0 <= i < len(array), f"index out of bounds"
    array[i] = value
    env_set(args[0], array, envs)
    return value

def do_array_size(args, envs):
    array = env_get(args[0], envs)
    assert isinstance(array, list), f"variable is not an array"
    return len(array)

def do_array_concat(args, envs):
    assert len(args)==2
    array_1 = env_get(args[0], envs)
    array_2 = env_get(args[1], envs)
    assert isinstance(array_1, list) and isinstance(array_2, list), f"both or one of the variables are not arrays"
    array_comb = array_1 + array_2
    return array_comb

def do_new_set(args, envs):
    return set()

def do_insert_set(args, envs):
    assert len(args) == 2
    s = env_get(args[0], envs)
    value = do(args[1], envs)
    assert isinstance(s, set), f"not a set"
    assert value not in s, f"value already in set, thus it cannot be inserted"
    s.add(value)
    env_set(args[0], s, envs)
    return value

def do_exist(args, envs):
    assert len(args) == 2
    s = env_get(args[0], envs)
    value = do(args[1], envs)
    exists = value in s
    return exists

def do_merge_set(args, envs):
    assert len(args) == 2
    s1 = env_get(args[0], envs)
    s2 = env_get(args[1], envs)
    assert isinstance(s1, set) and isinstance(s2, set), f"both or one of the variables is not a set"
    union = s1.union(s2)
    env_set(args[0], union, envs)
    return union

def do_string(args, envs):
    assert len(args)==1
    return args[0]

#Part 3------------------------------------------------------------
def do_map(args, envs):
    assert len(args) == 2
    array_name = args[0]        #"A"
    func_name = args[1]         #"sq_func"
    
    array = env_get(array_name, envs)   #[1,2,3,4]
    func = env_get(func_name, envs)     #["func", ["n"], ["mult", "n", "n"]]  
    
    assert isinstance(array, list), "first argument must be an array"
    assert isinstance(func, list) and func[0] == "func", "second argument must be a function"
    
    params = func[1]        #["n"]
    body = func[2]          #["mult", "n", "n"]
    
    res = []
    
    for element in array:
        local_env = {params[0]: element}    #{"n": 2}
        envs.append(local_env)              #[..., {"n": 2}]
        result = do(body, envs)             #4
        envs.pop()                          #[...]
        res.append(result)                  #[1,4]
    
    return res

def do_reduce(args, envs):
    assert len(args) == 2
    array_name = args[0]
    func_name = args[1]
    array = env_get(array_name, envs)
    assert isinstance(array, list), "first argument must be array"

    func = None
    if isinstance(func_name, str):
        try:
            func = env_get(func_name, envs)  
        except AssertionError:
            func = None

    if isinstance(func, list) and func != None and func[0] == "func":
        params = func[1]        
        body = func[2]          
        
        result = array[0] 

        for element in array[1:]:
            local_env = {params[0]: result, params[1]: element} 
            envs.append(local_env)
            result = do(body, envs)
            envs.pop()

        return result
    
    if func_name in OPS:
        result = array[0]
        for element in array[1:]:
            result = do([func_name, result, element], envs)
        return result
    
    raise AssertionError("second argument must be a defined function or a built-in operation")

def do_filter(args, envs):
    assert len(args) == 2
    array = env_get(args[0], envs)    #[1,2,3,4,15,22,34]
    func = env_get(args[1], envs)     #["func", ["n"], ["greater_than", "n", 10]]  
    
    assert isinstance(array, list), "first argument must be an array"
    assert isinstance(func, list) and func[0] == "func", "second argument must be a function"
    
    params = func[1]        #["n"]       
    body = func[2]          #["greater_than", "n", 10]
    
    res = []
    
    for element in array:
        local_env = {params[0]: element}    #{n: 1}
        envs.append(local_env)              #[...,{n: 1}]
        result = do(body,envs)              #False
        envs.pop()                          #[...]
        if result == True:      
            res.append(element)
    
    return res                              #[15,22,34]
#------------------------------------------------------------------

# {"addieren":do_addieren,
#  "absolutewert":do_absolutewert, 
#  "set":do_set,
#  ...}
OPS = {
    name.replace("do_",""): func
    for (name,func) in globals().items()
    if name.startswith("do_")
}


def do(program,envs):  
    if isinstance(program,int):
        return program
    assert program[0] in OPS, f"Unkown operation {program[0]}"
    func = OPS[program[0]]
    return func(program[1:],envs)


def main():
    filename = sys.argv[1]
    with open(filename,'r') as f:
        program = json.load(f)
        envs = [dict()] 
        result = do(program,envs)
    print(">>>" , result)
    pprint.pprint(envs)

if __name__ == '__main__':
    main()