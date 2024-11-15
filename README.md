# u8_encode
Encode a list or a DataFrame containing integers, floats, and strings into a list of 256 u8s (bytes) for Private Information Retrieval experiments.

## Usage
Encode a list or a pandas row:
```Python
from u8_encode import U8Encoder

# Encoding a record
record = [42, 3.14, "你好helloふぁ😀99"]
encoded_record = U8Encoder.encode_record(record)

# Decoding a record
decoded_record = U8Encoder.decode_record(encoded_record)

print(f"Encoded Record: {encoded_record}")
print(f"Decoded Record: {decoded_record}")

# Encoded Record: [72, 0, 0, 0, 0, 0, 0, 0, 42, 136, 64, 9, 30, 184, 81, 235, 133, 31, 215, 228, 189, 160, 229, 165, 189, 104, 101, 108, 108, 111, 227, 129, 181, 227, 129, 129, 240, 159, 152, 128, 57, 57, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# Decoded Record: [42, 3.14, '你好helloふぁ😀99']
```
Encode a DataFrame:
```Python
import pandas as pd
from u8_encode import U8Encoder

# Sample DataFrame
df = pd.DataFrame([[42, 3.14, "你好helloふぁ😀99"], [123, 2.71, "你好helloふぁ😀99"]])

# Encoding a DataFrame
encoded_df = U8Encoder.encode_database(df)

# Decoding a DataFrame
decoded_df = U8Encoder.decode_database(encoded_df)

print("Encoded DataFrame shape: {}".format(encoded_df.shape))
print("Decoded DataFrame shape: {}".format(decoded_df.shape))

# Encoded DataFrame shape: (2, 256)
# Decoded DataFrame shape: (2, 3)
``
