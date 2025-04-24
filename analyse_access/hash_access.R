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


library(dotenv)
library(digest)

load_dot_env("../.env")
APP_NAME = Sys.getenv("APP_NAME")
URL = Sys.getenv("URL")
today = Sys.Date()

Paths = list.files("/var/log/apache2/", pattern=paste0(APP_NAME, "_access"), full.names=TRUE)
# Paths = list.files("log", pattern=paste0(APP_NAME, "_access"), full.names=TRUE)

outdir = "hash_access"
if (!dir.exists(outdir)) {
    dir.create(outdir)
}

Id = stringr::str_extract(basename(Paths), "[[:digit:]]+")
Id[is.na(Id)] = 0
Id = as.numeric(Id)
Paths = Paths[order(Id)]
nPaths = length(Paths)

for (i in 1:nPaths) {
    path = Paths[i]
    date = today - i + 1

    isgz = grepl("[.]gz$", basename(path))
    if (isgz) {
        path = gzfile(path, "r")
    }
    Lines = readLines(path)
    if (isgz) {
        close(path)
    }
    
    Lines = Lines[grepl(URL, Lines)]
    IP = gsub("[ ].*", "", Lines)
    IP = IP[!duplicated(IP)]
    IPhash = sapply(IP, digest, algo="sha256",
                    USE.NAMES=FALSE)

    if (length(IPhash) > 0) {
        filepath = file.path(outdir,
                             paste0(APP_NAME, "_access_",
                                    date, ".txt"))
        writeLines(IPhash, filepath)
    }
}

warnings()
