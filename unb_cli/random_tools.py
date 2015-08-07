import json


def pp(struct):
  print json.dumps(struct, sort_keys=True, indent=4)
