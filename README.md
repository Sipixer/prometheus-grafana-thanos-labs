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

### Exercice 4 : Decouverte de service par fichier (file_sd)

J'ai remplace les `static_configs` par une decouverte dynamique via un fichier JSON. Le dossier `prometheus/sd/` est monte dans le conteneur sur `/etc/prometheus/sd`, et le job utilise `file_sd_configs` avec un `refresh_interval: 5s` pour voir les changements rapidement.

Au premier lancement, j'ai mis seulement `prometheus:9090` dans `targets.json` et verifie dans Status > Targets qu'une seule cible apparaissait.

![alt text](assets/file_1777282905106.png)

J'ai ensuite ajoute `node-exporter:9100` dans le JSON, sans recharger Prometheus. Apres quelques secondes, la nouvelle cible est apparue automatiquement dans Targets.

![alt text](assets/file_1777282919649.png)

### Exercice 5 : Recording rules

J'ai ajoute une mini-app Flask `demo-api` qui expose les metriques `demo_http_*` (compteurs, histogramme de latence). Elle est buildee directement par le docker-compose.

J'ai cree un fichier `prometheus/rules/api_rules.yml` avec un groupe evalue toutes les 30s qui pre-calcule la metrique `job:http_requests:rate5m` (taux de requetes par job sur 5min). J'ai monte le dossier `rules/` dans le conteneur et ajoute `rule_files` dans `prometheus.yml`.

Apres reload de Prometheus, j'ai verifie dans Status > Rules que le groupe `api` est bien pris en compte avec sa frequence de 30s.

![alt text](assets/file_1777283703349.png)

J'ai lance une boucle curl pour generer du trafic sur `/api/users` et `/api/orders`, puis interroge la nouvelle metrique `job:http_requests:rate5m` dans l'expression browser.

![alt text](assets/file_1777283802673.png)

### Exercice 6 : Regles d'alerte et Alertmanager

J'ai ajoute un service `alertmanager` (port 9093) au docker-compose, avec une config minimale dans `prometheus/alertmanager/alertmanager.yml` (un receiver vide suffit pour le TP).

J'ai cree le fichier `prometheus/rules/api_alerts.yml` avec une alerte `HighErrorRate` qui se declenche si le ratio d'erreurs 5xx depasse 5% pendant 2 minutes. J'ai ensuite ajoute le bloc `alerting.alertmanagers` dans `prometheus.yml` pour pointer vers `alertmanager:9093`.

Avec la boucle curl active (demo-api genere ~5-8% d'erreurs naturelles), l'alerte passe en PENDING des que le seuil est franchi, puis en FIRING apres 2 minutes.

![alt text](assets/file_1777284175646.png)

Une fois en FIRING, l'alerte est envoyee a Alertmanager et apparait dans son interface sur http://localhost:9093.

![alt text](assets/file_1777284193781.png)

![alt text](assets/file_1777284206163.png)

