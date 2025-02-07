import yaml
from dataclasses import dataclass
from typing import List

@dataclass
class DiscoverConfig:
    name: str
    description: str 
    ip: str
    port: int
    query_port: int
    announce: bool
    dedicated_server: bool

@dataclass
class GeneralConfig:
    max_players: int
    password: str
    token: str
    banned_ids: List[str]

@dataclass
class GameConfig:
    map: str
    game_mode: str
    packages: List[str]
    assets: List[str]
    loading_screen: str

@dataclass
class CustomSettings:
    pass

@dataclass 
class DebugConfig:
    log_level: int
    async_log: bool
    profiling: bool

@dataclass
class OptimizationConfig:
    tick_rate: int
    compression: int

@dataclass
class ServerConfig:
    discover: DiscoverConfig
    general: GeneralConfig
    game: GameConfig
    custom_settings: CustomSettings
    debug: DebugConfig
    optimization: OptimizationConfig

def parse_config(config_str: str) -> ServerConfig:
    print("🔄 Converting INI format to YAML...")
    # Convert the INI-style format to YAML
    yaml_str = config_str.replace("[", "").replace("]", ":")
    
    print("📝 Parsing YAML configuration...")
    # Parse YAML
    config_dict = yaml.safe_load(yaml_str)
    
    print("⚙️ Creating ServerConfig object...")
    return ServerConfig(
        discover=DiscoverConfig(**config_dict['discover']),
        general=GeneralConfig(**config_dict['general']),
        game=GameConfig(**config_dict['game']),
        custom_settings=CustomSettings(),
        debug=DebugConfig(**config_dict['debug']),
        optimization=OptimizationConfig(**config_dict['optimization'])
    )

def write_config(config: ServerConfig, file_path: str) -> None:
    """
    Write a ServerConfig object to a file in the server's config format.
    
    Args:
        config: ServerConfig object containing the configuration
        file_path: Path where the config file should be written
        
    Raises:
        PermissionError: If unable to write to the specified path
        TypeError: If config is not a valid ServerConfig object
    """
    try:
        print(f"📝 Writing config to: {file_path}")
        
        # Convert config object to dict
        config_dict = {
            'discover': vars(config.discover),
            'general': vars(config.general), 
            'game': vars(config.game),
            'custom_settings': vars(config.custom_settings),
            'debug': vars(config.debug),
            'optimization': vars(config.optimization)
        }

        # Convert to YAML format
        yaml_str = yaml.dump(config_dict, default_flow_style=False)
        
        # Convert YAML to INI-style format
        ini_str = yaml_str.replace(":", "]\n").replace("  ", "")
        sections = ini_str.split("\n")
        ini_str = "\n".join(f"[{line}" if not line.startswith(" ") and line.strip() else line 
                           for line in sections)

        # Write to file
        with open(file_path, 'w') as f:
            f.write(ini_str)
            
        print("✅ Config file written successfully")
        
    except PermissionError:
        print("❌ Permission denied when writing config file!")
        raise PermissionError(f"Unable to write config file to: {file_path}")
    except TypeError as e:
        print("⚠️ Invalid config object provided!")
        raise TypeError(f"Invalid ServerConfig object: {str(e)}")


def load_config(file_path: str) -> ServerConfig:
    """
    Load and parse a server config file from the given path.
    
    Args:
        file_path: Path to the config file
        
    Returns:
        ServerConfig object containing the parsed configuration
        
    Raises:
        FileNotFoundError: If config file does not exist
        yaml.YAMLError: If config file has invalid YAML format
    """
    try:
        print(f"📂 Loading config file from: {file_path}")
        with open(file_path, 'r') as f:
            config_str = f.read()
        print("✅ Config file loaded successfully")
        return parse_config(config_str)
    except FileNotFoundError:
        print("❌ Config file not found!")
        raise FileNotFoundError(f"Config file not found at: {file_path}")
    except yaml.YAMLError as e:
        print("⚠️ Invalid YAML format detected!")
        raise yaml.YAMLError(f"Invalid YAML format in config file: {str(e)}")

def create_empty_config(file_path: str):
    """
    Creates an empty config file with default values at the specified path.
    
    Args:
        file_path: Path where the config file should be created
        
    Raises:
        PermissionError: If unable to write to specified path
    """
    try:
        print(f"📝 Creating empty config file at: {file_path}")
        
        default_config = """[discover]
    name =              "nanos world server"
    ip =                "0.0.0.0"
    port =              7777
    query_port =        7778
    announce =          true
    dedicated_server =  true

[general]
    max_players =       64
    password =          ""
    token =             ""
    banned_ids = [
                        
    ]

[game]
    map =               "default-blank-map"
    game_mode =         ""
    packages = [
                        
    ]
    assets = [
                        
    ]
    loading_screen =    ""

[custom_settings]

[debug]
    log_level =         1
    async_log =         true
    profiling =         false

[optimization]
    tick_rate =         33
    compression =       1"""

        with open(file_path, 'w') as f:
            f.write(default_config)
            
        print("✅ Empty config file created successfully")
        
    except PermissionError:
        print("❌ Permission denied when creating config file!")
        raise PermissionError(f"Unable to create config file at: {file_path}")
