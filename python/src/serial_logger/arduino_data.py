from datetime import datetime

def decode_and_timestamp(data, board_type="default"):
    decoded_data = decode_arduino_data(data, board_type)
    timestamped_data = (datetime.now(), decoded_data)
    return timestamped_data

def decode_arduino_data(data, board_type="default"):
    # Use the specific decoder function based on the board type
    decoder_functions = {
        "default": default_decoder,
        "model_2": model_2_decoder
    }
    
    # Get the appropriate decoder function or use the default if none matches
    decoder = decoder_functions.get(board_type, default_decoder)
    return decoder(data)

def default_decoder(data):
    """
    Default decoder for standard Arduino data.
    """
    return data.decode()

def model_2_decoder(data):
    """
    Decoder for hypothetical 'model_2' Arduino board.
    """
    # Add decoding logic for model_2 here
    # For now, let's assume it's the same as default
    return data.decode()

# As you add support for more boards, simply add their decoding functions to the 'decoder_functions' dictionary.
