# Dotts - The Dotfiles Manager from the Future

Manage your dotfiles across different machines with ease and speed.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![PyPi](https://img.shields.io/badge/pypi-%23ececec.svg?style=for-the-badge&logo=pypi&logoColor=1f73b7)

## Features
- **Dotfiles Management**: Easily manage your dotfiles using Git.
- **Dependency Management**: Specify dependencies for your dotfiles.
- **Plugin Support**: Install and manage plugins for applications like Neovim.
- **Environment Variable Management**: Add, remove, and list environment variables.
- **Machine Management**: Keep track of different machines and their configurations.
- **User-Friendly CLI**: A clean and intuitive command-line interface.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sufremoak/dotts.git
   cd dotts
   ```

2. **Install Dependencies**:
   Make sure you have Python 3 and pip installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Dotts**:
   Run the following command to set up your dotfiles manager:
   ```bash
   python main.py init
   ```

## Usage

### Basic Commands

- **Initialize Dotts**:
  ```bash
  dotts init
  ```

- **Synchronize Dotfiles**:
  ```bash
  dotts sync
  ```

- **Show Git Status**:
  ```bash
  dotts status
  ```

- **Manage Dependencies**:
  ```bash
  dotts dependencies add <name> <install_method>
  dotts dependencies mod <name> <new_install_method>
  dotts dependencies list
  ```

- **Manage Plugins**:
  ```bash
  dotts install_plugin nvim <plugin_name>
  dotts list_plugins nvim
  ```

- **Manage Environment Variables**:
  ```bash
  dotts env add <VAR_NAME> <value>
  dotts env remove <VAR_NAME>
  dotts env list
  ```

- **Manage Machines**:
  ```bash
  dotts machines add <machine_name>
  dotts machines remove <machine_name>
  dotts machines list
  ```

### Example Usage

```bash
# Add a dependency
dotts dependencies add nvim --install_via_pm="apt"

# Install a plugin
dotts install_plugin nvim username/repo

# Add an environment variable
dotts env add MY_VAR "some_value"

# List all machines
dotts machines list
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Typer](https://typer.tiangolo.com/) for creating a great CLI framework.
- [Rich](https://github.com/Textualize/rich) for beautiful console output.
- [Python JSON Logger](https://github.com/madzak/python-json-logger) for structured logging.

Made with ❤ by [SufremOak](https://github.com/SufremOak)