

# # INSERT INTO aqi_daily_features (
# #     city_id,
# #     feature_date,
# #     mean_aqi,
# #     std_aqi,
# #     min_aqi,
# #     max_aqi,
# #     mean_pm2_5,
# #     mean_pm10,
# #     mean_no2,
# #     mean_co
# # )
# # SELECT
# #     city_id,
# #     DATE(hour_ts) AS feature_date,

# #     AVG(avg_aqi) AS mean_aqi,
# #     STDDEV(avg_aqi) AS std_aqi,
# #     MIN(avg_aqi) AS min_aqi,
# #     MAX(avg_aqi) AS max_aqi,

# #     AVG(avg_pm2_5) AS mean_pm2_5,
# #     AVG(avg_pm10)  AS mean_pm10,
# #     AVG(avg_no2)   AS mean_no2,
# #     AVG(avg_co)    AS mean_co

# # FROM aqi_hourly_history
# # WHERE hour_ts >= CURDATE() - INTERVAL 1 DAY
# #   AND hour_ts <  CURDATE()
# # GROUP BY city_id, feature_date
# # ON DUPLICATE KEY UPDATE
# #     mean_aqi = VALUES(mean_aqi),
# #     std_aqi  = VALUES(std_aqi),
# #     min_aqi  = VALUES(min_aqi),
# #     max_aqi  = VALUES(max_aqi),
# #     mean_pm2_5 = VALUES(mean_pm2_5),
# #     mean_pm10  = VALUES(mean_pm10),
# #     mean_no2   = VALUES(mean_no2),
# #     mean_co    = VALUES(mean_co);
# now all things of prediction db is ready but there is one issue like for local i run all things also college works i close the servers so i have not enough data for aqi_historical and aqi_feature so i want i truncat my all data and for starting i start to fetch data and deployee in cloud after mouth we write code for prediction because after mouth we have one mouth data in featureml table . but before it i complete all thing in code so in day to day it store data in tabel. i write query for delete so after mouth it delete data ans   

# psql 'postgresql://neondb_owner:npg_e9fsrgHWI6At@ep-young-fog-a8fnz1vx-pooler.eastus2.azure.neon.tech/
# neondb?sslmode=require&channel_binding=require'

# psql 'postgresql://neondb_owner:npg_e9fsrgHWI6At@ep-young-fog-a8fnz1vx-pooler.eastus2.azure.neon.tech/
# Project_Aqi?sslmode=require&channel_binding=require'