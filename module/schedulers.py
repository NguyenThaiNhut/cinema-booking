from apscheduler.schedulers.background import BackgroundScheduler

payment_scheduler = BackgroundScheduler()
custom_user_scheduler = BackgroundScheduler()

# Set up recurring payments on Friday every 2 weeks
def start_scheduler_payment(job_function):
    payment_scheduler.add_job(job_function, 'cron', day_of_week='fri', hour=0, minute=0, week='2')
    payment_scheduler.start()

# Set up remove expired refresh tokens in blacklist function
def start_scheduler_custom_user(job_function):
    custom_user_scheduler.add_job(job_function, 'interval', days=1)
    custom_user_scheduler.start()
