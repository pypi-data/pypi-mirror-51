# -*- coding: utf-8 -*-
from mergefier.mergefier import Mergefier
import sys

if __name__ == "__main__":
    m = Mergefier()
    m.check_input()
    m.mergefy(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
