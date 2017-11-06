# How to collect review file list
## 以下のホームページからデータベースを取得
http://kin-y.github.io/miningReviewRepo/

* OpenStack:Python
* LibreOffice:Iroiro
* AOSP:Java?
* Qt:C++(WARNING: this dataset is imcomplete since an issue of Qt official Gerrit API)
* Eclipse:Java
* GerritHub:C?

行数
```sh
$ wc  gm_*.csv
 2177886 2177886  497020692 gm_aosp.csv
  638419  638419  190031704 gm_eclipse.csv
 1490073 1490073  364248098 gm_gerrithub.csv
 1000295 1000295  198269467 gm_libreoffice.csv
  998260  998260  192177972 gm_libreoffice2.csv
 4528235 4528235 1006652644 gm_openstack.csv
```

ファイルサイズ
```sh
$ du -m gm_*.csv
474     gm_aosp.csv
182     gm_eclipse.csv
348     gm_gerrithub.csv
190     gm_libreoffice.csv
961     gm_openstack.csv
```

レビューシステムURL
* aosp:https://android-review.googlesource.com
* eclipse:https://git.eclipse.org/r
* gerrithub:https://review.gerrithub.io
* libreoffice:https://gerrit.libreoffice.org
* openstack:https://review.openstack.org