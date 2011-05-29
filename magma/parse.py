from tokenize import tokens # this is unused, but needed by PLY to build the parser
from models import Actor, Role, Task, Script, Action
from sys import stderr

names = {}
start = 'document'

action_accumulator = list()    
script_accumulator = list()    
role_accumulator = list()    
requirement_accumulator = list()    
description_accumulator = list()

def p_document(p):
    'document : statement_list'

def p_statements(p):
    '''statement_list : role_def statement_list
                      | actor_def statement_list
                      | task_def statement_list
                      | namespace_def statement_list
                      | empty'''

def p_namespace_def(p):
    '''namespace_def : NAMESPACE id'''

def p_identifier(p):
    '''id : ID
          | STRING'''
    p[0] = p[1].strip('"')

def p_role_def(p):
    'role_def : ROLE id'
    Role(p[2])

def p_actor_def(p):
    '''actor_def : ACTOR id
                 | ACTOR id LPAREN id RPAREN
    '''
    if len(p) > 3:
        if Role.lookup.get(p[4]) != None:
            Actor(p[2], p[4])
        else: 
            stderr.write("Error: Role %s not defined."%p[4])
    else:
        Actor(p[2])

def p_task_def(p):
    '''task_def : TASK id task_contents'''
    task = Task(p[2], script_accumulator[:])
    task.requirements = requirement_accumulator[:]
    task.roles = role_accumulator[:]
    if len(description_accumulator) == 1:
        task.description = description_accumulator[0]
    del(description_accumulator[:])
    del(script_accumulator[:])
    del(role_accumulator[:])
    del(requirement_accumulator[:])

def p_task_contents(p):
    '''task_contents : task_descriptions task_roles task_requirements task_scripts
                     | task_roles task_requirements task_scripts'''
    

def p_task_roles(p):
    '''task_roles : ROLE id 
                  | ROLE id task_roles
    '''
    role = Role.lookup.get(p[2])
    if role == None:
        stderr.write( "Warning: Role not found: %s\n"%p[2])
    else: 
        role_accumulator.append(role)

def p_namespace_path(p):
    '''path : id
            | id RIGHTBRACKET path 
    '''
    print "Path is: %s"%p[1]

def p_task_requirements(p):
    '''task_requirements : REQUIRES path
                         | REQUIRES path task_requirements 
    '''
    task = Task.lookup.get(p[2])
    if task == None:
        stderr.write("Warning: Task not found: %s\n"%p[2])
    else: 
        requirement_accumulator.append(task)

def p_task_descriptions(p):
    '''task_descriptions : DESCRIPTION id
                         | DESCRIPTION id task_descriptions
    '''
    p[0] = p[2]
    description_accumulator.append(p[2])

def p_task_scripts(p):
    '''task_scripts : SCRIPT id BLOCKSTART script_actions BLOCKEND
                    | SCRIPT id BLOCKSTART script_actions BLOCKEND task_scripts
    '''
    
    action_accumulator.reverse()
    s = Script(p[2], action_accumulator[:])
    del(action_accumulator[:])
    script_accumulator.append(s)
    

def p_script_actions(p):
    '''script_actions : ACTION id DESCRIPTION
                      | ACTION id DESCRIPTION script_actions
    '''
    # check Actor
    actor = Actor.lookup.get(p[2])
    if actor == None:
        stderr.write("Warning: Actor not found: %s\n"%p[2])
        p[0] = None
    else:
        action = Action(actor, p[3].strip(":").strip(" "))
        p[0] = action
        action_accumulator.append(action)
    

def p_empty(p):
    'empty :'
    pass


import ply.yacc as yacc
yacc.yacc()

if __name__ == '__main__':
    f = open ("blog.magma")
    contents = f.read()
    yacc.parse(contents)

def parse_file(filename):
    f = open (filename)
    contents = f.read()
    yacc.parse(contents)
    return Task.lookup
    
