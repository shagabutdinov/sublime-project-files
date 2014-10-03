import sublime
import sublime_plugin

import re

try:
  from FolderFiles.folder_files import open_file_or_folder_by_panel
  from FileList.file_list import FileList
  from ProjectFiles.project_files import ProjectFiles
except ImportError as error:
  sublime.error_message("Dependency import failed; please read readme for " +
   "ProjectFiles plugin for installation instructions; to disable this " +
   "message remove this plugin; message: " + str(error))
  raise error

class PrintProjectFiles(sublime_plugin.TextCommand):
  def run(self, edit):
    view = sublime.active_window().new_file()
    files = []
    for file in ProjectFiles().get():
      files.append(file[0])

    view.insert(edit, 0, "\n".join(files))

class GotoProjectFile(sublime_plugin.TextCommand):
  def _show_files(self, display = 'name', folders = False, files = True):
    self.display = display
    self.folders = folders
    self.files = files

    FileList(self._get_files, open_file_or_folder_by_panel).show()

  def _get_files(self):
    files = ProjectFiles().get(self._check_file, self.folders, self.files)
    return self._convert_files(self.display, files)

  def _convert_files(self, display, files):
    if display == 'name':
      return files
    elif display == 'short':
      new_files = []
      for file in files:
        new_files.append([file[0], file[2]])
      return new_files
    else:
      raise Exception('Unknown display value "' + display + '"')


class GotoProjectFileByRegexp(GotoProjectFile):
  def run(self, edit, regexp, ignore = None, display = 'short', folders = False,
    files = True):
    self.regexp = re.compile(regexp)
    self.ignore = ignore and re.compile(ignore)

    self._show_files(display, folders, files)

  def _check_file(self, path, short_path, file_name):
    if self.ignore != None and re.search(self.ignore, short_path) != None:
      return False

    if re.search(self.regexp, short_path) != None:
      return True

    return False

class GotoProjectFileByRegexpReplace(GotoProjectFile):
  def run(self, edit, regexps, ignore = None, display = 'name', folders = False,
    files = True):
    self.ignore = ignore and re.compile(ignore)

    self.file_name = self.view.file_name()
    for folder in self.view.window().folders():
      if folder == self.file_name[0:len(folder)]:
        self.file_name = self.file_name[len(folder) + 1:]

    prepared_regexps = []
    for regexp in regexps:
      file_name_regexp = re.sub(regexp[0], regexp[1], self.file_name)
      prepared_regexps.append(file_name_regexp)

    self.regexp = re.compile('(' + '|'.join(prepared_regexps) + ')')

    self._show_files(display, folders, files)

  def _check_file(self, path, short_path, file_name):
    if short_path == self.file_name or path + '/' + file_name == self.file_name:
      return False

    if self.ignore != None and re.search(self.ignore, short_path) != None:
      return False

    if re.search(self.regexp, short_path) != None:
      return True

    return False

class GotoProjectFileByEval(GotoProjectFile):
  def run(self, edit, code, ignore = None, display = 'name', folders = False,
    files = True):

    self.ignore = ignore and re.compile(ignore)
    self.regexp = re.compile(eval(code, {'view': self.view}))
    self._show_files(display, folders, files)

  def _check_file(self, path, short_path, file_name):
    if self.ignore != None and re.search(self.ignore, short_path) != None:
      return False

    if re.search(self.regexp, short_path) != None:
      return True

    return False
