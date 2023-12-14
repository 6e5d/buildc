def common():
	return ["-O3",
		"--std=c2x", "-D", "_POSIX_C_SOURCE=200809L",
		"-include", "assert.h",
		"-include", "stddef.h",
		"-include", "stdio.h",
		"-include", "stdlib.h",
		"-include", "string.h",
		"-include", "stdbool.h",
		"-include", "stdint.h",
		# warning should block, or mtime gets skipped in second build
		"-Werror",
		"-Wl,--no-undefined",
		"-Wl,--no-allow-shlib-undefined",
	]

def gcc():
	cmd = ["gcc"] + common() + [
		"-Wall",
		"-Wextra",
		"-Wconversion",
		"-Wpedantic",
	]
	return cmd

def clang():
	cmd = ["clang"] + common() + [
		"-Weverything",
		"-Wno-switch-enum", # it disallows default
		# wayland-scanner cannot handle it
		# first of all the design of qualifier in c is problematic
		"-Wno-cast-qual",
		# suppress warning by compiler attributes are not acceptable
		"-Wno-padded",
		"-Wno-unsafe-buffer-usage",
		"-Wno-missing-noreturn",
		# c99
		"-Wno-declaration-after-statement",
	]
	return cmd
