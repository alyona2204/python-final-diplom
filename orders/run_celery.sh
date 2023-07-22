#!/bin/bash
celery -A orders worker -l INFO -B
