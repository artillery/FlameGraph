#!/usr/bin/env python

import sys
import re

SEARCH_STACK = 1
CONSUME_THREAD_ID = 2
CONSUME_STACK = 3

def main():
  state = SEARCH_STACK
  curThreadId = None
  curStackList = []

  stackTree = dict()

  for line in sys.stdin:

    if state == SEARCH_STACK:
      if re.search(r'^==== JS stack trace ==', line):
        state = CONSUME_THREAD_ID
        continue

    elif state == CONSUME_THREAD_ID:
      m = re.search(r'Security context: 0x([0-9a-f]+) ', line)
      if m:
        curThreadId = m.group(1)
        state = CONSUME_STACK
        continue

    elif state == CONSUME_STACK:
      m = re.search(r'^=+$', line)
      if m:
        curStackList.reverse()
        d = stackTree.setdefault(curThreadId, [0, {}])
        for func in curStackList:
          d = d[1].setdefault(func, [0, {}])
        d[0] += 1

        curThreadId = None
        curStackList = []
        state = SEARCH_STACK
        continue

      m = re.search(r'([0-9]+): (\w+)', line)
      if m:
        curStackList.append(m.group(2))
        continue

  def traverse(node, path):
    for name, child in node.items():
      newPath = path[:] + [name]
      print ';'.join(newPath), child[0]
      traverse(child[1], newPath)

  traverse(stackTree, [])



if __name__ == '__main__':
  main()
