# u8_encode
Encode a list or a DataFrame containing integers, floats, and strings into a list of 256 u8s (bytes) for Private Information Retrieval experiments.

## Usage
Encode a list or a pandas row:
```Python
from u8_encode import U8Encoder

# Encoding a record
record = [42, 3.14, "hello"]
encoded_record = U8Encoder.encode_record(record)

# Decoding a record
decoded_record = U8Encoder.decode_record(encoded_record)

print(f"Encoded Record: {encoded_record}")
print(f"Decoded Record: {decoded_record}")
```
Encode a DataFrame:
```Python
import pandas as pd
from u8_encode import U8Encoder

# Sample DataFrame
df = pd.DataFrame([[42, 3.14, "hello"], [123, 2.71, "world"]])

# Encoding a DataFrame
encoded_df = U8Encoder.encode_database(df)

# Decoding a DataFrame
decoded_df = U8Encoder.decode_database(encoded_df)

print("Encoded DataFrame:")
print(encoded_df)
print("Decoded DataFrame:")
print(decoded_df)
``
