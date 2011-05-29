from parse import parse_file
import sys

def generate_rst(task):
    print task.name
    print "="*len(task.name)
    if task.description != "":
        print task.description
    print ""
    for script in task.scripts:
        print script.name
        print "-"*len(script.name)
        print ""
        for action in script.actions:
            print "* **%s** %s"%(action.actor.name, action.description)
    print ""


