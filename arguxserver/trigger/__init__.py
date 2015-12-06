# package

from threading import Thread

import time

from arguxserver.dao import ItemDAO

class TriggerWorker(Thread):

    def run(self):
        while(True):
            # Run once a minute.
            triggers = ItemDAO.getAllTriggers()
            for trigger in triggers:
                print(trigger.evaluate_rule())
            time.sleep(60)
            print("THREAD")
