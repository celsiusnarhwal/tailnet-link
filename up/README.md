# Tailnet Link Up

This variant of [Tailnet Link](https://github.com/celsiusnarhwal/tailnet-link) connects a GitHub Actions workflow
to Tailscale, but does _not_ explicitly disconnect it afterward. It takes the same inputs as Tailnet Link does.

Running this action will make the [Tailscale CLI](https://tailscale.com/kb/1080/cli) available in your workflow via the `tailscale` command.

```yaml
- name: Connect to Tailscale
  uses: celsiusnarhwal/tailnet-link/up@v1
  with:
    authkey: ${{ secrets.TS_OAUTH_SECRET }}
    tags: tag:github-actions
```

This action is intended, but not required, to be paired with [Tailnet Link Down](https://github.com/celsiusnarhwal/tailnet-link/blob/main/down).

Note that authenticating with an [OAuth client secret](https://tailscale.com/kb/1215/oauth-clients) will always
create an [ephemeral node](https://tailscale.com/kb/1111/ephemeral-nodes) that Tailscale will eventually remove from
your Tailnet even if you do not use Tailnet Link Down.