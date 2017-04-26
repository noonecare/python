# coding: utf-8
import numpy as np
import pandas as pd

"""
pandas 非常适合读入写出带 Schema 的文件
pandas DataFrame 概念在数据处理时，广泛使用。 R 语言， Spark-Sql 中都有 DataFrame 这个概念。
DataFrame 有 Series 组成。
"""


class PandasDemo:
    @staticmethod
    def write_and_read():
        """
        这里我写出 json 文件，并且把 json 文件读进来
        """
        data = pd.DataFrame()
        data["name"] = pd.Series(["wangmeng"] * 5 + ["lihang"] * 5)
        data["height"] = pd.Series([1.75] * 10)
        data["age"] = pd.Series(range(10))
        # 把 DataFrame 写入到文件
        data = data.to_json("data.json")
        # 从文件中读入 DataFrame
        reload_data = pd.read_json("data.json")
        return reload_data

    def iterate_data_frame(self):
        data = self.write_and_read()
        # 按行遍历
        for index, row in data.iterrows():
            print("-------------------")
            print(row)

    def slice_data_frame(self):
        data = self.write_and_read()

        # 按行切片
        # 打印出前两行
        print(data.iloc[0:2])
        # 打印出指定列
        print(data[["name", "age"]])

    def where_condition_in_data_frame(self):
        data = self.write_and_read()
        # 找出 name 为 wangmeng 的记录
        data_about_wangmeng = data[data["name"] == "wangmeng"]
        print(data_about_wangmeng)

    def concat_data_frame(self):
        data = self.write_and_read()
        double_data = pd.concat([data, data])
        print(len(double_data))
        print(double_data)

    def group_data_frame(self):
        data = self.write_and_read()
        for name, grouped_data in data.groupby("name"):
            print(name + " has {count} records".format(count=len(grouped_data)))

    def join_data_frame(self):
        data = self.write_and_read()

        score = pd.DataFrame()
        score["name"] = pd.Series(["wangmeng", "lihang"])
        score["score"] = pd.Series([8, 7])
        merged_data = pd.merge(data, score, on=["name"], how="left")
        print(merged_data)

    @staticmethod
    def apply_function():
        data = pd.DataFrame()
        data["sku_id"] = pd.Series(range(10000, 10010))
        data["kind"] = pd.Series(["京东商品"] * 5 + ["天猫商品"] * 5)
        data["count"] = pd.Series(range(10))

        # 用 apply 求得访问商品的 url
        data["url"] = data["sku_id"].apply(lambda x: "http://www.jd.com/?sku_id={sku_id}".format(sku_id=x))
        print(data["url"])

        # 这是对列，也可以对行，比如

        data["url"] = data.apply(lambda row: "http://www.jd.com/?sku_id={sku_id}".format(sku_id=row["sku_id"]) if row[
                                                                                                                      "kind"] == "京东商品" else "http://www.tmall.com/?sku_id={sku_id}".format(
            sku_id=row["sku_id"]), axis=1)

        print(data["url"])

        # apply 也可以对列，如统计一共买了多少件商品
        product_sum = data.apply(np.sum)
        print(product_sum)

    @staticmethod
    def map_function():
        """
        逐点 
        """
        data = pd.DataFrame()
        data["a"] = pd.Series([0] * 10)
        data["b"] = pd.Series([1] * 10)
        print(data)

        result = data.applymap(lambda x: x + 1)
        print(result)

        s = data["a"].map(lambda x: x + 1)
        print(s)

    @staticmethod
    def broadcast_operation():
        """
        这是继承之 numpy 的特性，到 numpy 的时候，再仔细研究
        """

        a = pd.Series([1] * 10)
        b = pd.Series([2] * 10)
        print(a + b)

    @staticmethod
    def handle_missing_value():
        data = pd.DataFrame()
        data["name"] = pd.Series(["wangmeng", "lihang", "haibao"])
        data["height"] = pd.Series([1.75, 1.75, np.nan])
        print(data)
        data = data.fillna("unknown")
        print(data)

    @staticmethod
    def drop_dumplicates_in_data_frame():
        data = pd.DataFrame()
        data["name"] = pd.Series(["wangmeng"] * 100)
        data["age"] = pd.Series([28] * 100)
        data = data.drop_duplicates()
        print(len(data))
        print(data)

    @staticmethod
    def pivot_table_in_data_frame():
        """
        pivot table （透视表）, 把列的取值转成 index 或者 column
        """
        data = pd.DataFrame()
        data["category"] = pd.Series(["手机", "手机", "pad", "pad", "pad", "pad", "pad", "pad", "电脑"])
        data["price"] = pd.Series([3500, 700, 1000, 1000, 4000, 4000, 2000, 1500, 8000])
        data["brand"] = pd.Series(["APPLE", "HUAWEI", "HUAWEI", "HUAWEI", "HUAWEI", "APPLE", "APPLE", "MI", "APPLE"])

        print(data)
        # 总结不同category (category 的值做 index), 不同 brand （brand 的值做 column）的商品的的均价
        print(pd.pivot_table(data, index=["category"], values="price", columns=["brand"], aggfunc=np.average))


if __name__ == '__main__':
    demo = PandasDemo()
    demo.iterate_data_frame()
    demo.slice_data_frame()
    demo.where_condition_in_data_frame()
    demo.concat_data_frame()
    demo.group_data_frame()
    demo.join_data_frame()
    demo.handle_missing_value()
    demo.apply_function()
    demo.map_function()
    demo.pivot_table_in_data_frame()
    demo.drop_dumplicates_in_data_frame()
    demo.broadcast_operation()
