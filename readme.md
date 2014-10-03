# Sublime ProjectFiles plugin

Glorious plugin that allows you to prefilter your files and navigate through it
by regexp. Especially good when used with mvc-frameworks to quickly open
controller, model, view or config files. Also provides ability to replace file
name with regexp and search project files for this file name - this is good
when opening test file for file or file for test file.


### Demo

![Demo](https://github.com/shagabutdinov/sublime-enhanced-demos/raw/master/project_files.gif "Demo")

### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.


### Features

By default have keybindings to access controllers, views, configs, routes, tests
and html, css, js and coffee files.


### Usage

Hit keyboard shortcut to display desired file list; than type use fuzzy search
to select desired file and open it. Plugin works on top of [sublime-file-list](http://github.com/shagabutdinov/sublime-file-list)
so file-list keyboard bindings will works there.


### Commands

| Description         | Keyboard Shortcut | Command palette                   |
|---------------------|-------------------|-----------------------------------|
| Show all files      | ctrl+n, n         | ProjectFiles: Show all            |
| Show all folders    | ctrl+n, ctrl+u    | ProjectFiles: Show all folders    |
| Show configs        | ctrl+n, ctrl+f    | ProjectFiles: Show configs        |
| Show routes         | ctrl+n, ctrl+r    | ProjectFiles: Show routes         |
| Show models         | ctrl+n, ctrl+m    | ProjectFiles: Show models         |
| Show migrations     | ctrl+n, ctrl+i    | ProjectFiles: Show migrations     |
| Show controllers    | ctrl+n, ctrl+c    | ProjectFiles: Show controllers    |
| Show views          | ctrl+n, ctrl+v    | ProjectFiles: Show views          |
| Show tests          | ctrl+n, ctrl+t    | ProjectFiles: Show tests          |
| Toggle test file    | ctrl+n, t         | ProjectFiles: Toggle test         |
| Show yaml           | ctrl+n, y         | ProjectFiles: Show yaml           |
| Show haml           | ctrl+n, a         | ProjectFiles: Show haml           |
| Show html           | ctrl+n, h         | ProjectFiles: Show html           |
| Show css            | ctrl+n, c         | ProjectFiles: Show css            |
| Show erb            | ctrl+n, e         | ProjectFiles: Show erb            |
| Show js             | ctrl+n, j         | ProjectFiles: Show js             |
| Show coffee         | ctrl+n, f         | ProjectFiles: Show coffee         |
| Print project files | ctrl+u, ctrl+p    | ProjectFiles: Print project files |


### Dependencies

* [FileList](https://github.com/shagabutdinov/sublime-file-list)