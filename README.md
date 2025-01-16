[![ProjectHUD CI](https://github.com/FRC-1721/ProjectHud/actions/workflows/build_docker.yml/badge.svg)](https://github.com/FRC-1721/ProjectHud/actions/workflows/build_docker.yml)

# Project Hud

Flask server for displaying a quick development HUD (built specifically for use with FRC1721's code environment.

![image](https://github.com/user-attachments/assets/84932072-f848-4ab0-b196-a35a51713776)

## Development

Example ENV file

```bash
GITHUB_TOKEN=<your token>
GITHUB_REPOS=FRC-1721/ProjectHud
USERNAME_MAP=KenwoodFox:Joe,Kredcool:Keegan
GIT_COMMIT=Whatever
```

```shell
pipenv shell
flask run --debug
```

Some screens now require js libs so be sure to install and package those locally
```shell
npm run install
npm run build
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

## Example setup with openbox autostart

```
#!/bin/bash

unclutter -idle 0.1 -grab -root &

while :
do
  until curl --output /dev/null --silent --head --fail "http://10.17.21.81:5000"; do
    printf '.'
    sleep 5
  done

  xrandr --auto
  chromium \
    --no-first-run \
    --start-maximized \
    --disable \
    --disable-translate \
    --disable-infobars \
    --disable-suggestions-service \
    --disable-save-password-bubble \
    --disable-session-crashed-bubble \
    --incognito \
    --kiosk "http://10.17.21.81:5000"
  sleep 5
done &
```