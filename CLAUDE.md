# MEANDRE-TRACC

Web presentation of the Explore2 hydrological projections for France at the
global warming levels of the TRACC (France at +2.0, +2.7 and +4.0 °C), by
region and narrative. It derives from MEANDRE (https://github.com/lou-heraut/MEANDRE)
and keeps its structure: a Flask app serves the page and a small JSON API read
by the frontend JS; the data is a PostgreSQL database; production runs under
Apache with mod_wsgi, on the same server as MEANDRE.

The maintainer works in French: answer in French. Code comments, docstrings
and commit messages are in English; output meant for the user (make help,
check_api.py) is in French.

## Layout
- `app.py`: Flask routes. The page routes render `templates/index.html`; the
  map uses `POST /get_narrative` (narratives of a region and warming level),
  `POST /get_narrative_data` (data of one indicator for a narrative) and
  `POST /define_data_palette` (shared colour scale of the three indicators).
- `app.wsgi`: mod_wsgi entry point, finds the app and its `.env` next to itself.
- `static/`: frontend (`js/`, `css/`, `html/` fragments, `data/` geojson of
  regions and rivers), `py/` Python helpers (`color.py` is used by `app.py`).
- `check_api.py`: queries the three API routes as the page does by default,
  on the real database without Apache, and prints a fingerprint of the responses.
- `Makefile`: the single entry point, `make help` lists the targets.
- `INSTALL.md`: server installation, as an ordered list of make targets.

## Commands
- Local: `make venv-dev` (venv `.python_env`), `make run` (http://127.0.0.1:5000).
- Server, from the code directory: `make update` (git pull --ff-only, pip
  install, `touch app.wsgi` to reload the mod_wsgi daemon), `make status`,
  `make check`, `make logs`.
- Access statistics are computed by MEANDRE (`access_log/stats.py` there),
  not in this repository.

## Conventions (shared with MEANDRE)
- Everything runs from the code directory: no hardcoded paths (Makefile uses
  `$(CURDIR)`, `app.wsgi` its own directory). The server is a plain git checkout,
  never edited by hand: changes go through a commit and `make update`.
- Production is detected in `static/js/script.js` from the hostname, so the
  deployed code is exactly the repository.
- Python dependencies are pinned in `requirements.txt` to the latest versions
  supporting the server's Python, and installed in `.python_env` locally and on
  the server.
- `.env` is a dotenv file (see `.env.example`): the Makefile reads its values
  with sed (`dotenv` function), it must never be sourced by a shell.
- Before changing the Python environment of the server, compare
  `make check PYTHON=<current python>` with `make check`: same fingerprints,
  same data served.

## Pitfalls
- GNU make runs a recipe line containing `$(MAKE)` even under `make -n`, and
  with `.ONESHELL` the whole recipe is one line: never call `$(MAKE)` inside a
  recipe, share code with `define` blocks instead.
- `app.py` is the production API: keep its changes minimal and verify them
  with `make check`.
