import sublime
import sublime_plugin

import os
import re

try:
  from FileList.file_list import FileList
except ImportError as error:
  sublime.error_message("Dependency import failed; please read readme for " +
   "ProjectFiles plugin for installation instructions; to disable this " +
   "message remove this plugin; message: " + str(error))
  raise error

class ProjectFiles():

  def __init__(self):
    settings = sublime.load_settings('ProjectFiles.sublime-settings')
    self.ignored = settings.get('ignore') and re.compile(settings.get('ignore'))
    self.maximal_files_count = settings.get('maximal_files_count')

  def is_ignored(self, path, is_dir, info):
    is_ignored = False

    if is_dir:
      is_ignored = (is_ignored or (
        info['folder_exclude_regexp'] != None and
        re.search(info['folder_exclude_regexp'], path) != None
      ))
    else:
      is_ignored = (is_ignored or (
        info['file_exclude_regexp'] != None and
        re.search(info['file_exclude_regexp'], path) != None
      ))

    is_ignored = (is_ignored or (
      self.ignored != None and
      re.search(self.ignored, path) != None
    ))

    return is_ignored

  def get(self, callback = None, folders = False, files = True):
    result = []
    project_data = sublime.active_window().project_data()
    if project_data == None:
      return None

    for folder in project_data['folders']:
      folder = self._prepare_folder(folder)
      self._get(callback, folder, folder['path'], folders, files, result)

    return result

  def _prepare_folder(self, folder):
    folder = folder.copy()

    ignored_folders = folder.get('folder_exclude_patterns', None)
    ignored_folders_regexp = self._convert_patterns_to_regexp(ignored_folders)
    folder['folder_exclude_regexp'] = ignored_folders_regexp

    ignored_files = folder.get('file_exclude_patterns', None)
    ignored_files_regexp = self._convert_patterns_to_regexp(ignored_files)
    if ignored_files_regexp != None:
      ignored_files_regexp = re.compile(ignored_files_regexp)

    folder['file_exclude_regexp'] = ignored_files_regexp

    return folder

  def _convert_patterns_to_regexp(self, patterns):
    regexps = []
    if patterns == None or not isinstance(patterns, list) or len(patterns) == 0:
      return None

    for pattern in patterns:
      pattern += '/'
      pattern = pattern.replace('*', '__STAR__')
      pattern = pattern.replace('**', '__DOUBLE_STAR__')
      pattern = pattern.replace('?', '__QUESTION__')
      pattern = re.escape(pattern)
      pattern = pattern.replace('__STAR__', '[^/]*')
      pattern = pattern.replace('__DOUBLE_STAR__', '.*')
      pattern = pattern.replace('__QUESTION__', '.')
      pattern = '^' + pattern
      regexps.append(pattern)

    return '(' + '|'.join(regexps) + ')'

  def _get(self, callback, info, path, folders, files, result = []):
    try:
      for file_name in os.listdir(path):
        file_path = path + '/' + file_name
        short_path = file_path[len(info['path']) + 1:]

        is_dir = os.path.isdir(file_path)

        if self.is_ignored(short_path, is_dir, info):
          continue

        if is_dir:
          append = folders and (callback == None or callback(file_path,
            short_path, file_name))

          if append:
            result.append([file_path, file_name, short_path])

          self._get(callback, info, file_path, folders, files, result)
        else:
          append = files and (callback == None or callback(file_path, short_path,
            file_name))

          if append:
            result.append([file_path, file_name, short_path])
    except:
      return []

    # if len(result) > self.maximal_files_count:
    #   message = 'FileList: too much files in project; try setup "ignore" ' + \
    #     'or "maximal_files_count" setting properly; current ' + \
    #     '"maximal_files_count" setting value: ' + str(self.maximal_files_count)
    #   sublime.error_message(message)
    #   raise Exception(message)

    return result