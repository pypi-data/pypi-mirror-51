

class IModel(object):

	@property
	def name(self): return self._name
	@name.setter
	def name(self, value): self._name = value

	@property
	def directory(self): return None


	def save(self, data, path): return data
	def load(self, data, path): return data


	def generate_child_name(self, prefix):

		count = 1
		index = 0
		children = self.children
		candidate = prefix + str(count)

		while index<len(children):

			child = children[index]
			if child.name == candidate:
				index = 0
				count += 1
				candidate = prefix + str(count)
			index += 1

		return candidate


