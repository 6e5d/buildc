def common():
	return ["-O3",
		"--std=c2x", "-D", "_POSIX_C_SOURCE=200809L",
		"-include", "stddef.h",
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
		# suppress warning by compiler attributes is not acceptable
		"-Wno-padded",
		"-Wno-unsafe-buffer-usage",
		"-Wno-missing-noreturn",
		"-Wno-unused-parameter",
		# c99
		"-Wno-declaration-after-statement",
		# style related warning are useless for generated code
		"-Wno-logical-op-parentheses",
		"-Wno-shift-op-parentheses",
		"-Wno-redundant-parens",
		"-Wno-parentheses",
		# qualifier is shit
		"-Wno-incompatible-pointer-types-discards-qualifiers",
		"-Wno-incompatible-function-pointer-types-strict",
		"-Wno-incompatible-function-pointer-types",
	]
	return cmd

cc = clang
# cc = cc.gcc
