data = {
	"termios.h": [],
	"unistd.h": [],
	"signal.h": [],
	"libgen.h": [],
	"wayland-util.h": [],
	"math.h": ["m"],
	"tgmath.h": ["m"],
}

def link_lookup(path):
	if path in data:
		return [f"-l{x}" for x in data[path]]
	path = path.removesuffix(".h")
	path = path.split("/")[0]
	if path == "sys":
		return []
	return [f"-l{path}"]
