from telnetlib import Telnet
import sublime_plugin
import sublime

import time
import os


class ziMayalogCommand(sublime_plugin.TextCommand):
    """Will open the maya log file in Sublime

    Need first to run in Maya:
    cmds.scriptEditorInfo(hfn="mayaconsole",
                          writeHistory=True,
                          clearHistoryFile=True)
    """

    def run(self, edit):

        consoleFile = r"C:\Users\stu\Documents\maya\mayaconsole"
        msg = self.view.window().status_message

        if not os.path.exists(consoleFile):
            msg("cannot find the mayaconsole file '%s'" % consoleFile)
            return

        sublime.active_window().open_file(consoleFile)
        msg("console loaded %s" % consoleFile)


class ZiReloadMayaCommand(sublime_plugin.TextCommand):
    """Reload the current file in maya
    looking for a main or launch function to execute
    """

    def run(self, edit):

        connex = Telnet("127.0.0.1", int(7002), timeout=5)
        cmd = self.getCommand()

        try:
            connex.write(cmd.encode(encoding="UTF-8"))
            print("\nsuccess:\n%s" % cmd)
            self.view.window().status_message("File reloaded successfully")

        except Exception as e:
            sublime.error_message("ZiReload failed: %s" % e)

        connex.close()

    def getLauncher(self):

        if self.view.find("def launch", 0):
            return "launch()"

        elif self.view.find("def main", 0):
            return "main()"

        else:
            self.window.message_dialog("cannot find the launcher function")
            return

    def getCommand(self):

        fileName = self.view.file_name()

        if not os.path.exists(fileName):
            sublime.message_dialog("cannot reload the current file to Maya")
            return

        fullPath = os.path.dirname(fileName)
        tokens = fullPath.split(os.sep)

        folders = list()
        while "__init__.py" in os.listdir(fullPath):

            fullPath = os.sep.join(tokens)
            folders.append(tokens.pop(-1))

        folders = folders[:-2]
        folders = sorted(folders, reverse=True)
        module = "{}.{}.{}".format(tokens[-1], ".".join(folders),
            os.path.basename(fileName).replace(".py", "") )

        cmd = "import {0}\nimport {1}\nreload({1})".format(tokens[-1], module)
        launcher = self.getLauncher()

        if launcher:
            cmd += "\n{}.{}".format(module, launcher)

        return cmd
