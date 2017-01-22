#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import sys
import csv
from datetime import datetime
today = datetime.now()


def main():
    """
    """
    visits = db(db.log_visit.processed == False).select()

    for visit in visits:
        referer_stat = db((db.referer_stats.url == visit['url']) &
                          (db.referer_stats.stat_day == visit['created_on'].date()) &
                          (db.referer_stats.referer_url == visit['referer_url'])
                          ).select().first()

        if referer_stat:

            hit_count = referer_stat['hit_count'] + 1
            referer_stat.update_record(hit_count=hit_count)
        else:
            db.referer_stats.insert(url=visit['url'], stat_day=visit['created_on'].date(),
                                    referer_url=visit['referer_url'], hit_count=1)

        browser_stat = db((db.browser_stats.url == visit['url']) &
                          (db.browser_stats.stat_day == visit['created_on'].date()) &
                          (db.browser_stats.browser == visit['browser'])
                          ).select().first()

        if browser_stat:
            hit_count = browser_stat['hit_count'] + 1
            browser_stat.update_record(hit_count=hit_count)
        else:
            db.browser_stats.insert(url=visit['url'], stat_day=visit['created_on'].date(),
                                    browser=visit['browser'], hit_count=1)

        platform_stat = db((db.platform_stats.url == visit['url']) &
                           (db.platform_stats.stat_day == visit['created_on'].date()) &
                           (db.platform_stats.platform == visit['platform'])
                           ).select().first()
        if platform_stat:
            hit_count = platform_stat['hit_count'] + 1
            platform_stat.update_record(hit_count=hit_count)

        else:
            db.platform_stats.insert(url=visit['url'], stat_day=visit['created_on'].date(),
                                     platform=visit['platform'], hit_count=1)
        db.commit()


if __name__ == '__main__':
    main()
