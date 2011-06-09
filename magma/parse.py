from tokenize import tokens # this is unused, but needed by PLY to build the parser
from models import Actor, Role, Task, Script, Action, TaskTemplate
from sys import stderr
tokens=tokens


names = {}
start = 'document'

action_accumulator = list()    
script_accumulator = list()    
role_accumulator = list()    
requirement_accumulator = list()    
description_accumulator = list()
template_var_accumulator = list()
implementation_params_accumulator = list()

building_task = False

def p_document(p):
    'document : statement_list'

def p_statements(p):
    '''statement_list : role_def statement_list
                      | actor_def statement_list
                      | task_def statement_list
                      | namespace_def statement_list
                      | task_template_def statement_list
                      | empty'''


def p_task_template(p):
    '''task_template_def : TASK_TEMPLATE id LPAREN template_vars RPAREN task_contents
    '''
    template_var_accumulator.reverse()
    task_template = TaskTemplate(p[2], template_var_accumulator, script_accumulator)
    task_template.requirements = requirement_accumulator[:]
    task_template.roles = role_accumulator[:]
    if len(description_accumulator) == 1:
        task_template.description = description_accumulator[0]

    del(template_var_accumulator[:])
    del(description_accumulator[:])
    del(script_accumulator[:])
    del(role_accumulator[:])
    del(requirement_accumulator[:])


def p_template_vars(p):
    '''template_vars : id COMMA template_vars
                     | id
    ''' 
    template_var_accumulator.append(p[1])
    
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
    '''task_def : TASK id IMPLEMENTS id LPAREN impl_params RPAREN
                | TASK id task_contents
    '''
    if p[3] != 'implements':
        task = Task(p[2], script_accumulator[:])
        task.requirements = requirement_accumulator[:]
        task.roles = role_accumulator[:]
        if len(description_accumulator) == 1:
            task.description = description_accumulator[0]
        del(description_accumulator[:])
        del(script_accumulator[:])
        del(role_accumulator[:])
        del(requirement_accumulator[:])
    else: 
        # get the task template from p[4]
        template = TaskTemplate.lookup.get(p[4])
        param_names = template.template_parameters
        implementation_params_accumulator.reverse()
        key = 0
        for param in param_names:
            template.set_parameter(param, implementation_params_accumulator[key])
            key += 1
        template.render_task(p[2])
        del(implementation_params_accumulator[:])
         
def p_impl_params(p):
    '''impl_params : id COMMA impl_params
                   | id 
    '''
    implementation_params_accumulator.append(p[1])
        

def p_task_contents(p):
    '''task_contents : task_descriptions task_roles task_requirements task_scripts
                     | task_roles task_requirements task_scripts
                     | task_roles task_scripts'''
    

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
    
    s = Script(p[2], p[4][:])
    script_accumulator.append(s)

def p_script_actions(p):
    '''script_actions : ACTION id DESCRIPTION
                      | ACTION id DESCRIPTION script_actions
    '''
    # check Actor
    actor = Actor.lookup.get(p[2])
    p[0] = []
    if actor == None:
        stderr.write("Warning: Actor not found: %s\n"%p[2])
        p[0] = []
    else:
        action = Action(actor, p[3].strip(":").strip(" "))
        if len(p) > 4:
            p[0] += [action] + p[4]
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
    
