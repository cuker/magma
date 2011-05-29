import hashlib

from sys import stderr

roles = dict()
actors = dict()
tasks = dict()
scripts = dict()
actions = dict()

class LookupElement(object):
    lookup = None

    def __init__(self, name):
        self.name = name
        if self.lookup != None:
            if self.lookup.get(name) == None:
                self.lookup[name] = self
            else:
                stderr.write("Warning: Duplicate Key: %s\n"%name)
        else:   
            raise Exception("Improperly Configured.  Must have a lookup")

class Role (LookupElement):
    lookup = roles

    def __init__(self, name, description = None):
        super(Role, self).__init__(name)

class Actor (LookupElement):
    lookup = actors
    
    def __init__(self, name, role_set=None):
        self.roles = role_set
        super(Actor, self).__init__(name) 

    def has_role(self, role_name):
        return role_name in self.roles

    def get_roles(self):
        return self.roles

class Task (LookupElement):
    lookup = tasks

    def __init__(self, name, script_set):
        self.scripts = script_set
        self.requirements = list()
        self.description = ""
        self.roles = list()
        super(Task, self).__init__(name)
    
    def add_script(self, script_name):
        self.scripts.append(script_name)
        Script.lookup.get(script_name).set_task(self)
    
    def get_scripts(self):
        return self.scripts
    
class Script (LookupElement):
    lookup = scripts

    def __init__(self, name, action_set):
        self.task = None
        self.actions = action_set
        super(Script, self).__init__(name)
        
    def add_action(self, action):
        self.actions.append(action)
        Action.lookup.get(action.name).set_script(self)
    
    def set_task(self, task):
        self.task = task

class Action (LookupElement):
    lookup = actions

    def __init__(self, actor, description):
        m = hashlib.md5()
        self.description = description
        self.actor = actor
        m.update(actor.name)
        m.update(description)
        name = m.hexdigest()
        self.script = None
        super(Action, self).__init__(name)

    def set_script(self, script):
        self.script = script
    
    def __str__(self):
        return self.description
