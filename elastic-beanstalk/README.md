# Elastic Beanstalk source bundle

Zip the **contents** of this folder (not the folder itself), so `application.py`
sits at the root of the ZIP:

```bash
cd elastic-beanstalk
zip -r ../computech-eb.zip application.py requirements.txt static
```

Test locally first:

```bash
pip install -r requirements.txt
python application.py   # open http://127.0.0.1:5000
```
