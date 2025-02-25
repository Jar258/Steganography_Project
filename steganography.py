import cv2
import numpy as np

def encode_image(image_path, secret_data, output_image="encoded_image.png"):
    # Load the image
    image = cv2.imread(image_path)

    # Debugging: Check if the image was loaded correctly
    if image is None:
        print(f"⚠️ ERROR: Could not open or find the image at '{image_path}'. Check the file path and try again.")
        return

    print("✅ Image successfully loaded!")

    # Convert the secret message to binary
    binary_secret_data = ''.join(format(ord(i), '08b') for i in secret_data) + '1111111111111110'  # End marker
    
    data_index = 0
    data_len = len(binary_secret_data)

    # Convert image to writable NumPy array (avoid OverflowError)
    image = np.array(image, dtype=np.uint8)

    for i in range(image.shape[0]):  # Loop over rows
        for j in range(image.shape[1]):  # Loop over columns
            for k in range(3):  # Loop over R, G, B channels
                if data_index < data_len:
                    # Safely modify pixel value
                    pixel_value = int(image[i, j, k])  # Convert to int (fixes OverflowError)
                    new_value = (pixel_value & ~1) | int(binary_secret_data[data_index])
                    image[i, j, k] = np.clip(new_value, 0, 255)  # Ensure pixel is within range
                    data_index += 1

    # Save the encoded image
    cv2.imwrite(output_image, image)
    print(f"✅ Data successfully hidden in '{output_image}'")

def decode_image(image_path):
    # Load the encoded image
    image = cv2.imread(image_path)

    # Debugging: Check if the image was loaded correctly
    if image is None:
        print(f"⚠️ ERROR: Could not open or find the image at '{image_path}'. Check the file path and try again.")
        return

    print("✅ Encoded image successfully loaded!")

    binary_data = ""

    for i in range(image.shape[0]):  # Loop over rows
        for j in range(image.shape[1]):  # Loop over columns
            for k in range(3):  # Loop over R, G, B channels
                binary_data += str(image[i, j, k] & 1)

    # Convert binary data to text
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = ''.join(chr(int(byte, 2)) for byte in all_bytes if int(byte, 2) != 254)  # Stop at end marker
    
    return decoded_data

# Example Usage:
input_image_path = r"C:\Users\Shivraj\Desktop\desktop\Steganography_Project\input_image.png"

# Encoding
encode_image(input_image_path, "Hello, this is a secret message!")

# Decoding
decoded_message = decode_image("encoded_image.png")
print("🔍 Decoded message:", decoded_message)
