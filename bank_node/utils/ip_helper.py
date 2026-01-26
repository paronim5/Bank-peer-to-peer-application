import socket
from bank_node.core.config_manager import ConfigManager

def is_local_ip(ip_address: str) -> bool:
    if not ip_address:
        return False
        
    normalized_input = "127.0.0.1" if ip_address.lower() == "localhost" else ip_address
    
    if normalized_input == "127.0.0.1":
        return True
    
    config = ConfigManager()
    server_config = config.get("server")
    
    configured_ip = "127.0.0.1"
    if server_config and "ip" in server_config:
        configured_ip = server_config["ip"]
        
    if configured_ip == "0.0.0.0":
        try:
            hostname = socket.gethostname()
            local_ips = socket.gethostbyname_ex(hostname)[2]
            return normalized_input in local_ips
        except Exception:
            pass

    normalized_config = "127.0.0.1" if configured_ip.lower() == "localhost" else configured_ip
    
    return normalized_input == normalized_config

def get_primary_local_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        config = ConfigManager()
        server_config = config.get("server")
        if server_config and "ip" in server_config and server_config["ip"] != "0.0.0.0":
            return server_config["ip"]
        return "127.0.0.1"
