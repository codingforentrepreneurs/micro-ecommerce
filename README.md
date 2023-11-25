# micro-ecommerce
Learn how to build a Micro eCommerce Web App with Python and Serverless Postgres


## Prerequisites
- Python experience with [30 Days of Python](https://www.codingforentrepreneurs.com/courses/30-days-python-38/) or similiar
- Django experience with [Try Django](https://www.codingforentrepreneurs.com/courses/try-django-3-2/) or similiar
- Basic understanding of HTML and CSS

## Required Software
- [Python 3.10](https://www.python.org/downloads/) or newer
- [Node.js 18.15 LTS](https://nodejs.org/) or newer (For Tailwind.CSS)
- [Git](https://git-scm.com/)


## Getting Started

```bash
mkdir -p ~/dev
cd ~/dev
git clone https://github.com/codingforentrepreneurs/micro-ecommerce
cd micro-ecommerce
git checkout start
```

### Create dotenv file:

Run `echo "" > .env` to create the `.env` in the root of your project:

```bash
DATABASE_URL=""
DJANGO_SECRET_KEY=<some-secret>
DJANGO_DEBUG=1
ALLOWED_HOST="*"
```
Replace `<some-secret>` by any of the following commands:

```bash
openssl rand -base64 32
```

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

```bash
python -c 'import secrets;print(secrets.token_urlsafe(32))'
```


=== Configure Environment

To install packages and run various command shortcuts, we use [rav](https://github.com/jmitchel3/rav). Open `rav.yaml` to see the various commands available if you prefer to not use `rav`.

_macOS/Linux Users_
```bash
python3 -m venv venv
source venv/bin/activate
venv/bin/python -m pip install pip pip-tools rav --upgrade
venv/bin/rav run installs
rav run freeze
```
In `rav.yaml`, you'll see that `rav run installs` maps to:

- `venv/bin/pip-compile src/requirements/requirements.in -o src/requirements.txt`
- `venv/bin/python -m pip install -r src/requirements.txt`
- `npm install`


_Windows Users_
```powershell
c:\Python310\python.exe -m venv venv
.\venv\Scripts\activate
python -m pip install pip pip-tools rav --upgrade
rav run win_installs
rav run win_freeze
```
In `rav.yaml`, you'll see that `rav run win_installs` maps to:

- `pip-compile src/requirements/requirements.in -o src/requirements.txt`
- `python -m pip install -r src/requirements.txt`
- `npm install`


=== Main Commands

With all the configuration done, here are the main commands you'll run:

```
rav run server
rav run watch
rav run vendor_pull
```

- `rav run server` maps to `python manage.py runserver` in the `src` folder
- `rav run watch` triggers tailwind to watch the tailwind input file to make the compiled tailwind output file via `npx tailwindcss -i <input-path> -o <output-path> --watch`
- `rav run vendor_pull` run this occasionally to pull the latest version of Flowbite, HTMX, and any other third party static vendor files you need.
