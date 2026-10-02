# Copyright (C) 2026
# Héraut, Louis (1) <louis.heraut@inrae.fr>

# (1) INRAE, UR RiverLy, Villeurbanne, France.

# This file is part of MEANDRE-TRACC.

# MEANDRE-TRACC is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# MEANDRE-TRACC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with MEANDRE-TRACC.
# If not, see https://www.gnu.org/licenses/.


"""Vérifie l'API de la carte sur la vraie base, sans passer par Apache.

Interroge les trois routes comme le fait la page par défaut (région K,
France à +4 °C, premier narratif, trois indicateurs) et affiche une
empreinte des réponses : deux environnements Python qui donnent les
mêmes empreintes servent exactement les mêmes données.
"""

import hashlib
import json
import sys

from app import app

QUERY = {"horizon": "gwl30", "region_id": "K"}
INDICATORS = {"QA": "data_point_QA", "QJXA": "data_point_QJXA",
              "VCN10_summer": "data_point_VCN10"}


def fingerprint(data):
    """Hash of a response, floats rounded to absorb numerical noise and
    records sorted, their order not being guaranteed by SQL."""
    def normalized(x):
        if isinstance(x, float):
            return float("%.6g" % x)
        if isinstance(x, dict):
            return {k: normalized(v) for k, v in x.items()}
        if isinstance(x, list):
            x = [normalized(v) for v in x]
            if x and all(isinstance(v, dict) for v in x):
                x.sort(key=lambda v: json.dumps(v, sort_keys=True))
            return x
        return x
    text = json.dumps(normalized(data), sort_keys=True)
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def post(route, query):
    """Response of a route, or stop with its error (traceback above)."""
    r = client.post(route, json=query)
    if r.status_code != 200:
        sys.exit("%s : erreur %d" % (route, r.status_code))
    return json.loads(r.data)


client = app.test_client()
narratives = post("/get_narrative", QUERY)
print("get_narrative        %4d narratifs  empreinte %s"
      % (len(narratives), fingerprint(narratives)))
chain = sorted(n["chain"] for n in narratives)[0]
data = {key: post("/get_narrative_data", dict(QUERY, chain=chain, variable=variable, n=4,
                                               exp=chain.split("_")[0].replace("-", "_"),
                                               check_cache=False))
        for variable, key in INDICATORS.items()}
print("get_narrative_data   %4d stations   empreinte %s"
      % (sum(len(d["data"]) for d in data.values()), fingerprint(data)))
palette = post("/define_data_palette", data)
print("define_data_palette  %4d stations   empreinte %s"
      % (sum(len(d["data"]) for d in palette.values()), fingerprint(palette)))
