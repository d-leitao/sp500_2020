# sp500_2020
<p>Analysis of the S&amp;P 500 Index throughout 2020<br>
(using plotly+pandas in python)</p><br>

<p>
<b>scrapers.py</b><br>
info_build() - scrapes wikipedia's S&P 500 Index stock list on 2020-12-31<br>
weights_build() - scrapes market cap weights from slickcharts.com on 2020-12-20<br>
summ_build() - joining the information for both (1) <br>
panel_build() - scrapes yahoo finance for daily adjusted close prices
</p>
<p><b>viz.py</b> includes the plotly code for some of the vizualizations</p>
<p><b>notebook.ipynb</b> presents the analysis</p><br>

<p>(1) <i>kept only the stocks that were present in the Index throughout the whole year</i></p>