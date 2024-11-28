# -*- coding: utf-8 -*-

import json
import logging
import re
import time

from concurrent_log import ConcurrentTimedRotatingFileHandler

# 日志配置
logger = logging.getLogger("agent_logger")
logger.setLevel(logging.INFO)
handler = ConcurrentTimedRotatingFileHandler(
    filename="log/agent", when="MIDNIGHT", interval=1, backupCount=3, encoding="utf-8"
)
handler.suffix = "%Y-%m-%d.log"
handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


def show_json(obj):
    return json.loads(obj.model_dump_json())


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json_file(obj_dic, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(obj_dic, file, ensure_ascii=False)


def wait_on_run(client, run, thread_id):
    sleep_seconds = 0
    while run.status == "queued" or run.status == "in_progress" or (run.status == "failed" and sleep_seconds <= 60):
        time.sleep(1)
        sleep_seconds += 1
        print("run.status: {}, sleep for {} seconds totally...".format(run.status, sleep_seconds))

        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
    return run
