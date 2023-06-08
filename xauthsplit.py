import sys
out = sys.argv[1]
split = out.split("-auth")
new_split = split[-1].split("\n")
print(new_split[0].lstrip())
