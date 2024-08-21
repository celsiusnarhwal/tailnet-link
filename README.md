# Tailnet Link

Tailnet Link connects a GitHub workflow to your [Tailscale](https://tailscale.com) network and disconnects it after the
workflow ends.

Unlike Tailscale's Linux-only [official action](https://github.com/tailscale/github-action), Tailnet Link also supports
macOS and Windows runners.

## Usage

### Inputs

| **Name**                | **Description**                                                                                                                                                                                                            | **Required?**                                                      | **Default** |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|-------------|
| `authkey`               | An [auth key](https://tailscale.com/kb/1085/auth-keys) or [OAuth client secret](https://tailscale.com/kb/1215/oauth-clients) with the `devices` scope. Using an OAuth client secret is recommended over using an auth key. | Yes                                                                | N/A         |
| `tags`                  | A comma separated list of [tags](https://tailscale.com/kb/1068/tags). Each tag must begin with `tag:`.                                                                                                                     | Yes if you use an OAuth client secret for `authkey`; no otherwise. | None        |
| `hostname`              | A fixed [machine name](https://tailscale.com/kb/1098/machine-names). A machine name will be derived from the runner's system hostname if you don't provide this.                                                           | No                                                                 | None        |
| `extra-args`            | Additional arguments to [`tailscale up`](https://tailscale.com/kb/1241/tailscale-up)  .                                                                                                                                    | No                                                                 | None        |
| `tailscaled-extra-args` | Additional arguments to [`tailscaled`](https://tailscale.com/kb/1278/tailscaled#flags-to-tailscaled).                                                                                                                      | No                                                                 | None        |
| `tailnet-lock`          | Set this to true if you're using [tailnet lock](https://tailscale.com/kb/1226/tailnet-lock).                                                                                                                               | No                                                                 | `false`     |

>[!WARNING]
> If you're using [tailnet lock](https://tailscale.com/kb/1226/tailnet-lock), `authkey` must be a [pre-signed](https://tailscale.com/kb/1226/tailnet-lock?q=pre+signed#add-a-node-using-a-pre-signed-auth-key) auth key It cannot be an OAuth client secret.

### Example

```yaml
- name: Connect to Tailscale
  uses: celsiusnarhwal/tailnet-link@v1
  with:
    authkey: ${{ secrets.TS_OAUTH_SECRET }}
    tags: tag:github-actions
```