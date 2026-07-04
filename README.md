# Home Assistant Apprise Notify

Home Assistant custom notify integration for sending rich notifications through an Apprise API server.

Home Assistant already ships a built-in Apprise notify platform. This custom integration exists for the Apprise API deployment model: Home Assistant sends notifications to a central Apprise API endpoint and can pass rich Apprise API fields such as markdown format, type, attachments, and tags.

## Installation

Add this repository as a HACS custom repository with category `Integration`, install it, and restart Home Assistant.

## Configuration

```yaml
notify:
  - platform: apprise_notify
    name: apprise
    url: http://apprise.apprise.svc.cluster.local/notify/matrix
```

Optional timeout:

```yaml
notify:
  - platform: apprise_notify
    name: apprise
    url: http://apprise.apprise.svc.cluster.local/notify/matrix
    timeout: 10
```

## Usage

```yaml
action: notify.apprise
data:
  title: Front door
  message: "**Door opened** at {{ now().strftime('%H:%M') }}"
  data:
    type: warning
    format: markdown
    attachment: https://example.test/snapshot.jpg
```

Supported `data` fields are passed to Apprise API when present:

- `type`
- `format`
- `attachment`
- `attach`
- `attachments`
- `tag`
- `tags`

If Home Assistant `target` is provided and no explicit `tag` or `tags` is set, `target` is forwarded as the Apprise `tag` filter.
