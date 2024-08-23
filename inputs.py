import os
import socket
import sys
import typing as t

import inflect as ifl
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

inflect = ifl.engine()


def set_environment_variable(name: str, value: t.Any):
    print(f"{name}={value}", file=open(os.getenv("GITHUB_ENV"), "a"))


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

    @field_validator("extra_args")
    def validate_extra_args(cls, v):
        forbidden_flags = ["--auth-key", "--advertise-tags", "--hostname"]
        found = []

        for flag in forbidden_flags:
            if any((token.startswith(flag) for token in v.split(" "))):
                found.append(flag)

        if found:
            error(f"extra-args may not contain {inflect.join(found, conj='or')}.")

        return v

    @field_validator("tailscaled_extra_args")
    def validate_tailscaled_extra_args(cls, v):
        if sys.platform == "win32":
            print("::warning::tailscaled-extra-args has no effect on Windows runners.")

    @field_validator("hostname")
    def validate_hostname(cls, v):
        return v or f"github-{socket.gethostname()}"


settings = TailscaleSettings()

set_environment_variable("TAILSCALED_ARGS", settings.tailscaled_extra_args)

tailscale_args = f"--auth-key '{settings.full_authkey}' --hostname {settings.hostname} {settings.extra_args}"

if settings.tags:
    tailscale_args = f"--advertise-tags {settings.tags} {tailscale_args}"

set_environment_variable("TAILSCALE_ARGS", tailscale_args)
