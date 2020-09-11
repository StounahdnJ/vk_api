#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import check_mes
import prov_user
from multiprocessing import Process

def main():
    p1.start()
    p2.start()

    p1.join()
    p2.join()
p1 = Process(target=prov_user.prov)
p2 = Process(target=check_mes.check)
if __name__ == '__main__':
    main()