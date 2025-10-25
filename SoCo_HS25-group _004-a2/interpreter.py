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

def do_seq(args,env):
    for each_ops in args:
        res = do(each_ops,env)
    return res

def do_addieren(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left + right

def do_absolutewert(args,env):
    assert len(args) == 1
    value = do(args[0],env)
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
    
def do_multiplizieren(args,env):
    left = do(args[0],env)
    right = do(args[1],env)
    return left * right 

def do_dividieren(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left/right

def do_potenzieren(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left ** right

def do_modulo(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left%right

def do_less_than(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left < right

def do_greater_than(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left > right

def do_less_than_or_equal(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left <= right

def do_greater_than_or_equal(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left >= right

def do_equal(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left == right

def do_not_equal(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left != right

def do_and(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    assert (left == 1 or left == 0) and (right == 1 or right == 0)
    if left == 1 and right == 1:
        return 1
    else:
        return 0
    
def do_or(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    assert (left == 1 or left == 0) and (right == 1 or right == 0)
    if left == 1 or right == 1:
        return 1
    else:
        return 0

def do_not(args,env):
    assert len(args) == 1
    left = do(args[0],env)
    assert (left == 1 or left == 0)
    if left == 1:
        return 0
    else:
        return 1
    
def do_print(args, env):
    args = [do(env, a) for a in args]
    print(*args)
    return None

def do_func(args, env):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["func",params,body]

def do_until(args,env):
    assert len(args) == 2
    cond = args[1]
    body = args[0]
    result = None
    while(do(cond,env)):
        print(env) #for checking if it works 
        result = do(body,env)
    print("The end of the loop")
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