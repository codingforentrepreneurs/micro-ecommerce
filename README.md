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

To install packages and run various command shortcuts, we use [rav](https://github.com/jmitchel3/rav). Open `rav.yaml` to see the various commands available if you prefer to not use `rav`.

_macOS/Linux Users_
```bash
python3 -m venv venv
source venv/bin/activate
venv/bin/python -m pip install pip pip-tools rav --upgrade
venv/bin/rav run installs
rav run freeze
```


_Windows Users_
```powershell
c:\Python310\python.exe -m venv venv
.\venv\Scripts\activate
python -m pip install pip pip-tools rav --upgrade
rav run win_installs
rav run win_freeze
```