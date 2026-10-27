# Site public Sowilo

Vitrine statique en français : découverte de Community, actualités du projet,
avancement des briques et présentation des usages Pro. HTML/CSS sans framework,
ressource graphique distante, mesure d’audience ou formulaire serveur.

## Pages

- `index.html` : présentation Sowilo et accès à Community.
- `community.html` : fonctions, licence, téléchargement des sources et installation Linux.
- `blog.html` et `articles/` : actualités datées et articles de présentation.
- `boutique.html` : avancement des briques (nom de fichier historique conservé).
- `pro.html` : présentation du prototype et des usages des indépendants.
- `contact.html` : email public et suivi GitHub.
- `confidentialite.html` : politique de confidentialité du site et de Sowilo Réseaux.
- `suppression-donnees.html` : retrait des accès Meta, suppression locale et demandes par email.
- `404.html`, `robots.txt`, `.nojekyll` : fichiers pour l’hébergement statique.

Le dépôt Community est public sur https://github.com/sowiloprojectcontact/sowilo-community.
Community est une préversion Linux à usage personnel non commercial gratuit,
sous licence personnelle propriétaire. Les autres applications ne sont pas
annoncées comme offres publiques disponibles. Le site ne prend aucun paiement.

## Prévisualiser et vérifier

```sh
python3 -m http.server 8080 --bind 127.0.0.1
python3 scripts/check_site.py
python3 scripts/package_site.py
```

Le paquet `dist/sowilo-github-pages.zip` contient uniquement les fichiers publics,
à la racine de l’archive. Ne pas envoyer le dossier `/home/remy`, les applications,
les bases, les environnements Python ou leurs configurations sur Pages.

## Publier sur GitHub Pages

Cible prévue : dépôt `sowiloprojectcontact/sowiloprojectcontact.github.io`.
L’adresse ne sera confirmée qu’après le résultat du déploiement.

Depuis ce dossier, avec GitHub CLI connecté au compte propriétaire :

```sh
python3 scripts/publish_github.py
```

Ce script vérifie les fichiers, l’identité connectée et le dépôt cible, crée un
dépôt public si absent, publie un commit atomique puis configure Pages sur la branche
par défaut, à la racine. Aucun push forcé ni changement de visibilité d’un dépôt
existant. Un autre site déjà présent est conservé. Le script attend une construction
Pages correspondant au commit envoyé avant d’annoncer une publication vérifiée.
Il utilise l’authentification `gh` existante ; aucune clé dans les sources ou arguments.
Si la connexion doit être renouvelée : `gh auth login -h github.com`, depuis le terminal
normal de la machine. Ne pas copier de jeton dans les échanges.

### Alternative depuis le navigateur

1. Créer le dépôt public `sowiloprojectcontact.github.io` sur le compte propriétaire.
2. Décompresser le ZIP puis envoyer son contenu à la racine du dépôt, y compris `.nojekyll`.
3. Dans Settings → Pages, choisir Deploy from a branch, branche main, dossier `/`.
4. Attendre la construction puis utiliser le lien Visit site fourni par GitHub.

## Actualiser les contenus

Ajouter une page dans `articles/`, sa date réelle et son lien dans blog.html.
Préserver la navigation commune et les chemins relatifs (`../` pour les articles).
Les états des briques doivent refléter leurs validations effectives. Relancer les
contrôles, puis publier après relecture. Le site peut ensuite être servi sur VPS
avec les mêmes fichiers statiques.

L’exception est la page 404, dont la base `/` cible le site utilisateur à la racine.
L’adapter si le site est finalement publié dans un sous-dossier.

## Validation de cette préparation

Voir [le rapport](docs/VALIDATION.md). Les captures de contrôle restent dans artifacts/
et ne sont jamais incluses dans l’archive publique.

Références officielles :
[création d’un site Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site),
[API Pages](https://docs.github.com/en/rest/pages/pages).
