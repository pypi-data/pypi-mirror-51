# pylbc

Une API Python3 pour LeBonCoin.

**SEULEMENT pour la catégorie immobilier pour le moment.**

## Installation

Requis : **python >= 3.0**

### Avec pip

```sh
python3 -m venv venv
source venv/bin/activate
python3 -m pip install pylbc 
```

### Depuis les sources 

```sh
git clone https://github.com/razaborg/pylbc.git
cd pylbc
```

Et utilisez le directement ou installez-le avec setuptools :-)


## Utilisation

### Directement en CLI

```sh
curl https://raw.githubusercontent.com/razaborg/pylbc/master/lbcli.py -o lbcli.py
chmod +x lbcli.py
./lbcli.py
usage: lbcli.py [-h] [--coordinates LAT LNG] [--radius RADIUS] --category
                {immobilier,ventes,locations,colocations} --real-estate-type
                {maison,appartement,terrain,parking,autre}
                [--price-range PRICE_RANGE PRICE_RANGE]
                [--square-range SQUARE_RANGE SQUARE_RANGE]
                [--rooms-range ROOMS_RANGE ROOMS_RANGE]
                [--order-by {price,time}] [--sort-order {asc,desc}]
                [--verbose] [-y]
lbcli.py: error: the following arguments are required: --category/-C, --real-estate-type/-T
```

### En tant que librairie

```python
import pylbc

'''
and do your magic here...
using pylbc.Search() and pylbc.SearchResult()
'''
```
Jettez un oeil aux exemples plus bas ;-)

## Documentation

### La classe Search()

Cette classe dispose de plusieurs méthodes permettant de faciliter la construction des requêtes de recherche.
Pour le moment, seule la fonctionnalité de recherche est visée par cette API, et tout particulièrement la catégorie "immobilier". A l'avenir, peut-être de nouvelles catégories/fonctionnalités de l'API y seront ajoutées.

Plusieurs fonctionnaliéts de recherche sont proposés par le site leboncoin.

Parmi lesquelles :

- définir une catégorie : la méthode **set\_category()**
- définir un fourchette de prix : la méthode **set\_price()**
- définir une fourchette de surface : la méthode **set\_square()**
- définir une fourchette de pièces : la méthode **set\_rooms()**
- définir un/des type de bien : la méthode **set\_real\_estate\_type()**
- définir un/des départements géographiques : la méthode **set\_departments()**
- définir une zone géographique et un rayon : la méthode **set_coordinates()**

Une fois la recherche paramétrée, la requete peut être lancée avec :

- la méthode **request_infos()** pour ne récupérer que les métadonnées des résultats
- la méthode **request_once()** pour charger une seule page de résultats
- la méthode **iter_results()** pour charger l'ensemble des résultats à travers un itérateur

### La classe SearchResult()

Cette classe est un "wrapper" permettant de manipuler plus facilement les résultats renvoyés par l'API.
Elle dispose ainsi de méthodes et d'attributs spécifiques en ce sens.

Actuellement ce type d'objet ne peut être généré qu'automatiquement à partir de la classe Search(). 

#### Les méthodes "custom" 

- **is_recent()** renvoie un booléen
- **is_appartment()** renvoie un booléen
- **is_house()** renvoie un booléen
- **price_per_square()** renvoie le prix au m2 du résultat

#### Les attributs

Voici à quoi ressemble un objet de cette classe, avec l'ensemble de ses attributs:

```python
SearchResult(\
 title="Charmante maison en pierre centre-ville", \
 publication_date="2019-06-16", \
 price=510, \
 coordinates=(48.20384, -1.48986), \
 real_estate_type="maison", \
 square=60, \
 url="https://www.leboncoin.fr/locations/xxxxxxxxxxx.htm", \
 thumbnail="https://img6.leboncoin.fr/ad-thumb/xxxxxxxxxxxxxxx.jpg"\
)
```

## Exemples 


```python
#!/usr/bin/env python3
import pylbc

lat_paris, lng_paris = 48.864716, 2.349014
radius = 50 # in kilometers

query = pylbc.Search()
query.set_price(mini=500, maxi=900)
query.set_category('locations')
query.set_real_estate_types(['maison'])

# option 1: faire une recherche autour d'un point donné (ici, paris) dans un rayon donné (ici 50kms)
query.set_coordinates(lat=lat_paris, lng=lng_paris, radius=radius)

# option 2 : recherche par départements, ici toute la bretagne :-)
# query.set_departments(['22', '56', '35', '29'])

# affichage de la requete avant envoi
query.show_filters()

# pré-requête pour récupérer les métadonnées
infos = query.request_infos()
print(infos)
print("A total of %d results is announced by the server." % infos['total'])

# récupération et affichage de tous les résultats
for result in query.iter_results():
    print(result)
```



