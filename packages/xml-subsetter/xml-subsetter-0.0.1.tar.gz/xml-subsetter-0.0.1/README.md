# Xml Subsetter

decimate data while keeping others intact 

### before
```xml
# bulk.xml
<r>
    <meta>
    some meta data
    </meta>

    <something>
    thing thing thing thing
    </something>

    <e>e0</e>
    <e>e1</e>
    <e>e2</e>
    <e>e3</e>
    <some-annoying-non-data-you-have-to-keep-1>ah yah yah</some-annoying-non-data-you-have-to-keep-1>
    <some-annoying-non-data-you-have-to-keep-2>ah yah yah</some-annoying-non-data-you-have-to-keep-2>
    <some-annoying-non-data-you-have-to-keep-3>ah yah yah</some-annoying-non-data-you-have-to-keep-3>
    <e>e4</e>
    <e>e5</e>
    <e>e6</e>
    <e>e7</e>
    <e>e8</e>
    <e>e9</e>
    <e>e10</e>
    ...
    <e>e99</e>
</r>
```

`subset_head("bulk.xml", target_file='/tmp/small.xml', data_tag='e',ratio=0.05)`

### after

```xml
# small.xml
<r>
    <meta>
    some meta data
    </meta>

    <something>
    thing thing thing thing
    </something>

    <e>e0</e>
    <e>e1</e>
    <e>e2</e>
    <e>e3</e>
    <some-annoying-non-data-you-have-to-keep-1>ah yah yah</some-annoying-non-data-you-have-to-keep-1>
    <some-annoying-non-data-you-have-to-keep-2>ah yah yah</some-annoying-non-data-you-have-to-keep-2>
    <some-annoying-non-data-you-have-to-keep-3>ah yah yah</some-annoying-non-data-you-have-to-keep-3>
    <e>e4</e>
</r>
```
