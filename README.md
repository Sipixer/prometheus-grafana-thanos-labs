# Observabilite avec Prometheus, Grafana et Thanos

## Module 1 - Prometheus

### Exercice 1 : Installer Prometheus et acceder a l'interface web

J'ai mis en place un docker-compose pour lancer Prometheus sur le port 9090 avec un volume persistant.

```bash
cd prometheus
docker compose up -d
```

J'ai ensuite ouvert http://localhost:9090 et verifie dans Status > Targets que Prometheus se scrape bien lui-meme (cible UP).

![alt text](assets/file_1777281319020.png)

### Exercice 2 : Ecrire votre premier prometheus.yml

J'ai ecrit mon propre `prometheus.yml` avec un `scrape_interval` global de 10s et un external label `environment=lab`. J'ai ajoute le flag `--web.enable-lifecycle` au docker-compose pour pouvoir recharger la config a chaud.

Apres avoir relance le conteneur, j'ai verifie dans Status > Configuration que mes parametres etaient bien pris en compte.

![alt text](assets/file_1777281988601.png)

J'ai ensuite modifie une valeur dans le fichier (passage de `environment: lab` a `environment: staging`) et declenche un reload sans redemarrer le conteneur :

```bash
curl -X POST http://localhost:9090/-/reload
```

La nouvelle valeur apparait dans Status > Configuration.

![alt text](assets/file_1777281996711.png)

### Exercice 3 : Ajouter node_exporter et scraper les metriques systeme

J'ai ajoute le service `node-exporter` au docker-compose (port 9100) et un nouveau job `node` dans `prometheus.yml` qui pointe vers `node-exporter:9100` (DNS interne du reseau Compose).

Apres `docker compose up -d`, j'ai verifie dans Status > Targets que la cible `node` est UP.

![alt text](assets/file_1777282443426.png)

J'ai ensuite teste la metrique `node_cpu_seconds_total` dans l'expression browser pour confirmer que les metriques systeme remontent bien.

![alt text](assets/file_1777282475751.png)
