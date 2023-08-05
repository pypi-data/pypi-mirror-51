import os
import tasklib
from tasklib.task import Task

from vit import util

class TaskListModel(object):
    def __init__(self, task_config, reports, report=None, data_location=None):

        if not data_location:
            data_location = task_config.subtree('data.location')
        self.data_location = os.path.expanduser(data_location)
        self.tw = tasklib.TaskWarrior(self.data_location)
        self.reports = reports
        self.report = report
        self.tasks = []
        if report:
            self.update_report(report)

    def add(self, contact):
        pass

    def active_report(self):
        return self.reports[self.report]

    def update_report(self, report, extra_filters=[]):
        self.report = report
        active_report = self.active_report()
        filters = active_report['filter'] if 'filter' in active_report else []
        all_filters = filters + extra_filters
        self.tasks = self.tw.tasks.filter(*all_filters) if len(all_filters) > 0 else self.tw.tasks.all()

    def get_task(self, uuid):
        try:
            return self.tw.tasks.get(uuid=uuid)
        except Task.DoesNotExist:
            return False

    def task_id(self, uuid):
        try:
            task = self.tw.tasks.get(uuid=uuid)
            return util.task_id_or_uuid_short(task)
        except Task.DoesNotExist:
            return False

    def task_description(self, uuid, description):
        task = self.get_task(uuid)
        if task:
            task['description'] = description
            task.save()
            return task
        return False

    def task_annotate(self, uuid, description):
        task = self.get_task(uuid)
        if task:
            task.add_annotation(description)
            return task
        return False

    def task_denotate(self, uuid, annotation):
        task = self.get_task(uuid)
        if task:
            task.remove_annotation(annotation)
            return task
        return False

    def task_priority(self, uuid, priority):
        task = self.get_task(uuid)
        if task:
            task['priority'] = priority
            task.save()
            return task
        return False

    def task_project(self, uuid, project):
        task = self.get_task(uuid)
        if task:
            task['project'] = project
            task.save()
            return task
        return False

    def task_done(self, uuid):
        task = self.get_task(uuid)
        if task:
            try:
                task.done()
                return True, task
            except (Task.CompletedTask, Task.DeletedTask) as e:
                return False, e
        return False, None

    def task_delete(self, uuid):
        task = self.get_task(uuid)
        if task:
            try:
                task.delete()
                return True, task
            except Task.DeletedTask as e:
                return False, e
        return False, None

    def task_start_stop(self, uuid):
        task = self.get_task(uuid)
        if task:
            try:
                task.stop() if task.active else task.start()
                return True, task
            except (Task.CompletedTask, Task.DeletedTask, Task.ActiveTask, Task.InactiveTask) as e:
                return False, e
        return False, None

    def task_tags(self, uuid, tags):
        task = self.get_task(uuid)
        if task:
            for tag in tags:
                marker = tag[0]
                if marker in ('+', '-'):
                    tag = tag[1:]
                    if marker == '+':
                        task['tags'].add(tag)
                    elif tag in task['tags']:
                        task['tags'].remove(tag)
                else:
                    task['tags'].add(tag)
            task.save()
            return task
        return False

#    def get_summary(self, report=None):
#        report = report or self.report
#        self.update_report(report)
#        summary = []
#        for task in self.tasks:
#            summary.append(self.build_task_row(task))
#        return summary
#
#    def _reload_list(self, new_value=None):
#        self._list_view.options = self._model.get_summary()
#        self._list_view.value = new_value
