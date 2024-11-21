import typer

from split import split

app = typer.Typer()
app.command()(split)

if __name__ == "__main__":
    app()
