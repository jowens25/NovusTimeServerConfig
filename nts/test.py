import click
import serial
import time


@click.group()
def cli():
    """A complex serial CLI application."""
    pass


@cli.command()
@click.option('--port', required=True, help='Serial port to connect to')
@click.option('--baudrate', default=9600, help='Baud rate for the serial connection')
@click.pass_context
def connect(ctx, port, baudrate):
    """Connect to a serial port."""
    try:
        ctx.obj = serial.Serial(port, baudrate, timeout=1)
        click.echo(f"Connected to {port} at {baudrate} baud")
    except serial.SerialException as e:
        click.echo(f"Error: {e}")


@cli.command()
@click.argument('message')
@click.pass_obj
def write(ser, message):
    """Write a message to the serial port."""
    if not ser:
        click.echo("Error: Not connected to any serial port")
        return
    ser.write(message.encode())
    click.echo(f"Sent: {message}")


@cli.command()
@click.option('--timeout', default=1.0, help='Read timeout in seconds')
@click.pass_obj
def read(ser, timeout):
    """Read data from the serial port."""
    if not ser:
        click.echo("Error: Not connected to any serial port")
        return
    ser.timeout = timeout
    data = ser.read(100).decode('utf-8', errors='ignore')
    if data:
        click.echo(f"Received: {data}")
    else:
        click.echo("No data received")


if __name__ == '__main__':
    cli()
