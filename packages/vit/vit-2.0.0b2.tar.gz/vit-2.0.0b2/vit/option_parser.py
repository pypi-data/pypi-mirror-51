import sys
import optparse

from vit import version

class OptionParser(optparse.OptionParser):
    def format_epilog(self, formatter):
        return self.epilog

parser = OptionParser(
  usage='%prog [options] [report] [filters]',
  version=version.VIT,
  epilog="""
VIT (Visual  Interactive Taskwarrior) is a lightweight, curses-based front end for
Taskwarrior that provides a convenient way to quickly navigate and process tasks.
VIT allows you to interact with tasks in a Vi-intuitive way.

A goal of VIT is to allow you to customize the way in which you use Taskwarrior's
core commands as well as to provide a framework for easily dispatching external
commands.

While VIT is running, type :help followed by enter to review basic command/navigation actions.

See https://github.com/scottkosty/vit for more information.

"""
)

parser.add_option('--list-actions',
  dest="list_actions",
  default=False,
  action="store_true",
  help="list all available actions",
)

def parse_options():
    options, filters = parser.parse_args()
    if options.list_actions:
        list_actions()
        sys.exit(0)
    return options, filters

def format_dictionary_list(item, description):
    print("%s:" % item)
    print("\t%s\n" % description)

def list_actions():
    from vit.registry import ActionRegistry
    from vit.actions import Actions
    action_registry = ActionRegistry()
    actions = Actions(action_registry)
    actions.register()
    any(format_dictionary_list(action, data['description']) for action, data in actions.get().items())
