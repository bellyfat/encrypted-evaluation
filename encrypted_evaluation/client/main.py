from typing import List
import tenseal as ts
import typer
from encrypted_evaluation.client import Client


VERBOSE = False

app = typer.Typer()

# ctx = ts.context(ts.SCHEME_TYPE.CKKS, 8192, -1, [40, 21, 21, 21, 21, 21, 40])
# ctx.global_scale = 2 ** 21
# ctx.generate_galois_keys()

# vec = ts.ckks_vector(ctx, [0.01] * 64)

# client = Client("http://localhost:8000")
# is_up = client.ping()
# print(f"[+] API is {'up' if is_up else 'down'}")
# print("[*] Sending context and encrypted vector for evaluation")
# result = client.evaluate("fc", ctx, vec)
# print(f"[+] Result: {result.decrypt()}")


def check_power_of_two(value: int):
    if value & (value - 1) != 0 or value <= 0:
        raise typer.BadParameter("Only powers of two greater than zero are allowed")


@app.command()
def ping(
    url: str = typer.Argument(..., help="base url of the API (e.g. 'http://myapi.com')")
):
    """Check if the API at URL is up"""
    client = Client(url)
    is_up = client.ping()
    if is_up:
        typer.secho("API is up", fg=typer.colors.GREEN)
    else:
        typer.secho("API is down", fg=typer.colors.RED)


@app.command()
def list_models(
    url: str = typer.Argument(
        ..., help="base url of the API (e.g. 'http://myapi.com')"
    ),
    only_names: bool = typer.Option(
        False, "--only-names", "-n", help="show only the model names"
    ),
):
    client = Client(url)
    models = client.list_models()
    print(models)


@app.command()
def model_info(
    url: str = typer.Argument(
        ..., help="base url of the API (e.g. 'http://myapi.com')"
    ),
    model_name: str = typer.Argument(...),
):
    client = Client(url)
    model_info = client.model_info(model_name)
    print(model_info)


@app.command()
def evaluate(
    url: str = typer.Argument(
        ..., help="base url of the API (e.g. 'http://myapi.com')"
    ),
    model_name: str = typer.Argument(...),
    context_file: typer.FileBinaryRead = typer.Argument(..., envvar="TENSEAL_CONTEXT"),
    input_file: typer.FileBinaryRead = typer.Argument(...),
    output_file: typer.FileBinaryWrite = typer.Argument(..., mode="xb"),
):
    pass


@app.command()
def decrypt(
    context_file: typer.FileBinaryRead = typer.Argument(..., envvar="TENSEAL_CONTEXT"),
    output_file: typer.FileBinaryWrite = typer.Argument(...),
):
    pass


@app.command()
def encode(
    input_file: typer.FileBinaryRead = typer.Argument(...),
    file_type: str = typer.Option(
        "", "--type", "-t", help="type of the file to encode"
    ),
    method: str = typer.Option("", "--method", "-m", help="encoding method to use"),
):
    pass


@app.command()
def create_context(
    file_name: typer.FileBinaryWrite = typer.Argument(...),
    poly_mod_degree: int = typer.Argument(
        ..., help="polynomial modulus degree", callback=check_power_of_two
    ),
    coeff_mod_bit_sizes: List[int] = typer.Argument(
        ..., help="bit size of the coeffcients modulus"
    ),
    global_scale: float = typer.Option(
        None, "--scale", min=1, help="scale to use by default for CKKS encoding",
    ),
    gen_galois_keys: bool = typer.Option(
        False, "--gk/--no-gk", "-g/-G", help="generate galois keys"
    ),
    gen_relin_keys: bool = typer.Option(
        True, "--rk/--no-rk", "-r/-R", help="generate relinearization keys"
    ),
    save_secret_key: bool = typer.Option(
        True, "--sk/--no-sk", "-s/-S", help="save the secret key into the context"
    ),
):
    print(coeff_mod_bit_sizes)
    print(gen_galois_keys)
    print(
        f"GRS flag is {int(gen_galois_keys)}{int(gen_relin_keys)}{int(save_secret_key)}"
    )


@app.callback()
def main(
    verbose: int = typer.Option(0, "--verbose", "-v", count=True, help="verbose level")
):
    """What this CLI is about?"""
    if verbose > 0:  # might be worth using the level later
        VERBOSE = True


if __name__ == "__main__":
    app()
