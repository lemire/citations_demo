# Tableau de bord Metabase pour le classement Stanford

Ce projet vous permet de visualiser les données du fichier `stanford_ranking_2025.csv` dans un tableau de bord Metabase. Aucune base de données existante n'est requise : nous utiliserons SQLite pour stocker les données.


### Installation de Docker sous Windows

Pour installer Docker sous Windows, commencez par vérifier que votre système répond aux exigences : Windows 10 (version 2004 ou ultérieure) ou Windows 11, avec la fonctionnalité Hyper-V activée pour les éditions Pro, Enterprise ou Education. Rendez-vous sur le site officiel de Docker (docker.com) et téléchargez **Docker Desktop** pour Windows. Exécutez le programme d’installation, qui vous guidera à travers un processus simple. Assurez-vous que l’option "Enable WSL 2" est sélectionnée si vous utilisez Windows Subsystem for Linux (WSL 2), car cela améliore les performances. Une fois l’installation terminée, redémarrez votre ordinateur si nécessaire. Lancez Docker Desktop, qui s’exécutera en arrière-plan, et vérifiez son bon fonctionnement en ouvrant un terminal (PowerShell ou Invite de commandes) et en tapant `docker --version`. Si la commande renvoie une version, Docker est prêt à être utilisé.


Après l’installation, vous pouvez exécuter des commandes Docker comme `docker run` depuis un terminal. Par exemple, pour tester, tapez `docker run hello-world`, ce qui télécharge une image de test et exécute un conteneur affichant un message de confirmation. Assurez-vous que Docker Desktop est en cours d’exécution, car il gère le moteur Docker. Si vous utilisez WSL 2, vous pouvez également exécuter des commandes Docker depuis une distribution Linux installée (comme Ubuntu) via le terminal WSL. Les commandes comme `docker pull` (pour télécharger une image), `docker build` (pour créer une image à partir d’un Dockerfile) ou `docker ps` (pour lister les conteneurs en cours) fonctionnent de la même manière que sur d’autres systèmes. Consultez la documentation officielle pour explorer les options de `docker run`, comme le mappage de ports ou de volumes.

### Installation de Docker sous macOS

Sur macOS, Docker s’installe via **Docker Desktop** pour Mac, compatible avec macOS 10.15 (Catalina) ou versions ultérieures. Téléchargez l’installateur depuis le site officiel de Docker. Deux versions sont proposées : une pour les processeurs Intel et une pour les puces Apple Silicon (M1/M2). Choisissez celle correspondant à votre matériel. Une fois téléchargé, ouvrez le fichier .dmg, faites glisser l’icône Docker dans le dossier Applications et lancez Docker Desktop. Lors du premier démarrage, macOS peut demander une autorisation pour exécuter le logiciel. Docker Desktop s’intègre au système via HyperKit (pour Intel) ou la virtualisation native d’Apple (pour M1/M2). Après le lancement, vérifiez l’installation en ouvrant un terminal et en tapant `docker --version`. Si une version s’affiche, l’installation est réussie.


Une fois Docker Desktop lancé sur macOS, vous pouvez utiliser des commandes comme `docker run` dans le terminal. Par exemple, exécutez `docker run hello-world` pour tester votre configuration : cela télécharge une image légère et affiche un message confirmant que Docker fonctionne. Les commandes Docker sont identiques à celles sous Windows ou Linux, comme `docker run -d -p 80:80 nginx` pour lancer un conteneur Nginx accessible via un navigateur sur le port 80. Assurez-vous que Docker Desktop est actif, car il gère le moteur Docker en arrière-plan. Pour des tâches avancées, explorez des options comme `docker run --rm` (pour supprimer automatiquement le conteneur après son arrêt) ou `docker run -v` (pour monter des volumes). La documentation Docker fournit des exemples détaillés pour personnaliser ces commandes selon vos besoins.



### Contexte et méthodologie du jeu de données (Stanford/Elsevier Top 2% Scientist Rankings)

Le classement Stanford/Elsevier des 2 % des scientifiques les plus influents, souvent appelé « World’s Top 2% Scientists », est une initiative conjointe de l’université Stanford et de l’éditeur scientifique Elsevier. Il vise à identifier les chercheurs les plus cités à l’échelle mondiale, en s’appuyant sur des données bibliométriques standardisées extraites de la base Scopus, gérée par Elsevier. Ce classement, mis à jour annuellement, repose sur une méthodologie développée par le professeur John P.A. Ioannidis et son équipe, publiée initialement en 2020 dans *PLOS Biology*. L’objectif est de fournir une mesure transparente de l’impact scientifique, tout en évitant les biais liés à une utilisation inappropriée des métriques de citations. Les données sont basées sur un instantané de Scopus (par exemple, août 2024 pour la version 7) et incluent des indicateurs comme le nombre total de citations, l’indice h, l’indice hm ajusté pour la co-auteurship, et un score composite (c-score). Les chercheurs sont classés dans 22 domaines scientifiques et 174 sous-domaines, selon la classification Science-Metrix, avec des données distinctes pour l’impact sur l’ensemble de la carrière et sur une année récente (par exemple, 2023 pour la dernière mise à jour).


