from pathlib import Path

stds = [line.strip() for line in\
	open(Path(__file__).parent / "stdheader.txt")]

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
		self.latest = 0
		self.objs = [False, False, False] # main lib test
		self.systems = set()
		self.relatives = set()
		self.cfiles = set()
		self.deps = set() # kjkj relative path dep, fs path
		self.sysdeps = set() # system dep

	# build include info
	def b1(self, proj):
		files = []
		src = proj / "src"
		if src.exists():
			files += list(src.iterdir())
		include = proj / "include"
		if include.exists():
			files += list(include.iterdir())
		for file in files:
			# just make everything easier
			# even only test.c changes, still rebuild whole project
			mtime = file.stat().st_mtime
			self.latest = max(mtime, self.latest)
			if file.name.endswith(".c"):
				# do not distinguish test dependency
				if file.name != "test.c":
					self.cfiles.add(file.name)
			systems2, relatives2 = include_resolver(file)
			self.systems |= systems2
			self.relatives |= relatives2
	# build kjkj dependencies
	def b2(self, proj):
		for r in self.relatives:
			try:
				mtime = r.stat().st_mtime
				self.latest = max(mtime, self.latest)
			except FileNotFoundError:
				print("skipping", r)
				pass
			p = r.resolve().parent
			if p.name != "include":
				print("skipping", r)
				continue
			p = p.parent
			if p == proj:
				continue
			self.deps.add(p.resolve())
	# build sysdeps for -l linking options
	def b3(self):
		for system in self.systems:
			if system in stds:
				continue
			self.sysdeps.add(system)
	# build objects
	def b4(self, proj):
		src = proj / "src"
		if (src / "main.c").exists():
			self.objs[0] = True
		elif self.cfiles and self.cfiles != ["test.c"]:
			self.objs[1] = True
		if (src / "test.c").exists():
			self.objs[2] = True
	def build(self, proj):
		self.b1(proj)
		self.b2(proj)
		self.b3()
		self.b4(proj)
