#!/usr/bin/env python

import time
import syringe_pumper as sp

my_sp = sp.SyringePumper( time.time(), 10.0, 8.0 )

#my_sp.reset()
my_sp.set_addr( 2 )

my_sp.close()

