# Tailnet Link Down

This variant of [Tailnet Link](https://github.com/celsiusnarhwal/tailnet-link) disconnects a GitHub Actions workflow from Tailscale. [Tailnet Link Up](https://github.com/celsiusnarhwal/tailnet-link/blob/main/up)
must be run before this action.

This action does not take any inputs.

```yaml
- name: Connect to Tailscale
  uses: celsiusnarhwal/tailnet-link/down@v1
```

Note that using Tailnet Link Up with an [OAuth client secret](https://tailscale.com/kb/1215/oauth-clients) will always
create an [ephemeral node](https://tailscale.com/kb/1111/ephemeral-nodes) that Tailscale will eventually remove from
your Tailnet even if you do not use this action.