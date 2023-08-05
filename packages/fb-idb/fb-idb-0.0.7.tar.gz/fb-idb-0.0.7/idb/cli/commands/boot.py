#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.

from argparse import Namespace

from idb.cli.commands.base import TargetCommand
from idb.common.types import IdbClient


class BootCommand(TargetCommand):
    @property
    def description(self) -> str:
        return "Boots a simulator (only works on mac)"

    @property
    def name(self) -> str:
        return "boot"

    async def run_with_client(self, args: Namespace, client: IdbClient) -> None:
        await client.boot()