La sélection repose sur deux critères principaux : les 100 000 premiers scientifiques selon leur c-score (avec et sans auto-citations) ou ceux ayant un rang percentile de 2 % ou plus dans leur sous-domaine. Le c-score est un indicateur composite qui agrège plusieurs métriques, telles que le nombre de citations (excluant ou incluant les auto-citations), l’indice h (nombre de publications ayant au moins h citations), et les citations reçues pour des articles où le chercheur est premier, dernier ou auteur unique, soulignant ainsi son rôle clé. Les données incluent également des informations sur les articles rétractés (via la base Retraction Watch) et les citations liées à ces articles. Seuls les scientifiques ayant publié au moins cinq articles sont pris en compte, et les percentiles spécifiques à chaque domaine et sous-domaine permettent une comparaison équitable entre disciplines, où les pratiques de citation varient.


Ce classement est largement utilisé par les institutions académiques pour évaluer l’influence de leurs chercheurs, comme en témoignent les annonces de l’université de Prince Edward Island (17 chercheurs inclus) ou de l’American University of Sharjah (33 chercheurs reconnus). Il est divisé en deux listes : une pour l’impact sur l’ensemble de la carrière (jusqu’à fin 2023 pour la version 7) et une pour l’impact sur une seule année (citations reçues en 2023). Cela permet de reconnaître à la fois les contributions historiques et les performances récentes. 

## Étapes rapides


1. **Créer la base de données SQLite à partir du CSV**

```sh
python python/create.py
```

2. **Lancer Metabase avec Docker**

```sh
docker run -d -p 3000:3000 \
  -v $PWD/data:/data \
  --name metabase \
  metabase/metabase
```

**ATTENTION**: assurez-vous de démarrer dans le répertoire principal du projet.
Si vous ne faites pas cela, le dossier `data` sera introuvable.

3. **Configurer Metabase**
- Accédez à [http://localhost:3000](http://localhost:3000)
- Ajoutez une base de données SQLite : `data/stanford_ranking_2025.db` avec comme nom `stanford_ranking_2025.db`
- Créez un tableau de bord en important la table générée


## Activitée suggérée

- Ouvrez Metabase et sélectionnez votre base SQLite (stanford_ranking_2025.db).
- Dans le menu principal, cliquez sur “Questions” puis “Nouvelle question”.
- Choisissez la table stanford_ranking_2025.
- Filtrez les lignes où la colonne cntry est égale à `can`. Cliquez sur “Filtrer”, sélectionnez cntry, puis “est égal à” et entrez can.
- Filtrez les lignes où la colonne `Inst Name` contient `Université`. Cliquez sur “Filtrer” (`+`), sélectionnez `Inst Name`, puis “Contient” et entrez `Université`.
- Sous résumer, nombre de liens, puis Inst Name.
- Cliquez sur 'Visualiser`.
- Vous deviez alor voir un tableau. Cliquez sur visualiser, puis Histogramme. Vous devriez voir la liste des institutions par nombre de chercheur.

Si vous enregistrez cette visualisation, vous devriez être capable de l'ajouter à un tableau de bord.

## Arrêter et supprimer Metabase (Docker)
Pour arrêter le conteneur Metabase :

```sh
docker stop metabase
```

Pour le supprimer complètement :

```sh
docker rm metabase
```


## Script d'importation
Le script `python/create.py` lit le CSV et crée la base SQLite `data/stanford_ranking_2025.db`.
Vous n'avez pas besoin de ce script.

Le script `python/extract.py` va créer le CSV à partir du fichier Excel original.
Vous n'avez pas besoin de ce script.

## Pourquoi Metabase peut lire la base SQLite ?
Metabase inclut nativement le support de SQLite. Vous n'avez pas besoin d'installer SQLite séparément : il suffit d'indiquer le chemin du fichier `.db` lors de la configuration de la source de données dans Metabase. Metabase utilise le moteur SQLite embarqué pour lire et interroger la base.

## Colonnes disponibles
- `authfull` : Nom complet de l'auteur
- `inst_name` : Institution
- `cntry` : Pays
- `firstyr` : Première année
- `lastyr` : Dernière année
- `rank (ns)` : Rang
