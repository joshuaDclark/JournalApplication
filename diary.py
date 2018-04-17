#!/usr/bin/env python3
from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('diary.db')


class Entry(Model):
    # content
    content = TextField()
    # timestamp
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """Create the database and the table if the don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """Show the menu"""
    choice = None
    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('%s) %s' % (key, value.__doc__))
            choice = input('Action: ').lower().strip()
        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    """Add an entry"""
    print("Enter your entry. Press Crtl+D when finished.")
    clear()
    data = sys.stdin.read().strip()
    if data and input('Save entry? [Y/N] ').lower() != 'n':
                Entry.create(content=data)
                print("Saved successfully!")


def view_entries(search_query=None):
    """View previous entries."""
    query = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        query = query.where(Entry.content.contains(search_query))

    for entry in query:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print('=' * len(timestamp))
        print(entry.content)
        print('\n\n' + '=' * len(timestamp))
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')
        action = input('Choice? (Ndq ').lower().strip()
        if action == 'q':
            break
        elif action == 'd':
            entry.delete_instance()
            break


def delete_entry(entry):
    """Delete an entry."""
    if input("Are you sure? [yN] ").lower() == 'y':
        entry.delete_instance()
        print("Entry deleted")


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
])

if __name__ == '__main__':
    initialize()
    menu_loop()
