import click
import serial
import configparser

# fpga <-> axi <-> serial <-> string <-> buttons

# [server]
# device = /dev/ttyUSB0

# [ntp]
# enable = 1

# gets converted to:

# ser = serial.Serial(config.get(device))

# and
# in a ntp section....
# ser.write("$WC,0xB0020000,0x00000001")

cfg = configparser.ConfigParser()
cfg.read("nts.conf")


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Novus Timeserver Configuration Tool")
        click.echo(ctx.get_help())


@cli.command()  # write
def test():
    print(cfg.get("server", "file_descriptor"))
    print(cfg.get('ntp', 'enable'))


if __name__ == '__main__':
    cli()
