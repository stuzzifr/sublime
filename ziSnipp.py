import sublime, sublime_plugin

functionTemplate = '''{0}def {1}( {2} ):
{0}\'\'\'
{0}Description:
{0}Param: {2}
{0}Return:
{0}\'\'\'
'''

classTemplate = '''class {0}({1}):\n\n\tdef __init__(self, {2}):
'''

class ZiSnippCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		region = self.getLineRegion()

		res = self.parse(self.view.substr(region))

		if not res:
			sublime.error_message('cannot find pattern')
			return

		self.view.replace(edit, region, res)

	def getLineRegion(self):
		regionSets = self.view.sel()
		region = self.view.line(regionSets[0])

		return region

	def parse(self, line):

		tokens = line.split(',')

		func = tokens[0]
		args = tokens[1:]

		# function snippet =================================
		if not 'init' in line:
			tabs = func.count('\t')
			func = func.lstrip()

			return functionTemplate.format( '\t'*tabs, func, ', '.join(args) )

		# class snippet =================================
		elif 'init' in line:

			beginInit = args.index('init')

			return classTemplate.format(func, ', '.join(args[:beginInit]),
			', '.join(args[beginInit:]))


		else:
			return None

