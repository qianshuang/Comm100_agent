# -*- coding: utf-8 -*-

import json


def show_json(obj):
    return json.loads(obj.model_dump_json())
