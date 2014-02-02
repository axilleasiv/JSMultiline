import sublime, sublime_plugin


class Multiline(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if region.empty():
				continue
			text = self.view.substr(region)
			replacement = self.format(text)
			
			self.view.replace(edit, region, replacement)
	
	def escLastTabs(self, line):
		if line.endswith('\t'):
			return self.escLastTabs(line[:-1])

		return line
	
	def checkFormat(self, lines):
		formatted = False

		if lines[0].endswith('+'):
			formatted = ['+']
		elif lines[0].endswith('\\'):
			formatted = ['\\']

		return formatted

	def unFormat(self, lines, char):
		print 'unFormat'
		print char
		
		if char[0] == '+':
			for index in range(len(lines)):
			
				tIndex = lines[index].rfind('\t') + 1
				line = lines[index]
			
				if(index == len(lines) - 1):
					lines[index] = line[0: tIndex] + line[tIndex + 1: len(line) - 2]  
				else:
					lines[index] = line[0: tIndex] + line[tIndex + 1: len(line) - 3]
		elif char[0] == '\\':
			for index in range(len(lines)):
			
				tIndex = lines[index].rfind('\t') + 1
				line = lines[index]
			
				if index == len(lines) - 1:
					lines[index] = line[0: len(line) - 2]  
				elif index == 0:
					lines[index] = line[0: tIndex] + line[tIndex + 1: len(line) - 1]
				else:
					lines[index] = line[0: len(line) - 1]

		return '\n'.join(lines)


class PlusCommand(Multiline):
	def format(self, lines):
		lines = lines.split('\n')
		charFormat = self.checkFormat(lines)

		if charFormat:
			return self.unFormat(lines, charFormat)
		
		for index in range(len(lines)):
			lines[index] = self.escLastTabs(lines[index])
			
			tIndex = lines[index].rfind('\t') + 1
			line = lines[index]
			
			if(index == len(lines) - 1):
				lines[index] = line[0: tIndex] + "'" + line[tIndex: len(line)] + "';"  
			else:
				lines[index] = line[0: tIndex] + "'" + line[tIndex: len(line)] + "' +"
			
		return '\n'.join(lines)



class SlashCommand(Multiline):
	def format(self, lines):
		lines = lines.split('\n')
		charFormat = self.checkFormat(lines)

		if charFormat:
			return self.unFormat(lines, charFormat)
		
		for index in range(len(lines)):
			lines[index] = self.escLastTabs(lines[index])
			
			if(index == len(lines) - 1):
				lines[index] = lines[index] + "';"  
			elif (index == 0):
				lines[index] = "'" + lines[index] + "\\"
			else:
				lines[index] = lines[index] + "\\"
			
		return '\n'.join(lines)