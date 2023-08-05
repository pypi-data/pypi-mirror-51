"""
Contains class representation of task and helper functions.
"""
from prompt_toolkit import prompt
from senile import database as db
from senile import icons
from texttable import Texttable
import datetime
import json
import logging
import os
import time
import uuid

data_file = os.path.expanduser('~/.senile')
logger = logging.getLogger(__name__)

status_desc = {
    'hidden': -1,
    'done': 0,
    'todo': 1,
    'active': 2,
    }
status_icons = icons.get_theme(os.getenv('SENILE_ICON_THEME'))

def is_int(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

#def get_tasks_per_status(status):
#    tasks_query = """
#        SELECT uuid FROM tasks
#        WHERE tasks.status = ?;
#        """
#    res = db.execute(tasks_query, (status,))
#    tasks = [ Task.load(x[0]) for x in res ]
#    return tasks

def get_tags_count():
    tags_query = """
        SELECT COUNT(tag), tag
        FROM task_tags
        WHERE task_tags.task_id != task_tags.tag
        GROUP BY tag ;
        """
    res = db.execute(tags_query)
    return sorted(res, key=lambda x: x[0], reverse=True)

def normalize():
    "Delete orphaned tags and fix issues with tasks."
    tasks = [ Task.load(x[0]) for x in db.execute("SELECT uuid FROM tasks;") ]
    for task in tasks:
        if task.status == status_desc['hidden']: # pragma: no cover
            task.id = 0
        task.save()
    tags_query = """
        DELETE FROM task_tags
        WHERE task_id NOT IN
        (SELECT tasks.uuid FROM tasks)
        """
    db.execute(tags_query)

def task_table(tasks):
    "Return ascii table of tasks."
    table = Texttable()
    table.header(['id', 'uuid', 'tags', 'text', 'duration', 'p', 's'])
    table.set_cols_align(["r", "l", "l", "l", "l", "l", "l"])
    table.set_cols_dtype(['t', 't', 't', 't', 't', 't', "t"])
    table.set_header_align(["r", "l", "l", "l", "l", "l", "l"])
    table.set_deco(Texttable.HEADER + Texttable.VLINES)
    for task in tasks:
        table.add_row([
            task.id if task.id >= 0 else "-",
            task.uuid.split('-')[0],
            ' '.join(sorted(task.tags)),
            task.text,
            task.calc_duration(),
            task.priority,
            task.get_status_icon(),
            ])
    return table.draw()

class Task(object):
    "Task entry."
    
    def __init__(self):
        self.uuid = str(uuid.uuid1())
        self.id = 0
        self.text = ''
        self.priority = 0
        self.status = status_desc['todo']
        self.created_time = time.time()
        self.modified_time = self.created_time
        self.start_time = 0
        self.done_time = 0
        self.duration = 0
        self.notes = ""
        self.tags = set()

    def __eq__(self, other):
        return self.uuid == other.uuid

    def parse(data):
        parsed = {
                'include_tags': set(),
                'exclude_tags': set(),
                'words': [],
                'priority': 0,
                'status': [],
                }
        for item in data:
            if item[0] == '+':
                parsed['include_tags'].add(item[1:])
            elif item[0] == '-':
                parsed['exclude_tags'].add(item[1:])
            elif item[0] == '%' and is_int(item[1:]):
                parsed['priority'] = max(parsed['priority'], int(item[1:]))
            elif item[0] == '@' and item[1:] in status_desc.keys():
                parsed['status'].append(status_desc[item[1:]])
            else:
                parsed['words'].append(item)
        return parsed
 
    def find(data):
        tasks = None
        p = Task.parse(data)
        if not p: return None
        tasks_query = "SELECT uuid FROM tasks"
        if len(p['words']):
            tasks_query +=  """
                WHERE 0
                """
            for word in set(p['words']):
                tasks_query += """
                OR tasks.text LIKE '%{}%'
                OR tasks.notes LIKE '%{}%'
                """.format(word, word)
        tasks_query += """
            ORDER BY status ASC, priority ASC;
            """
        ids = [ x[0] for x in db.execute(tasks_query) ]
        tasks = [ Task.load(x) for x in ids ]
        tasks_with_tags = tasks[:]
        for tag in p['include_tags']:
            for task in tasks:
                if tag not in task.tags:
                    tasks_with_tags.remove(task)
        tasks_without_tags = tasks_with_tags[:]
        for tag in p['exclude_tags']:
            for task in tasks_with_tags:
                if tag in task.tags:
                    tasks_without_tags.remove(task)
        tasks_with_status = tasks_without_tags
        if len(p['status']):
            tasks_with_status = [ x for x in tasks_without_tags if x.status in p['status'] ]
        tasks = [ x for x in tasks_with_status if x.priority >= p['priority'] ]
        return tasks

    def modify(self, options):
        "Populates data in options."
        data = []
        for option in options:
            data.extend([ x for x in option.split(" ") if x])
        p = Task.parse(data)
        logger.info("Updating data in task: {}".format(self.uuid))
        self.tags = self.tags.difference(p['exclude_tags']).union(p['include_tags'].difference(p['exclude_tags']))
        self.text = p['words'] or self.text
        self.priority = p['priority'] or self.priority
        if len(p['status']):
            status = {v: k for k, v in status_desc.items()}[p['status'][-1]]
            if status == "active":
                self.start()
            elif status == "todo":
                self.todo()
            elif status == "done":
                self.done()
            elif status == "hidden":
                self.hide()
            else: # pragma: no cover
                raise("Unknown status: " + status)
        if len(p['words']):
            self.text = " ".join(p['words'])
        self.modified_time = time.time()

    def hide(self):
        if self.status == status_desc['hidden']:
            logger.warning("Task was already hidden: {}".format(self.uuid))
            return
        self.status = status_desc['hidden']
        self.id = 0

    def done(self):
        if self.status in (status_desc['done'], status_desc['hidden']):
            return
        self.done_time = time.time()
        if self.status == status_desc['active']:
            self.duration += self.done_time - self.start_time
        self.status = status_desc['done']

    def todo(self):
        if self.status == status_desc['todo']:
            logger.warning("Task was already todo: {}".format(self.uuid))
            return
        if self.status == status_desc['active']:
            self.duration += time.time() - self.start_time
        self.status = status_desc['todo']

    def start(self):
        if self.status == status_desc['active']:
            logger.warning("Task was already started: {}".format(self.uuid))
            return
        self.start_time = time.time()
        self.status = status_desc['active']
        self.done_time = 0

    def stop(self):
        if self.status != status_desc['active']:
            logger.warning("Task was not started: {}".format(self.uuid))
            return
        self.todo()

    def calc_duration(self):
        dur = 0
        if self.status == status_desc['active']:
            dur = self.duration + time.time() - self.start_time
        else:
            dur = self.duration
        return str(datetime.timedelta(seconds=int(dur)))
    
    def get_status_icon(self):
        return {v: k for k, v in status_icons.items()}[self.status]

    def get_status_text(self):
        return {v: k for k, v in status_desc.items()}[self.status]

    def __str__(self):
        return " | ".join([
            str(self.id),
            self.uuid.split("-")[0],
            self.text,
            str(self.priority),
            self.get_status_icon()
            ])
    
    def info(self):
        done_time = "N/A"
        if self.done_time > 0:
            if self.status in (status_desc['done'], status_desc['hidden']):
                done_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.done_time))
        table = Texttable()
        table.set_cols_align(["r", "l"])
        table.set_cols_dtype(['t', 't'])
        table.set_deco(Texttable.BORDER)
        table.add_rows([
            ('id:', self.id),
            ('uuid:', self.uuid),
            ('text:', self.text),
            ('priority:', self.priority),
            ('status:', self.get_status_text() + " " + self.get_status_icon()),
            ('created:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.created_time))),
            ('modified:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.modified_time))),
            ('done:', done_time),
            ('duration:', self.calc_duration()),
            ], header=False)
        output = table.draw()
        if self.notes:
            output += "\n\nNOTES:\n" + self.notes
        return output

    def take_note(self): # pragma: no cover
        self.notes = prompt("", default=self.notes, multiline=True)

    def load(ident):
        task_sql = None
        res = None
        if len(ident) >= 8 or '-' in ident:
            task_sql = """
                SELECT * FROM tasks
                WHERE tasks.uuid LIKE ?;
                """
            res = db.execute(task_sql, (ident+"%",))
        else:
            task_sql = """
                SELECT * FROM tasks
                WHERE tasks.id = ?
                AND tasks.status != ?;
                """
            res = db.execute(task_sql, (ident, status_desc['hidden']))
        if len(res) > 1: # pragma: no cover
            logger.warning("Found multiple tasks with id '{}'.".format(ident))
            return None
        if len(res) < 1:
            logger.warning("Task with id '{}' not found.".format(ident))
            return None
        task = Task()
        task.uuid           = res[0][0]
        task.id             = res[0][1]
        task.text           = res[0][2]
        task.priority       = res[0][3]
        task.status         = res[0][4]
        task.created_time   = res[0][5]
        task.modified_time  = res[0][6]
        task.start_time     = res[0][7]
        task.done_time      = res[0][8]
        task.duration       = res[0][9]
        task.notes          = res[0][10]
        tags_sql = """
            SELECT tag FROM task_tags
            WHERE task_id = ?;
        """
        res = db.execute(tags_sql, (task.uuid,))
        for r in res:
            task.tags.add(r[0])
        return task

    def save(self):
        if not self.text:
            logger.error("Can't add task with no description.")
            return
        if self.id < 1 and self.status != status_desc['hidden']:
            ids_query = """
                SELECT id from tasks;
                """
            ids = [ x[0] for x in db.execute(ids_query) ]
            x = 1
            while True:
                if x not in ids: break
                else: x+=1
            self.id = x
        if self.status == status_desc['hidden']:
            self.id = 0
        logger.info("Saving task: {}".format(self.uuid))
        task_sql = """
        INSERT OR REPLACE INTO tasks
        (uuid, id, text, priority, status, created_time, modified_time,
        start_time, done_time, duration, notes)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        logger.info("Saving task '{}'.".format(self.uuid))
        db.execute(task_sql, (
            self.uuid,
            self.id,
            self.text,
            self.priority,
            self.status,
            self.created_time,
            self.modified_time,
            self.start_time,
            self.done_time,
            self.duration,
            self.notes,
            ))
        remove_tags_sql = """
        DELETE FROM task_tags WHERE task_id = ?;
        """
        logger.info("Deleting all task tags for '{}'.".format(self.uuid))
        db.execute(remove_tags_sql, (self.uuid,))
        for tag in self.tags:
            tag_sql = """
            INSERT OR REPLACE INTO task_tags
            (task_id, tag) values (?, ?);
            """
            logger.info("Adding tags '{}' for '{}'.".format(tag, self.uuid))
            db.execute(tag_sql, (self.uuid, tag))
        return

    def remove(self):
        del_task_sql = """
        DELETE FROM tasks WHERE uuid = ?;
        """
        logger.info("Deleting task: {}".format(self.uuid))
        db.execute(del_task_sql, (self.uuid,))
        del_tags_sql = """
        DELETE FROM task_tags WHERE task_id = ?;
        """
        logger.info("Deleting tags asociated with task: {}".format(self.uuid))
        db.execute(del_tags_sql, (self.uuid,))
        return "DELETED - text: {} | tags: {} | notes: {}".format(
                self.text,
                " ".join(self.tags),
                self.notes,
                )

