import sublime, sublime_plugin
from telnetlib import Telnet
import os


class ZiReloadmayaCommand(sublime_plugin.TextCommand):

	reloadCmd='import {0}\nimport {1}\nreload({1})'

	def run(self, edit):

		cmd = self.getCommand()
		try:
			connex = Telnet( '127.0.0.1', 7002, timeout = 3)
			connex.write(self.reloadCmd.encode(encoding='UTF-8'))
			connex.close()

		except Exception as e:
			print(cmd)
			sublime.error_message('%s' % e)

	def getLauncher( self ):
		region = self.view.find('def launch', 0)

		if not region: return None
		else: return 'launch()'

	def getCommand(self):

		fil = self.view.file_name()
		fullPath = os.path.dirname( fil )

		tokens = fullPath.split(os.sep)
		folders = list()
		while '__init__.py' in os.listdir(fullPath):
			fullPath = os.sep.join(tokens)
			folders.append( tokens.pop(-1) )

		folders = sorted(folders, reverse=True)
		module ='{}.{}{}'.format( tokens[-1], '.'.join(folders), os.path.basename( fil ).replace('.py', ''))

		launcher = self.getLauncher()

		cmd = self.reloadCmd.format(tokens[-1], module)

		if launcher:
			cmd += '\n{}.{}'.format(module, launcher)

		return cmd

