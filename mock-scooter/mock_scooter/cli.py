"""CLI client — sends commands to a running mock-scooter REST API."""

import sys

import click
import requests

DEFAULT_BASE_URL = "http://localhost:5000"


@click.group()
@click.option("--base-url", "-b", default=DEFAULT_BASE_URL, help="REST API base URL.")
@click.pass_context
def cli(ctx: click.Context, base_url: str) -> None:
    """Control a mock e-scooter via its REST API."""
    ctx.ensure_object(dict)
    ctx.obj["base_url"] = base_url.rstrip("/")


@cli.command()
@click.pass_context
def state(ctx: click.Context) -> None:
    """Show the current scooter state."""
    resp = requests.get(f"{ctx.obj['base_url']}/state")
    click.echo(resp.text)


@cli.command()
@click.argument("level", type=float)
@click.pass_context
def set_battery(ctx: click.Context, level: float) -> None:
    """Set battery LEVEL (0‑100)."""
    resp = requests.post(f"{ctx.obj['base_url']}/set-battery", json={"level": level})
    click.echo(resp.text)


@cli.command()
@click.pass_context
def lock(ctx: click.Context) -> None:
    """Lock the scooter."""
    resp = requests.post(f"{ctx.obj['base_url']}/lock")
    click.echo(resp.text)


@cli.command()
@click.pass_context
def unlock(ctx: click.Context) -> None:
    """Unlock the scooter."""
    resp = requests.post(f"{ctx.obj['base_url']}/unlock")
    click.echo(resp.text)


@cli.command()
@click.argument("lat", type=float)
@click.argument("lng", type=float)
@click.pass_context
def set_position(ctx: click.Context, lat: float, lng: float) -> None:
    """Set geographic position (LAT LNG)."""
    resp = requests.post(
        f"{ctx.obj['base_url']}/set-position", json={"lat": lat, "lng": lng}
    )
    click.echo(resp.text)


def main() -> None:
    """Entry point for the CLI (installed via console_scripts)."""
    cli()


if __name__ == "__main__":
    main()