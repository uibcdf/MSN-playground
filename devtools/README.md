# Instructions to set up the environment

# Create a new conda environment

Replace `envname` with the name of your choice.
`conda` can be replaced by `mamba` for faster package installation.

```bash
conda env create --name envname --file=conda-env.yml
```

# Update the environment

If you need to update the environment after making changes to the `conda-env.yml` file, you can use the following command.
Execute this command in the same directory as the `conda-env.yml` file with your environment activated.

```bash
conda env update -f conda-env.yaml
```

