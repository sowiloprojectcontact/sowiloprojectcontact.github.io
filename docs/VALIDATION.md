# Préparation GitHub Pages — 26 octobre 2026

## Contenu vérifié

- 12 pages HTML : accueil, Community, briques, actualités, Pro, contact, 404 et cinq articles.
- Navigation commune, métadonnées de partage, titre et description de chaque page.
- Téléchargement des sources vers le dépôt public Community ; état de préversion Linux explicite.
- Licence personnelle et usage non commercial indiqués, sans promesse de disponibilité Pro.
- Deux actualités datées sur Community et les briques du Builder.
- Contact par email et suivi GitHub ; aucun paiement ou formulaire serveur.
- Paquet public par liste blanche, sans application, base, secret ou environnement Python.

## Vérifications réalisées

- `python3 scripts/check_site.py` : 12 pages contrôlées, liens et ancres internes valides,
  un H1 par page et métadonnées essentielles présentes.
- `python3 -m unittest discover -s tests -v` : 4 tests réussis du script de publication
  avec API simulée : compte différent refusé, site existant non géré préservé,
  ancien déploiement non présenté comme succès, confirmation du commit attendu.
- Compilation Python des scripts réussie.
- Archive ZIP construite avec les seuls fichiers publics et somme SHA256 fournie.

Le navigateur Chromium local n’a pas pu démarrer dans cet environnement (opération
système refusée avant chargement des pages). Aucun résultat de contrôle visuel ou
capture n’est donc revendiqué. Le rendu bureau/mobile reste à vérifier dans un navigateur.

## Publication

Le dépôt public Community a été vérifié par lecture GitHub. La connexion API GitHub
nécessaire à la création/publication du site n’est pas accessible depuis cette session.
L’intégration GitHub installée retourne également une indisponibilité d’outil.
Le script de publication s’est arrêté avant toute écriture distante.

**Aucun site GitHub Pages publié ni aucune URL active n’est confirmé à cette étape.**
Le paquet et le script permettent de reprendre depuis le terminal normal de la
machine, avec GitHub CLI connecté. Le script ne confirme un lien qu’après une
construction Pages correspondant au commit envoyé.
