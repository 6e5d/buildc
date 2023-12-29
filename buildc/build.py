import os, sys, shutil
from subprocess import run
from pathlib import Path
from .cc import cc
from .depinfo import Depinfo
from pycdb.link import link_lookup
from gid import path2gid, gid2c

def nsdef(proj):
	gid = path2gid(proj)
	name = gid[-1]
	camel = gid2c(gid, "camel")
	snake = gid2c(gid, "snake")
	return name, camel, snake

def nsmacro(proj):
	name, camel, snake = nsdef(proj)
	return [
		f"-D{name}(sym)={snake}_##sym",
		f"-D{name.capitalize()}(sym)={camel}##sym",
	]

def build_cmd(proj, depinfo, obj, test, rebuild):
	Path("build").mkdir(exist_ok = True)
	cmd = cc()
	cmd += ["-include", "assert.h"]
	cmd += ["-include", "stdlib.h"]
	cmd += ["-include", "stdio.h"]
	cmd += ["-include", "string.h"]
	name = proj.name
	# order is important
	if obj.suffix == ".so":
		cmd += ["-fPIC", "-shared"]
	else:
		cmd += ["-fPIE"]
	for c in depinfo.cfiles:
		cmd.append(str(c))
	if test:
		cmd.append("src/test.c")
	cmd += ["-o", str(obj)]
	links = []
	cmd += nsmacro(proj)
	for dep in depinfo.deps:
		cmd += nsmacro(dep)
		sopath = dep / "build" / f"lib{dep.name}.so"
		# test if sopath is real library(or virtual)
		if not sopath.is_file():
			continue
		cmd.append(str(sopath))
	cmd += list(depinfo.links)
	return cmd

def runner(cmd):
	if cmd:
		p = run(cmd)
		if p.returncode != 0:
			print(p.returncode, " ".join(cmd))
			sys.exit(1)

def convert_objs(p, v):
	name = p.name
	if v.objs[0]:
		file = p / f"build/{name}.elf"
		v.objs[0] = file
	if v.objs[1]:
		file = p / f"build/lib{name}.so"
		v.objs[1] = file
	if v.objs[2]:
		file = p / f"build/test.elf"
		v.objs[2] = file

def build(proj):
	v = Depinfo()
	v.build(proj)
	convert_objs(proj, v)
	for idx, obj in enumerate(v.objs):
		if obj == False:
			continue
		os.chdir(proj)
		cmd = build_cmd(proj, v, obj, idx == 2, True)
		runner(cmd)
