from bank_node.core.config_manager import ConfigManager

def is_local_ip(ip_address: str) -> bool:
    """
    Checks if the given IP address corresponds to the local server instance.
    
    Args:
        ip_address (str): The IP address to check.
        
    Returns:
        bool: True if the IP is local (matches config or loopback alias), False otherwise.
    """
    if not ip_address:
        return False
        
    # Normalize localhost to 127.0.0.1
    normalized_input = "127.0.0.1" if ip_address.lower() == "localhost" else ip_address
    
    # Get configured server IP
    config = ConfigManager()
    server_config = config.get("server")
    
    configured_ip = "127.0.0.1" # Default
    if server_config and "ip" in server_config:
        configured_ip = server_config["ip"]
        
    # Normalize configured IP as well
    normalized_config = "127.0.0.1" if configured_ip.lower() == "localhost" else configured_ip
    
    return normalized_input == normalized_config
