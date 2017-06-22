Gtk openstack review
====================

This is a work in progress tool to help developers in their review process in
openstack projects.

Right now it uses openstack firehose queue, subscribing to projects, and as the
new reviews arrives, it checks if jenkins gave the verified status and then the
developer can go and review the code. Once the developer reviews the code, the
review is automatically removed from the queue.

Requirements
============

It requires to have gobject introspection package installed

Usage
=====

Right now the tool only shows the changes, and to use you just need to run:

     python opennstack_review/application.py

Ideas for the future
====================

- Add a new window to list openstack projects and subscribe to it
- Add a settings window where you can set your gerrit username
- Shows notification in gnome-shell
- Search
- Split the list per project
- Notification settings

