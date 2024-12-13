# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "hachitool",
#     "inflect",
#     "pydantic-settings",
# ]
# ///

import os
import socket
import sys
import typing as t

import inflect as ifl
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

inflect = ifl.engine()


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
    def tailscale_up_args(self):
        authkey = self.authkey

        if self.authkey_is_oauth:
            authkey += "?preauthorized=true&ephemeral=true"

        args = f"--auth-key '{authkey}' --hostname {self.hostname} {self.extra_args}"

        if self.tags:
            args = f"--advertise-tags {self.tags} {args}"

        return args

    @model_validator(mode="after")
    def validate_tags(self):
        if self.authkey_is_oauth and not self.tags:
            hachitool.error("You must provide at least one tag when using an OAuth secret.")

        return self

    @field_validator("extra_args")
    def validate_extra_args(cls, v):
        forbidden_flags = ["--auth-key", "--advertise-tags", "--hostname"]
        found = []

        for flag in forbidden_flags:
            if any((token.startswith(flag) for token in v.split(" "))):
                found.append(flag)

        if found:
            hachitool.error(f"extra-args may not contain {inflect.join(found, conj='or')}.")

        return v

    @field_validator("tailscaled_extra_args")
    def validate_tailscaled_extra_args(cls, v):
        if v and sys.platform == "win32":
            hachitool.warning("tailscaled-extra-args has no effect on Windows runners.")

        return v

    @field_validator("hostname")
    def validate_hostname(cls, v):
        return v or f"github-{socket.gethostname()}"


settings = TailscaleSettings()

hachitool.set_output(
    cmd="./tailscale.exe" if sys.platform == "win32" else "sudo tailscale",
    daemon=settings.tailscaled_extra_args,
    up=settings.tailscale_up_args,
)
