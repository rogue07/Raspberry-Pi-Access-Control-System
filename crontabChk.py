from crontab import CronTab
my_cron = CronTab(user='accessc')
for job in my_cron
    if job.comment == 'temp':
        my_cron.remove(job)
        my_cron.write()
