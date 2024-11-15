import struct
import unittest
from typing import Any, List, Tuple, Union

import pandas as pd


class U8Encoder:
    """
    U8Encoder 类用于将
    """

    @staticmethod
    def _encode_hint(data_type: str, data_bits: int) -> int:
        """
        将数据类型和数据位数编码为一个0~255的整数。

        :param data_type: 数据类型，取值范围为1~3，分别对应整数、浮点数和字符串
        :param data_bits: 数据位数，取值范围为0~63
        :return: 编码后的整数
        """
        type_map = {"int": 1, "float": 2, "str": 3}
        if data_type not in type_map:
            raise ValueError("不支持的数据类型: {}".format(data_type))
        if not (0 <= data_bits <= 63):
            raise ValueError("数据位数必须在0~63之间")

        return (type_map[data_type] << 6) | data_bits

    @staticmethod
    def _decode_hint(encoded_value: int) -> Tuple[str, int]:
        """
        从0~255的整数中解码出数据类型和数据位数。

        :param encoded_value: 编码后的整数
        :return: 一个元组 (data_type, data_bits)
        """
        type_map = {1: "int", 2: "float", 3: "str"}
        data_type = (encoded_value >> 6) & 0x3
        data_bits = encoded_value & 0x3F
        if data_type not in type_map:
            raise ValueError("未知数据类型编码：{}".format(data_type))
        return type_map[data_type], data_bits

    @staticmethod
    def _encode_item(item: Union[int, float, str]) -> List[int]:
        """
        将单个数据项编码为字节列表。

        :param item: 要编码的数据项
        :return: 编码后的字节列表
        """
        if isinstance(item, int):
            return [U8Encoder._encode_hint("int", 8)] + list(struct.pack(">Q", item))
        elif isinstance(item, float):
            return [U8Encoder._encode_hint("float", 8)] + list(struct.pack(">d", item))
        elif isinstance(item, str):
            encoded_bytes = item.encode("utf-8")
            return [U8Encoder._encode_hint("str", len(encoded_bytes))] + list(
                struct.pack(">{}s".format(len(encoded_bytes)), encoded_bytes)
            )
        else:
            raise ValueError(f"不支持数据类型: {type(item)}")

    @staticmethod
    def _decode_item(item_type: str, item_len: int, encoded_item: List[int]) -> Any:
        """
        从编码后的字节列表中解码出单个数据项。

        :param item_type: 数据类型
        :param item_len: 数据长度
        :param encoded_item: 编码后的字节列表
        :return: 解码后的数据项
        """
        if item_type == "int":
            return struct.unpack(">Q", bytes(encoded_item))[0]
        elif item_type == "float":
            return struct.unpack(">d", bytes(encoded_item))[0]
        elif item_type == "str":
            return struct.unpack(">{}s".format(item_len), bytes(encoded_item))[0].decode(
                "utf-8"
            )
        else:
            raise ValueError(f"未知数据类型: {item_type}")

    @staticmethod
    def encode_record(record: List[Any]) -> List[int]:
        """
        将记录编码为固定长度的字节列表。

        :param record: 要编码的记录
        :return: 编码后的字节列表
        """
        encoded_items = []
        for item in record:
            encoded_items.extend(U8Encoder._encode_item(item))

        if len(encoded_items) > 256:
            raise ValueError(
                "编码该数据所需字节数预计为{}，超过上限256。数据: \n{}\n".format(
                    len(encoded_items), record
                )
            )

        return encoded_items + [0] * (256 - len(encoded_items))

    @staticmethod
    def decode_record(encoded_record: List[int]) -> List[Any]:
        """
        从固定长度的字节列表中解码出记录。

        :param encoded_record: 编码后的字节列表
        :return: 解码后的记录
        """
        if len(encoded_record) != 256:
            raise ValueError(
                "编码数据长度应为256，实际长度为{}".format(len(encoded_record))
            )

        decoded_items = []
        i = 0
        while i < 256:
            if encoded_record[i] == 0:
                break
            item_type, item_len = U8Encoder._decode_hint(encoded_record[i])
            decoded_item = U8Encoder._decode_item(
                item_type, item_len, encoded_record[i + 1 : i + 1 + item_len]
            )
            decoded_items.append(decoded_item)
            i += item_len + 1

        return decoded_items

    @staticmethod
    def encode_database(df: pd.DataFrame) -> pd.DataFrame:
        """
        将整个数据库编码为DataFrame。

        :param df: 要编码的DataFrame
        :return: 编码后的DataFrame
        """
        return pd.DataFrame([U8Encoder.encode_record(row) for _, row in df.iterrows()])

    @staticmethod
    def decode_database(encoded_df: pd.DataFrame) -> pd.DataFrame:
        """
        从编码后的DataFrame中解码出整个数据库。

        :param encoded_df: 编码后的DataFrame
        :return: 解码后的DataFrame
        """
        return pd.DataFrame(
            [U8Encoder.decode_record(row) for _, row in encoded_df.iterrows()]
        )


class TestU8Encoder(unittest.TestCase):
    def setUp(self):
        self.test_cases_item = [
            (42, 42),
            (3.14, 3.14),
            ("he啊lloさせていふぁ😀99", "he啊lloさせていふぁ😀99"),
        ]
        self.test_cases_record = [
            [42, 3.14, "he啊llo😀99"],
            [123, 2.71, "he啊lloa啊"],
        ]
        self.test_cases_database = [
            pd.DataFrame([[42, 3.14, "he啊llo😀99"], [123, 2.71, "he啊lloa啊"]]),
            pd.DataFrame([[0, 0.0, ""], [999, 999.999, "test"]]),
        ]

    def test_encode_decode_item(self):
        for item, expected in self.test_cases_item:
            with self.subTest(item=item):
                encoded = U8Encoder._encode_item(item)
                item_type, item_len = U8Encoder._decode_hint(encoded[0])
                encoded_item = encoded[1:]
                decoded = U8Encoder._decode_item(item_type, item_len, encoded_item)
                self.assertEqual(decoded, expected)

    def test_encode_decode_record(self):
        for record in self.test_cases_record:
            with self.subTest(record=record):
                encoded = U8Encoder.encode_record(record)
                decoded = U8Encoder.decode_record(encoded)
                self.assertEqual(decoded, record)

    def test_encode_decode_database(self):
        for df in self.test_cases_database:
            with self.subTest(df=df):
                encoded_df = U8Encoder.encode_database(df)
                decoded_df = U8Encoder.decode_database(encoded_df)
                pd.testing.assert_frame_equal(decoded_df, df)

    def test_encode_hint_invalid_type(self):
        with self.assertRaises(ValueError):
            U8Encoder._encode_hint("invalid", 8)

    def test_encode_hint_invalid_bits(self):
        with self.assertRaises(ValueError):
            U8Encoder._encode_hint("int", 64)

    def test_decode_hint_invalid_type(self):
        with self.assertRaises(ValueError):
            U8Encoder._decode_hint(0)

    def test_encode_item_invalid_type(self):
        with self.assertRaises(ValueError):
            U8Encoder._encode_item(None)

    def test_decode_item_invalid_type(self):
        with self.assertRaises(ValueError):
            U8Encoder._decode_item("invalid", 8, [0] * 8)

    def test_encode_record_exceed_limit(self):
        with self.assertRaises(ValueError):
            U8Encoder.encode_record([1] * 33)

    def test_decode_record_invalid_length(self):
        with self.assertRaises(ValueError):
            U8Encoder.decode_record([0] * 255)


if __name__ == "__main__":
    unittest.main()
