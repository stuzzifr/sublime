"""My custom tool for sublime Text
"""
import os
import subprocess

import sublime_plugin
import sublime


FUNCTEMPLATE = "{spaces}def {func}({args}):\n" '{indent}"""Description\n'
CLSTEMPLATE = (
    "class {func}({subcls}):\n\n" "{indent}def __init__(self, {args}):\n"
)


class ZiDocstringCommand(sublime_plugin.TextCommand):
    """usage:
    type toto,self,myarg
    then you should have all these tokens organized perfectly
    """

    padd = 4

    def run(self, edit):
        """Description

        :Param var(None): desc.
        :Return (None): desc.
        """
        region = self.get_line_region()
        res = self.parse(self.view.substr(region))

        if not res:
            sublime.error_message("cannot find pattern")
            return

        self.view.replace(edit, region, res)

    def get_line_region(self):
        """Description

        :Param var(None): desc.
        :Return (None): desc.
        """
        region_sets = self.view.sel()
        region = self.view.line(region_sets[0])

        return region

    def parse(self, line):
        """Description

        :Param var(None): desc.
        :Return (None): desc.
        """
        tokens = line.split(",")

        func = tokens[0]
        args = tokens[1:]
        args_doc = [token for token in args if "self" not in token]

        nspaces = func.count(" ")
        spaces = " " * nspaces
        indent = spaces + (" " * self.padd) if nspaces else " " * self.padd

        func = func.lstrip()

        print("line: ", line)

        # -- function snippet
        if "init" not in line:
            template = FUNCTEMPLATE.format(
                args=", ".join(args),
                spaces=spaces,
                indent=indent,
                func=func,
            )

            if not args_doc:
                args_doc = ["var"]

            for arg in args_doc:
                template += ("\n{indent}:Param {arg}(None): desc.\n").format(
                    indent=indent,
                    arg=arg,
                )

            template += "{indent}:Return (None): desc.\n".format(indent=indent)
            template += '{indent}"""'.format(indent=indent)

            return template

        # -- class snippet
        elif "init" in line:
            begin_init = args.index("init")

            return CLSTEMPLATE.format(
                func=func,
                subcls=", ".join(args[:begin_init]),
                spaces=spaces,
                indent=indent,
                args=", ".join(args[begin_init + 1:]),
            )

        else:
            return None


class ZiQuoteCommand(sublime_plugin.TextCommand):
    """Add quote at each side of the selection"""

    def run(self, edit):
        """Description

        :Param var(None): desc.
        :Return (None): desc.
        """
        region = self.view.sel()
        wordreg = self.view.word(region[0])
        word = self.view.substr(wordreg)

        if "'" not in word:
            self.view.replace(edit, wordreg, "'%s'" % word)


class ZiCommentCommand(sublime_plugin.TextCommand):
    """Add special art symbols all around the selection"""

    def run(self, edit):
        """Description

        :Param var(None): desc.
        :Return (None): desc.
        """
        region = self.view.sel()
        wordreg = self.view.line(region[0])
        word = self.view.substr(wordreg)
        indentation = " " * word.count(" ")

        word = word.lstrip()
        wlen = len(word)

        replaced = (
            "{indent}{deco:#>{llen}}\n"
            "{indent}{deco} {word} {deco}\n"
            "{indent}{deco:#>{llen}}\n"
        )

        self.view.replace(
            edit,
            wordreg,
            replaced.format(
                indent=indentation,
                word=word,
                deco="#",
                wlen=wlen,
                llen=wlen + 4,
            ),
        )


class ZiStyle(sublime_plugin.TextCommand):
    """Run pylint to see what is not conventional in the current
    code
    """

    def run(self, edit):
        """Description

        :Param var(None): desc.
        :Return (None): desc.
        """
        console_file = r"C:\Users\stu\Documents\consolelog"
        folder_name = os.path.dirname(console_file)

        if not os.path.exists(folder_name):
            raise Exception("the path does not exists : %s" % folder_name)

        outputstr = self.get_output()
        with open(console_file, "w") as fil:
            fil.write(outputstr)

        active_win = sublime.active_window()
        num_grps = active_win.num_groups()
        activ_grp = active_win.active_group()

        activ_grp = num_grps - 1 if activ_grp + 1 > num_grps else activ_grp + 1

        active_win.open_file(console_file, group=activ_grp)

    def get_output(self):
        """Description

        :Param var(None): desc.
        :Return (None): desc.
        """
        file_name = self.view.window().active_view().file_name()
        process = subprocess.Popen(["python", "-m", "pylint", file_name],
                                   shell=True,
                                   stdout=subprocess.PIPE)

        output = process.stdout.read()
        outputstr = output.decode("utf-8")

        return outputstr


class ZiBlack(sublime_plugin.TextCommand):
    """Run black linter and change the current code"""

    def run(self, edit):
        """Description

        :Param var(None): desc.
        :Return (None): desc.
        """
        file_name = self.view.window().active_view().file_name()
        process = subprocess.Popen(["python3", "-m", "black", "-v", file_name],
                                   shell=True,
                                   stdout=subprocess.PIPE)

        output = process.stdout.read()
        print(output.decode("utf-8"))
