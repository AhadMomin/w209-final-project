# w209-final-project

### Instructions to set up personal web server in i-school:

1. Copy w209-deploy to your server dir: ~/w209
2. You should see a directory structure like below:

```
harbinger:~/w209$ pwd
/home/ngchuchi/w209
harbinger:~/w209$ ls -lrt -r *.py templates lib static
-rw-rw-r-- 1 ngchuchi ngchuchi 5500 Nov 25 23:47 otd_page1.py
-rw-rw-r-- 1 ngchuchi ngchuchi 4848 Nov 25 23:47 otd_page2.py
-rw-rw-r-- 1 ngchuchi ngchuchi 4663 Nov 25 23:47 otd_page3.py
-rw-rw-r-- 1 ngchuchi ngchuchi 1892 Nov 25 23:47 w209.py

lib:
total 20
drwxrwxr-x 3 ngchuchi ngchuchi 4096 Sep 18 14:24 python3.11/
-rw-rw-r-- 1 ngchuchi ngchuchi 9992 Nov 25 23:47 otd_utils.py
drwxr-xr-x 2 ngchuchi ngchuchi 4096 Nov 25 23:48 __pycache__/

templates:
total 24
-rw-rw-r-- 1 ngchuchi ngchuchi  4132 Nov 26 17:52 chart.html
-rw-rw-r-- 1 ngchuchi ngchuchi 15382 Nov 26 17:53 w209.html

static:
total 9872
-rw-rw-r-- 1 ngchuchi ngchuchi 2832282 Nov 24 17:57 DataCoSupplyChainDataset_DS_AGG.csv
-rw-rw-r-- 1 ngchuchi ngchuchi 7189114 Nov 24 17:58 DataCoSupplyChainDataset_DS_MAP.csv
-rw-rw-r-- 1 ngchuchi ngchuchi   22568 Nov 26 11:16 prepros.config
drw-rw-rw- 6 ngchuchi ngchuchi    4096 Nov 26 16:55 assets/
drw-rw-r-- 4 ngchuchi ngchuchi    4096 Nov 26 16:56 vendor/
harbinger:~/w209$
```
3. Open w209.html and chart.html, replace ngchuchi with your username.
4. Reload your server (cd ~/w209; touch start.wsgi)
5. From a browser, enter URL https://apps-fall.ischool.berkeley.edu/~ngchuchi/w209/ (replace ngchuchi with your username.) 
6. If everything works, you should see the landing page.

