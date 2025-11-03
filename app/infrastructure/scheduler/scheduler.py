# app/infrastructure/scheduler/scheduler.py
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
import asyncio

from app.infrastructure.scheduler.jobs.expire_membresia import expire_membresias

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

def start_scheduler():
    """
    Configura y arranca el scheduler global.
    """
    # Registrar job async directamente, AsyncIOScheduler sabe manejar coroutines
    scheduler.add_job(
        expire_membresias,
        CronTrigger(hour=22, minute=20, timezone=timezone("America/Guayaquil")),  # hora local
        id="expire_membresias",
        replace_existing=True,
    )

    scheduler.start()

    # Logging de jobs registrados
    logger.info("✅ Scheduler iniciado con tareas registradas:")
    for job in scheduler.get_jobs():
        logger.info(f" - Job ID: {job.id}, próximo run: {job.next_run_time}")
