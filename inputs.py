import os
import socket
from tempfile import TemporaryDirectory

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def error(message: str):
    print(f"::error::{message}")
    exit(1)


class TailscaleSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TS_")

    authkey: str
    tags: str
    extra_args: str
    tailscaled_extra_args: str
    hostname: str
    tailnet_lock: bool

    @property
    def authkey_is_oauth(self):
        return self.authkey.startswith("tskey-client")

    @property
    def full_authkey(self):
        key = self.authkey

        if self.authkey_is_oauth:
            key += "?preauthorized=true&ephemeral=true"

        return key

    @model_validator(mode="after")
    def validate_tags(self):
        if self.authkey_is_oauth and not self.tags:
            error("You must provide at least one tag when using an OAuth secret.")

        return self

    @field_validator("hostname")
    def validate_hostname(cls, v):
        return v or f"github-{socket.gethostname()}"


settings = TailscaleSettings()

tailscaled_args = settings.tailscaled_extra_args

print(f"TAILSCALED_ARGS={tailscaled_args}", file=open(os.getenv("GITHUB_ENV"), "a"))

tailscale_args = f"--auth-key '{settings.full_authkey}' --hostname {settings.hostname} {settings.extra_args}"

if settings.tags:
    tailscale_args = f"--advertise-tags {settings.tags} {tailscale_args}"

print(f"TAILSCALE_ARGS={tailscale_args}", file=open(os.getenv("GITHUB_ENV"), "a"))