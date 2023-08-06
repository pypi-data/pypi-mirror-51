# ibm-apidocs-cli
![Status](https://img.shields.io/badge/status-beta-yellow.svg)
[![Latest Stable Version](https://img.shields.io/pypi/v/ibm-apidocs-cli.svg)](https://pypi.python.org/pypi/ibm-apidocs-cli)

This tool allows users to generate the api documentation.

## Installation

- Install the CLI with `pip` or `easy_install`:

    ```bash
    pip install -U ibm-apidocs-cli
    ```

    or

    ```bash
    easy_install -U ibm-apidocs-cli
    ```

- Clone a [cloud-api-docs](https://github.ibm.com/cloud-api-docs) repo to a local directory. Make sure the repo contains the required `apiref-index.json` file and the front-matter configuration file (typically `<openapi>-config.json`).

- Configure your GitHub access token. You can skip this step if you do not want the CLI to automatically download the latest front-matter and SDK generator code.

  Follow these steps:

  1. Get an access token from [GitHub Enterprise](https://github.ibm.com/settings/tokens. For more information, see the [GitHub help](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line).

  1. Set the `GITHUB_TOKEN` environment variable:

    ```
    export GITHUB_TOKEN=<token>
    ```

- **Optional:** Clone the [frontmatter generator](https://github.ibm.com/cloud-doc-build/frontmatter-generator) to a local directory. If you do not have a local clone of the front-matter generator repo, the CLI will automatically clone it to a temporary directory.

- **Optional:** Install the [SDK generator](https://github.ibm.com/CloudEngineering/openapi-sdkgen/releases) to a local directory. If you do not have a local copy of the SDK generator, the CLI will automatically download the latest version to a temporary directory.

  To install the SDK generator, you do not need to clone or download the full repository or build the project. Instead, use the [installer](https://github.ibm.com/CloudEngineering/openapi-sdkgenreleases). For more information, see [the generator README](https://github.ibm.comCloudEngineering/openapi-sdkgen#using-a-pre-built-installer).

  **Note:** The SDK generator .jar file must be named `openapi-sdkgen.jar`. If you have downloaded or built a version of the file with a different name (e.g.`openapi-sdkgen-<version>.jar`), you must rename it.

## Usage

```
ibm-apidocs-cli --help
```

```
usage: ibm-apidocs-cli [-h] -i <openapi_file>
                       [--config <config_file>]
                       [--sdk_generator <sdk_generator_path>]
                       [--sdkgen_release <sdkgen_release>]
                       [--frontmatter <frontmatter_path>]
                       [--apidocs <apidocs_path>]
                       [--templates <templates_path>]
                       [--output_folder <output_path>]
                       [--keep_sdk] [--keep_temp] [--verbose] [--version]
```

Required arguments:

- `-i <openapi_file>`: The path to the input OpenAPI definition file (e.g. `assistant-v1.json`).

Optional arguments:

- `--config <config_file>`: The front matter config file (e.g. `assistant-v1-config.json`). You can optionally specify the full path to the config file; if you do not include the path, the file is assumed to be in the `apidocs` directory. If you do not specify the config file, the file name is looked up from the map file, and the file is assumed to be in the
`apidocs` directory.
- `--sdk_generator <sdk_generator_path>`: Path to the directory containing the SDK generator JAR file, optionally including the file name. If you specify a directory but not a file name, the JAR file is assumed to be `openapi-sdkgen.jar`. Use this option if you need to use local copy of the SDK generator. If you do not specify this parameter, the CLI will automatically download the the `openapi-sdkgen.jar` file to a temporary directory and use that copy.
- `--sdkgen_release <sdkgen_release>`: Release of the SDK generator to download, if you are allowing the CLI to download the generator automatically. Specify the GitHub release tag (for example, `1.0.0.1`). If you do not specify a release, the CLI uses the most recent maintenance release for the major release specified in the map file. This argument is ignored if `--sdk_generator` is specified.
- `--frontmatter <frontmatter_path>`: Path to the directory containing the front-matter generator `app.js` file. Use this option if you need to use a specific version or branch of the front-matter generator code, or if you do not have a GitHub access token configured. If you do not specify a location, the CLI will automatically clone the latest version of the front-matter generator repo to a temporary directory and use that clone.
- `--apidocs <apidocs_path>`: The path to the `cloud-api-docs` repository or other directory containing `apiref-index.json` and front matter config file. If you do not specify this argument, the current directory is used.
- `--templates <templates_path>`: Path to the directory containing the front-matter templates to use. You can specify either an absolute path or just the directory name (for example, `templates-data`; if you specify just the directory name, it is assumed to be a subdirectory of the front-matter generator location. If you do not specify a templates directory, the CLI will use the templates directory specified in the map file.
- `--output_folder <output_folder>`: The target directory for generated files. If you do not specify this argument, output files are written to the current directory.
- `--keep_sdk`: Preserve the `_sdktemp` directory containing generated SDK artifacts. Useful for debugging purposes.
- `--keep_temp`: Preserve the temporary directory containing the downloaded front-matter and SDK generators, if applicable. Useful for debugging purposes.
- `--no_update`: Use front-matter config file as-is without updating SDK versions. If you do not specify this argument, the config file is updated with the latest GitHub release for each supported SDK language.
- `--mapfile`: The path to a local map file, including file name (for example, `generate-apidocs.json`). If you do not specify a local map file, the current map file is downloaded from the `developer-cloud--api-definitions` repo as needed.
- `-h`, `--help`: Show usage information and exit.
- `--verbose`: Verbose flag.
- `--version`: Show program's version number and exit.

### Example commands

This example assumes that the command is being run from the `apidocs` repo directory containing the API Reference files, and that the CLI is automatically downloading and using the latest code for the front-matter and SDK generators. All output files are written to the current directory:

```bash
ibm-apidocs-cli -i assistant-v1.json
```

This example uses different locations for the input and output files, and also specifies local copies of the SDK generator and front-matter generator code:

```
ibm-apidocs-cli -i '/Users/my_user/Documents/GitHub/api-apidocs-cli/test/resources/config/assistant-openapi3-v1.json' \
                -c '/Users/my_user/Documents/GitHub/api-apidocs-cli/test/resources/config/test-input-config.yaml' \
                --output_folder '/Users/my_user/Documents/GitHub/api-apidocs-cli/test/target' \
                --frontmatter '/Users/my_user/Documents/GitHub/frontmatter-generator' \
                --sdk_generator '/Users/my_user/Documents/Release/openapi-sdkgen/lib'
```

## Python version

✅ Tested on Python 3.5, 3.6, and 3.7.

## Contributing

See [CONTRIBUTING.md][CONTRIBUTING].

## License

MIT

[ibm_cloud]: https://cloud.ibm.com
[responses]: https://github.com/getsentry/responses
[requests]: http://docs.python-requests.org/en/latest/
[CONTRIBUTING]: ./CONTRIBUTING.md
