
import click
import rpi_motion.config as config
import rpi_motion.convo as convo
import rpi_motion.sender as sender

@click.command()
@click.option('--config-file', '-c', help='Alternative config YAML')
def bot(config_file=None):
    cfg = config.load(config_file)
    convo.listen(cfg, lambda sig,frame: sender.goodbye(cfg, sig, frame))

@click.command()
@click.option('--config-file', '-c', help='Alternative config YAML')
@click.argument('imagefile')
def send(config_file=None, imagefile=None):
    cfg = config.load(config_file)
    sender.send(cfg, imagefile)
