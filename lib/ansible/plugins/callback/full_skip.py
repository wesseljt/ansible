# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

'''
DOCUMENTATION:
    callback: full_skip
    type: stdout
    short_description: suppreses tasks if all hosts skipped
    description:
      - Use this plugin when you dont care about any output for tasks that were completly skipped
    version_added: "2.4"
    requirements:
      - set as stdout in configuation
'''
# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback.default import CallbackModule as CallbackModule_default


class CallbackModule(CallbackModule_default):

    '''
    This is the default callback interface, which simply prints messages
    to stdout when new callback events are received.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'full_skip'

    def v2_runner_on_skipped(self, result):
        self.outlines = []

    def v2_playbook_item_on_skipped(self, result):
        self.outlines = []

    def v2_runner_item_on_skipped(self, result):
        self.outlines = []

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.display()
        super(CallbackModule, self).v2_runner_on_failed(result, ignore_errors)

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.outlines = []
        self.outlines.append("TASK [%s]" % task.get_name().strip())
        if self._display.verbosity >= 2:
            path = task.get_path()
            if path:
                self.outlines.append("task path: %s" % path)

    def v2_playbook_item_on_ok(self, result):
        self.display()
        super(CallbackModule, self).v2_playbook_item_on_ok(result)

    def v2_runner_on_ok(self, result):
        self.display()
        super(CallbackModule, self).v2_runner_on_ok(result)

    def display(self):
        if len(self.outlines) == 0:
            return
        (first, rest) = self.outlines[0], self.outlines[1:]
        self._display.banner(first)
        for line in rest:
            self._display.display(line)
        self.outlines = []
