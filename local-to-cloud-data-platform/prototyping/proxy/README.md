# Proxy setup - Traefik

```bash
docker compose --profile proxy up
```

open: http://whoami.dev.datajourney.expert in a browser

> we have nice URLs and they resolve to localhost

SSL is still missing - wait 90 seconds

> https://whoami.dev.datajourney.expert/

## SSL letsencrypt

### handling local firewwall

Allow Docker to Access DNS Ports for Resolution

    Process: docker or com.docker.backend (or the process that Docker uses on your machine).
    Destination: Any IP address (as DNS queries go to various servers).
    Ports: 53 (UDP/TCP)
    Direction: Outbound
    Purpose: This allows Docker to resolve domain names via DNS.

2. Allow Docker to Communicate with Cloudflare's API

    Process: docker or com.docker.backend.
    Destination: api.cloudflare.com
    Ports: 443 (HTTPS)
    Direction: Outbound
    Purpose: This allows Traefik (via Docker) to update DNS records for the DNS challenge using Cloudflare's API.

3. Allow Docker to Communicate with Let's Encrypt Servers

    Process: docker or com.docker.backend.
    Destination: acme-v02.api.letsencrypt.org
    Ports: 443 (HTTPS)
    Direction: Outbound
    Purpose: This allows Traefik to complete the certificate issuance/renewal process by communicating with Let's Encrypt.