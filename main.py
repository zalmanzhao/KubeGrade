import click
from resource.resource import fetch_kubernetes_resource
from validator.validator import run_validate


@click.command()
@click.option('--config', default=None, help='config file path')
def root(config):
    k_resource = fetch_kubernetes_resource()
    run_validate(k_resource)
    print("result:")


if __name__ == '__main__':
    root()
