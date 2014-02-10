import sublime
import sublime_plugin
import re
import os


rexLastTabs = re.compile(r'(\t+|\s+)$', re.MULTILINE)
rexEmptyLines = re.compile('^[ \t]*$\r?\n', re.MULTILINE)
rexCont = re.compile(r'[^\t\s].*[^\t\s]')
rexFormatted = re.compile(r"((?<=\s)'|(?<=\t)')|('*\s[\+|\\|])")

class RunMultilineAction(sublime_plugin.TextCommand):
	def run(self, edit, action=None):

		if not is_js_buffer(self.view):
			sublime.status_message('Multiline: Not supported format.')
			return False

		for region in self.view.sel():
			if region.empty():
				continue
			text = self.view.substr(region)
			formatted = self.checkFormat(text)

			if formatted:
				replacement = formatted
			else:
				text = re.sub(r"'", '"', text)
				replacement = self.format( rexEmptyLines.sub('', text), action )
			
			self.view.replace(edit, region, replacement)

			sublime.status_message('Multiline: Formatting is done.')
	
	def checkFormat(self, text):
		formatted = False

		# only one line formatted
		if text.find('\n') == -1 and (text.endswith("';") or text.endswith("\\")):
			return text[1: len(text) -2]


		if rexFormatted.search( text ):
			formatted = rexFormatted.sub('', text)
			formatted =formatted[1: len(formatted) -2]


		return formatted

	def format(self, text, action=None):

		lines = text.split('\n')
		symbol = action == 'plus' and '+' or r'\\'
		quote = action == 'plus' and "'" or  ""

		for index in range(len(lines)):
			
			lines[index] = rexLastTabs.sub('', lines[index])
			
			if index == len(lines) - 1:
				lines[index] = rexCont.sub( quote + rexCont.search( lines[index] ).group() + "';", lines[index])
			elif index == 0 and action == 'slash':
				lines[index] = rexCont.sub( "'" + rexCont.search( lines[index] ).group() + " " + symbol, lines[index])
			else:
				lines[index] = rexCont.sub( quote + rexCont.search( lines[index] ).group() + quote + " " + symbol, lines[index])
			
		
		return '\n'.join(lines)


#https://github.com/jdc0589/JsFormat line 47
def is_js_buffer(view):
	fName = view.file_name()
	vSettings = view.settings()
	syntaxPath = vSettings.get('syntax')
	syntax = ""
	ext = ""

	if (fName != None): # file exists, pull syntax type from extension
		ext = os.path.splitext(fName)[1][1:]
	if(syntaxPath != None):
		syntax = os.path.splitext(syntaxPath)[0].split('/')[-1].lower()

	return ext in ['js', 'json'] or "javascript" in syntax or "json" in syntax