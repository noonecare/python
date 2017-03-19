## Pandas  中比较难理解的概念

### Series
### DataFrame
- 从外部读取文件， pd.read_csv, pd.read_excel
- 合并， merge, join, concat, append
> pd.concat 和 DataFrame.append 一样，就是简单的添加（可以按行也可以按列）。
> DataFrame.join, DataFrame.merge 和 pd.merge 类似于 SQL 中的 join。



- slice, referrence
> - DataFrame 是 Series 的序列。所以DataFrame["label"] 表示的是选取列，而不是选取行。
> - 为了选取 index， 你需要用到 **ix, iloc, loc 函数**。这三个函数有微妙的区别，这个[issue](http://stackoverflow.com/questions/31593201/pandas-iloc-vs-ix-vs-loc-explanation/31593712)是我见过的讲的最清楚的。你要清楚 label 和 integer-position 的概念。特别注意， 选取 DataFrame 的列时， 如果用 integer-postion 的方式选取，可以使用 DataFrame[0:3] 这样的表示方式，但是如果使用 label 的方式访问，这样方式不对，比如不能 DataFrame["Year":"Click"]。
> - **Boolean Series**(or list of tuple) 选择 index。这是很奇怪的一点， DataFrame 和 Series 都可以这样用。numpy 不可以这样用， list, tuple 也不可以这样用。

- Multiple Index, level
- pivot\_table, pivot, stack, unstack

## Operator and Function

DataFrame 中的运算都是逐点运算。如果要进行矩阵运算，一般就会使用 DataFrame 的底层实现 numpy 的数据结构进行。
>DataFrame: apply, applymap
>Series: map