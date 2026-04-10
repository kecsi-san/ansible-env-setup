# (C) 2016, Joel, https://github.com/jjshoe
# (C) 2015, Tom Paine, <github@aioue.net>
# (C) 2014, Jharrod LaFon, @JharrodLaFon
# (C) 2012-2013, Michael DeHaan, <michael.dehaan@gmail.com>
# (C) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Local override of ansible.posix.profile_tasks — customises timestamp format.
# Original: '%A %d %B %Y  %H:%M:%S %z'  →  e.g. "Friday 10 April 2026  21:45:27 +0200"
# Custom:   '%b %d %H:%M:%S'             →  e.g. "Apr 10 21:45:27"

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import collections
import time

from ansible.module_utils.six.moves import reduce
from ansible.plugins.callback import CallbackBase

# define start time
t0 = tn = time.time()


def secondsToStr(t):
    def rediv(ll, b):
        return list(divmod(ll[0], b)) + ll[1:]
    return "%d:%02d:%02d.%03d" % tuple(reduce(rediv, [[t * 1000, ], 1000, 60, 60]))


def filled(msg, fchar="*"):
    if len(msg) == 0:
        width = 79
    else:
        msg = "%s " % msg
        width = 79 - len(msg)
    if width < 3:
        width = 3
    filler = fchar * width
    return "%s%s " % (msg, filler)


def timestamp(self):
    if self.current is not None:
        elapsed = time.time() - self.stats[self.current]['started']
        self.stats[self.current]['elapsed'] += elapsed


def tasktime():
    global tn
    time_current = time.strftime('%b %d %H:%M:%S')
    time_elapsed = secondsToStr(time.time() - tn)
    time_total_elapsed = secondsToStr(time.time() - t0)
    tn = time.time()
    return filled('%s (%s)%s%s' % (time_current, time_elapsed, ' ' * 7, time_total_elapsed))


class CallbackModule(CallbackBase):
    """
    Per-task timing with compact timestamps.
    Local override of ansible.posix.profile_tasks.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'profile_tasks'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        self.stats = collections.OrderedDict()
        self.current = None
        self.sort_order = None
        self.summary_only = None
        self.task_output_limit = None
        super(CallbackModule, self).__init__()

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)

        self.sort_order = self.get_option('sort_order')
        if self.sort_order is not None:
            if self.sort_order == 'ascending':
                self.sort_order = False
            elif self.sort_order == 'descending':
                self.sort_order = True
            elif self.sort_order == 'none':
                self.sort_order = None

        self.summary_only = self.get_option('summary_only')

        self.task_output_limit = self.get_option('output_limit')
        if self.task_output_limit is not None:
            if self.task_output_limit == 'all':
                self.task_output_limit = None
            else:
                self.task_output_limit = int(self.task_output_limit)

    def _display_tasktime(self):
        if not self.summary_only:
            self._display.display(tasktime())

    def _record_task(self, task):
        self._display_tasktime()
        timestamp(self)
        self.current = task._uuid
        if self.current not in self.stats:
            self.stats[self.current] = {'started': time.time(), 'elapsed': 0.0, 'name': task.get_name()}
        else:
            self.stats[self.current]['started'] = time.time()
        if self._display.verbosity >= 2:
            self.stats[self.current]['path'] = task.get_path()

    def v2_playbook_on_task_start(self, task, is_conditional):
        self._record_task(task)

    def v2_playbook_on_handler_task_start(self, task):
        self._record_task(task)

    def playbook_on_setup(self):
        self._display_tasktime()

    def playbook_on_stats(self, stats):
        self._display_tasktime()
        self._display.display(filled("", fchar="="))

        timestamp(self)
        self.current = None

        results = list(self.stats.items())

        if self.sort_order is not None:
            results = sorted(
                self.stats.items(),
                key=lambda x: x[1]['elapsed'],
                reverse=self.sort_order,
            )

        results = list(results)[:self.task_output_limit]

        for uuid, result in results:
            msg = u"{0:-<{2}}{1:->9}".format(result['name'] + u' ', u' {0:.02f}s'.format(result['elapsed']), self._display.columns - 9)
            if 'path' in result:
                msg += u"\n{0:-<{1}}".format(result['path'] + u' ', self._display.columns)
            self._display.display(msg)
