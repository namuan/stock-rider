from datetime import datetime

import click

from krider.tasks.filter_valid_tickers import filter_valid_tickers
from krider.tasks.historical_data_downloader import historical_data_downloader
from krider.tasks.volume_analysis import volume_analysis_task
from krider.utils.log_helper import init_logger

init_logger()


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--start",
    help="Start date which will be preferred over period. Eg. 2017-01-01",
    required=False,
)
@click.option(
    "--end",
    help="End date which will be preferred over period. Eg 2019-01-01",
    required=False,
)
@click.option(
    "--interval",
    help="Data interval. 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo",
    required=True,
    default="60m",
)
@click.option(
    "--stock",
    help="Download historical data for just this stock. Useful to backfill gaps",
)
def populate_data(interval, start, end, stock):
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    result = historical_data_downloader.run_with(interval, start_dt, end_dt, stock)
    click.echo(result, nl=False)


@cli.command()
@click.option(
    "--period",
    help="Time period. 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max.",
    required=False,
    default="1mo",
)
def latest_data(period):
    click.echo("Loading Latest data for the last {}".format(period))


@cli.command()
def filter_tickers():
    result = filter_valid_tickers.run_with()
    click.echo(result, nl=False)


@cli.command()
@click.option(
    "--period",
    help="Number of entries to use when running volume analysis",
    required=True,
)
def volume_analysis(period):
    result = volume_analysis_task.run_with(period)
    click.echo(result, nl=False)
