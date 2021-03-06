# ReportPhotos
![GitHub](https://img.shields.io/github/license/adamrees89/ReportPhotos.svg)
![GitHub repo size in bytes](https://img.shields.io/github/repo-size/adamrees89/ReportPhotos.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/adamrees89/ReportPhotos.svg)
[![Build Status](https://travis-ci.org/adamrees89/ReportPhotos.svg?branch=master)](https://travis-ci.org/adamrees89/ReportPhotos)
[![Coverage Status](https://coveralls.io/repos/github/adamrees89/ReportPhotos/badge.svg?branch=master)](https://coveralls.io/github/adamrees89/ReportPhotos?branch=master)

[![Known Vulnerabilities](https://snyk.io/test/github/adamrees89/ReportPhotos/badge.svg)](https://snyk.io/test/github/adamrees89/ReportPhotos)
![GitHub issues](https://img.shields.io/github/issues/adamrees89/ReportPhotos.svg)
![GitHub pull requests](https://img.shields.io/github/issues-pr/adamrees89/ReportPhotos.svg)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/adamrees89/ReportPhotos.svg)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WWZP5GMRRVPTQ&source=url)

This is a Python script to resize and crop photos to a sensible size (5cm square) for inclusion in reports (Designed for Microsoft Word Reports in A4).

## Future Development

Next items for development:

1. Unit Testing
2. CI with Travis
3. Progress Bar

## Speed

Currently the script can process approximately 20 photos per second, depending on available cores as it uses the [concurrent.futures module.](https://docs.python.org/3.3/library/concurrent.futures.html).  See the table below for the speed comparison before and after adding multithreading.

More information and quick tutorial on concurrent.futures:  https://gist.github.com/mangecoeur/9540178

|  |Number of Photos | Elapsed Time | Photos/second | Seconds/photo |
|---|---|---|---|---|
No Multithreading | 129 | 25.93 seconds| 4.97 | 0.20 |
Mulithreading with concurrent.futures | 129 | 6.45 seconds| 20.00 | 0.05|
