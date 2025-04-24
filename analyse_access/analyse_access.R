# Copyright 2024
# Louis Héraut (louis.heraut@inrae.fr)*1

# *1   INRAE, France

# This file is part of MEANDRE.

# MEANDRE is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# MEANDRE is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with MEANDRE.
# If not, see <https://www.gnu.org/licenses/>.


library(dplyr)
library(ggplot2)
library(lubridate)


## GET ACCESS DATA ___________________________________________________
Paths = list.files("hash_access", full.names=TRUE)
access = dplyr::tibble()

for (path in Paths) {
    IPhash = readLines(path)
    date = as.Date(gsub("(.*[_])|([.].*)", "",
                        basename(path)))
    access = dplyr::bind_rows(access,
                              dplyr::tibble(date=date,
                                            IPhash=IPhash))
}

ASHE::write_tibble(access, "access.csv")


## PLOT ______________________________________________________________
figdir = "figures"
if (!dir.exists(figdir)) {
    dir.create(figdir)
}


### 
access_daily <- access %>%
    group_by(date) %>%
    summarise(unique_IPs = n_distinct(IPhash))

plot = ggplot(access_daily, aes(x = date, y = unique_IPs)) +
    geom_col(fill = "steelblue") +
    labs(title = "Unique IPs per Day", x = "Date", y = "Unique IPs") +
    theme_minimal()

ggsave(plot=plot,
       path=figdir,
       filename="access_daily.pdf",
       width=20, height=10, units='cm',
       dpi=300, device=cairo_pdf)


###
access_monthly <- access %>%
    mutate(month = floor_date(date, "month")) %>%
    group_by(month) %>%
    summarise(unique_IPs = n_distinct(IPhash))

plot = ggplot(access_monthly, aes(x = month, y = unique_IPs)) +
    geom_col(fill = "darkorange") +
    labs(title = "Unique IPs per Month", x = "Month", y = "Unique IPs") +
    theme_minimal()

ggsave(plot=plot,
       path=figdir,
       filename="access_monthly.pdf",
       width=20, height=10, units='cm',
       dpi=300, device=cairo_pdf)


### 
access_cumulative <- access %>%
    arrange(date) %>%
    distinct(IPhash, date) %>%
    group_by(date) %>%
    summarise(new_unique_IPs = n_distinct(IPhash)) %>%
    mutate(cum_unique_IPs = cumsum(new_unique_IPs))

plot = ggplot(access_cumulative, aes(x = date, y = cum_unique_IPs)) +
    geom_line(color = "purple", linewidth = 0.4) +
    labs(title = "Cumulative Unique IPs Over Time", x = "Date", y = "Cumulative IPs") +
    theme_minimal()

ggsave(plot=plot,
       path=figdir,
       filename="access_cumulative.pdf",
       width=20, height=10, units='cm',
       dpi=300, device=cairo_pdf)
