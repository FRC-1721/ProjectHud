[![ProjectHUD CI](https://github.com/FRC-1721/ProjectHud/actions/workflows/build_docker.yml/badge.svg)](https://github.com/FRC-1721/ProjectHud/actions/workflows/build_docker.yml)

# Project Hud

Flask server for displaying a quick development HUD (built specifically for use with FRC1721's code environment.

![image](https://github.com/user-attachments/assets/4e62c869-bbb0-4391-9818-1196055490b4)

## Development

```shell
pipenv shell
flask run --debug
```

## Deploy

Deployment is handled with docker.

```yaml
# Example Docker Compose File

services:
  project_hud:
    image: ghcr.io/frc-1721/project_hud-bot:main
    environment:
      TZ: America/New_York
      GITHUB_TOKEN: YOUR_TOKEN
      GITHUB_REPOS: YOUR,REPOS
      USERNAME_MAP: username:realname,
```

