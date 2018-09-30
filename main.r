#clear Environment
rm(list=ls())
if(!is.null(dev.list())) dev.off()

csv_uffwind_res <- read.delim("2018.csv")

uffenheim <- csv_uffwind_res

remove(csv_uffwind_res)

uffenheim$measurement_date <- as.POSIXlt(uffenheim$measurement_date, format = "%Y-%m-%d %H:%M:%S")

# remove attributes that do not really impact final result
uffenheim <- uffenheim[, !(colnames(uffenheim) %in% c("pitch_degrees", "rotor_speed_rpm", "wind_direction_degrees", "rotation_gondola_degrees", "charging_station_w", "battery_drain_or_load_w", "state_of_charge_percent", "battery_voltage_v", "rlm_solar_kw", "slp_solar_kw"))]

# clean up data, not all of it is useful, sometimes it is just wrong (total is not equal to wind+solar+chp)
uffenheim <- uffenheim[abs((uffenheim$solar_generation_kw + uffenheim$wind_generation_kw + uffenheim$chp_kw) - uffenheim$total_production_kw) < 1,]
uffenheim <- uffenheim[uffenheim$power_use_kw != 0,]
uffenheim <- uffenheim[(uffenheim$total_production_kw + uffenheim$electricity_purchase_kw) - uffenheim$power_use_kw > -1,]
uffenheim <- uffenheim[uffenheim$chp_kw < 1000,]
uffenheim <- uffenheim[uffenheim$electricity_purchase_kw < 10000,]

uffenheim$green_energy <- ifelse(uffenheim$total_production_kw > uffenheim$power_use_kw, 1, 0)
uffenheim$chp_online <- ifelse(uffenheim$chp_kw > 10, 1, 0)

# not really used in the model in the end, except time of day
uffenheim$weekday <- uffenheim$measurement_date$wday
uffenheim$time_of_day <- uffenheim$measurement_date$hour
uffenheim$month <- uffenheim$measurement_date$mon


model_data <- uffenheim[, (colnames(uffenheim) %in% c("time_of_day", "wind_speed_m_s", "chp_online", "green_energy"))]

library(rpart)

# could improve it with more data on weather (cloudiness, amount of sunlight), might not also be the best method
fit <- rpart(green_energy ~ time_of_day + wind_speed_m_s + chp_online, method="class", data=model_data)

printcp(fit)
summary(fit)

plot(fit, uniform=TRUE, main="Classification Tree for Uffenheim")
text(fit, use.n=TRUE, all=TRUE, cex=.8)
