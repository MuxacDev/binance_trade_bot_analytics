use TradeBotDb;
INSERT INTO MainTable0 (sel_interval, period,step,vol_btc,vol_usd,bal_btc,bal_usd,old_ord,max_usage,margin,per,total_sum,comb_status)
SELECT year, period,step,vol_btc,vol_usd,bal_btc,bal_usd,old_ord,max_usage,margin,per,total_sum,comb_status FROM TableByYears;


