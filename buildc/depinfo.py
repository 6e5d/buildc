from pathlib import Path
from pycdb.header import system_header

def include_resolver(file):
	base = Path(file).parent
	include_relative = set()
	include_system = set()
	for line in open(file):
		if not line.startswith("#include"):
			continue
		line = line.removeprefix("#include").strip();
		if line.startswith("<") and line.endswith(">"):
			include_system.add(line[1:-1])
		elif line.startswith("\"") and line.endswith("\""):
			path = base / line[1:-1]
			if path.is_file():
				include_relative.add(path)
			else:
				include_system.add(line[1:-1])
	return (include_system, include_relative)

class Depinfo:
	def __init__(self):
		self.objs = [False, False, False] # main lib test
		self.cfiles = set()
		self.systems = set()
		self.relatives = set()
		self.deps = set()

	# build include info
	def b1(self, proj):
		files = []
		src = proj / "src"
		if src.exists():
			files += list(src.iterdir())
		include = proj / "include"
		if include.exists():
			files += list(include.iterdir())
		generated = proj / "build"
		if generated.exists():
			files += list(generated.iterdir())
		for file in files:
			if file.suffix not in [".c", ".h"]:
				continue
			if file.name.endswith(".c"):
				# do not distinguish test dependency
				if file.name != "test.c":
					self.cfiles.add(file)
			systems2, relatives2 = include_resolver(file)
			self.systems |= systems2
			self.relatives |= relatives2
	# build kjkj dependencies
	def b2(self, proj):
		for r in self.relatives:
			p = r.resolve().parent.parent
			if p == proj:
				continue
			self.deps.add(p.resolve())
	# build objects
	def b4(self, proj):
		src = proj / "src"
		if (src / "main.c").exists():
			self.objs[0] = True
		else:
			self.objs[1] = True
		if (src / "test.c").exists():
			self.objs[2] = True
	def build(self, proj):
		self.b1(proj)
		self.b2(proj)
		self.b4(proj)
