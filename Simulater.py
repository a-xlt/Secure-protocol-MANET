from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from KeyAuthority import get_public_key_by_nodeNumber


def encrypt_file(public_key, input_file, output_file):
    # Load the public key
    public_key_obj = serialization.load_pem_public_key(
        public_key,
        backend=default_backend()
    )

    # Read the content of the input file
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Encrypt the file
    ciphertext = public_key_obj.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Save the encrypted content to the output file
    with open(output_file, 'wb') as f:
        f.write(ciphertext)


# Example usage
NodeNumber = 1
public_key = get_public_key_by_nodeNumber(NodeNumber)

if public_key:
    input_file = 'sample_file.txt'
    output_file = 'encrypted_sample_file.bin'

    encrypt_file(public_key, input_file, output_file)

else:
    print(f"Public Key not found for NodeNumber: {NodeNumber}")
