# Tailnet Link

Tailnet Link connects a GitHub workflow to your [Tailscale](https://tailscale.com) network and disconnects it after the
workflow ends.

Unlike Tailscale's Linux-only [official action](https://github.com/tailscale/github-action), Tailnet Link also supports
macOS and Windows runners.

This action allows authentication with either an [auth key](https://tailscale.com/kb/1085/auth-keys) or an
[OAuth client secret](https://tailscale.com/kb/1215/oauth-clients) with the `devices` scope. Using an OAuth client
secret is recommended; you won't have to rotate it every 90 days, and nodes authenticated with this action will be
automatically preapproved on tailnets that use [device approval](https://tailscale.com/kb/1099/device-approval).

## Usage

### Inputs

| **Name**                | **Description**                                                                                                                                                  | **Required?**                                                      |
| ----------------------- |------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------------------------------------------------------------------ |
| `authkey`               | An [auth key](https://tailscale.com/kb/1085/auth-keys) or [OAuth client secret](https://tailscale.com/kb/1215/oauth-clients) with the `devices` scope.           | Yes                                                                |
| `tags`                  | A comma separated list of [tags](https://tailscale.com/kb/1068/tags) to apply to nodes authenticated with this action Each tag must begin with `tag:`.           | Yes if you use an OAuth client secret for `authkey`; no otherwise. |
| `hostname`              | A fixed [machine name](https://tailscale.com/kb/1098/machine-names). A machine name will be derived from the runner's system hostname if you don't provide this. | No                                                                 |
| `extra-args`            | Additional arguments to [`tailscale up`](https://tailscale.com/kb/1241/tailscale-up). May not include `--auth-key`, `--advertise-tags`, or `--hostname`.         | No                                                                 |
| `tailscaled-extra-args` | Additional arguments to [`tailscaled`](https://tailscale.com/kb/1278/tailscaled#flags-to-tailscaled). Only applicable on macOS and Linux runners.                | No                                                                 |

> [!WARNING]
> If you're using [tailnet lock](https://tailscale.com/kb/1226/tailnet-lock), `authkey` must be
> a [pre-signed](https://tailscale.com/kb/1226/tailnet-lock#add-a-node-using-a-pre-signed-auth-key) auth key (_not_ an
> OAuth client secret).

### Example

```yaml
- name: Connect to Tailscale
  uses: celsiusnarhwal/tailnet-link@v1
  with:
    authkey: ${{ secrets.TS_OAUTH_SECRET }}
    tags: tag:github-actions
```
