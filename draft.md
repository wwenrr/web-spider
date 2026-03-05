crawl_app/
├── app.py                          # Router + DI wiring + ui.run()
├── pyproject.toml                  # nicegui, peewee, pybgworker, eralchemy
├── .gitignore
├── README.md
│
├── src/                            # CLEAN ARCHITECTURE + FEATURE-BASED
│   ├── __init__.py
│   │
│   ├── utils/                      # GLOBAL UTILITIES (pure math < 5 files)
│   │   ├── __init__.py
│   │   ├── math.py                # calculate_discount(), average()
│   │   └── string.py              # slugify(), sanitize()
│   │
│   ├── ui/                         # PRESENTATION LAYER (NiceGUI)
│   │   ├── __init__.py
│   │   ├── constants/              # UI constants folder
│   │   │   ├── __init__.py
│   │   │   ├── colors.py          # 'primary': 'blue-6'
│   │   │   ├── table_ids.py       # 'jobs': 'jobs_table'
│   │   │   └── routes.py          # '/': 'dashboard'
│   │   ├── helpers/                # UI helpers
│   │   │   ├── __init__.py
│   │   │   ├── formatters.py      # format_price(), format_date()
│   │   │   └── notifications.py   # show_success(), show_error()
│   │   ├── static/                 # CSS
│   │   │   ├── __init__.py
│   │   │   ├── custom.css
│   │   │   └── theme.css
│   │   ├── components/             # Reusable widgets
│   │   │   ├── __init__.py
│   │   │   ├── cards/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── job_card.py
│   │   │   │   └── product_card.py
│   │   │   ├── badges/
│   │   │   │   ├── __init__.py
│   │   │   │   └── status_badge.py
│   │   │   └── forms/
│   │   │       ├── __init__.py
│   │   │       └── crawl_form.py
│   │   ├── layout/
│   │   │   ├── __init__.py
│   │   │   ├── global_layout.py
│   │   │   └── page_layouts.py
│   │   └── pages/
│   │       ├── __init__.py
│   │       ├── dashboard.py       # @ui.page('/')
│   │       ├── crawl.py          # @ui.page('/crawl')
│   │       ├── jobs.py           # @ui.page('/jobs')
│   │       └── job_detail.py     # @ui.page('/jobs/{job_id}')
│   │
│   ├── domain/                     # BUSINESS LAYER (FEATURE-BASED)
│   │   ├── __init__.py
│   │   ├── common/
│   │   │   ├── __init__.py
│   │   │   ├── constants/
│   │   │   │   ├── __init__.py
│   │   │   │   └── common.py     # PAGE_SIZE=50
│   │   │   ├── helpers/
│   │   │   │   ├── __init__.py
│   │   │   │   └── validators.py # validate_job_config()
│   │   │   ├── i_storage.py
│   │   │   └── base_service.py
│   │   ├── crawl/
│   │   │   ├── __init__.py
│   │   │   ├── constants/
│   │   │   │   ├── __init__.py
│   │   │   │   └── crawl.py      # MAX_PAGES=100
│   │   │   ├── helpers/
│   │   │   │   ├── __init__.py
│   │   │   │   └── url_parser.py
│   │   │   ├── interfaces/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── i_crawl_repo.py
│   │   │   │   └── i_spider.py
│   │   │   └── services/
│   │   │       ├── __init__.py
│   │   │       └── crawl_service.py
│   │   └── jobs/
│   │       ├── __init__.py
│   │       ├── constants/
│   │       │   ├── __init__.py
│   │       │   │   └── jobs.py   # JOB_STATUS enum
│   │       ├── helpers/
│   │       │   ├── __init__.py
│   │       │   └── priority.py
│   │       ├── interfaces/
│   │       │   ├── __init__.py
│   │       │   └── i_job_queue.py
│   │       └── services/
│   │           ├── __init__.py
│   │           ├── job_manager.py
│   │           └── scheduler_service.py
│   │
│   ├── models/                     # ENTITIES
│   │   ├── __init__.py
│   │   ├── constants/
│   │   │   ├── __init__.py
│   │   │   ├── table_names.py
│   │   │   └── field_names.py
│   │   ├── helpers/
│   │   │   ├── __init__.py
│   │   │   └── query_helpers.py
│   │   ├── base.py
│   │   ├── todo.py
│   │
│   ├── infrastructure/             # INFRASTRUCTURE LAYER
│   │   ├── __init__.py
│   │   ├── constants/
│   │   │   ├── __init__.py
│   │   │   ├── db.py
│   │   │   └── queue.py
│   │   ├── helpers/
│   │   │   ├── __init__.py
│   │   │   ├── db_utils.py
│   │   │   └── migration_helpers.py
│   │   ├── database.py
│   │   ├── queues/
│   │   │   ├── __init__.py
│   │   │   ├── pybgworker_queue.py
│   │   │   └── task_registry.py
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── todo.py
│   │       └── migrate_history.py
│   │
│   └── adapters/
│       ├── __init__.py
│       └── spiders/
│           ├── __init__.py
│           ├── constants/
│           │   ├── __init__.py
│           │   └── spiders.py
│           ├── helpers/
│           │   ├── __init__.py
│           │   └── selectors.py
│           ├── base_spider.py
│           ├── tiki_spider.py
│           └── shopee_spider.py
