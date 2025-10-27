                            _           
 _ __   ___  __ _  _ _   __| | _ _  ___ 
| '  \ / -_)/ _` || ' \ / _` || '_|/ -_)
|_|_|_|\___|\__,_||_||_|\__,_||_|  \___|                      
| |_  _ _  __ _  __  __ 
|  _|| '_|/ _` |/ _|/ _|
 \__||_|  \__,_|\__|\__|
                                                          
Généré le [DATE] par MEANDRE-TRACC
https://meandre-tracc.explore2.inrae.fr/
contact.meandre@listes.inrae.fr


INFORMATIONS GENERALES _______________________________________________
MEANDRE-TRACC présente de manière guidée les résultats des projections
hydrologiques réalisées sur la France suivant les niveaux de 
réchauffement dans le cadre de la TRACC (Trajectoire de 
Réchauffement de référence pour l'Adaptation au Changement Climatique).

Les résultats sont présentés sous forme de narratifs qui correspondent
à une sélection de projections permettant de couvrir au mieux les 
futurs possibles pour la ressource en eau. Les narratifs sont 
sélectionnés à l'échelle d'un territoire et pour un niveau de 
réchauffement donné.

Retrouvez la méthode de sélection des narratifs :
https://doi.org/10.57745/FE356V

Retrouvez les fiches résultats par secteur hydrographique :
https://doi.org/10.57745/QDCSBZ

Retrouvez les messages et enseignements du projet Explore2 :
https://doi.org/10.57745/J3XIPW


INFORMATIONS COMPLÉMENTAIRES _________________________________________
Soutien fiancier : Le projet EHCLO est financé par l'Agence de l'Eau
Loire-Bretagne

Partenaires :
- AELB https://agence.eau-loire-bretagne.fr/home.html

Entrepôt de donnée du projet Explore2 :

 - Retrouvez, entre autres, les rapports et les fiches de résultats
   pour chaque point de simulation sur Recherche Data Gouv.
   https://entrepot.recherche.data.gouv.fr/dataverse/explore2

 - Mise à disposition des projections hydrologiques des eaux de
   surface et souterraines, réalisées dans le cadre du projet
   national Explore2, ainsi que de l’ensemble des informations
   utiles à leur bonne utilisation, sous différentes formes
   graphiques ou numériques.
   DRIAS Eau https://drias-eau.fr

Développement : Blaise Calmel et Louis Héraut, RiverLy, INRAE, France
Référent scientifique : Jean-Philippe Vidal, RiverLy, INRAE, France
Contact : contact.meandre@listes.inrae.fr

Code source : https://github.com/BlaiseCalmel/MEANDRE-TRACC
Hébergement web : Data Center de INRAE, Île-de-France


INFORMATIONS METHODOLOGIQUES _________________________________________
Les séries annuelles de variables hydrologiques qui sont à la base de
ces résultats sont disponibles sur DRIAS Eau https://drias-eau.fr.


PARAMÈTRES D'ANALYSE _________________________________________________
[PARAM]


APERCUS DES DONNEES ET FICHIERS ______________________________________
Arborescence :
./
├── data.csv
├── ETALAB-Licence-Ouverte-v2.0.pdf
├── ETALAB-Open-Licence-v2.0.pdf
├── map_QA.png
├── map_QJXA.png
├── map_VCN10.png
├── meta_point.csv
├── meta_projection.csv
├── meta_variable.csv
└── README.txt

- data.csv 
Changement (relatif) de la variable étudiée

- ETALAB-Licence-Ouverte-v2.0.pdf et ETALAB-Open-Licence-v2.0.pdf
Licence Ouvcerte en français et en anglais

- meta_point.csv
Métadonnées des points de simulation

- meta_projection.csv
Métadonnées des différentes chaînes de projections sélectionnées

- meta_variable.csv
Métadonnées de la variable étudiée


INFORMATIONS SPECIFIQUES POUR : *.csv ________________________________
séparateur décimal : "."


INFORMATIONS SPECIFIQUES POUR : data.csv _____________________________
code
  -- nom : code hydro 3
  -- description : Code du point de simulation disponible dans
                   la variable code de meta_point.csv 
  -- valeurs autorisées : 10 caratères

value *variable*
  -- nom : *variable*
  -- description : Acronyme de la variable disponible dans
                   meta_variable.csv avec variable_en
  -- unité : Unité de la variable disponible dans meta_variable.csv
             avec unit_en
  -- valeurs autorisées : numérique

fill *variable*
  -- nom : couleur
  -- description : Couleur hexadécimale associée à la valeur
                   de changement selon la palette de couleur
		   disponible dans meta_variable.csv
  -- valeurs autorisées : caratère


INFORMATIONS SPECIFIQUES POUR : meta_point.csv _______________________
code
  -- nom : code hydro 3
  -- description : Code du point de simulation
  -- valeurs autorisées : 10 caratères

code_hydro2
  -- nom : code hydro 2
  -- description : Code du point de simulation dans suivant
                   l'ancien formalisme Hydro2
  -- valeurs autorisées : 8 caratères

is_reference
  -- nom : station de référence ?
  -- description : Est ce que le point est associé à une station
                   hydrométrique de référence définie ici :
		   https://doi.org/10.57745/DE9SPE
  -- valeurs autorisées : booléen
  
name
  -- nom : nom
  -- description : nom du point de simulation
  -- valeurs autorisées : caratère

hydrological_region
  -- nom : région hydrologique
  -- description : région hydrologique de la station
  -- valeurs autorisées : caratère

lat_deg
  -- nom : longitude
  -- description : Longitude en WGS 84
  -- unité : degré
  -- valeurs autorisées : numérique
  
lat_deg
  -- nom : latitude
  -- description : Latitude en WGS 84
  -- unité : degré
  -- valeurs autorisées : numérique

xL93_m
  -- nom : X lambert 93
  -- description : position X de la station en lambert 93 
  -- unité : m
  -- valeurs autorisées : numérique
  
yL93_m
  -- nom : Y lambert 93
  -- description : position Y de la station en lambert 93 
  -- unité : m
  -- valeurs autorisées : numérique

surface_km2
  -- nom : surface
  -- description : Surface du bassin versant couvert par le point
                   de simulation
  -- unité : km2
  -- valeurs autorisées : numérique
  ** Cette variable est dérivée en surface_[HM]_km2 pour chaque modèle
     hydrologique défini dans la variable HM de meta_projection.csv
     afin connaître la surface de ce même bassin mais dans le monde
     du modèle.

n_rcp26
  -- nom : n RCP 26
  -- description : Nombre de modèle hydrologique pour le RCP 26
                   qui simulent le point considéré
  -- unité : sans dimension
  -- valeurs autorisées : numérique
  ** Cette variable est dérivée pour les RCP 45 et 85 car le nombre
     de modèle hydrologique au point dépend du RCP sélectionné


INFORMATIONS SPECIFIQUES POUR : meta_projection.csv __________________
chain
  -- nom : chaîne
  -- description : Chaîne de modélisation choisis
  -- valeurs autorisées : caratère
  -- particularité : Les étapes de la chaîne de modélisation sont
                     séparées par des "_"

RCP
  -- nom : RCP
  -- description : Scénario d'émission considéré
  -- valeurs autorisées : caratère

GCM
  -- nom : GCM
  -- description : Modèle Climatique Global considéré
  -- valeurs autorisées : caratère

RCM
  -- nom : RCM
  -- description : Modèle Climatique Régional considéré
  -- valeurs autorisées : caratère

BC
  -- nom : BC
  -- description : Correction de biais considérée
  -- valeurs autorisées : caratère

HM
  -- nom : HM
  -- description : Modèle hydrologique considéré
  -- valeurs autorisées : caratère

storyline_name
  -- nom : nom du narratif
  -- description : Nom du narratif associé si il existe
  -- valeurs autorisées : caratère

storyline_info
  -- nom : information du narratif
  -- description : Informations caractéristiques du narratif associé
                   si il existe
  -- valeurs autorisées : caratère
  
storyline_color
  -- nom : couleur du narratif
  -- description : Couleur hexadécimale associée au narratif
                   si il existe
  -- valeurs autorisées : caratère


INFORMATIONS SPECIFIQUES POUR : meta_variable.csv ____________________
variable_en
  -- nom : variable
  -- description : Acronyme de la variable en anglais
  -- valeurs autorisées : caratère

unit_en
  -- nom : unité
  -- description : Unité de la variable en anglais
  -- valeurs autorisées : caratère

name_en
  -- nom : nom
  -- description : Nom de la variable en anglais
  -- valeurs autorisées : caratère

description_en
  -- nom : description
  -- description : Description de la variable en anglais
  -- valeurs autorisées : caratère

method_en
  -- nom : méthode
  -- description : Méthode de calcul de la variable en anglais
  -- valeurs autorisées : caratère

sampling_period_en
  -- nom : périod d'échantillonnage
  -- description : Période d'échantillonnage de l'année hydrologique
                   en anglais
  -- valeurs autorisées : caratère

topic_en
  -- nom : sujet
  -- description : Mot clé concerant la variable en anglais
  -- valeurs autorisées : caratère

** l'ensemble des paramètres ci-dessus sont dérivés en français **

is_date
  -- nom : date de date ?
  -- description : Est ce que la variable est associée à un jour
                   de l'année ?
  -- valeurs autorisées : booléen

to_normalise
  -- nom : variable normalisable ?
  -- description : Est ce que la variable doit être normalisée ?
  -- valeurs autorisées : booléen

palette
  -- nom : palette
  -- description : Palette de couleur à utiliser pour la variable
  -- valeurs autorisées : caratère
  -- particularité : couleurs séparées par des ", "

palette
  -- nom : palette
  -- description : Palette de couleur à utiliser pour la variable
  -- valeurs autorisées : caratère
  -- particularité : couleurs séparées par des ", "

bin
  -- nom : intervalles
  -- description : Intervalles de valeurs associés à la palette
  -- valeurs autorisées : caratère
  -- particularité : couleurs séparées par des ", "
