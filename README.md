# Observabilite avec Prometheus, Grafana et Thanos

## Module 1 - Prometheus

### Exercice 1 : Installer Prometheus et acceder a l'interface web

**Objectif** : Lancer un conteneur Prometheus, acceder a l'interface web sur le port 9090 et verifier que Prometheus se scrape lui-meme.

**Fichiers** :
- `prometheus/docker-compose.yml` — lance Prometheus sur le port 9090 avec un volume persistant

**Lancer** :

```bash
cd prometheus
docker compose up -d
```

**Verifications** :

![alt text](assets/file_1777281319020.png)

